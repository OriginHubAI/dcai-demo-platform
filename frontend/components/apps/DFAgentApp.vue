<template>
  <div class="h-full bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
    <div class="px-5 py-4 border-b border-gray-200">
      <h2 class="text-lg font-semibold text-gray-900">DataFlow-Agent</h2>
      <p class="text-sm text-gray-500">Embedded Gradio workspace for operator QA, pipeline recommendation, and web collection.</p>
    </div>
    <div v-if="iframeError" class="flex-1 flex items-center justify-center bg-slate-50 text-center px-6">
      <div>
        <p class="text-slate-700 mb-2">DataFlow-Agent service is not reachable.</p>
        <p class="text-sm text-slate-500 mb-4">Expected URL: {{ iframeSrc }}</p>
        <button class="px-3 py-1.5 rounded-lg bg-blue-600 text-white text-sm" @click="reloadIframe">Retry</button>
      </div>
    </div>
    <iframe
      v-else
      ref="frameRef"
      :src="iframeSrc"
      class="flex-1 border-0 w-full"
      sandbox="allow-scripts allow-forms allow-same-origin"
      @error="iframeError = true"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { resolveServiceUrl } from '@/config/index.js'

const route = useRoute()
const frameRef = ref(null)
const iframeError = ref(false)

const iframeSrc = computed(() => {
  const baseUrl = resolveServiceUrl(import.meta.env.VITE_DFAGENT_URL, 7860)
  const url = new URL(baseUrl)
  if (typeof route.query.tab === 'string' && route.query.tab) {
    url.searchParams.set('tab', route.query.tab)
  }
  return url.toString()
})

function reloadIframe() {
  iframeError.value = false
  if (frameRef.value) {
    frameRef.value.src = iframeSrc.value
  }
}
</script>
