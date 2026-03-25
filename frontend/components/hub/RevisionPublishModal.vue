<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
    <div class="flex max-h-[calc(100vh-2rem)] w-full max-w-3xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
      <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Publish Revision</h2>
          <p class="text-sm text-gray-500">{{ repoId }}</p>
        </div>
        <button class="text-gray-400 hover:text-gray-600" @click="$emit('close')">✕</button>
      </div>

      <div class="grid flex-1 gap-4 overflow-y-auto p-6 md:grid-cols-2">
        <label class="space-y-1 text-sm">
          <span class="text-gray-600">Revision</span>
          <input v-model="form.revision" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="flex items-center gap-2 pt-6 text-sm text-gray-700">
          <input v-model="form.markLatest" type="checkbox" />
          Mark as latest
        </label>

        <template v-if="repoType === 'model'">
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Framework</span>
            <input v-model="form.framework" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Params</span>
            <input v-model="form.params" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
          <label class="space-y-1 text-sm md:col-span-2">
            <span class="text-gray-600">Artifact URI</span>
            <input
              v-model="form.artifactUri"
              placeholder="s3://bucket/path or mlflow artifact URI"
              class="w-full rounded-lg border border-gray-300 px-3 py-2"
            />
          </label>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Registry Stage</span>
            <select v-model="form.stage" class="w-full rounded-lg border border-gray-300 px-3 py-2">
              <option value="">none</option>
              <option value="Staging">Staging</option>
              <option value="Production">Production</option>
              <option value="Archived">Archived</option>
            </select>
          </label>
        </template>

        <template v-else-if="repoType === 'dataset'">
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Row Count Override</span>
            <input v-model="form.rowCount" type="number" min="0" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
        </template>

        <template v-else>
          <label class="space-y-1 text-sm">
            <span class="text-gray-600">Manifest Source Dataset</span>
            <input v-model="form.sourceDataset" class="w-full rounded-lg border border-gray-300 px-3 py-2" />
          </label>
        </template>

        <label class="space-y-2 text-sm md:col-span-2">
          <span class="text-gray-600">Files</span>
          <input type="file" multiple class="block w-full rounded-lg border border-gray-300 px-3 py-2" @change="handleFiles" />
          <span class="text-xs text-gray-500">{{ fileHint }}</span>
        </label>

        <div class="rounded-lg border border-gray-200 bg-gray-50 p-3 md:col-span-2">
          <div class="mb-2 text-sm font-medium text-gray-800">Selected Files</div>
          <div v-if="selectedFiles.length" class="space-y-1 text-xs text-gray-600">
            <div v-for="file in selectedFiles" :key="file.name" class="flex items-center justify-between gap-3">
              <span class="truncate">{{ file.name }}</span>
              <span>{{ formatSize(file.size) }}</span>
            </div>
          </div>
          <div v-else class="text-xs text-gray-500">No files selected.</div>
        </div>
      </div>

      <div v-if="errorMessage" class="px-6 pb-2 text-sm text-red-600">{{ errorMessage }}</div>

      <div class="shrink-0 flex items-center justify-end gap-3 border-t border-gray-200 px-6 py-4">
        <button class="rounded-lg px-4 py-2 text-sm text-gray-600 hover:bg-gray-100" @click="$emit('close')">Cancel</button>
        <button
          class="rounded-lg bg-dc-primary px-4 py-2 text-sm font-medium text-white hover:bg-dc-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="submitting || !canPublish"
          @click="publish"
        >
          {{ submitting ? 'Publishing...' : 'Publish Revision' }}
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
  repoId: { type: String, required: true },
})

const emit = defineEmits(['close', 'published'])

const selectedFiles = ref([])
const submitting = ref(false)
const errorMessage = ref('')

const form = reactive({
  revision: 'main',
  markLatest: true,
  framework: 'transformers',
  params: '',
  artifactUri: '',
  stage: '',
  rowCount: '',
  sourceDataset: '',
})

const canPublish = computed(() => {
  if (!form.revision) return false
  if (props.repoType === 'model') {
    return Boolean(selectedFiles.value.length || form.artifactUri.trim())
  }
  return Boolean(selectedFiles.value.length)
})

const fileHint = computed(() => {
  if (props.repoType === 'model') {
    return 'Upload small files, or publish directly with an existing artifact URI.'
  }
  return 'Small files only for now. Text files get preview support automatically.'
})

watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      form.revision = 'main'
      form.markLatest = true
      form.framework = 'transformers'
      form.params = ''
      form.artifactUri = ''
      form.stage = ''
      form.rowCount = ''
      form.sourceDataset = ''
      selectedFiles.value = []
      errorMessage.value = ''
      submitting.value = false
    }
  },
)

