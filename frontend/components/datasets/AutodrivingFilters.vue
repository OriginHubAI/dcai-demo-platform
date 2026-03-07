<template>
  <div class="space-y-4">
    <!-- Dataset Type Filter -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Dataset Type</h4>
      <div class="space-y-1">
        <label v-for="type in datasetTypeFilters" :key="type.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="type.value"
            :checked="selected.datasetTypes?.includes(type.value)"
            @change="toggleFilter('datasetTypes', type.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ type.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ formatCount(type.count) }}</span>
        </label>
      </div>
    </div>

    <!-- Time Range Filter -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Time Conditions</h4>
      <div class="space-y-1">
        <label v-for="time in timeRangeFilters" :key="time.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="time.value"
            :checked="selected.timeRanges?.includes(time.value)"
            @change="toggleFilter('timeRanges', time.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ time.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ formatCount(time.count) }}</span>
        </label>
      </div>
    </div>

    <!-- Weather Filter -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Weather Conditions</h4>
      <div class="space-y-1">
        <label v-for="weather in weatherFilters" :key="weather.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="weather.value"
            :checked="selected.weather?.includes(weather.value)"
            @change="toggleFilter('weather', weather.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ weather.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ formatCount(weather.count) }}</span>
        </label>
      </div>
    </div>

    <!-- Scene Type Filter -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Scene Types</h4>
      <div class="space-y-1">
        <label v-for="scene in sceneTypeFilters" :key="scene.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="scene.value"
            :checked="selected.sceneTypes?.includes(scene.value)"
            @change="toggleFilter('sceneTypes', scene.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ scene.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ formatCount(scene.count) }}</span>
        </label>
      </div>
    </div>

    <!-- Annotation Type Filter -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Annotation Types</h4>
      <div class="space-y-1">
        <label v-for="ann in annotationTypeFilters" :key="ann.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="ann.value"
            :checked="selected.annotations?.includes(ann.value)"
            @change="toggleFilter('annotations', ann.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ ann.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ formatCount(ann.count) }}</span>
        </label>
      </div>
    </div>

    <!-- Semantic Search -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Semantic Search</h4>
      <div class="space-y-2">
        <input
          v-model="semanticQuery"
          type="text"
          placeholder="Search objects, scenes, actions..."
          class="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-dc-primary focus:border-transparent"
          @input="updateSemanticSearch"
        />
        <div v-if="selected.semanticTags?.length" class="flex flex-wrap gap-1">
          <span 
            v-for="tag in selected.semanticTags" 
            :key="tag"
            class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full flex items-center space-x-1"
          >
            {{ tag }}
            <button @click="removeSemanticTag(tag)" class="hover:text-purple-900">×</button>
          </span>
        </div>
      </div>
    </div>

    <!-- Spatial Search -->
    <div>
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Spatial Bounds</h4>
      <div class="space-y-2">
        <input
          v-model="spatialQuery"
          type="text"
          placeholder="Region name or coordinates..."
          class="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-dc-primary focus:border-transparent"
          @input="updateSpatialSearch"
        />
        <div class="grid grid-cols-2 gap-2">
          <input
            v-model="latRange[0]"
            type="number"
            step="0.01"
            placeholder="Min Lat"
            class="text-xs border border-gray-300 rounded px-2 py-1"
            @input="updateLatRange"
          />
          <input
            v-model="latRange[1]"
            type="number"
            step="0.01"
            placeholder="Max Lat"
            class="text-xs border border-gray-300 rounded px-2 py-1"
            @input="updateLatRange"
          />
          <input
            v-model="lonRange[0]"
            type="number"
            step="0.01"
            placeholder="Min Lon"
            class="text-xs border border-gray-300 rounded px-2 py-1"
            @input="updateLonRange"
          />
          <input
            v-model="lonRange[1]"
            type="number"
            step="0.01"
            placeholder="Max Lon"
            class="text-xs border border-gray-300 rounded px-2 py-1"
            @input="updateLonRange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  datasetTypeFilters,
  timeRangeFilters,
  weatherFilters,
  sceneTypeFilters,
  annotationTypeFilters
} from '@/data/filters.js'

const props = defineProps({
  selected: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:selected'])

const semanticQuery = ref('')
const spatialQuery = ref('')
const latRange = ref([null, null])
const lonRange = ref([null, null])

function toggleFilter(category, value) {
  const current = props.selected[category] || []
  const updated = current.includes(value)
    ? current.filter(v => v !== value)
    : [...current, value]
  
  emit('update:selected', {
    ...props.selected,
    [category]: updated
  })
}

function updateSemanticSearch() {
  // Debounce and update semantic tags
  const tags = semanticQuery.value
    .split(/[,\s]+/)
    .filter(t => t.trim())
  
  emit('update:selected', {
    ...props.selected,
    semanticQuery: semanticQuery.value,
    semanticTags: tags
  })
}

function removeSemanticTag(tag) {
  const tags = (props.selected.semanticTags || []).filter(t => t !== tag)
  semanticQuery.value = tags.join(' ')
  emit('update:selected', {
    ...props.selected,
    semanticTags: tags
  })
}

function updateSpatialSearch() {
  emit('update:selected', {
    ...props.selected,
    spatialQuery: spatialQuery.value
  })
}

function updateLatRange() {
  emit('update:selected', {
    ...props.selected,
    latRange: latRange.value.filter(v => v !== null).length === 2 ? latRange.value : null
  })
}

function updateLonRange() {
  emit('update:selected', {
    ...props.selected,
    lonRange: lonRange.value.filter(v => v !== null).length === 2 ? lonRange.value : null
  })
}

function formatCount(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n.toString()
}
</script>
