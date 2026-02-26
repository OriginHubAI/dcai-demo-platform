<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('apps.title') }}</h1>
      <span class="text-sm text-gray-500">{{ $t('apps.count', { count: totalItems }) }}</span>
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
        <SearchBar v-model="searchQuery" :placeholder="$t('apps.searchPlaceholder')" />
      </div>
      <SortDropdown v-model="sortBy" :options="translatedSortOptions" />
    </div>
    <!-- Results -->
    <div v-if="loading" class="text-center py-16 text-gray-500">
      <p class="text-lg">Loading...</p>
    </div>
    <div v-else-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <AppCard v-for="app in paginatedItems" :key="app.id" :app="app" />
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p class="text-lg">{{ $t('apps.noResults') }}</p>
      <p class="text-sm mt-1">{{ $t('apps.noResultsHint') }}</p>
    </div>
    <PaginationBar v-model="currentPage" :total-pages="totalPages" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { appApi } from '@/services/api.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import AppCard from '@/components/apps/AppCard.vue'

const { t } = useI18n()
const searchQuery = ref('')
const sortBy = ref('default')
const activeCategory = ref('all')
const apps = ref([])
const loading = ref(false)

const translatedCategories = computed(() => [
  { value: 'all', label: t('apps.categories.all') },
  { value: 'agent-based', label: t('apps.categories.agentBased') },
  { value: 'image-generation', label: t('apps.categories.imageGeneration') },
  { value: 'video-generation', label: t('apps.categories.videoGeneration') },
  { value: 'text-generation', label: t('apps.categories.textGeneration') },
  { value: 'audio', label: t('apps.categories.audio') },
  { value: 'cad', label: t('apps.categories.cad') },
])

const translatedSortOptions = computed(() => [
  { value: 'default', label: t('apps.sort.default') },
  { value: 'likes', label: t('apps.sort.mostLikes') },
  { value: 'trending', label: t('apps.sort.trending') },
  { value: 'recent', label: t('apps.sort.recentlyUpdated') },
])

function selectCategory(cat) {
  activeCategory.value = cat
}

// Load apps from API
async function loadApps() {
  loading.value = true
  try {
    const params = {}
    if (activeCategory.value !== 'all') {
      params.category = activeCategory.value
    }
    const data = await appApi.getApps(params)
    apps.value = data
  } catch (error) {
    console.error('Failed to load apps:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadApps()
})

const filtered = computed(() => {
  let result = [...apps.value]

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
      case 'trending': return b.likes - a.likes
      case 'default':
      default: return 0
    }
  })

  return result
})

const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 12)

watch([activeCategory], () => {
  currentPage.value = 1
  loadApps()
})

watch([searchQuery], () => {
  currentPage.value = 1
})
</script>
