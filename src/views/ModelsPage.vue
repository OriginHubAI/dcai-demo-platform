<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Models</h1>
      <span class="text-sm text-gray-500">{{ totalItems }} models</span>
    </div>
    <div class="lg:grid lg:grid-cols-4 lg:gap-6">
      <!-- Sidebar -->
      <aside class="hidden lg:block lg:col-span-1">
        <div class="sticky top-20">
          <SearchBar v-model="searchQuery" placeholder="Filter models..." />
          <div class="mt-4">
            <ModelFilters v-model:selected="filters" />
          </div>
          <button
            v-if="activeFilterCount > 0"
            @click="clearFilters"
            class="mt-3 text-xs text-gray-500 hover:text-gray-700 underline"
          >
            Clear all filters ({{ activeFilterCount }})
          </button>
        </div>
      </aside>
      <!-- Main content -->
      <div class="lg:col-span-3">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2 lg:hidden">
            <button @click="showMobileFilters = !showMobileFilters" class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 hover:bg-gray-50">
              Filters
              <span v-if="activeFilterCount" class="ml-1 bg-hf-yellow text-gray-900 rounded-full px-1.5 text-xs">{{ activeFilterCount }}</span>
            </button>
          </div>
          <SortDropdown v-model="sortBy" :options="sortOptions" />
        </div>
        <!-- Mobile filters -->
        <div v-if="showMobileFilters" class="lg:hidden mb-4 p-4 border border-gray-200 rounded-lg bg-white">
          <SearchBar v-model="searchQuery" placeholder="Filter models..." />
          <div class="mt-3">
            <ModelFilters v-model:selected="filters" />
          </div>
        </div>
        <!-- Results -->
        <div v-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <ModelCard v-for="model in paginatedItems" :key="model.id" :model="model" />
        </div>
        <div v-else class="text-center py-16 text-gray-500">
          <p class="text-lg">No models found</p>
          <p class="text-sm mt-1">Try adjusting your search or filters</p>
        </div>
        <PaginationBar v-model="currentPage" :total-pages="totalPages" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { models } from '@/data/models.js'
import { sortOptions } from '@/data/filters.js'
import { useSearch } from '@/composables/useSearch.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import ModelCard from '@/components/models/ModelCard.vue'
import ModelFilters from '@/components/models/ModelFilters.vue'

const route = useRoute()
const showMobileFilters = ref(false)

const { searchQuery, filters, sortBy, filtered, clearFilters, activeFilterCount } = useSearch(models)
const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
})
</script>
