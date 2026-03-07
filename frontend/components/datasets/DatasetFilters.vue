<template>
  <div class="space-y-4">
    <!-- Standard Filters -->
    <FilterSidebar
      :filter-groups="filterGroups"
      :selected="selected"
      @update:selected="$emit('update:selected', $event)"
    />
    
    <!-- Dataset Type Filter -->
    <div class="border-t border-gray-200 pt-4">
      <h4 class="text-sm font-semibold text-gray-900 mb-2">Dataset Type</h4>
      <div class="space-y-1">
        <label v-for="type in datasetTypeFilters" :key="type.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
          <input
            type="checkbox"
            :value="type.value"
            :checked="selected.datasetType?.includes(type.value)"
            @change="toggleFilter('datasetType', type.value)"
            class="rounded border-gray-300 text-dc-primary focus:ring-dc-primary"
          />
          <span class="text-sm text-gray-700">{{ type.label }}</span>
          <span class="text-xs text-gray-400 ml-auto">{{ type.count }}</span>
        </label>
      </div>
    </div>
    
    <!-- Autodriving-specific Filters (shown when autonomous-driving domain is selected) -->
    <div v-if="isAutodrivingSelected" class="border-t border-gray-200 pt-4">
      <h4 class="text-sm font-semibold text-teal-700 mb-2 flex items-center space-x-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0121 18.382V7.618a1 1 0 01-.447-.894L15 7m0 13V7m0 0L9.553 4.553A1 1 0 009 4.118v.004" />
        </svg>
        <span>Autonomous Driving</span>
      </h4>
      
      <!-- Time Range Filter -->
      <div class="mb-3">
        <h5 class="text-xs font-medium text-gray-600 mb-1">Time Conditions</h5>
        <div class="space-y-1">
          <label v-for="time in timeRangeFilters" :key="time.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
            <input
              type="checkbox"
              :value="time.value"
              :checked="selected.timeRange?.includes(time.value)"
              @change="toggleFilter('timeRange', time.value)"
              class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
            />
            <span class="text-sm text-gray-700">{{ time.label }}</span>
          </label>
        </div>
      </div>
      
      <!-- Weather Filter -->
      <div class="mb-3">
        <h5 class="text-xs font-medium text-gray-600 mb-1">Weather</h5>
        <div class="space-y-1">
          <label v-for="weather in weatherFilters" :key="weather.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
            <input
              type="checkbox"
              :value="weather.value"
              :checked="selected.weather?.includes(weather.value)"
              @change="toggleFilter('weather', weather.value)"
              class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
            />
            <span class="text-sm text-gray-700">{{ weather.label }}</span>
          </label>
        </div>
      </div>
      
      <!-- Scene Type Filter -->
      <div class="mb-3">
        <h5 class="text-xs font-medium text-gray-600 mb-1">Scene Types</h5>
        <div class="space-y-1">
          <label v-for="scene in sceneTypeFilters" :key="scene.value" class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
            <input
              type="checkbox"
              :value="scene.value"
              :checked="selected.sceneType?.includes(scene.value)"
              @change="toggleFilter('sceneType', scene.value)"
              class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
            />
            <span class="text-sm text-gray-700">{{ scene.label }}</span>
          </label>
        </div>
      </div>
      
      <!-- Semantic Search -->
      <div class="mb-3">
        <h5 class="text-xs font-medium text-gray-600 mb-1">Semantic Search</h5>
        <input
          v-model="semanticQuery"
          type="text"
          placeholder="objects, scenes, actions..."
          class="w-full text-xs border border-gray-300 rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          @input="updateSemanticQuery"
        />
      </div>
      
      <!-- Spatial Search -->
      <div class="mb-3">
        <h5 class="text-xs font-medium text-gray-600 mb-1">Spatial Search</h5>
        <input
          v-model="spatialQuery"
          type="text"
          placeholder="region or city..."
          class="w-full text-xs border border-gray-300 rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          @input="updateSpatialQuery"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import FilterSidebar from '@/components/common/FilterSidebar.vue'
import { 
  domainFilters, 
  modalityFilters, 
  languageFilters, 
  licenseFilters,
  datasetTypeFilters,
  timeRangeFilters,
  weatherFilters,
  sceneTypeFilters
} from '@/data/filters.js'

const props = defineProps({
  selected: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:selected'])

const semanticQuery = ref(props.selected.semanticQuery || '')
const spatialQuery = ref(props.selected.spatialQuery || '')

const isAutodrivingSelected = computed(() => 
  props.selected.domain?.includes('autonomous-driving')
)

const filterGroups = [
  { key: 'domain', label: 'Domain', options: domainFilters, open: true },
  { key: 'modality', label: 'Modality', options: modalityFilters, open: true },
  { key: 'language', label: 'Languages', options: languageFilters, open: false },
  { key: 'license', label: 'Licenses', options: licenseFilters, open: false },
]

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

function updateSemanticQuery() {
  emit('update:selected', {
    ...props.selected,
    semanticQuery: semanticQuery.value
  })
}

function updateSpatialQuery() {
  emit('update:selected', {
    ...props.selected,
    spatialQuery: spatialQuery.value
  })
}
</script>
