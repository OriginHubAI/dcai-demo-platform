<template>
  <div
    class="block border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-gray-300 transition-all bg-white relative group"
  >
    <!-- Edit Button -->
    <button
      @click.stop="openEditor"
      class="absolute top-3 right-3 w-8 h-8 rounded-lg bg-gray-100 hover:bg-blue-500 hover:text-white text-gray-500 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-200 shadow-sm"
      title="Edit in VSCode"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
      </svg>
    </button>

    <router-link
      :to="`/dataflow/${pkg.id}`"
      class="block"
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

    <!-- VSCode Editor Dialog -->
    <VSCodeEditorDialog
      v-model:visible="showEditor"
      :pkg="pkg"
      @close="showEditor = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import VSCodeEditorDialog from './VSCodeEditorDialog.vue'

defineProps({
  pkg: { type: Object, required: true }
})

const showEditor = ref(false)

function openEditor() {
  showEditor.value = true
}

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
