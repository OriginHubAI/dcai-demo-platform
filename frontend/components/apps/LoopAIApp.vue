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
          <div class="flex items-center justify-between gap-3 mb-2">
            <label class="block text-sm font-medium text-slate-700">Task Prompt</label>
            <span class="text-xs text-slate-500">Describe a workflow task, not a casual chat prompt.</span>
          </div>
          <textarea
            v-model="taskPrompt"
            rows="6"
            class="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm resize-none"
            placeholder="Describe the training or optimization goal for LoopAI."
          />
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-600 uppercase tracking-wide mb-2">Examples</p>
          <div class="space-y-2">
            <button
              v-for="example in promptExamples"
              :key="example.title"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-left hover:border-blue-300 hover:bg-blue-50 transition-colors"
              @click="applyExample(example.prompt)"
            >
              <p class="text-sm font-medium text-slate-700">{{ example.title }}</p>
              <p class="text-xs text-slate-500 mt-1">{{ example.prompt }}</p>
            </button>
          </div>
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
        <div v-if="agentInterrupt" class="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
          <p class="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-1">Agent Waiting For Input</p>
          <p class="text-sm text-amber-900 whitespace-pre-wrap">{{ agentInterrupt }}</p>
        </div>
      </div>

      <div class="flex flex-col min-h-0">
        <div class="px-5 py-3 border-b border-gray-200 bg-white space-y-2">
          <div class="flex items-center justify-between gap-4">
            <h3 class="text-sm font-semibold text-slate-700">Live Messages</h3>
            <span class="text-xs text-slate-500">{{ streamMessages.length }} messages</span>
          </div>
          <div v-if="finalSummary" class="rounded-xl bg-emerald-50 border border-emerald-100 px-4 py-3">
            <p class="text-xs font-semibold text-emerald-700 uppercase tracking-wide mb-1">Final Summary</p>
            <p class="text-sm text-emerald-900 whitespace-pre-wrap">{{ finalSummary }}</p>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto px-5 py-4 bg-white space-y-3">
          <div
            v-for="message in streamMessages"
            :key="message.id"
            class="rounded-2xl border px-4 py-3 text-sm"
            :class="message.tone"
          >
            <p class="text-[11px] font-semibold uppercase tracking-wide mb-2">{{ message.label }}</p>
            <pre class="whitespace-pre-wrap break-words font-sans">{{ message.text }}</pre>
          </div>
          <p v-if="!streamMessages.length" class="text-sm text-slate-500">No messages streamed yet.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
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
const agentInterrupt = ref('')
let eventSource = null
let pollTimer = null
const promptExamples = [
  {
    title: 'SFT Pipeline',
    prompt: '请设计一个从原始文本数据到 SFT 数据集的处理流程，并说明每一步输入输出。',
  },
  {
    title: 'Training Plan',
    prompt: '请为一个代码模型微调任务生成执行计划，包含数据准备、训练、评测和最终产出。',
  },
  {
    title: 'Task Breakdown',
    prompt: '请复述收到的任务，并输出一个三步执行计划，每一步单独说明目标和产物。',
  },
]

function summarizeAgentMessage(message) {
  if (!message || typeof message !== 'object') {
    return JSON.stringify(message, null, 2)
  }

  if ('type' in message && 'data' in message) {
    const kind = message.type
    const payload = message.data || {}
    const content = typeof payload.content === 'string' ? payload.content.trim() : ''

    if (content) {
      return `[${kind}] ${content}`
    }

    if (Array.isArray(payload.tool_calls) && payload.tool_calls.length) {
      const names = payload.tool_calls.map((item) => item.name || item.function?.name || 'tool').join(', ')
      return `[${kind}] tool calls: ${names}`
    }

    if (payload.name && payload.status) {
      return `[${kind}] ${payload.name} (${payload.status})`
    }
  }

  return JSON.stringify(message, null, 2)
}

