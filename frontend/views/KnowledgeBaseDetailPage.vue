<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="loading" class="py-20 text-center text-gray-500">Loading knowledge base...</div>
    <div v-else-if="knowledgeBase">
      <div class="mb-4 flex items-center space-x-2 text-sm text-gray-500">
        <router-link to="/knowledge-base" class="hover:text-gray-700">Knowledge Bases</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ knowledgeBase.id }}</span>
      </div>

      <div class="mb-6 space-y-4">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 text-lg font-bold text-indigo-700">
                {{ knowledgeBase.author.charAt(0).toUpperCase() }}
              </div>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">{{ knowledgeBase.name }}</h1>
                <p class="text-sm text-gray-500">by {{ knowledgeBase.author }}</p>
              </div>
              <span
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                :class="statusClass"
              >
                {{ knowledgeBase.status }}
              </span>
            </div>
            <p class="max-w-3xl text-sm leading-6 text-gray-700">{{ knowledgeBase.description }}</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in knowledgeBase.tags || []"
                :key="tag"
                class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-700"
              >
                {{ tag }}
              </span>
              <span
                v-if="knowledgeBase.hfCompatible"
                class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-1 text-xs text-green-700"
              >
                HF Compatible
              </span>
            </div>
          </div>

          <div class="flex flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 lg:min-w-80">
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div>
                <div class="text-gray-500">Documents</div>
                <div class="font-semibold text-gray-900">{{ formatCount(knowledgeBase.documentCount) }}</div>
              </div>
              <div>
                <div class="text-gray-500">Files</div>
                <div class="font-semibold text-gray-900">{{ formatCount(knowledgeBase.fileCount) }}</div>
              </div>
              <div>
                <div class="text-gray-500">Vectors</div>
                <div class="font-semibold text-gray-900">{{ formatCount(knowledgeBase.vectorStore?.vectorCount) }}</div>
              </div>
              <div>
                <div class="text-gray-500">Visibility</div>
                <div class="font-semibold text-gray-900">{{ knowledgeBase.visibility }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button
                @click="showPublishModal = true"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Publish Revision
              </button>
              <button
                v-if="canSyncFromGit"
                @click="syncFromGit"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
                :disabled="syncing"
              >
                {{ syncing ? 'Syncing...' : 'Sync from Git' }}
              </button>
              <button
                @click="triggerBuild"
                class="inline-flex items-center justify-center rounded-lg bg-dc-primary px-3 py-2 text-sm font-medium text-white hover:bg-dc-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
                :disabled="buildStarting"
              >
                {{ buildStarting ? 'Starting...' : 'Trigger Build' }}
              </button>
              <button
                @click="showGraphModal = true"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                :disabled="!knowledgeBase.knowledgeGraph?.enabled"
              >
                View Graph
              </button>
              <router-link
                :to="{ name: 'notebook', query: { knowledge_base: knowledgeBase.id } }"
                class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Open Notebook
              </router-link>
            </div>
            <div v-if="syncError" class="text-xs text-red-600">{{ syncError }}</div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <label class="text-sm text-gray-600">Revision</label>
          <select
            v-model="selectedRevision"
            class="rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 focus:border-blue-500 focus:outline-none"
          >
            <option
              v-for="version in knowledgeBase.versions || []"
              :key="version.revision"
              :value="version.revision"
            >
              {{ version.revision }}{{ version.isLatest ? ' (latest)' : '' }}
            </option>
          </select>
          <span class="text-xs text-gray-500">Source dataset: {{ knowledgeBase.sourceDataset || 'n/a' }}</span>
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

      <div v-if="activeTab === 'card'" class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
        <div class="space-y-6">
          <div class="rounded-lg border border-gray-200 bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Knowledge Card</h2>
            </div>
            <div class="space-y-5 p-6">
              <section v-for="section in knowledgeBase.cardSections || []" :key="section.title" class="space-y-2">
                <h3 class="text-base font-semibold text-gray-900">{{ section.title }}</h3>
                <p class="whitespace-pre-wrap text-sm leading-6 text-gray-700">{{ section.content }}</p>
              </section>
            </div>
          </div>

          <div class="rounded-lg border border-gray-200 bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Usage</h2>
            </div>
            <div class="space-y-4 p-4">
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">HF Datasets style</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ knowledgeBase.usage?.hfDatasets }}</pre>
              </div>
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Notebook</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ knowledgeBase.usage?.notebook }}</pre>
              </div>
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Git Clone</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ knowledgeBase.usage?.gitClone }}</pre>
              </div>
              <div>
                <div class="mb-2 text-sm font-medium text-gray-900">Git Push</div>
                <pre class="overflow-x-auto whitespace-pre-wrap rounded-lg bg-gray-50 p-4 text-xs">{{ knowledgeBase.usage?.gitPush }}</pre>
              </div>
            </div>
          </div>
        </div>

        <aside class="space-y-4">
          <ProviderSyncPanel
            :sync-status="knowledgeBase.syncStatus"
            :provider-bindings="knowledgeBase.providerBindings"
            :selected-version="knowledgeBase.selectedVersion"
            :selected-build="knowledgeBase.builds?.[0] || null"
          />

          <div class="rounded-lg border border-gray-200 bg-white p-4">
            <h3 class="mb-3 text-sm font-semibold text-gray-700">Vector Store</h3>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Provider</span>
                <span class="font-medium text-gray-900">{{ knowledgeBase.vectorStore?.provider || 'n/a' }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Collection</span>
                <span class="break-all text-right font-medium text-gray-900">{{ knowledgeBase.vectorStore?.collection || 'n/a' }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Dimension</span>
                <span class="font-medium text-gray-900">{{ knowledgeBase.vectorStore?.dimension || 'n/a' }}</span>
              </div>
            </div>
          </div>

          <div class="rounded-lg border border-gray-200 bg-white p-4">
            <h3 class="mb-3 text-sm font-semibold text-gray-700">Knowledge Graph</h3>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Enabled</span>
                <span class="font-medium text-gray-900">{{ knowledgeBase.knowledgeGraph?.enabled ? 'Yes' : 'No' }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Entities</span>
                <span class="font-medium text-gray-900">{{ formatCount(knowledgeBase.knowledgeGraph?.entityCount) }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Relations</span>
                <span class="font-medium text-gray-900">{{ formatCount(knowledgeBase.knowledgeGraph?.relationCount) }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>

      <div v-else-if="activeTab === 'sources'" class="grid gap-6 lg:grid-cols-2">
        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <h2 class="mb-3 font-semibold text-gray-900">Lineage</h2>
          <div class="space-y-3 text-sm">
            <div>
              <div class="text-gray-500">Source dataset</div>
              <router-link
                v-if="knowledgeBase.sourceDataset"
                :to="{ name: 'dataset-detail', params: { id: knowledgeBase.sourceDataset } }"
                class="font-medium text-blue-600 hover:underline"
              >
                {{ knowledgeBase.sourceDataset }}
              </router-link>
              <div v-else class="font-medium text-gray-900">n/a</div>
            </div>
            <div>
              <div class="text-gray-500">Source files</div>
              <ul class="mt-2 space-y-2">
                <li v-for="file in knowledgeBase.sourceFiles || []" :key="file" class="rounded-md bg-gray-50 px-3 py-2 font-mono text-xs text-gray-700">
                  {{ file }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <h2 class="mb-3 font-semibold text-gray-900">Retrieval</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between gap-3">
              <span class="text-gray-500">Top K</span>
              <span class="font-medium text-gray-900">{{ knowledgeBase.retrieval?.topK || 'n/a' }}</span>
            </div>
            <div class="flex justify-between gap-3">
              <span class="text-gray-500">Reranker</span>
              <span class="font-medium text-gray-900">{{ knowledgeBase.retrieval?.reranker || 'n/a' }}</span>
            </div>
            <div class="flex justify-between gap-3">
              <span class="text-gray-500">Chunk size</span>
              <span class="font-medium text-gray-900">{{ knowledgeBase.retrieval?.chunkSize || 'n/a' }}</span>
            </div>
          </div>
        </div>
      </div>

      <HubFilesBrowser
        v-else-if="activeTab === 'files'"
        repo-type="knowledge"
        :repo-id="knowledgeBase.id"
        :versions="knowledgeBase.versions || []"
        :revision="selectedRevision"
        :default-revision="selectedRevision || knowledgeBase.defaultRevision || knowledgeBase.latestRevision"
        :show-revision-selector="false"
        @update:revision="selectedRevision = $event"
      />

      <div v-else class="space-y-4">
        <div class="rounded-lg border border-gray-200 bg-white">
          <div class="border-b border-gray-200 px-4 py-3">
            <h2 class="font-semibold text-gray-900">Build History</h2>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-for="build in knowledgeBase.builds || []" :key="build.id" class="px-4 py-4">
              <div class="flex items-start justify-between gap-4">
                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-semibold text-gray-900">{{ build.trigger }}</span>
                    <span class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-700">{{ build.status }}</span>
                  </div>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="stage in build.stages || []"
                      :key="`${build.id}-${stage.name}`"
                      class="inline-flex items-center rounded-full px-2 py-0.5 text-xs"
                      :class="stageBadgeClass(stage.status)"
                    >
                      {{ stage.name }}: {{ stage.status }}
                    </span>
                  </div>
                  <div v-if="build.providerStatus || build.providerJobId" class="flex flex-wrap gap-2 text-xs text-gray-500">
                    <span v-if="build.providerStatus">provider: {{ build.providerStatus }}</span>
                    <span v-if="build.providerJobId" class="break-all">job: {{ build.providerJobId }}</span>
                  </div>
                  <p v-if="build.errorMessage" class="text-xs text-red-600">{{ build.errorMessage }}</p>
                </div>
                <div class="text-right text-xs text-gray-500">
                  <div>{{ build.progress }}%</div>
                  <div>{{ formatDateTime(build.createdAt) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <KnowledgeGraphModal
        :visible="showGraphModal"
        :kb="knowledgeBase"
        @close="showGraphModal = false"
      />

      <RevisionPublishModal
        :visible="showPublishModal && !!knowledgeBase"
        repo-type="knowledge"
        :repo-id="knowledgeBase?.id || route.params.id"
        @close="showPublishModal = false"
        @published="handleRevisionPublished"
      />
    </div>

    <div v-else class="py-20 text-center">
      <p class="text-lg text-gray-500">Knowledge base not found</p>
      <router-link to="/knowledge-base" class="mt-2 inline-block text-sm text-blue-600 hover:underline">Back to Knowledge Bases</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { knowledgeBaseApi } from '@/services/api.js'
import HubFilesBrowser from '@/components/hub/HubFilesBrowser.vue'
import ProviderSyncPanel from '@/components/hub/ProviderSyncPanel.vue'
import RevisionPublishModal from '@/components/hub/RevisionPublishModal.vue'
import KnowledgeGraphModal from '@/components/knowledgeBase/KnowledgeGraphModal.vue'

const route = useRoute()
const knowledgeBase = ref(null)
const loading = ref(false)
const buildStarting = ref(false)
const syncing = ref(false)
const syncError = ref('')
const showGraphModal = ref(false)
const showPublishModal = ref(false)
const selectedRevision = ref('')
const activeTab = ref('card')

const tabs = [
  { id: 'card', label: 'Knowledge Card' },
  { id: 'sources', label: 'Sources' },
  { id: 'files', label: 'Files' },
  { id: 'builds', label: 'Builds' },
]

const statusClass = computed(() => {
  const status = knowledgeBase.value?.status || ''
  if (status === 'ready') return 'bg-green-100 text-green-700'
  if (status === 'processing') return 'bg-yellow-100 text-yellow-700'
  if (status === 'error') return 'bg-red-100 text-red-700'
  return 'bg-gray-100 text-gray-700'
})

const canSyncFromGit = computed(() => {
  const bindings = knowledgeBase.value?.providerBindings || {}
  return Boolean(bindings.gitea || bindings.localgit)
})

async function loadKnowledgeBase(revision = selectedRevision.value) {
  loading.value = true
  try {
    knowledgeBase.value = await knowledgeBaseApi.getKnowledgeBaseById(route.params.id, { revision })
    if (!selectedRevision.value) {
      selectedRevision.value = knowledgeBase.value?.selectedRevision || knowledgeBase.value?.defaultRevision || knowledgeBase.value?.latestRevision || ''
    }
  } catch (error) {
    console.error('Failed to load knowledge base:', error)
    knowledgeBase.value = null
  } finally {
    loading.value = false
  }
}

async function triggerBuild() {
  if (!knowledgeBase.value) return
  buildStarting.value = true
  try {
    await knowledgeBaseApi.startKnowledgeBuild(knowledgeBase.value.id)
    await loadKnowledgeBase(selectedRevision.value)
    activeTab.value = 'builds'
  } catch (error) {
    console.error('Failed to start build:', error)
  } finally {
    buildStarting.value = false
  }
}

watch(() => route.params.id, () => {
  selectedRevision.value = ''
  activeTab.value = 'card'
  syncError.value = ''
  loadKnowledgeBase('')
})

watch(selectedRevision, (next, prev) => {
  if (!next || next === prev) return
  loadKnowledgeBase(next)
})

onMounted(() => loadKnowledgeBase(''))

function handleRevisionPublished(response) {
  showPublishModal.value = false
  activeTab.value = 'card'
  const revision = response?.version?.revision || ''
  if (revision) {
    selectedRevision.value = revision
    return
  }
  loadKnowledgeBase(selectedRevision.value)
}

async function syncFromGit() {
  if (!knowledgeBase.value) return
  syncing.value = true
  syncError.value = ''
  try {
    const response = await knowledgeBaseApi.syncKnowledgeBase(
      knowledgeBase.value.id,
      selectedRevision.value || knowledgeBase.value.defaultRevision || knowledgeBase.value.latestRevision || '',
    )
    const revision = response?.version?.revision || selectedRevision.value || knowledgeBase.value.defaultRevision || ''
    if (revision && revision !== selectedRevision.value) {
      selectedRevision.value = revision
    } else {
      await loadKnowledgeBase(revision)
    }
  } catch (error) {
    console.error('Failed to sync knowledge base from git:', error)
    syncError.value = error.message || 'Failed to sync from Git'
  } finally {
    syncing.value = false
  }
}

function stageBadgeClass(status) {
  if (status === 'completed') return 'bg-green-100 text-green-700'
  if (status === 'running') return 'bg-blue-100 text-blue-700'
  if (status === 'error') return 'bg-red-100 text-red-700'
  return 'bg-gray-100 text-gray-700'
}

function formatCount(value) {
  const n = Number(value || 0)
  if (n >= 1000000) return `${(n / 1000000).toFixed(1).replace(/\.0$/, '')}M`
  if (n >= 1000) return `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k`
  return String(n)
}

function formatDateTime(value) {
  if (!value) return 'n/a'
  return new Date(value).toLocaleString()
}
</script>
