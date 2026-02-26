<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('tasks.title') }}</h1>
      <span class="text-sm text-gray-500">{{ $t('tasks.count', { count: filteredTasks.length }) }}</span>
    </div>
    <!-- Status filter tabs -->
    <div class="flex items-center space-x-2 mb-6 overflow-x-auto pb-2">
      <button
        v-for="sf in translatedStatusFilters"
        :key="sf.value"
        @click="activeStatus = sf.value"
        class="px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors"
        :class="activeStatus === sf.value
          ? 'bg-gray-900 text-white'
          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >
        {{ sf.label }}
        <span
          v-if="sf.value !== 'all'"
          class="ml-1 text-xs"
          :class="activeStatus === sf.value ? 'text-gray-300' : 'text-gray-400'"
        >{{ statusCount(sf.value) }}</span>
      </button>
    </div>
    <!-- Search + Sort -->
    <div class="flex items-center gap-3 mb-6">
      <div class="flex-1 max-w-md">
        <SearchBar v-model="searchQuery" :placeholder="$t('tasks.searchPlaceholder')" />
      </div>
      <SortDropdown v-model="sortBy" :options="translatedSortOptions" />
    </div>
    <!-- Results -->
    <div v-if="filteredTasks.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <TaskCard v-for="task in filteredTasks" :key="task.id" :task="task" />
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p class="text-lg">{{ $t('tasks.noResults') }}</p>
      <p class="text-sm mt-1">{{ $t('tasks.noResultsHint') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { taskApi } from '@/services/api.js'
import SearchBar from '@/components/common/SearchBar.vue'
import SortDropdown from '@/components/common/SortDropdown.vue'
import TaskCard from '@/components/dataflow/TaskCard.vue'

const { t } = useI18n()
const searchQuery = ref('')
const activeStatus = ref('all')
const sortBy = ref('recent')
const tasks = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const response = await taskApi.getTasks()
    tasks.value = response.list || []
  } catch (error) {
    console.error('Failed to load tasks:', error)
  } finally {
    loading.value = false
  }
})

const translatedStatusFilters = computed(() => [
  { value: 'all', label: t('tasks.status.all') },
  { value: 'running', label: t('tasks.status.running') },
  { value: 'completed', label: t('tasks.status.completed') },
  { value: 'failed', label: t('tasks.status.failed') },
])

const translatedSortOptions = computed(() => [
  { value: 'recent', label: t('tasks.sort.mostRecent') },
  { value: 'name', label: t('tasks.sort.name') },
  { value: 'status', label: t('tasks.sort.status') },
])

function statusCount(status) {
  return tasks.value.filter(t => t.status === status).length
}

const filteredTasks = computed(() => {
  let result = [...tasks.value]

  if (activeStatus.value !== 'all') {
    result = result.filter(t => t.status === activeStatus.value)
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(t =>
      t.name.toLowerCase().includes(q) ||
      t.dataset.toLowerCase().includes(q) ||
      t.package.toLowerCase().includes(q) ||
      t.author.toLowerCase().includes(q)
    )
  }

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'name': return a.name.localeCompare(b.name)
      case 'status': {
        const order = { running: 0, failed: 1, completed: 2 }
        return (order[a.status] ?? 3) - (order[b.status] ?? 3)
      }
      case 'recent':
      default:
        return new Date(b.startedAt) - new Date(a.startedAt)
    }
  })

  return result
})
</script>
