<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ $t('knowledgeBase.title') }}</h1>
        <p class="text-sm text-gray-500 mt-1">{{ $t('knowledgeBase.subtitle') }}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-500">{{ $t('knowledgeBase.count', { count: totalItems }) }}</span>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center gap-2 px-4 py-2 bg-dc-primary text-white text-sm font-medium rounded-lg hover:bg-dc-primary-dark transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          {{ $t('knowledgeBase.create') }}
        </button>
      </div>
    </div>

    <div>
      <!-- Search and Sort -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex-1 max-w-md">
          <SearchBar v-model="searchQuery" :placeholder="$t('knowledgeBase.searchPlaceholder')" />
        </div>
        <SortDropdown v-model="sortBy" :options="sortOptions" />
      </div>

      <!-- Results -->
        <div v-if="paginatedItems.length" class="grid grid-cols-1 xl:grid-cols-2 gap-4">
          <KnowledgeBaseCard
            v-for="kb in paginatedItems"
            :key="kb.id"
            :kb="kb"
            @chat="handleChat"
            @graph="handleGraph"
            @delete="handleDelete"
          />
        </div>
        <div v-else class="text-center py-16 text-gray-500">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <p class="text-lg">{{ $t('knowledgeBase.noResults') }}</p>
          <p class="text-sm mt-1">{{ $t('knowledgeBase.noResultsHint') }}</p>
        </div>

        <PaginationBar v-model="currentPage" :total-pages="totalPages" />
    </div>

    <!-- Create Knowledge Base Modal (placeholder) -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="showCreateModal = false">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">{{ $t('knowledgeBase.createTitle') }}</h2>
          <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <p class="text-sm text-gray-600 mb-4">{{ $t('knowledgeBase.createDescription') }}</p>
        <div class="flex justify-end gap-3">
          <button
            @click="showCreateModal = false"
            class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {{ $t('common.cancel') }}
          </button>
          <button
            @click="showCreateModal = false"
            class="px-4 py-2 text-sm bg-dc-primary text-white rounded-lg hover:bg-dc-primary-dark transition-colors"
          >
            {{ $t('knowledgeBase.selectDataset') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { knowledgeBases, kbStatusMap, kbTypeMap } from '@/data/knowledgeBase.js'
import { usePagination } from '@/composables/usePagination.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'
import KnowledgeBaseCard from '@/components/knowledgeBase/KnowledgeBaseCard.vue'

const { t } = useI18n()
const showCreateModal = ref(false)

// Search and sort
const searchQuery = ref('')
const sortBy = ref('recentlyUpdated')

const sortOptions = [
  { value: 'recentlyUpdated', label: '最近更新' },
  { value: 'name', label: '名称' },
  { value: 'vectorCount', label: '向量数量' }
]

// Filter logic
const filtered = computed(() => {
  let result = [...knowledgeBases]

  // Search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(kb =>
      kb.name.toLowerCase().includes(query) ||
      kb.description.toLowerCase().includes(query) ||
      kb.id.toLowerCase().includes(query)
    )
  }

  // Sort
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'vectorCount':
        return b.vectorStore.vectorCount - a.vectorStore.vectorCount
      case 'recentlyUpdated':
      default:
        return new Date(b.lastModified) - new Date(a.lastModified)
    }
  })

  return result
})

const { currentPage, totalPages, paginatedItems, totalItems } = usePagination(filtered, 8)

// Event handlers
function handleChat(kb) {
  console.log('Start chat with KB:', kb.id)
  // Navigate to chat page or open chat modal
}

function handleGraph(kb) {
  console.log('Open knowledge graph for KB:', kb.id)
  // Navigate to knowledge graph page
}

function handleDelete(kb) {
  if (confirm(t('knowledgeBase.confirmDelete', { name: kb.name }))) {
    console.log('Delete KB:', kb.id)
    // Call API to delete knowledge base
  }
}
</script>