function resolveMessageMeta(payload) {
  if (payload && typeof payload === 'object' && 'type' in payload && 'data' in payload) {
    switch (payload.type) {
      case 'human':
        return {
          label: 'User Input',
          tone: 'border-slate-200 bg-slate-50 text-slate-700',
        }
      case 'ai':
        return {
          label: 'Agent',
          tone: 'border-blue-200 bg-blue-50 text-blue-950',
        }
      case 'tool':
        return {
          label: 'Tool Result',
          tone: 'border-amber-200 bg-amber-50 text-amber-950',
        }
      default:
        return {
          label: payload.type,
          tone: 'border-slate-200 bg-slate-50 text-slate-700',
        }
    }
  }

  return {
    label: 'Event',
    tone: 'border-slate-200 bg-slate-50 text-slate-700',
  }
}

function pushStreamMessage(payload) {
  const text = Array.isArray(payload)
    ? payload.map((item) => summarizeAgentMessage(item)).join('\n\n')
    : summarizeAgentMessage(payload)

  if (!text.trim()) return

  const meta = Array.isArray(payload)
    ? { label: 'Agent Messages', tone: 'border-blue-200 bg-blue-50 text-blue-950' }
    : resolveMessageMeta(payload)

  streamMessages.value.push({
    id: `${Date.now()}-${streamMessages.value.length}`,
    label: meta.label,
    tone: meta.tone,
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

function isShellStreamEvent(payload) {
  return payload?.message === 'Agent messages' && !Array.isArray(payload?.data)
}

function hasRenderableMessages(messages) {
  return Array.isArray(messages) && messages.length > 0
}

const finalSummary = computed(() => {
  for (let index = streamMessages.value.length - 1; index >= 0; index -= 1) {
    const message = streamMessages.value[index]
    if (message.label === 'Agent' && message.text.trim()) {
      return message.text
    }
  }
  return ''
})

async function pollMessages(attempt = 0) {
  if (attempt >= 10) {
    return
  }

  try {
    const status = await loopaiApi.getStatus()
    agentInterrupt.value = typeof status?.interrupt_value === 'string' ? status.interrupt_value : ''
    if (agentInterrupt.value) {
      statusText.value = 'Agent is waiting for another instruction.'
    }

    const messages = await loopaiApi.getMessages()
    if (hasRenderableMessages(messages)) {
      streamMessages.value = []
      messages.forEach((message) => pushStreamMessage(message))
      statusText.value = agentInterrupt.value
        ? 'Fetched LoopAI messages. Agent is waiting for another instruction.'
        : 'Fetched LoopAI messages.'
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

      if (isShellStreamEvent(payload)) {
        statusText.value = 'Stream connected. Waiting for buffered agent messages...'
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
      statusText.value = 'Stream disconnected. Fetching buffered agent messages...'
      source.close()
      if (eventSource === source) {
        eventSource = null
      }
      pollMessages()
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
  agentInterrupt.value = ''
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

function applyExample(prompt) {
  taskPrompt.value = prompt
}

async function refreshStatus() {
  try {
    const status = await loopaiApi.getStatus()
    agentInterrupt.value = typeof status?.interrupt_value === 'string' ? status.interrupt_value : ''
    if (!status) {
      statusText.value = 'No LoopAI status available.'
      return
    }
    if (agentInterrupt.value) {
      statusText.value = 'LoopAI is waiting for another instruction.'
      return
    }
    if (status.current) {
      statusText.value = `Current node: ${status.current}`
      return
    }
    statusText.value = 'Fetched latest LoopAI status.'
  } catch (error) {
    statusText.value = `Status refresh failed: ${error.message}`
  }
}

async function stopAgent() {
  try {
    await loopaiApi.stopAgent()
    agentInterrupt.value = ''
    statusText.value = 'LoopAI agent stopped.'
  } catch (error) {
    statusText.value = `Stop failed: ${error.message}`
  }
}

onMounted(() => {
  if (typeof route.query.task === 'string' && route.query.task) {
    taskPrompt.value = route.query.task
  } else if (!taskPrompt.value) {
    taskPrompt.value = promptExamples[0].prompt
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
