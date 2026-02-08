<template>
  <router-link
    :to="`/datasets/${dataset.id}`"
    class="block border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-gray-300 transition-all bg-white"
  >
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0 flex-1">
        <div class="flex items-center space-x-2 mb-1">
          <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center text-xs font-bold text-green-700 flex-shrink-0">
            {{ dataset.author.charAt(0).toUpperCase() }}
          </div>
          <span class="text-sm font-semibold text-gray-900 truncate">{{ dataset.id }}</span>
        </div>
        <p class="text-xs text-gray-500 line-clamp-2 mt-1">{{ dataset.description }}</p>
      </div>
    </div>
    <div class="flex items-center flex-wrap gap-2 mt-3">
      <TagBadge :label="dataset.domain" :color="domainColorMap[dataset.domain] || 'gray'" />
      <TagBadge :label="dataset.modality" color="teal" />
      <TagBadge :label="dataset.task" :color="taskColorMap[dataset.task] || 'gray'" />
      <span class="text-xs text-gray-400">{{ dataset.size }}</span>
    </div>
    <div class="flex items-center space-x-4 mt-2">
      <StatBadge icon="download" :value="dataset.downloads" />
      <StatBadge icon="like" :value="dataset.likes" />
      <span class="text-xs text-gray-400">{{ formatRows(dataset.rows) }} rows</span>
    </div>
  </router-link>
</template>

<script setup>
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import { taskColorMap, domainColorMap } from '@/data/filters.js'

defineProps({
  dataset: { type: Object, required: true }
})

function formatRows(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k'
  return n.toString()
}
</script>
