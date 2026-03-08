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
    <div v-if="loading" class="text-center py-16 text-gray-500">
      <p class="text-lg">Loading package workspace...</p>
    </div>
    <div v-else-if="paginatedItems.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <DataFlowCard v-for="pkg in paginatedItems" :key="pkg.id" :pkg="pkg" />
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p class="text-lg">{{ $t('packages.noResults') }}</p>
      <p class="text-sm mt-1">{{ $t('packages.noResultsHint') }}</p>
    </div>
    <PaginationBar v-model="currentPage" :total-pages="totalPages" />

    <VSCodeEditorDialog
      v-if="selectedPackage"
      v-model:visible="showEditor"
      :pkg="selectedPackage"
      @close="closeEditor"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { dataflowApi } from '@/services/api.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import DataFlowCard from '@/components/dataflow/DataFlowCard.vue'
import VSCodeEditorDialog from '@/components/dataflow/VSCodeEditorDialog.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const sortBy = ref('downloads')
const activeCategory = ref('all')
const dataflowPackages = ref([])
const loading = ref(false)
const showEditor = ref(false)
const selectedPackage = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    dataflowPackages.value = await dataflowApi.getPackages()
  } catch (error) {
    console.error('Failed to load packages:', error)
  } finally {
    loading.value = false
  }
})

const translatedCategories = computed(() => [
  { value: 'all', label: t('packages.categories.all') },
  { value: 'core', label: 'Core' },
  { value: 'training', label: 'Training' },
  { value: 'rag', label: 'RAG' },
  { value: 'science', label: t('packages.categories.science') },
  { value: 'multimodal', label: t('packages.categories.multimodal') },
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
  let result = [...dataflowPackages.value]

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

watch(
  () => [route.query.editorPackage, dataflowPackages.value.length],
  () => {
    const packageId = route.query.editorPackage
    if (!packageId) return
    const match = dataflowPackages.value.find((item) => item.id === packageId)
    if (!match) return
    selectedPackage.value = match
    showEditor.value = true
  },
  { immediate: true },
)

function closeEditor() {
  showEditor.value = false
  selectedPackage.value = null
  if (route.query.editorPackage) {
    const query = { ...route.query }
    delete query.editorPackage
    router.replace({ query })
  }
}
</script>
