<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
    <div class="w-full max-w-2xl rounded-2xl bg-white shadow-2xl">
      <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
        <h2 class="text-lg font-semibold text-gray-900">Create {{ title }}</h2>
        <button class="text-gray-400 hover:text-gray-600" @click="$emit('close')">✕</button>
      </div>

      <div class="grid gap-4 p-6 md:grid-cols-2">
        <label class="space-y-1 text-sm">
          <span class="text-gray-600">Namespace</span>
          <input v-model="form.namespace" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="space-y-1 text-sm">
          <span class="text-gray-600">Slug</span>
          <input v-model="form.slug" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="space-y-1 text-sm md:col-span-2">
          <span class="text-gray-600">Name</span>
          <input v-model="form.name" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="space-y-1 text-sm md:col-span-2">
          <span class="text-gray-600">Description</span>
          <textarea v-model="form.description" rows="3" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="space-y-1 text-sm md:col-span-2">
          <span class="text-gray-600">Summary</span>
          <textarea v-model="form.summary" rows="2" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="space-y-1 text-sm">
          <span class="text-gray-600">Visibility</span>
          <select v-model="form.visibility" class="w-full rounded-lg border border-gray-300 px-3 py-2">
            <option value="public">public</option>
            <option value="private">private</option>
          </select>
        </label>
        <label class="space-y-1 text-sm">
          <span class="text-gray-600">Tags</span>
          <input v-model="form.tagsInput" placeholder="comma,separated,tags" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>

        <template v-if="repoType === 'dataset'">
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Task</span>
            <input v-model="form.task" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Domain</span>
            <input v-model="form.domain" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Modality</span>
            <input v-model="form.modality" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Language</span>
            <input v-model="form.language" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">License</span>
            <input v-model="form.license" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Dataset Type</span>
            <input v-model="form.datasetType" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
        </template>

        <template v-else-if="repoType === 'model'">
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Pipeline Tag</span>
            <input v-model="form.pipelineTag" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Library</span>
            <input v-model="form.library" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Language</span>
            <input v-model="form.language" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">License</span>
            <input v-model="form.license" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Base Model</span>
            <input v-model="form.baseModel" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Training Dataset</span>
            <input v-model="form.dataset" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
        </template>

        <template v-else>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Source Dataset</span>
            <input v-model="form.sourceDataset" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Status</span>
            <select v-model="form.status" class="w-full rounded-lg border border-gray-300 px-3 py-2">
              <option value="pending">pending</option>
              <option value="processing">processing</option>
              <option value="ready">ready</option>
              <option value="error">error</option>
            </select>
          </label>
        </template>
      </div>

      <div v-if="errorMessage" class="px-6 pb-2 text-sm text-red-600">{{ errorMessage }}</div>

      <div class="flex items-center justify-end gap-3 border-t border-gray-200 px-6 py-4">
        <button class="rounded-lg px-4 py-2 text-sm text-gray-600 hover:bg-gray-100" @click="$emit('close')">Cancel</button>
        <button
          class="rounded-lg bg-dc-primary px-4 py-2 text-sm font-medium text-white hover:bg-dc-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="submitting || !form.namespace || !form.slug || !form.name"
          @click="submit"
        >
          {{ submitting ? 'Creating...' : 'Create Repo' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

import { datasetApi, knowledgeBaseApi, modelApi } from '@/services/api.js'

const props = defineProps({
  visible: { type: Boolean, default: false },
  repoType: { type: String, required: true },
})

const emit = defineEmits(['close', 'created'])

const errorMessage = ref('')
const submitting = ref(false)

const form = reactive(getInitialForm())

const title = computed(() => {
  if (props.repoType === 'dataset') return 'Dataset Repo'
  if (props.repoType === 'model') return 'Model Repo'
  return 'Knowledge Repo'
})

watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      Object.assign(form, getInitialForm())
      errorMessage.value = ''
      submitting.value = false
    }
  },
)

function getInitialForm() {
  return {
    namespace: 'OpenDCAI',
    slug: '',
    name: '',
    description: '',
    summary: '',
    visibility: 'public',
    tagsInput: '',
    task: 'text-generation',
    domain: 'general',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    datasetType: '',
    pipelineTag: 'text-generation',
    library: 'transformers',
    baseModel: '',
    dataset: '',
    sourceDataset: '',
    status: 'pending',
  }
}

async function submit() {
  submitting.value = true
  errorMessage.value = ''
  const tags = form.tagsInput
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)

  try {
    let created
    if (props.repoType === 'dataset') {
      created = await datasetApi.createDataset({
        namespace: form.namespace,
        slug: form.slug,
        name: form.name,
        description: form.description,
        summary: form.summary,
        visibility: form.visibility,
        tags,
        task: form.task,
        domain: form.domain,
        modality: form.modality,
        language: form.language,
        license: form.license,
        datasetType: form.datasetType,
      })
    } else if (props.repoType === 'model') {
      created = await modelApi.createModel({
        namespace: form.namespace,
        slug: form.slug,
        name: form.name,
        description: form.description,
        summary: form.summary,
        visibility: form.visibility,
        tags,
        pipelineTag: form.pipelineTag,
        library: form.library,
        language: form.language,
        license: form.license,
        baseModel: form.baseModel,
        dataset: form.dataset,
      })
    } else {
      created = await knowledgeBaseApi.createKnowledgeBase({
        namespace: form.namespace,
        slug: form.slug,
        name: form.name,
        description: form.description,
        summary: form.summary,
        visibility: form.visibility,
        tags,
        sourceDataset: form.sourceDataset,
        status: form.status,
      })
    }
    emit('created', created)
  } catch (error) {
    errorMessage.value = error.message || 'Failed to create repo'
  } finally {
    submitting.value = false
  }
}
</script>
