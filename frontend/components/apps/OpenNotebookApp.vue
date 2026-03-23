<template>
  <div class="h-full bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
    <div class="px-5 py-4 border-b border-gray-200 space-y-3">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">Notebook Workspace</h2>
        <p class="text-sm text-gray-500">
          Open-NotebookLM runs as a separate workspace for document upload, source-grounded QA, and notebook-style knowledge outputs.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span class="inline-flex items-center rounded-full bg-indigo-50 px-2.5 py-1 font-medium text-indigo-700">
          Open-NotebookLM
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
    <iframe
      :src="iframeSrc"
      class="flex-1 border-0 w-full min-h-[780px]"
      sandbox="allow-scripts allow-forms allow-same-origin allow-downloads allow-modals"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { resolveServiceUrl } from '@/config/index.js'

const iframeSrc = computed(() => {
  const baseUrl = resolveServiceUrl(import.meta.env.VITE_OPEN_NOTEBOOK_URL, 3001)
  return `${baseUrl}/`
})
</script>