function handleFiles(event) {
  selectedFiles.value = Array.from(event.target.files || [])
}

async function publish() {
  submitting.value = true
  errorMessage.value = ''
  try {
    const files = await Promise.all(selectedFiles.value.map((file) => serializeFile(file, props.repoType)))
    const payload = {
      revision: form.revision,
      markLatest: form.markLatest,
      files,
    }
    if (props.repoType === 'dataset' && form.rowCount) {
      payload.rowCount = Number(form.rowCount)
    }
    if (props.repoType === 'model') {
      payload.framework = form.framework
      payload.params = form.params
      payload.artifactUri = form.artifactUri
      payload.stage = form.stage
    }
    if (props.repoType === 'knowledge' && form.sourceDataset) {
      payload.manifest = { sourceDataset: form.sourceDataset }
    }

    let response
    if (props.repoType === 'dataset') {
      response = await datasetApi.createDatasetRevision(props.repoId, payload)
    } else if (props.repoType === 'model') {
      response = await modelApi.createModelRevision(props.repoId, payload)
    } else {
      response = await knowledgeBaseApi.createKnowledgeRevision(props.repoId, payload)
    }
    emit('published', response)
  } catch (error) {
    errorMessage.value = error.message || 'Failed to publish revision'
  } finally {
    submitting.value = false
  }
}

async function serializeFile(file, repoType) {
  const path = file.webkitRelativePath || file.name
  const extension = path.split('.').pop()?.toLowerCase() || ''
  const payload = {
    path,
    fileType: extension || 'bin',
    sizeBytes: file.size,
  }

  const textExtensions = new Set(['txt', 'md', 'json', 'jsonl', 'csv', 'yaml', 'yml', 'py', 'js', 'ts'])
  if (textExtensions.has(extension)) {
    const text = await file.text()
    payload.content = text
    payload.encoding = 'utf-8'
    payload.previewText = extension === 'jsonl' || extension === 'csv' ? '' : text.slice(0, 4000)
    const previewRows = parsePreviewRows(text, extension)
    const rowCount = countRows(text, extension, previewRows)
    if (previewRows.length) {
      payload.previewRows = previewRows
    }
    if (rowCount) {
      payload.rowCount = rowCount
    }
    if (repoType === 'dataset' && rowCount) {
      payload.split = inferSplit(path)
    }
    return payload
  }

  payload.content = await fileToBase64(file)
  payload.encoding = 'base64'
  return payload
}

function parsePreviewRows(text, extension) {
  try {
    if (extension === 'jsonl') {
      return text
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean)
        .slice(0, 20)
        .map((line) => JSON.parse(line))
    }
    if (extension === 'json') {
      const parsed = JSON.parse(text)
      return Array.isArray(parsed) ? parsed.slice(0, 20) : []
    }
    if (extension === 'csv') {
      const lines = text.split('\n').map((line) => line.trim()).filter(Boolean)
      if (lines.length < 2) return []
      const headers = lines[0].split(',').map((value) => value.trim())
      return lines.slice(1, 21).map((line) => {
        const values = line.split(',')
        return headers.reduce((result, header, index) => {
          result[header] = (values[index] || '').trim()
          return result
        }, {})
      })
    }
  } catch (error) {
    return []
  }
  return []
}

function countRows(text, extension, previewRows = []) {
  try {
    if (extension === 'jsonl') {
      return text
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean)
        .length
    }
    if (extension === 'json') {
      const parsed = JSON.parse(text)
      return Array.isArray(parsed) ? parsed.length : 0
    }
    if (extension === 'csv') {
      const lines = text.split('\n').map((line) => line.trim()).filter(Boolean)
      return Math.max(0, lines.length - 1)
    }
  } catch (error) {
    return previewRows.length
  }
  return previewRows.length
}

function inferSplit(path) {
  const value = path.toLowerCase()
  if (value.includes('train')) return 'train'
  if (value.includes('validation') || value.includes('valid') || value.includes('dev')) return 'validation'
  if (value.includes('test')) return 'test'
  return ''
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = String(reader.result || '')
      resolve(result.split(',')[1] || '')
    }
    reader.onerror = () => reject(reader.error)
    reader.readAsDataURL(file)
  })
}

function formatSize(size) {
  if (size >= 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)}MB`
  if (size >= 1024) return `${(size / 1024).toFixed(1)}KB`
  return `${size}B`
}
</script>
