<template>
  <div class="space-y-4">
    <div class="flex flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 md:flex-row md:items-center md:justify-between">
      <div>
        <div class="text-sm font-medium text-gray-900">Repository Files</div>
        <div class="text-xs text-gray-500">Browse revision-aware files from the current dataset repo.</div>
      </div>
      <label class="flex items-center gap-2 text-sm text-gray-600">
        <span>Revision</span>
        <select v-model="selectedRevision" class="rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900">
          <option v-for="version in versions" :key="version.revision" :value="version.revision">
            {{ version.revision }}{{ version.isLatest ? ' (latest)' : '' }}
          </option>
        </select>
      </label>
    </div>

    <div class="flex items-center flex-wrap gap-2 text-sm text-gray-500">
      <button class="hover:text-gray-700" @click="navigateTo('')">root</button>
      <template v-for="(segment, index) in breadcrumbSegments" :key="segment">
        <span>/</span>
        <button
          class="hover:text-gray-700"
          :class="index === breadcrumbSegments.length - 1 ? 'text-gray-900 font-medium' : ''"
          @click="navigateToSegment(index)"
        >
          {{ segment }}
        </button>
      </template>
    </div>

    <div class="grid gap-4 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)]">
      <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <div class="border-b border-gray-200 px-4 py-3">
          <div class="text-sm font-semibold text-gray-900">Files</div>
        </div>
        <div v-if="loadingTree" class="px-4 py-10 text-sm text-gray-500">Loading files...</div>
        <div v-else-if="treeItems.length" class="divide-y divide-gray-100">
          <button
            v-if="currentPath"
            class="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-gray-600 hover:bg-gray-50"
            @click="navigateUp"
          >
            <span class="inline-flex h-8 w-8 items-center justify-center rounded-md bg-gray-100 text-gray-500">..</span>
            <span>Parent directory</span>
          </button>
          <button
            v-for="item in treeItems"
            :key="item.path"
            class="flex w-full items-center gap-3 px-4 py-3 text-left hover:bg-gray-50"
            @click="handleItemClick(item)"
          >
            <span
              class="inline-flex h-8 w-8 items-center justify-center rounded-md"
              :class="item.type === 'directory' ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-500'"
            >
              {{ item.type === 'directory' ? 'D' : 'F' }}
            </span>
            <div class="min-w-0 flex-1">
              <div class="truncate text-sm font-medium" :class="item.type === 'directory' ? 'text-blue-700' : 'text-gray-900'">
                {{ item.name }}
              </div>
              <div class="mt-1 text-xs text-gray-500">
                <template v-if="item.type === 'directory'">
                  Directory
                </template>
                <template v-else>
                  {{ item.fileType }}
                  <span v-if="item.split"> · {{ item.split }}</span>
                  <span v-if="item.rows"> · {{ formatRows(item.rows) }} rows</span>
                </template>
              </div>
            </div>
            <div class="text-xs text-gray-400">
              {{ item.type === 'directory' ? item.size || '' : item.size }}
            </div>
          </button>
        </div>
        <div v-else class="px-4 py-10 text-sm text-gray-500">No files found for this path.</div>
      </div>

      <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <div class="border-b border-gray-200 px-4 py-3">
          <div class="text-sm font-semibold text-gray-900">Preview</div>
        </div>
        <div class="p-4">
          <div v-if="loadingPreview" class="text-sm text-gray-500">Loading preview...</div>
          <div v-else-if="selectedFile" class="space-y-4">
            <div>
              <div class="text-sm font-medium text-gray-900 break-all">{{ selectedFile.path }}</div>
              <div class="mt-1 text-xs text-gray-500">
                {{ selectedFile.fileType }}
                <span v-if="selectedFile.split"> · {{ selectedFile.split }}</span>
                <span v-if="selectedFile.rows"> · {{ formatRows(selectedFile.rows) }} rows</span>
              </div>
            </div>

            <div v-if="previewColumns.length" class="overflow-x-auto">
              <table class="min-w-full border border-gray-200 text-xs">
                <thead class="bg-gray-50">
                  <tr>
                    <th
                      v-for="column in previewColumns"
                      :key="column"
                      class="border-b border-gray-200 px-3 py-2 text-left font-medium text-gray-600"
                    >
                      {{ column }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in selectedFile.previewRows" :key="index" class="border-b border-gray-100">
                    <td
                      v-for="column in previewColumns"
                      :key="column"
                      class="px-3 py-2 align-top text-gray-700"
                    >
                      {{ formatCell(row[column]) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <pre v-else class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs text-gray-700">{{ selectedFile.previewText || 'Preview not available.' }}</pre>
          </div>
          <div v-else class="text-sm text-gray-500">Choose a file from the left panel to inspect it.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import { datasetApi } from '@/services/api.js'

const props = defineProps({
  repoId: { type: String, required: true },
  versions: { type: Array, default: () => [] },
  defaultRevision: { type: String, default: '' },
})

const selectedRevision = ref(props.defaultRevision || props.versions.find((item) => item.isLatest)?.revision || props.versions[0]?.revision || '')
const currentPath = ref('')
const treeItems = ref([])
const selectedFile = ref(null)
const loadingTree = ref(false)
const loadingPreview = ref(false)

const breadcrumbSegments = computed(() => currentPath.value ? currentPath.value.split('/') : [])
const previewColumns = computed(() => {
  const rows = selectedFile.value?.previewRows || []
  return rows.length ? Object.keys(rows[0]) : []
})

async function loadTree() {
  if (!props.repoId || !selectedRevision.value) return
  loadingTree.value = true
  try {
    const payload = await datasetApi.getDatasetTree(props.repoId, {
      revision: selectedRevision.value,
      path: currentPath.value,
    })
    treeItems.value = payload.items || []
  } catch (error) {
    console.error('Failed to load dataset tree:', error)
    treeItems.value = []
  } finally {
    loadingTree.value = false
  }
}

async function loadPreview(path) {
  loadingPreview.value = true
  try {
    selectedFile.value = await datasetApi.getDatasetPreview(props.repoId, path, selectedRevision.value)
  } catch (error) {
    console.error('Failed to load dataset preview:', error)
    selectedFile.value = null
  } finally {
    loadingPreview.value = false
  }
}

function handleItemClick(item) {
  if (item.type === 'directory') {
    currentPath.value = item.path
    selectedFile.value = null
    return
  }
  loadPreview(item.path)
}

function navigateTo(path) {
  currentPath.value = path
}

function navigateToSegment(index) {
  currentPath.value = breadcrumbSegments.value.slice(0, index + 1).join('/')
}

function navigateUp() {
  const parts = breadcrumbSegments.value.slice(0, -1)
  currentPath.value = parts.join('/')
}

function formatRows(value) {
  const rows = Number(value || 0)
  if (rows >= 1000000) return `${(rows / 1000000).toFixed(1).replace(/\.0$/, '')}M`
  if (rows >= 1000) return `${(rows / 1000).toFixed(1).replace(/\.0$/, '')}k`
  return String(rows)
}

function formatCell(value) {
  if (Array.isArray(value)) return value.join(', ')
  if (value && typeof value === 'object') return JSON.stringify(value)
  return value
}

watch(() => props.defaultRevision, (value) => {
  if (value) selectedRevision.value = value
})

watch(selectedRevision, () => {
  currentPath.value = ''
  selectedFile.value = null
  loadTree()
})

watch(currentPath, () => {
  loadTree()
})

onMounted(loadTree)
</script>
