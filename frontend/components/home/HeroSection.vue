<template>
  <section class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 text-slate-800">
        Empowering Industries with<br>Data-Centric AI
      </h1>
      <p class="text-lg sm:text-xl text-slate-600 max-w-[840px] mx-auto mb-10">
        The Data-Centric AI platform where AI developers, data scientists, and domain experts collaborate around data to build professional models, agents, and applications.
      </p>

      <div class="inline-flex flex-col w-full max-w-[840px] mx-auto">
        <div class="mb-6 w-full">
          <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-4">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div class="min-w-0">
                    <p class="text-slate-400 text-left text-lg leading-7">
                      Just tell about your data needs, and DataMaster will help you get things done.
                    </p>
                    <p class="mt-2 text-xs text-slate-400 text-left break-all">
                      Endpoint: {{ endpointLabel }}
                    </p>
                  </div>
                  <div class="flex items-center gap-2 self-end sm:self-auto sm:pl-4">
                    <span class="text-xs text-slate-500">Model</span>
                    <select
                      v-model="selectedModel"
                      class="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 min-w-[150px]"
                    >
                      <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
                    </select>
                  </div>
                </div>

                <div
                  ref="historyRef"
                  class="mt-4 max-h-[320px] overflow-y-auto rounded-xl bg-slate-50 border border-slate-100 px-3 py-3 space-y-3"
                >
                  <div
                    v-for="message in messages"
                    :key="message.id"
                    class="flex"
                    :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
                  >
                    <div
                      class="max-w-[88%] rounded-2xl px-4 py-3 text-left"
                      :class="message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-slate-200 text-slate-700'"
                    >
                      <div class="text-[11px] mb-1 opacity-70">
                        {{ message.role === 'user' ? 'You' : selectedModel || 'DataMaster' }}
                      </div>
                      <pre class="whitespace-pre-wrap break-words font-sans text-sm leading-6">{{ message.content }}</pre>
                      <div v-if="message.streaming" class="mt-2 flex items-center gap-2 text-[11px] text-slate-400">
                        <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
                        Streaming...
                      </div>
                    </div>
                  </div>
                </div>

                <div class="mt-4 flex flex-wrap gap-2">
                  <button
                    v-for="prompt in quickPrompts"
                    :key="prompt"
                    @click="inputText = prompt"
                    class="text-left bg-slate-50 rounded-xl border border-slate-100 px-3 py-2 text-sm text-slate-600 hover:border-blue-200 hover:bg-white transition-all"
                  >
                    {{ prompt }}
                  </button>
                </div>
              </div>
            </div>

            <div class="mt-4 border-t border-slate-100 pt-4">
              <div class="flex gap-3 items-end">
                <textarea
                  v-model="inputText"
                  :disabled="submitting"
                  @keydown.enter.exact.prevent="handleSubmit"
                  rows="3"
                  placeholder="Ask DataMaster anything..."
                  class="flex-1 rounded-2xl border border-slate-200 px-4 py-3 text-slate-700 text-sm resize-none outline-none focus:border-blue-400 disabled:opacity-60"
                />
                <button
                  @click="handleSubmit"
                  :disabled="!inputText.trim() || submitting"
                  class="w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors"
                  :class="!inputText.trim() || submitting ? 'bg-slate-300' : 'bg-blue-500 hover:bg-blue-600'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                  </svg>
                </button>
              </div>
              <p v-if="statusMessage" class="mt-3 text-left text-sm" :class="statusError ? 'text-rose-600' : 'text-slate-500'">
                {{ statusMessage }}
              </p>
            </div>
          </div>
        </div>

        <div class="w-full text-left">
          <h3 class="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <span class="w-1 h-4 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></span>
            Try these queries
          </h3>
          <div class="space-y-3">
            <button
              v-for="query in exampleQueries"
              :key="query"
              @click="inputText = query"
              class="w-full text-left bg-white rounded-xl shadow-md border border-slate-100 p-4 hover:shadow-lg hover:border-blue-200 transition-all duration-200 group"
            >
              <p class="text-slate-700 text-sm sm:text-base group-hover:text-slate-900">
                {{ query }}
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'

import { chatApi } from '@/services/api.js'

