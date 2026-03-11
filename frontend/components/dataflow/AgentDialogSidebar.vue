<template>
  <div class="w-[360px] bg-white border-l border-gray-200 flex flex-col">
    <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
      <div>
        <h3 class="text-sm font-semibold text-gray-900">DataMaster</h3>
        <p class="text-xs text-gray-500">{{ contextLabel }}</p>
      </div>
      <button
        class="w-8 h-8 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-400 hover:text-gray-700"
        @click="$emit('close')"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-3 bg-slate-50">
      <div
        v-for="message in messages"
        :key="message.id"
        class="rounded-2xl px-4 py-3 text-sm"
        :class="message.role === 'user' ? 'bg-blue-600 text-white ml-8' : 'bg-white text-slate-700 mr-8 border border-slate-200'"
      >
        {{ message.content }}
      </div>
      <div v-if="submitting" class="rounded-2xl px-4 py-3 text-sm bg-white text-slate-500 mr-8 border border-slate-200">
        Routing through DataMaster...
      </div>
    </div>

    <div class="px-4 py-3 border-t border-gray-100 bg-white">
      <textarea
        v-model="draft"
        :disabled="submitting"
        rows="3"
        class="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none focus:border-blue-400 resize-none"
        placeholder="Describe the operator change or ask DataMaster to open another tool."
        @keydown.enter.exact.prevent="send"
      />
      <div class="flex items-center justify-between mt-3">
        <p class="text-xs text-slate-500">{{ helperText }}</p>
        <button
          class="px-3 py-1.5 rounded-lg text-sm text-white"
          :class="draft.trim() && !submitting ? 'bg-blue-600 hover:bg-blue-700' : 'bg-slate-300'"
          :disabled="!draft.trim() || submitting"
          @click="send"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { chatApi } from '@/services/api.js'

const props = defineProps({
  packageId: { type: String, default: '' },
  currentPath: { type: String, default: '' },
})

defineEmits(['close'])

const router = useRouter()
const draft = ref('')
const submitting = ref(false)
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    content: 'Describe the operator you want to write, test, or route to another workspace.',
  },
])

const contextLabel = computed(() => {
  if (props.packageId && props.currentPath) {
    return `${props.packageId} · ${props.currentPath}`
  }
  if (props.packageId) {
    return `${props.packageId} workspace`
  }
  return 'Workspace orchestration'
})

const helperText = computed(() => {
  if (!props.packageId) {
    return 'Use @DataFlow, @LoopAI, @DFAgent, or @PackageEditor.'
  }
  return 'Package context is appended to the request. This side panel gives suggestions and routing hints; it does not edit code directly.'
})

function appendMessage(role, content) {
  messages.value.push({
    id: `${Date.now()}-${messages.value.length}`,
    role,
    content,
  })
}

async function send() {
  const question = draft.value.trim()
  if (!question || submitting.value) return

  appendMessage('user', question)
  draft.value = ''
  submitting.value = true

const context = [props.packageId, props.currentPath].filter(Boolean).join(' / ')
  const composedQuestion = context
    ? `[Package Context: ${context}] ${question}`
    : question

  try {
    const result = await chatApi.sendMessage({ question: composedQuestion })
    appendMessage('assistant', result.answer || 'Request routed.')
    if (result.type === 'tool_call' && result.iframe_url && result.agent !== 'PackageEditor-Agent') {
      router.push(result.iframe_url)
    }
  } catch (error) {
    appendMessage('assistant', `Routing failed: ${error.message}`)
  } finally {
    submitting.value = false
  }
}
</script>
