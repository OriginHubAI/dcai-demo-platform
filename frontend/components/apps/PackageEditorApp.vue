<template>
  <div class="h-full bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
    <div class="px-5 py-4 border-b border-gray-200 space-y-3">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">PackageEditor-Agent</h2>
        <p class="text-sm text-gray-500">
          OpenCode web workspace bound to an isolated DataFlow sandbox copy. The main DataFlow repository is not edited directly.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span class="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-1 font-medium text-emerald-700">
          Sandbox mode
        </span>
        <span v-if="selectedPackage" class="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-700">
          package: {{ selectedPackage }}
        </span>
        <a
          :href="iframeSrc"
          target="_blank"
          rel="noreferrer"
          class="inline-flex items-center rounded-full bg-slate-900 px-2.5 py-1 font-medium text-white hover:bg-slate-800"
        >
          Open in new tab
        </a>
      </div>
    </div>
    <div v-if="iframeError" class="flex-1 flex items-center justify-center bg-slate-50 text-center px-6">
      <div>
        <p class="text-slate-700 mb-2">PackageEditor-Agent service is not reachable.</p>
        <p class="text-sm text-slate-500 mb-4">Expected URL: {{ iframeSrc }}</p>
        <button class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-sm" @click="reloadIframe">Retry</button>
      </div>
    </div>
    <iframe
      v-else
      ref="frameRef"
      :src="iframeSrc"
      class="flex-1 border-0 w-full min-h-[760px]"
      sandbox="allow-scripts allow-forms allow-same-origin allow-downloads allow-modals"
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

const selectedPackage = computed(() => {
  if (typeof route.query.package !== 'string') return ''
  return route.query.package
})

const iframeSrc = computed(() => {
  return resolveServiceUrl(import.meta.env.VITE_PACKAGE_EDITOR_URL, 18004)
})

function reloadIframe() {
  iframeError.value = false
  if (frameRef.value) {
    frameRef.value.src = iframeSrc.value
  }
}
</script>
