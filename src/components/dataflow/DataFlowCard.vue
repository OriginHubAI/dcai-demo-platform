<template>
  <router-link
    :to="`/dataflow/${pkg.id}`"
    class="block border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-gray-300 transition-all bg-white"
  >
    <div class="flex items-start justify-between gap-2">
      <div class="min-w-0 flex-1">
        <div class="flex items-center space-x-2 mb-1">
          <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-xs font-bold text-blue-700 flex-shrink-0">
            DF
          </div>
          <span class="text-sm font-semibold text-gray-900 truncate">{{ pkg.name }}</span>
          <span class="text-xs text-gray-400">v{{ pkg.version }}</span>
        </div>
        <p class="text-xs text-gray-500 line-clamp-2 mt-1">{{ pkg.description }}</p>
      </div>
    </div>
    <div class="flex items-center flex-wrap gap-2 mt-3">
      <TagBadge v-for="tag in pkg.tags.slice(0, 3)" :key="tag" :label="tag" :color="tagColor(tag)" />
    </div>
    <div class="flex items-center space-x-4 mt-2">
      <StatBadge icon="download" :value="pkg.downloads" />
      <StatBadge icon="like" :value="pkg.likes" />
      <span class="text-xs text-gray-400">{{ pkg.lastModified }}</span>
    </div>
  </router-link>
</template>

<script setup>
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'

defineProps({
  pkg: { type: Object, required: true }
})

const tagColorMap = {
  core: 'blue',
  pipeline: 'indigo',
  'data-processing': 'teal',
  multimodal: 'purple',
  image: 'green',
  video: 'orange',
  audio: 'pink',
  'material-science': 'red',
  crystal: 'orange',
  molecular: 'yellow',
  math: 'blue',
  numerical: 'indigo',
  statistics: 'teal',
  optimization: 'green',
  'time-series': 'purple',
  forecasting: 'orange',
  'anomaly-detection': 'red',
  streaming: 'pink',
  geology: 'yellow',
  seismic: 'orange',
  geospatial: 'green',
  subsurface: 'teal',
}

function tagColor(tag) {
  return tagColorMap[tag] || 'gray'
}
</script>
