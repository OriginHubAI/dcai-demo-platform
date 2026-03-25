<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="loading" class="text-center py-20 text-gray-500">Loading model...</div>
    <div v-else-if="model">
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/models" class="hover:text-gray-700">Models</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ model.id }}</span>
      </div>

      <div class="lg:grid lg:grid-cols-3 lg:gap-8">
        <div class="lg:col-span-2 space-y-6">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-lg font-bold text-gray-600">
              {{ model.author.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">{{ model.name }}</h1>
              <p class="text-sm text-gray-500">by {{ model.author }}</p>
            </div>
          </div>

          <div class="flex flex-wrap gap-2">
            <TagBadge :label="model.pipeline_tag" :color="taskColorMap[model.pipeline_tag] || 'gray'" />
            <TagBadge v-for="tag in model.tags" :key="tag" :label="tag" color="gray" />
            <TagBadge v-if="model.hfCompatible" label="HF Compatible" color="green" />
          </div>

          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600">Revision</label>
            <select
              v-model="selectedRevision"
              class="rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 focus:border-blue-500 focus:outline-none"
            >
              <option v-for="version in model.versions" :key="version.revision" :value="version.revision">
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

          <div class="border border-gray-200 rounded-lg bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Model Card</h2>
            </div>
            <div class="p-6 space-y-5">
              <section v-for="section in model.cardSections" :key="section.title" class="space-y-2">
                <h3 class="text-base font-semibold text-gray-900">{{ section.title }}</h3>
                <p class="text-sm leading-6 text-gray-700 whitespace-pre-wrap">{{ section.content }}</p>
              </section>
            </div>
          </div>

          <HubFilesBrowser
            repo-type="model"
            :repo-id="model.id"
            :versions="model.versions"
            :revision="selectedRevision"
            :default-revision="selectedRevision || model.selectedRevision || model.defaultRevision || model.latestRevision"
            :show-revision-selector="false"
            @update:revision="selectedRevision = $event"
          />

          <div class="border border-gray-200 rounded-lg bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Revisions</h2>
            </div>
            <div class="divide-y divide-gray-100">
              <div v-for="version in model.versions" :key="version.revision" class="px-4 py-3 flex items-start justify-between gap-4">
                <div>
                  <div class="text-sm font-medium text-gray-900 flex items-center gap-2">
                    <span>{{ version.revision }}</span>
                    <span v-if="version.isLatest" class="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700">latest</span>
                  </div>
                  <div class="text-xs text-gray-500 mt-1">commit {{ version.commitSha }} · {{ version.framework }} · {{ version.params || 'n/a' }}</div>
                </div>
                <div class="text-xs text-gray-500">{{ formatDateTime(version.createdAt) }}</div>
              </div>
            </div>
          </div>

          <div class="border border-gray-200 rounded-lg bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Usage</h2>
            </div>
            <div class="p-4 space-y-4">
              <div>
                <div class="text-sm font-medium text-gray-900 mb-2">Transformers</div>
                <pre class="bg-gray-50 rounded-lg p-4 text-xs overflow-x-auto whitespace-pre-wrap">{{ model.usage?.transformers }}</pre>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-900 mb-2">Git Clone</div>
                <pre class="bg-gray-50 rounded-lg p-4 text-xs overflow-x-auto whitespace-pre-wrap">{{ model.usage?.gitClone }}</pre>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-900 mb-2">Git Push</div>
                <pre class="bg-gray-50 rounded-lg p-4 text-xs overflow-x-auto whitespace-pre-wrap">{{ model.usage?.gitPush }}</pre>
              </div>
            </div>
          </div>
        </div>

        <aside class="mt-6 lg:mt-0">
          <div class="border border-gray-200 rounded-lg bg-white p-4 space-y-4 sticky top-20">
            <div class="flex items-center justify-between">
              <StatBadge icon="download" :value="model.downloads" />
              <StatBadge icon="like" :value="model.likes" />
            </div>
            <hr class="border-gray-200" />
            <div class="space-y-3 text-sm">
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Library</span>
                <span class="font-medium text-gray-900 text-right">{{ model.library }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Language</span>
                <span class="font-medium text-gray-900 text-right">{{ model.language }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">License</span>
                <span class="font-medium text-gray-900 text-right">{{ model.license }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Visibility</span>
                <span class="font-medium text-gray-900 text-right">{{ model.visibility }}</span>
              </div>
              <div class="flex justify-between gap-3">
                <span class="text-gray-500">Latest revision</span>
                <span class="font-medium text-gray-900 text-right">{{ model.latestRevision }}</span>
              </div>
              <div v-if="model.baseModel" class="flex justify-between gap-3">
                <span class="text-gray-500">Base model</span>
                <span class="font-medium text-gray-900 text-right break-all">{{ model.baseModel }}</span>
              </div>
              <div v-if="model.dataset" class="flex justify-between gap-3">
                <span class="text-gray-500">Training dataset</span>
                <span class="font-medium text-gray-900 text-right break-all">{{ model.dataset }}</span>
              </div>
            </div>
            <hr class="border-gray-200" />
            <div>
              <h4 class="text-sm font-semibold text-gray-700 mb-2">Metrics</h4>
              <div class="space-y-2">
                <div v-for="metric in model.metrics" :key="metric.name" class="flex justify-between text-sm">
                  <span class="text-gray-500">{{ metric.name }}</span>
                  <span class="font-medium text-gray-900">{{ metric.value }}</span>
                </div>
              </div>
            </div>
          </div>
          <ProviderSyncPanel
            class="mt-4"
            :sync-status="model.syncStatus"
            :provider-bindings="model.providerBindings"
            :selected-version="model.selectedVersion"
          />
        </aside>
      </div>
    </div>
    <div v-else class="text-center py-20">
      <p class="text-lg text-gray-500">Model not found</p>
      <router-link to="/models" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Back to Models</router-link>
    </div>

    <RevisionPublishModal
      :visible="showPublishModal && !!model"
      repo-type="model"
      :repo-id="model?.id || route.params.id"
      @close="showPublishModal = false"
      @published="handleRevisionPublished"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { modelApi } from '@/services/api.js'
import { taskColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import HubFilesBrowser from '@/components/hub/HubFilesBrowser.vue'
import ProviderSyncPanel from '@/components/hub/ProviderSyncPanel.vue'
import RevisionPublishModal from '@/components/hub/RevisionPublishModal.vue'

const route = useRoute()
const model = ref(null)
const loading = ref(false)
const selectedRevision = ref('')
const showPublishModal = ref(false)
const syncing = ref(false)
const syncError = ref('')

const canSyncFromGit = computed(() => {
  const bindings = model.value?.providerBindings || {}
  return Boolean(bindings.gitea || bindings.localgit)
})

async function loadModel(revision = selectedRevision.value) {
  loading.value = true
  try {
    model.value = await modelApi.getModelById(route.params.id, { revision })
    if (!selectedRevision.value) {
      selectedRevision.value = model.value?.selectedRevision || model.value?.defaultRevision || model.value?.latestRevision || ''
    }
  } catch (error) {
    console.error('Failed to load model:', error)
    model.value = null
  } finally {
    loading.value = false
  }
}

onMounted(loadModel)
watch(() => route.params.id, () => {
  selectedRevision.value = ''
  syncError.value = ''
  loadModel('')
})
watch(selectedRevision, (next, prev) => {
  if (!next || next === prev) return
  loadModel(next)
})

function handleRevisionPublished(response) {
  showPublishModal.value = false
  const revision = response?.version?.revision || ''
  if (revision) {
    selectedRevision.value = revision
    return
  }
  loadModel(selectedRevision.value)
}

async function syncFromGit() {
  if (!model.value) return
  syncing.value = true
  syncError.value = ''
  try {
    const response = await modelApi.syncModel(
      model.value.id,
      selectedRevision.value || model.value.defaultRevision || model.value.latestRevision || '',
    )
    const revision = response?.version?.revision || selectedRevision.value || model.value.defaultRevision || ''
    if (revision && revision !== selectedRevision.value) {
      selectedRevision.value = revision
    } else {
      await loadModel(revision)
    }
  } catch (error) {
    console.error('Failed to sync model from git:', error)
    syncError.value = error.message || 'Failed to sync from Git'
  } finally {
    syncing.value = false
  }
}

function formatDateTime(value) {
  return new Date(value).toLocaleString()
}
</script>
