<template>
  <div class="h-full bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
    <div class="px-5 py-4 border-b border-gray-200 flex items-center justify-between gap-4">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">LoopAI Workspace</h2>
        <p class="text-sm text-gray-500">Create a task from the current LoopAI config, start the agent, and stream responses.</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="px-3 py-1.5 rounded-lg border border-slate-200 text-sm hover:bg-slate-100" @click="refreshStatus">
          Refresh Status
        </button>
        <button class="px-3 py-1.5 rounded-lg border border-rose-200 text-sm text-rose-600 hover:bg-rose-50" @click="stopAgent">
          Stop
        </button>
      </div>
    </div>

    <div class="grid lg:grid-cols-[360px,1fr] flex-1 min-h-0">
      <div class="border-r border-gray-200 p-5 space-y-4 bg-slate-50">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">Task Name</label>
          <input v-model="taskName" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">Initial Prompt</label>
          <textarea
            v-model="taskPrompt"
            rows="6"
            class="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm resize-none"
            placeholder="Describe the training or optimization goal for LoopAI."
          />
        </div>
        <button
          class="w-full rounded-xl px-4 py-2.5 text-sm font-medium text-white"
          :class="creating ? 'bg-slate-400' : 'bg-blue-600 hover:bg-blue-700'"
          :disabled="creating || !taskPrompt.trim()"
          @click="createAndStart"
        >
          {{ creating ? 'Launching...' : 'Create Task and Start Agent' }}
        </button>
        <div class="rounded-xl border border-slate-200 bg-white p-4 text-sm space-y-2">
          <p><span class="text-slate-500">Task ID:</span> <span class="font-mono text-xs">{{ taskId || '-' }}</span></p>
          <p><span class="text-slate-500">Stream:</span> <span :class="streaming ? 'text-emerald-600' : 'text-slate-500'">{{ streaming ? 'connected' : 'idle' }}</span></p>
          <p class="text-slate-500">{{ statusText }}</p>
        </div>
      </div>

      <div class="flex flex-col min-h-0">
        <div class="px-5 py-3 border-b border-gray-200 bg-white">
          <h3 class="text-sm font-semibold text-slate-700">Live Messages</h3>
        </div>
        <div class="flex-1 overflow-y-auto px-5 py-4 bg-white space-y-3">
          <div
            v-for="message in streamMessages"
            :key="message.id"
            class="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700"
          >
            <pre class="whitespace-pre-wrap break-words font-sans">{{ message.text }}</pre>
          </div>
          <p v-if="!streamMessages.length" class="text-sm text-slate-500">No messages streamed yet.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { loopaiApi } from '@/services/api.js'

const route = useRoute()
const creating = ref(false)
const streaming = ref(false)
const taskName = ref('LoopAI Routed Task')
const taskPrompt = ref('')
const taskId = ref('')
const statusText = ref('Idle')
const streamMessages = ref([])
let eventSource = null
let pollTimer = null

function pushStreamMessage(payload) {
  const text = Array.isArray(payload?.data)
    ? payload.data.map((item) => JSON.stringify(item, null, 2)).join('\n')
    : JSON.stringify(payload, null, 2)
  streamMessages.value.push({
    id: `${Date.now()}-${streamMessages.value.length}`,
    text,
  })
}

function clearMessagePoll() {
  if (pollTimer) {
    clearTimeout(pollTimer)
    pollTimer = null
  }
}

function isPendingPayload(payload) {
  return payload?.message === 'wait for message' || payload?.message === 'No messages available'
}

async function pollMessages(attempt = 0) {
  if (attempt >= 6 || streamMessages.value.length) {
    return
  }

  try {
    const messages = await loopaiApi.getMessages()
    if (Array.isArray(messages) && messages.length) {
      messages.forEach((message) => pushStreamMessage(message))
      statusText.value = 'Fetched LoopAI messages.'
      return
    }
  } catch {
    // Keep the UI responsive even when LoopAI only exposes delayed messages.
  }

  pollTimer = window.setTimeout(() => {
    pollMessages(attempt + 1)
  }, 2000)
}

function connectStream() {
  if (eventSource) {
    eventSource.close()
  }
  clearMessagePoll()

  return new Promise((resolve, reject) => {
    let opened = false
    const source = new EventSource(loopaiApi.getStreamUrl())
    eventSource = source

    source.onopen = () => {
      opened = true
      streaming.value = true
      statusText.value = 'Stream connected.'
      resolve()
    }

    source.onmessage = (event) => {
      let payload
      try {
        payload = JSON.parse(event.data)
      } catch {
        pushStreamMessage({ raw: event.data })
        return
      }

      if (isPendingPayload(payload)) {
        return
      }

      pushStreamMessage(payload)
      if (payload.status === 'success') {
        statusText.value = 'Agent finished the latest streamed step.'
      } else if (payload.status === 'loading') {
        statusText.value = 'Agent is processing.'
      }
    }

    source.onerror = () => {
      streaming.value = false
      statusText.value = 'Stream disconnected.'
      source.close()
      if (eventSource === source) {
        eventSource = null
      }
      if (!opened) {
        reject(new Error('Unable to connect to LoopAI stream'))
      }
    }
  })
}

async function createAndStart() {
  creating.value = true
  statusText.value = 'Loading LoopAI config...'
  streamMessages.value = []
  clearMessagePoll()
  try {
    const config = await loopaiApi.getConfig()
    const task = await loopaiApi.createTask({
      name: taskName.value,
      system: config.system,
      states: config.states,
    })
    taskId.value = task.task_id
    statusText.value = 'Starting agent...'
    await loopaiApi.startAgent(task.task_id)
    await connectStream()
    await loopaiApi.sendInput(taskPrompt.value)
    statusText.value = 'Prompt sent to agent.'
    pollMessages()
  } catch (error) {
    statusText.value = `LoopAI request failed: ${error.message}`
  } finally {
    creating.value = false
  }
}

async function refreshStatus() {
  try {
    const status = await loopaiApi.getStatus()
    statusText.value = status ? 'Fetched latest LoopAI status.' : 'No LoopAI status available.'
  } catch (error) {
    statusText.value = `Status refresh failed: ${error.message}`
  }
}

async function stopAgent() {
  try {
    await loopaiApi.stopAgent()
    statusText.value = 'LoopAI agent stopped.'
  } catch (error) {
    statusText.value = `Stop failed: ${error.message}`
  }
}

onMounted(() => {
  if (typeof route.query.task === 'string' && route.query.task) {
    taskPrompt.value = route.query.task
  }
})

onBeforeUnmount(() => {
  clearMessagePoll()
  if (eventSource) {
    eventSource.close()
    streaming.value = false
    eventSource = null
  }
})
</script>
