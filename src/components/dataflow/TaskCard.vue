<template>
  <div
    class="border rounded-lg p-4 hover:shadow-md transition-all bg-white cursor-pointer"
    :class="[borderClass, isClickable && (task.type === 'Model Evaluation' ? 'hover:border-emerald-300 hover:bg-emerald-50/30' : task.type === 'Model Tuning' ? 'hover:border-purple-300 hover:bg-purple-50/30' : 'hover:border-blue-300 hover:bg-blue-50/30')]"
    @click="handleClick"
  >
    <!-- Header: name + status badge + type badge -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2 flex-1 min-w-0">
        <span
          v-if="task.type"
          class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium flex-shrink-0"
          :class="typeBadgeClass"
        >
          {{ task.type }}
        </span>
        <h3 class="text-sm font-semibold text-gray-900 truncate">{{ task.name }}</h3>
      </div>
      <span
        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium flex-shrink-0"
        :class="statusBadgeClass"
      >
        <span v-if="task.status === 'running'" class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1.5 animate-pulse"></span>
        <span v-else-if="task.status === 'completed'" class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
        <span v-else class="w-1.5 h-1.5 rounded-full bg-red-500 mr-1.5"></span>
        {{ statusLabel }}
      </span>
    </div>

    <!-- Progress bar (running/failed) -->
    <div v-if="task.status === 'running' || task.status === 'failed'" class="mb-3">
      <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
        <span>Progress</span>
        <span>{{ task.progress }}%</span>
      </div>
      <div class="w-full bg-gray-100 rounded-full h-1.5">
        <div
          class="h-1.5 rounded-full transition-all"
          :class="task.status === 'failed' ? 'bg-red-400' : 'bg-blue-500'"
          :style="{ width: task.progress + '%' }"
        ></div>
      </div>
    </div>

    <!-- Info rows -->
    <div class="space-y-2 text-xs">
      <!-- Dataset -->
      <div class="flex items-center gap-2">
        <svg class="w-3.5 h-3.5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
        </svg>
        <span class="text-gray-500">Dataset</span>
        <span class="text-gray-800 font-medium truncate ml-auto">{{ task.dataset }}</span>
      </div>
      <!-- Package / Base Model -->
      <div class="flex items-center gap-2">
        <svg class="w-3.5 h-3.5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
        <span class="text-gray-500">{{ task.type === 'Model Tuning' ? 'Base Model' : 'Package' }}</span>
        <span class="text-gray-800 font-medium truncate ml-auto">{{ task.type === 'Model Tuning' ? task.baseModel : task.package }}</span>
      </div>
      <!-- Time -->
      <div class="flex items-center gap-2">
        <svg class="w-3.5 h-3.5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span class="text-gray-500">{{ task.status === 'running' ? 'Started' : 'Duration' }}</span>
        <span class="text-gray-800 font-medium ml-auto">{{ timeDisplay }}</span>
      </div>
    </div>

    <!-- Footer: author + started date -->
    <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100 text-xs text-gray-400">
      <span>by {{ task.author }}</span>
      <span>{{ formatDate(task.startedAt) }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  task: { type: Object, required: true }
})

const isClickable = computed(() => props.task.type === 'Model Tuning' || props.task.type === 'Model Evaluation' || props.task.type === 'Data Processing')

function handleClick() {
  if (isClickable.value) {
    router.push({ name: 'task-detail', params: { id: props.task.id } })
  }
}

const typeBadgeClass = computed(() => {
  switch (props.task.type) {
    case 'Model Tuning': return 'bg-purple-100 text-purple-700'
    case 'Model Evaluation': return 'bg-emerald-100 text-emerald-700'
    case 'Data Processing': return 'bg-blue-100 text-blue-700'
    default: return 'bg-gray-100 text-gray-700'
  }
})

const statusBadgeClass = computed(() => {
  switch (props.task.status) {
    case 'running': return 'bg-blue-50 text-blue-700'
    case 'completed': return 'bg-green-50 text-green-700'
    case 'failed': return 'bg-red-50 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
})

const borderClass = computed(() => {
  switch (props.task.status) {
    case 'running': return 'border-blue-200'
    case 'failed': return 'border-red-200'
    default: return 'border-gray-200'
  }
})

const statusLabel = computed(() => {
  switch (props.task.status) {
    case 'running': return 'Running'
    case 'completed': return 'Completed'
    case 'failed': return 'Failed'
    default: return props.task.status
  }
})

const timeDisplay = computed(() => {
  if (props.task.status === 'running') {
    return formatTime(props.task.startedAt)
  }
  return props.task.duration || '-'
})

function formatTime(isoStr) {
  const d = new Date(isoStr)
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
}

function formatDate(isoStr) {
  const d = new Date(isoStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
}
</script>
