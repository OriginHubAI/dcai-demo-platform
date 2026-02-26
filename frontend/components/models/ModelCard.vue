<template>
  <router-link
    :to="`/models/${model.id}`"
    class="block border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-gray-300 transition-all bg-white"
  >
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0 flex-1">
        <div class="flex items-center space-x-2 mb-1">
          <div class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-600 flex-shrink-0">
            {{ model.author.charAt(0).toUpperCase() }}
          </div>
          <span class="text-sm font-semibold text-gray-900 truncate">{{ displayId }}</span>
        </div>
        <p class="text-xs text-gray-500 line-clamp-2 mt-1">{{ model.description }}</p>
      </div>
    </div>
    <div class="flex items-center flex-wrap gap-2 mt-3">
      <TagBadge :label="model.pipeline_tag" :color="taskColorMap[model.pipeline_tag] || 'gray'" />
      <span class="text-xs text-gray-400">Updated {{ formatDate(model.lastModified) }}</span>
    </div>
    <div v-if="model.baseModel || model.dataset" class="flex flex-wrap gap-2 mt-2">
      <span v-if="model.baseModel" class="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-100">
        Base: {{ model.baseModel }}
      </span>
      <span v-if="model.dataset" class="text-xs bg-green-50 text-green-700 px-2 py-0.5 rounded border border-green-100">
        Dataset: {{ model.dataset }}
      </span>
    </div>
    <div class="flex items-center space-x-4 mt-2">
      <StatBadge icon="download" :value="model.downloads" />
      <StatBadge icon="like" :value="model.likes" />
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import { taskColorMap } from '@/data/filters.js'

const props = defineProps({
  model: { type: Object, required: true }
})

const displayId = computed(() => {
  // Remove "Qwen/" prefix from display
  return props.model.id.replace(/^Qwen\//, '')
})

function formatDate(dateStr) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return 'today'
  if (days === 1) return 'yesterday'
  if (days < 30) return `${days} days ago`
  if (days < 365) return `${Math.floor(days / 30)} months ago`
  return `${Math.floor(days / 365)} years ago`
}
</script>
