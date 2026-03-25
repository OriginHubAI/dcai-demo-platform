<template>
  <div class="rounded-lg border border-gray-200 bg-white p-4">
    <div class="flex items-center justify-between gap-3">
      <div>
        <h3 class="text-sm font-semibold text-gray-900">Provider Sync</h3>
        <p class="mt-1 text-xs text-gray-500">External registry and storage bindings for the current repo.</p>
      </div>
      <span class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium" :class="syncStatusClass">
        {{ syncStatusLabel }}
      </span>
    </div>

    <div v-if="providerList.length" class="mt-4 space-y-3">
      <div
        v-for="provider in providerList"
        :key="provider.key"
        class="rounded-lg border border-gray-200 bg-gray-50 p-3"
      >
        <div class="flex items-center justify-between gap-3">
          <div class="text-sm font-medium text-gray-900">{{ provider.label }}</div>
          <span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium" :class="stateClass(provider.binding.state)">
            {{ provider.binding.state || 'unknown' }}
          </span>
        </div>

        <div v-if="provider.rows.length" class="mt-3 space-y-2">
          <div
            v-for="row in provider.rows"
            :key="`${provider.key}-${row.label}`"
            class="flex items-start justify-between gap-3 text-xs"
          >
            <span class="text-gray-500">{{ row.label }}</span>
            <a
              v-if="row.isLink"
              :href="row.value"
              target="_blank"
              rel="noreferrer"
              class="break-all text-right font-medium text-blue-600 hover:underline"
            >
              {{ row.value }}
            </a>
            <span v-else class="break-all text-right font-medium text-gray-900">{{ row.value }}</span>
          </div>
        </div>

        <p v-if="provider.binding.errorMessage" class="mt-3 text-xs text-red-600">{{ provider.binding.errorMessage }}</p>
      </div>
    </div>
    <div v-else class="mt-4 rounded-lg border border-dashed border-gray-200 bg-gray-50 px-3 py-4 text-sm text-gray-500">
      No external provider is bound. This repo is currently local-only.
    </div>

    <div v-if="versionRows.length || versionPayloadText" class="mt-4 rounded-lg border border-gray-200 p-3">
      <div class="text-sm font-medium text-gray-900">Selected Revision Sync</div>
      <div v-if="versionRows.length" class="mt-3 space-y-2">
        <div v-for="row in versionRows" :key="row.label" class="flex items-start justify-between gap-3 text-xs">
          <span class="text-gray-500">{{ row.label }}</span>
          <a
            v-if="row.isLink"
            :href="row.value"
            target="_blank"
            rel="noreferrer"
            class="break-all text-right font-medium text-blue-600 hover:underline"
          >
            {{ row.value }}
          </a>
          <span v-else class="break-all text-right font-medium text-gray-900">{{ row.value }}</span>
        </div>
      </div>
      <pre
        v-if="versionPayloadText"
        class="mt-3 max-h-64 overflow-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-3 text-[11px] text-gray-700"
      >{{ versionPayloadText }}</pre>
    </div>

    <div v-if="buildRows.length || buildPayloadText" class="mt-4 rounded-lg border border-gray-200 p-3">
      <div class="text-sm font-medium text-gray-900">Latest Build Provider</div>
      <div v-if="buildRows.length" class="mt-3 space-y-2">
        <div v-for="row in buildRows" :key="row.label" class="flex items-start justify-between gap-3 text-xs">
          <span class="text-gray-500">{{ row.label }}</span>
          <span class="break-all text-right font-medium text-gray-900">{{ row.value }}</span>
        </div>
      </div>
      <pre
        v-if="buildPayloadText"
        class="mt-3 max-h-64 overflow-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-3 text-[11px] text-gray-700"
      >{{ buildPayloadText }}</pre>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  syncStatus: { type: String, default: 'local' },
  providerBindings: { type: Object, default: () => ({}) },
  selectedVersion: { type: Object, default: null },
  selectedBuild: { type: Object, default: null },
})

const syncStatusLabelMap = {
  synced: 'synced',
  partial: 'partial',
  error: 'error',
  local: 'local-only',
}

const syncStatusClassMap = {
  synced: 'bg-green-100 text-green-700',
  partial: 'bg-yellow-100 text-yellow-700',
  error: 'bg-red-100 text-red-700',
  local: 'bg-gray-100 text-gray-700',
}

const providerList = computed(() =>
  Object.entries(props.providerBindings || {}).map(([key, binding]) => ({
    key,
    label: providerLabel(key),
    binding: binding || {},
    rows: bindingRows(binding || {}),
  })),
)

const syncStatusLabel = computed(() => syncStatusLabelMap[props.syncStatus] || props.syncStatus || 'unknown')
const syncStatusClass = computed(() => syncStatusClassMap[props.syncStatus] || syncStatusClassMap.local)

const versionRows = computed(() => {
  const version = props.selectedVersion || {}
  const rows = []
  pushRow(rows, 'Provider revision', version.providerRevision)
  pushRow(rows, 'Provider commit', version.providerCommit)
  pushRow(rows, 'Artifact URI', version.artifactUri, isHttpUrl(version.artifactUri))
  pushRow(rows, 'MLflow stage', version.providerPayload?.mlflow?.currentStage)
  return rows
})

const buildRows = computed(() => {
  const build = props.selectedBuild || {}
  const rows = []
  pushRow(rows, 'Provider status', build.providerStatus)
  pushRow(rows, 'Provider job ID', build.providerJobId)
  return rows
})

const versionPayloadText = computed(() => payloadText(props.selectedVersion?.providerPayload))
const buildPayloadText = computed(() => payloadText(props.selectedBuild?.providerPayload))

function stateClass(state) {
  if (state === 'ready') return 'bg-green-100 text-green-700'
  if (state === 'error') return 'bg-red-100 text-red-700'
  if (state === 'disabled') return 'bg-gray-100 text-gray-700'
  return 'bg-yellow-100 text-yellow-700'
}

function providerLabel(key) {
  const labels = {
    gitea: 'Gitea',
    localgit: 'Local Git',
    lakefs: 'lakeFS',
    mlflow: 'MLflow',
    ragflow: 'RAGFlow',
  }
  return labels[key] || key
}

function bindingRows(binding) {
  return Object.entries(binding || {})
    .filter(([key, value]) => !['state', 'provider', 'errorMessage'].includes(key) && hasValue(value))
    .map(([key, value]) => ({
      label: humanize(key),
      value: formatValue(value),
      isLink: typeof value === 'string' && isHttpUrl(value),
    }))
}

function payloadText(payload) {
  if (!payload || !Object.keys(payload).length) return ''
  return JSON.stringify(payload, null, 2)
}

function pushRow(rows, label, value, isLink = false) {
  if (!hasValue(value)) return
  rows.push({ label, value: formatValue(value), isLink })
}

function hasValue(value) {
  if (value === null || value === undefined || value === '') return false
  if (Array.isArray(value)) return value.length > 0
  if (typeof value === 'object') return Object.keys(value).length > 0
  return true
}

function formatValue(value) {
  if (Array.isArray(value)) return value.join(', ')
  if (value && typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

function humanize(value) {
  return String(value)
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .replace(/[_-]+/g, ' ')
    .replace(/\b\w/g, (match) => match.toUpperCase())
}

function isHttpUrl(value) {
  return /^https?:\/\//.test(String(value || ''))
}
</script>
