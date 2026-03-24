<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('models.title') }}</h1>
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-500">{{ $t('models.count', { count: totalItems }) }}</span>
        <button
          class="rounded-lg bg-dc-primary px-4 py-2 text-sm font-medium text-white hover:bg-dc-primary-dark"
          @click="showCreateModal = true"
        >
          New Model Repo
        </button>
      </div>
    </div>
    <div class="lg:grid lg:grid-cols-4 lg:gap-6">
      <aside class="hidden lg:block lg:col-span-1">
        <div class="sticky top-20">
          <SearchBar v-model="searchQuery" :placeholder="$t('models.searchPlaceholder')" />
          <div class="mt-4">
            <ModelFilters v-model:selected="filters" />
          </div>
          <button
            v-if="activeFilterCount > 0"
            @click="clearFilters"
            class="mt-3 text-xs text-gray-500 hover:text-gray-700 underline"
          >
            {{ $t('common.clearAllFilters') }} ({{ activeFilterCount }})
          </button>
        </div>
      </aside>
      <div class="lg:col-span-3">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2 lg:hidden">
            <button @click="showMobileFilters = !showMobileFilters" class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 hover:bg-gray-50">
              {{ $t('common.filters') }}
              <span v-if="activeFilterCount" class="ml-1 bg-dc-primary text-white rounded-full px-1.5 text-xs">{{ activeFilterCount }}</span>
            </button>
          </div>
          <SortDropdown v-model="sortBy" :options="sortOptions" />
        </div>

        <div v-if="showMobileFilters" class="lg:hidden mb-4 p-4 border border-gray-200 rounded-lg bg-white">
          <SearchBar v-model="searchQuery" :placeholder="$t('models.searchPlaceholder')" />
          <div class="mt-3">
            <ModelFilters v-model:selected="filters" />
          </div>
        </div>

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

    <RepoCreateModal
      :visible="showCreateModal"
      repo-type="model"
      @close="showCreateModal = false"
      @created="handleCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { modelApi } from '@/services/api.js'
import { sortOptions } from '@/data/filters.js'
import { useSearch } from '@/composables/useSearch.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import ModelCard from '@/components/models/ModelCard.vue'
import ModelFilters from '@/components/models/ModelFilters.vue'
import RepoCreateModal from '@/components/hub/RepoCreateModal.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const showMobileFilters = ref(false)
const showCreateModal = ref(false)
const models = ref([])

const { searchQuery, filters, sortBy, filtered, clearFilters, activeFilterCount } = useSearch(models, { defaultSort: 'default' })
const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

onMounted(async () => {
  models.value = await modelApi.getModels()
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
})

async function handleCreated(repo) {
  showCreateModal.value = false
  models.value = await modelApi.getModels()
  router.push({ name: 'model-detail', params: { id: repo.id } })
}
</script>
