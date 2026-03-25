<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="loading" class="py-20 text-center text-gray-500">Loading dataset...</div>
    <div v-else-if="dataset">
      <div class="mb-4 flex items-center space-x-2 text-sm text-gray-500">
        <router-link to="/datasets" class="hover:text-gray-700">Datasets</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ dataset.id }}</span>
      </div>

      <div class="mb-6 space-y-4">
        <div class="flex items-start justify-between gap-4">
          <div class="flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-full bg-green-100 text-lg font-bold text-green-700">
              {{ dataset.author.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">{{ dataset.name }}</h1>
              <p class="text-sm text-gray-500">by {{ dataset.author }}</p>
            </div>
          </div>
          <div class="hidden items-center space-x-3 sm:flex">
            <StatBadge icon="download" :value="dataset.downloads" />
            <StatBadge icon="like" :value="dataset.likes" />
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <TagBadge :label="dataset.task" :color="taskColorMap[dataset.task] || 'gray'" />
          <TagBadge :label="dataset.domain" :color="domainColorMap[dataset.domain] || 'gray'" />
          <TagBadge :label="dataset.modality" color="teal" />
          <TagBadge v-if="dataset.datasetType" :label="dataset.datasetType" :color="datasetTypeColorMap[dataset.datasetType] || 'gray'" />
          <TagBadge v-if="dataset.readonly" label="read-only" color="red" />
          <TagBadge v-if="dataset.hfCompatible" label="HF Compatible" color="green" />
        </div>

        <div class="flex items-center gap-3">
          <label class="text-sm text-gray-600">Revision</label>
          <select
            v-model="selectedRevision"
            class="rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 focus:border-blue-500 focus:outline-none"
          >
            <option v-for="version in dataset.versions" :key="version.revision" :value="version.revision">
              {{ version.revision }}{{ version.isLatest ? ' (latest)' : '' }}
            </option>
          </select>
          <button
            class="inline-flex items-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="showPublishModal = true"
          >
            Publish Revision
          </button>
          <button
            v-if="canSyncFromGit"
            class="inline-flex items-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="syncing"
            @click="syncFromGit"
          >
            {{ syncing ? 'Syncing...' : 'Sync from Git' }}
          </button>
          <span v-if="syncError" class="text-xs text-red-600">{{ syncError }}</span>
        </div>

        <div class="border-b border-gray-200">
          <nav class="-mb-px flex flex-wrap gap-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              class="border-b-2 px-1 py-3 text-sm font-medium transition-colors"
              :class="activeTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </div>

      <div v-if="activeTab === 'card'" class="lg:grid lg:grid-cols-3 lg:gap-8">
        <div class="space-y-6 lg:col-span-2">
          <div class="rounded-lg border border-gray-200 bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Dataset Card</h2>
            </div>
            <div class="space-y-5 p-6">
              <section v-for="section in dataset.cardSections" :key="section.title" class="space-y-2">
                <h3 class="text-base font-semibold text-gray-900">{{ section.title }}</h3>
                <p class="whitespace-pre-wrap text-sm leading-6 text-gray-700">{{ section.content }}</p>
              </section>
            </div>
          </div>

          <div class="rounded-lg border border-gray-200 bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Revisions</h2>
            </div>
            <div class="divide-y divide-gray-100">
              <div v-for="version in dataset.versions" :key="version.revision" class="flex items-start justify-between gap-4 px-4 py-3">
                <div>
                  <div class="flex items-center gap-2 text-sm font-medium text-gray-900">
                    <span>{{ version.revision }}</span>
                    <span v-if="version.isLatest" class="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700">latest</span>
                  </div>
                  <div class="mt-1 text-xs text-gray-500">
                    commit {{ version.commitSha }} · {{ formatRows(version.rows) }} rows · {{ version.size }}
                  </div>
                </div>
                <div class="text-xs text-gray-500">{{ formatDateTime(version.createdAt) }}</div>
              </div>
            </div>
          </div>

          <div class="rounded-lg border border-gray-200 bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Usage</h2>
            </div>
            <div class="space-y-4 p-4">
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Hugging Face Datasets style</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ dataset.usage?.hfDatasets }}</pre>
              </div>
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Git Clone</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ dataset.usage?.gitClone }}</pre>
              </div>
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Git Push</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ dataset.usage?.gitPush }}</pre>
              </div>
            </div>
          </div>
        </div>

        <aside class="mt-6 lg:mt-0">
          <div class="sticky top-20 space-y-4 rounded-lg border border-gray-200 bg-white p-4">
            <div class="flex items-center justify-between sm:hidden">
              <StatBadge icon="download" :value="dataset.downloads" />
              <StatBadge icon="like" :value="dataset.likes" />
            </div>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Rows</span>
                <span class="text-right font-medium text-gray-900">{{ formatRows(dataset.rows) }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Size</span>
                <span class="text-right font-medium text-gray-900">{{ dataset.size }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Language</span>
                <span class="text-right font-medium text-gray-900">{{ dataset.language }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">License</span>
                <span class="text-right font-medium text-gray-900">{{ dataset.license }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Latest revision</span>
                <span class="text-right font-medium text-gray-900">{{ dataset.latestRevision }}</span>
              </div>
            </div>
            <hr class="border-gray-200" />
            <div class="space-y-2">
              <h4 class="text-sm font-semibold text-gray-700">Metadata</h4>
              <div v-for="(value, key) in dataset.metadata" :key="key" class="text-sm">
                <div class="capitalize text-gray-500">{{ key }}</div>
                <div class="break-words text-gray-900">{{ formatCell(value) }}</div>
              </div>
            </div>
          </div>
          <ProviderSyncPanel
            class="mt-4"
            :sync-status="dataset.syncStatus"
            :provider-bindings="dataset.providerBindings"
            :selected-version="dataset.selectedVersion"
          />
        </aside>
      </div>

      <DatasetFilesBrowser
        v-else-if="activeTab === 'files'"
        :repo-id="dataset.id"
        :versions="dataset.versions"
        :default-revision="selectedRevision || dataset.defaultRevision || dataset.latestRevision"
      />

      <DataStudioLite
        v-else
        :repo-id="dataset.id"
        :versions="dataset.versions"
        :default-revision="selectedRevision || dataset.defaultRevision || dataset.latestRevision"
      />
    </div>
    <div v-else class="py-20 text-center">
      <p class="text-lg text-gray-500">Dataset not found</p>
      <router-link to="/datasets" class="mt-2 inline-block text-sm text-blue-600 hover:underline">Back to Datasets</router-link>
    </div>

    <RevisionPublishModal
      :visible="showPublishModal && !!dataset"
      repo-type="dataset"
      :repo-id="dataset?.id || route.params.id"
      @close="showPublishModal = false"
      @published="handleRevisionPublished"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { datasetApi } from '@/services/api.js'
import { taskColorMap, domainColorMap, datasetTypeColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import DatasetFilesBrowser from '@/components/datasets/DatasetFilesBrowser.vue'
import DataStudioLite from '@/components/datasets/DataStudioLite.vue'
import ProviderSyncPanel from '@/components/hub/ProviderSyncPanel.vue'
import RevisionPublishModal from '@/components/hub/RevisionPublishModal.vue'

const route = useRoute()
const dataset = ref(null)
const loading = ref(false)
const activeTab = ref('card')
const selectedRevision = ref('')
const showPublishModal = ref(false)
const syncing = ref(false)
const syncError = ref('')

const tabs = [
  { id: 'card', label: 'Dataset Card' },
  { id: 'files', label: 'Files' },
  { id: 'datastudio', label: 'Data Studio Lite' },
]

const canSyncFromGit = computed(() => {
  const bindings = dataset.value?.providerBindings || {}
  return Boolean(bindings.gitea || bindings.localgit)
})

async function loadDataset(revision = selectedRevision.value) {
  loading.value = true
  try {
    dataset.value = await datasetApi.getDatasetById(route.params.id, { revision })
    if (!selectedRevision.value) {
      selectedRevision.value = dataset.value?.selectedRevision || dataset.value?.defaultRevision || dataset.value?.latestRevision || ''
    }
  } catch (error) {
    console.error('Failed to load dataset:', error)
    dataset.value = null
  } finally {
    loading.value = false
  }
}

onMounted(loadDataset)
watch(() => route.params.id, () => {
  activeTab.value = 'card'
  selectedRevision.value = ''
  syncError.value = ''
  loadDataset('')
})
watch(selectedRevision, (next, prev) => {
  if (!next || next === prev) return
  loadDataset(next)
})

function handleRevisionPublished(response) {
  showPublishModal.value = false
  activeTab.value = 'card'
  const revision = response?.version?.revision || ''
  if (revision) {
    selectedRevision.value = revision
    return
  }
  loadDataset(selectedRevision.value)
}

async function syncFromGit() {
  if (!dataset.value) return
  syncing.value = true
  syncError.value = ''
  try {
    const response = await datasetApi.syncDataset(
      dataset.value.id,
      selectedRevision.value || dataset.value.defaultRevision || dataset.value.latestRevision || '',
    )
    const revision = response?.version?.revision || selectedRevision.value || dataset.value.defaultRevision || ''
    if (revision && revision !== selectedRevision.value) {
      selectedRevision.value = revision
    } else {
      await loadDataset(revision)
    }
  } catch (error) {
    console.error('Failed to sync dataset from git:', error)
    syncError.value = error.message || 'Failed to sync from Git'
  } finally {
    syncing.value = false
  }
}

function formatRows(n) {
  const value = Number(n || 0)
  if (value >= 1000000) return `${(value / 1000000).toFixed(1).replace(/\.0$/, '')}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1).replace(/\.0$/, '')}k`
  return String(value)
}

function formatDateTime(value) {
  return new Date(value).toLocaleString()
}

function formatCell(value) {
  if (Array.isArray(value)) return value.join(', ')
  if (value && typeof value === 'object') return JSON.stringify(value)
  return value
}
</script>
