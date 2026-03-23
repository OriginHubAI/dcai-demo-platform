<template>
  <div class="space-y-4">
    <div class="rounded-lg border border-gray-200 bg-white p-4">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div class="text-sm font-semibold text-gray-900">Data Studio Lite</div>
          <div class="text-xs text-gray-500">Real preview rows driven by the new HF-compatible read APIs.</div>
        </div>
        <div class="grid gap-3 sm:grid-cols-3">
          <label class="text-sm text-gray-600">
            <span class="mb-1 block text-xs uppercase tracking-wide text-gray-400">Revision</span>
            <select v-model="selectedRevision" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900">
              <option v-for="version in versions" :key="version.revision" :value="version.revision">
                {{ version.revision }}{{ version.isLatest ? ' (latest)' : '' }}
              </option>
            </select>
          </label>
          <label class="text-sm text-gray-600">
            <span class="mb-1 block text-xs uppercase tracking-wide text-gray-400">Split</span>
            <select v-model="selectedSplit" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900">
              <option value="">Auto</option>
              <option v-for="split in splits" :key="split.split" :value="split.split">
                {{ split.split }} ({{ formatRows(split.num_rows) }})
              </option>
            </select>
          </label>
          <label class="text-sm text-gray-600">
            <span class="mb-1 block text-xs uppercase tracking-wide text-gray-400">Filter current rows</span>
            <input
              v-model="searchQuery"
              type="text"
              class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900"
              placeholder="Search loaded preview rows"
            />
          </label>
        </div>
      </div>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-gray-400">Rows</div>
        <div class="mt-2 text-2xl font-semibold text-gray-900">{{ formatRows(totalRows) }}</div>
      </div>
      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-gray-400">Split Count</div>
        <div class="mt-2 text-2xl font-semibold text-gray-900">{{ splits.length }}</div>
      </div>
      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-gray-400">Features</div>
        <div class="mt-2 text-2xl font-semibold text-gray-900">{{ featureCount }}</div>
      </div>
      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-gray-400">Source File</div>
        <div class="mt-2 break-all text-sm font-medium text-gray-900">{{ activeFilePath || 'Auto-selected' }}</div>
      </div>
    </div>

    <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <div class="border-b border-gray-200 px-4 py-3">
        <div class="text-sm font-semibold text-gray-900">Preview Rows</div>
      </div>
      <div class="p-4">
        <div v-if="loading" class="text-sm text-gray-500">Loading dataset rows...</div>
        <div v-else-if="filteredRows.length && columns.length" class="overflow-x-auto">
          <table class="min-w-full border border-gray-200 text-xs">
            <thead class="bg-gray-50">
              <tr>
                <th class="border-b border-gray-200 px-3 py-2 text-left font-medium text-gray-600">#</th>
                <th
                  v-for="column in columns"
                  :key="column"
                  class="border-b border-gray-200 px-3 py-2 text-left font-medium text-gray-600"
                >
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in filteredRows" :key="row.row_idx" class="border-b border-gray-100">
                <td class="px-3 py-2 align-top text-gray-400">{{ row.row_idx }}</td>
                <td
                  v-for="column in columns"
                  :key="column"
                  class="px-3 py-2 align-top text-gray-700"
                >
                  {{ formatCell(row.row[column]) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-sm text-gray-500">No preview rows available for the selected revision and split.</div>
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
const selectedSplit = ref('')
const searchQuery = ref('')
const splits = ref([])
const rowsPayload = ref({ rows: [], features: {}, num_rows_total: 0, file: null })
const loading = ref(false)

const columns = computed(() => {
  const firstRow = rowsPayload.value.rows?.[0]?.row
  return firstRow ? Object.keys(firstRow) : []
})

const totalRows = computed(() => rowsPayload.value.num_rows_total || 0)
const featureCount = computed(() => Object.keys(rowsPayload.value.features || {}).length)
const activeFilePath = computed(() => rowsPayload.value.file?.path || '')

const filteredRows = computed(() => {
  const rows = rowsPayload.value.rows || []
  if (!searchQuery.value) return rows
  const query = searchQuery.value.toLowerCase()
  return rows.filter((entry) => JSON.stringify(entry.row).toLowerCase().includes(query))
})

async function loadSplitsAndRows() {
  if (!props.repoId || !selectedRevision.value) return
  loading.value = true
  try {
    const [splitPayload, rowsData] = await Promise.all([
      datasetApi.getHFDatasetSplits(props.repoId, { revision: selectedRevision.value }),
      datasetApi.getHFDatasetRows(props.repoId, {
        revision: selectedRevision.value,
        split: selectedSplit.value,
        length: 20,
      }),
    ])
    splits.value = splitPayload.splits || []
    rowsPayload.value = rowsData
  } catch (error) {
    console.error('Failed to load Data Studio data:', error)
    splits.value = []
    rowsPayload.value = { rows: [], features: {}, num_rows_total: 0, file: null }
  } finally {
    loading.value = false
  }
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

watch([selectedRevision, selectedSplit], () => {
  loadSplitsAndRows()
})

onMounted(loadSplitsAndRows)
</script>