const messages = ref([
  {
    id: 'assistant-initial',
    role: 'assistant',
    content: '你好，我是 DataMaster。现在首页可以直接进行真实模型对话。',
    streaming: false,
  },
])
const inputText = ref('')
const submitting = ref(false)
const statusMessage = ref('')
const statusError = ref(false)
const availableModels = ref(['gpt-4o'])
const selectedModel = ref('gpt-4o')
const historyRef = ref(null)

const endpointLabel = computed(() => import.meta.env.VITE_LLM_PROVIDER_LABEL || 'Configured via backend .env')

const quickPrompts = [
  '总结一下 DataFlow、LoopAI、DFAgent 这三个服务的区别。',
  '给我一个构建数据处理 pipeline 的高层设计思路。',
  '解释一下为什么流式输出对首页聊天体验更重要。',
]

const exampleQueries = [
  '#kb/arxiv-stem-papers what are recent advances on superconductivity?',
  '@DataFlow generate CoT SFT data from #data/k12-science-textbooks',
  '@DataFlow extract knowledge graphs from #data/chemistry-books',
  '@LoopAI finetune a model on #data/math-proofs-corpus',
]

function buildRequestMessages() {
  return messages.value
    .filter((message) => !message.streaming)
    .map((message) => ({
      role: message.role,
      content: message.content,
    }))
}

async function scrollToBottom() {
  await nextTick()
  historyRef.value?.scrollTo({
    top: historyRef.value.scrollHeight,
    behavior: 'smooth',
  })
}

async function loadModels() {
  try {
    const payload = await chatApi.getModels()
    availableModels.value = payload.models?.length ? payload.models : ['gpt-4o']
    selectedModel.value = payload.default_model || availableModels.value[0]
    statusError.value = false
    statusMessage.value = `Provider ready. Default model: ${selectedModel.value}`
  } catch (error) {
    statusError.value = true
    statusMessage.value = `Unable to load models: ${error.message}`
  }
}

async function handleSubmit() {
  const question = inputText.value.trim()
  if (!question || submitting.value) return

  const userMessage = {
    id: `user-${Date.now()}`,
    role: 'user',
    content: question,
    streaming: false,
  }
  const assistantMessage = {
    id: `assistant-${Date.now()}`,
    role: 'assistant',
    content: '',
    streaming: true,
  }

  messages.value.push(userMessage)
  messages.value.push(assistantMessage)
  inputText.value = ''
  submitting.value = true
  statusError.value = false
  statusMessage.value = `Streaming response from ${selectedModel.value}...`
  scrollToBottom()

  try {
    const response = await chatApi.streamMessage({
      question,
      model: selectedModel.value,
      messages: buildRequestMessages(),
    })

    if (!response.ok || !response.body) {
      const text = await response.text()
      let message = text || `HTTP ${response.status}`
      try {
        message = JSON.parse(text).msg || message
      } catch {
        // Keep raw text if the backend didn't return JSON.
      }
      throw new Error(message)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const events = buffer.split('\n\n')
      buffer = events.pop() || ''

      for (const event of events) {
        const dataLine = event.split('\n').find((line) => line.startsWith('data: '))
        if (!dataLine) continue

        const payload = JSON.parse(dataLine.slice(6))
        if (payload.type === 'delta') {
          assistantMessage.content += payload.content
        } else if (payload.type === 'route') {
          assistantMessage.content = payload.data.answer || 'Agent routing is available but not enabled in the homepage UI yet.'
        } else if (payload.type === 'error') {
          throw new Error(payload.message)
        } else if (payload.type === 'done') {
          assistantMessage.streaming = false
          statusMessage.value = `Response complete from ${selectedModel.value}.`
        }
      }

      scrollToBottom()
    }

    assistantMessage.streaming = false
    if (!assistantMessage.content.trim()) {
      assistantMessage.content = 'No text was returned by the provider.'
    }
  } catch (error) {
    assistantMessage.streaming = false
    assistantMessage.content = `Request failed: ${error.message}`
    statusError.value = true
    statusMessage.value = error.message
  } finally {
    submitting.value = false
    scrollToBottom()
  }
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  await loadModels()
  scrollToBottom()
})
</script>
