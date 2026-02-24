<template>
  <div class="bg-white border border-gray-200 rounded-lg hover:shadow-md hover:border-gray-300 transition-all overflow-hidden flex flex-col h-full">
    <!-- Card Content -->
    <div class="p-5 flex-grow">
      <!-- Header: Title + Indexing Status Badge -->
      <div class="flex items-start justify-between gap-2 mb-3">
        <h3 class="text-lg font-semibold text-gray-900 flex-1">{{ kb.name }}</h3>
        <span
          :class="[
            'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium flex-shrink-0',
            isIndexed
              ? 'bg-green-50 text-green-700'
              : 'bg-yellow-50 text-yellow-700'
          ]"
        >
          <svg v-if="isIndexed" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          {{ indexingStatusLabel }}
        </span>
      </div>

      <!-- Source Dataset -->
      <div v-if="sourceDataset" class="mb-2">
        <p class="text-sm text-gray-600">
          <span class="text-gray-400">{{ $t('knowledgeBase.sourceDataset') }}:</span>
          <span class="ml-1 text-indigo-600 font-medium">{{ sourceDataset.name }}</span>
        </p>
      </div>

      <!-- Description -->
      <div class="mb-2">
        <p class="text-sm text-gray-600">
          <span class="text-gray-400">{{ $t('knowledgeBase.introduction') }}：</span>{{ kb.description }}
        </p>
      </div>

      <!-- File Count -->
      <div class="mb-2">
        <p class="text-sm text-gray-600">
          <span class="text-gray-400">{{ $t('knowledgeBase.fileCount') }}:</span> {{ kb.fileCount }}
        </p>
      </div>

      <!-- Update Time -->
      <div>
        <p class="text-sm text-gray-600">
          <span class="text-gray-400">{{ $t('knowledgeBase.lastUpdated') }}：</span>{{ kb.lastModified }}
        </p>
      </div>
    </div>

    <!-- Card Actions -->
    <div class="border-t border-gray-200 flex divide-x divide-gray-200">
      <button
        @click="$emit('chat', kb)"
        class="flex-1 flex items-center justify-center gap-1.5 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
        :disabled="kb.status !== 'ready'"
        :class="{ 'opacity-50 cursor-not-allowed': kb.status !== 'ready' }"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        {{ $t('knowledgeBase.conversation') }}
      </button>
      <button
        @click="$emit('graph', kb)"
        class="flex-1 flex items-center justify-center gap-1.5 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
        :disabled="!kb.knowledgeGraph.enabled"
        :class="{ 'opacity-50 cursor-not-allowed': !kb.knowledgeGraph.enabled }"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
        </svg>
        {{ $t('knowledgeBase.knowledgeGraph') }}
      </button>
      <button
        @click="$emit('delete', kb)"
        class="flex-1 flex items-center justify-center gap-1.5 py-3 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        {{ $t('knowledgeBase.delete') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { getDatasetById } from '@/data/datasets.js'

const props = defineProps({
  kb: { type: Object, required: true }
})

defineEmits(['chat', 'graph', 'delete'])

const { t } = useI18n()

// Determine if the knowledge base is fully indexed (ready) or still indexing
const isIndexed = computed(() => {
  return props.kb.status === 'ready'
})

const indexingStatusLabel = computed(() => {
  return isIndexed.value
    ? t('knowledgeBase.indexingStatus.indexed')
    : t('knowledgeBase.indexingStatus.indexing')
})

const sourceDataset = computed(() => {
  if (props.kb.datasetId) {
    return getDatasetById(props.kb.datasetId)
  }
  return null
})
</script>
