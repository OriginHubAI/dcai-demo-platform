<template>
  <div class="h-full bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
    <div class="px-5 py-4 border-b border-gray-200 space-y-3">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">PackageEditor-Agent</h2>
        <p class="text-sm text-gray-500">
          Clicking a package creates an isolated DataFlow sandbox copy and opens it in OpenCode. Type coding instructions inside OpenCode itself.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span class="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-1 font-medium text-emerald-700">
          Sandbox mode
        </span>
        <span v-if="selectedPackage" class="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-700">
          package: {{ selectedPackage }}
        </span>
        <span v-if="sessionInfo?.package_path" class="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-700">
          path: {{ sessionInfo.package_path }}
        </span>
        <a
          v-if="iframeSrc"
          :href="iframeSrc"
          target="_blank"
          rel="noreferrer"
          class="inline-flex items-center rounded-full bg-slate-900 px-2.5 py-1 font-medium text-white hover:bg-slate-800"
        >
          Open in new tab
        </a>
        <button
          v-if="selectedPackage"
          class="inline-flex items-center rounded-full bg-emerald-600 px-2.5 py-1 font-medium text-white hover:bg-emerald-700"
          @click="rebuildSandbox"
        >
          Rebuild Sandbox
        </button>
      </div>
    </div>
    <div v-if="loading" class="flex-1 flex items-center justify-center bg-slate-50 px-6 text-center">
      <div>
        <p class="text-slate-700 mb-2">Preparing isolated sandbox for {{ selectedPackage || 'package' }}...</p>
        <p class="text-sm text-slate-500">A fresh DataFlow copy is being created before OpenCode starts.</p>
      </div>
    </div>
    <div v-else-if="statusMessage" class="flex-1 flex items-center justify-center bg-slate-50 text-center px-6">
      <div>
        <p class="text-slate-700 mb-2">{{ statusMessage }}</p>
        <p v-if="sessionInfo?.sandbox_path" class="text-sm text-slate-500 mb-4">Sandbox: {{ sessionInfo.sandbox_path }}</p>
        <button
          v-if="selectedPackage"
          class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-sm"
          @click="rebuildSandbox"
        >
          Retry
        </button>
      </div>
    </div>
    <div v-else-if="iframeError" class="flex-1 flex items-center justify-center bg-slate-50 text-center px-6">
      <div>
        <p class="text-slate-700 mb-2">PackageEditor-Agent service is not reachable.</p>
        <p class="text-sm text-slate-500 mb-4">Expected URL: {{ iframeSrc }}</p>
        <button class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-sm" @click="reloadIframe">Retry</button>
      </div>
    </div>
    <iframe
      v-else-if="iframeSrc"
      ref="frameRef"
      :src="iframeSrc"
      :key="iframeKey"
      class="flex-1 border-0 w-full min-h-[760px]"
      sandbox="allow-scripts allow-forms allow-same-origin allow-downloads allow-modals"
      @error="iframeError = true"
    />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { resolveServiceUrl } from '@/config/index.js'
import { dataflowApi } from '@/services/api.js'

const route = useRoute()
const frameRef = ref(null)
const iframeError = ref(false)
const iframeKey = ref(0)
const loading = ref(false)
const statusMessage = ref('')
const sessionInfo = ref(null)

const selectedPackage = computed(() => {
  if (typeof route.query.package !== 'string') return ''
  return route.query.package
})

const packageEditorBaseUrl = computed(() => {
  return sessionInfo.value?.url || import.meta.env.VITE_PACKAGE_EDITOR_URL || ''
})

function encodeDirectoryPath(value) {
  if (!value) return ''
  const bytes = new TextEncoder().encode(value)
  let binary = ''
  for (const byte of bytes) {
    binary += String.fromCharCode(byte)
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '')
}

const iframeSrc = computed(() => {
  if (sessionInfo.value?.mode !== 'external' || !sessionInfo.value?.url) return ''
  const baseUrl = resolveServiceUrl(packageEditorBaseUrl.value, 18004)
  if (sessionInfo.value?.session_id && sessionInfo.value?.session_directory) {
    const encodedDirectory = encodeDirectoryPath(sessionInfo.value.session_directory)
    return `${baseUrl}/${encodedDirectory}/session/${sessionInfo.value.session_id}?t=${iframeKey.value}`
  }
  return `${baseUrl}/?package=${encodeURIComponent(selectedPackage.value)}&t=${iframeKey.value}`
})

async function startEditorSession(force = false) {
  if (!selectedPackage.value) {
    statusMessage.value = 'No package selected.'
    return
  }

  iframeError.value = false
  loading.value = true
  statusMessage.value = ''
  try {
    if (force) {
      await dataflowApi.stopPackageEditor(selectedPackage.value)
    }
    const session = await dataflowApi.startPackageEditor(selectedPackage.value)
    sessionInfo.value = session
    iframeKey.value = Date.now()
    if (session.mode !== 'external') {
      statusMessage.value = session.reason || 'Package editor is unavailable.'
    }
  } catch (error) {
    statusMessage.value = `Failed to prepare sandbox: ${error.message}`
  } finally {
    loading.value = false
  }
}

async function reloadIframe() {
  iframeError.value = false
  await startEditorSession(true)
}

async function rebuildSandbox() {
  await startEditorSession(true)
}

watch(selectedPackage, () => {
  startEditorSession()
}, { immediate: true })
</script>
