<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('packages.title') }}</h1>
      <span class="text-sm text-gray-500">{{ $t('packages.count', { count: totalItems }) }}</span>
    </div>
    <!-- Category tabs -->
    <div class="flex items-center space-x-2 mb-6 overflow-x-auto pb-2">
      <button
        v-for="cat in translatedCategories"
        :key="cat.value"
        @click="selectCategory(cat.value)"
        class="px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors"
        :class="activeCategory === cat.value
          ? 'bg-gray-900 text-white'
          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >
        {{ cat.label }}
      </button>
    </div>
    <!-- Search + Sort -->
    <div class="flex items-center gap-3 mb-6">
      <div class="flex-1 max-w-md">
        <SearchBar v-model="searchQuery" :placeholder="$t('packages.searchPlaceholder')" />
      </div>
      <SortDropdown v-model="sortBy" :options="translatedSortOptions" />
    </div>
    <!-- Results -->
    <div v-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <DataFlowCard v-for="pkg in paginatedItems" :key="pkg.id" :pkg="pkg" />
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p class="text-lg">{{ $t('packages.noResults') }}</p>
      <p class="text-sm mt-1">{{ $t('packages.noResultsHint') }}</p>
    </div>
    <PaginationBar v-model="currentPage" :total-pages="totalPages" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { dataflowPackages } from '@/data/dataflow.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import DataFlowCard from '@/components/dataflow/DataFlowCard.vue'

const { t } = useI18n()
const searchQuery = ref('')
const sortBy = ref('downloads')
const activeCategory = ref('all')

const translatedCategories = computed(() => [
  { value: 'all', label: t('packages.categories.all') },
  { value: 'multimodal', label: t('packages.categories.multimodal') },
  { value: 'science', label: t('packages.categories.science') },
  { value: 'time-series', label: t('packages.categories.timeSeries') },
])

const translatedSortOptions = computed(() => [
  { value: 'downloads', label: t('packages.sort.mostDownloads') },
  { value: 'likes', label: t('packages.sort.mostLikes') },
  { value: 'recent', label: t('packages.sort.recentlyUpdated') },
])

function selectCategory(cat) {
  activeCategory.value = cat
}

const filtered = computed(() => {
  let result = [...dataflowPackages]

  if (activeCategory.value !== 'all') {
    result = result.filter(p => p.category === activeCategory.value)
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q))
    )
  }

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'likes': return b.likes - a.likes
      case 'recent': return new Date(b.lastModified) - new Date(a.lastModified)
      case 'downloads':
      default: return b.downloads - a.downloads
    }
  })

  return result
})

const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

watch([activeCategory, searchQuery], () => {
  currentPage.value = 1
})
</script>
