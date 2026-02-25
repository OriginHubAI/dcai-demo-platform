<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('models.title') }}</h1>
      <span class="text-sm text-gray-500">{{ $t('models.count', { count: totalItems }) }}</span>
    </div>
    <div>
      <!-- Main content -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <SearchBar v-model="searchQuery" :placeholder="$t('models.searchPlaceholder')" class="flex-1 max-w-md" />
          <SortDropdown v-model="sortBy" :options="sortOptions" />
        </div>
        <!-- Results -->
        <div v-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <ModelCard v-for="model in paginatedItems" :key="model.id" :model="model" />
        </div>
        <div v-else class="text-center py-16 text-gray-500">
          <p class="text-lg">{{ $t('models.noResults') }}</p>
          <p class="text-sm mt-1">{{ $t('models.noResultsHint') }}</p>
        </div>
        <PaginationBar v-model="currentPage" :total-pages="totalPages" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { models } from '@/data/models.js'
import { sortOptions } from '@/data/filters.js'
import { useSearch } from '@/composables/useSearch.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import ModelCard from '@/components/models/ModelCard.vue'

const { t } = useI18n()
const route = useRoute()

const { searchQuery, sortBy, filtered } = useSearch(models)
const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
})
</script>
