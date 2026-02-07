<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Spaces</h1>
      <span class="text-sm text-gray-500">{{ totalItems }} spaces</span>
    </div>
    <!-- Category tabs -->
    <div class="flex items-center space-x-2 mb-6 overflow-x-auto pb-2">
      <button
        v-for="cat in spaceCategories"
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
        <SearchBar v-model="searchQuery" placeholder="Search spaces..." />
      </div>
      <SortDropdown v-model="sortBy" :options="spaceSortOptions" />
    </div>
    <!-- Results -->
    <div v-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <SpaceCard v-for="space in paginatedItems" :key="space.id" :space="space" />
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p class="text-lg">No spaces found</p>
      <p class="text-sm mt-1">Try adjusting your search or category</p>
    </div>
    <PaginationBar v-model="currentPage" :total-pages="totalPages" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { spaces } from '@/data/spaces.js'
import { spaceCategories } from '@/data/filters.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import SpaceCard from '@/components/spaces/SpaceCard.vue'

const searchQuery = ref('')
const sortBy = ref('likes')
const activeCategory = ref('all')

const spaceSortOptions = [
  { value: 'likes', label: 'Most Likes' },
  { value: 'trending', label: 'Trending' },
  { value: 'recent', label: 'Recently Updated' },
]

function selectCategory(cat) {
  activeCategory.value = cat
}

const filtered = computed(() => {
  let result = [...spaces]

  if (activeCategory.value !== 'all') {
    result = result.filter(s => s.category === activeCategory.value)
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(s =>
      s.title.toLowerCase().includes(q) ||
      s.author.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q)
    )
  }

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'likes': return b.likes - a.likes
      case 'recent': return 0
      case 'trending':
      default: return b.likes - a.likes
    }
  })

  return result
})

const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

watch([activeCategory, searchQuery], () => {
  currentPage.value = 1
})
</script>
