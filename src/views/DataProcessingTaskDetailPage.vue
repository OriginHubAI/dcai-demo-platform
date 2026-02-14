<template>
  <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Back button -->
    <button
      @click="goBack"
      class="flex items-center text-sm text-gray-500 hover:text-gray-700 mb-6 transition-colors"
    >
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      Back to Tasks
    </button>

    <!-- Task Header -->
    <div class="mb-8">
      <div class="flex items-center gap-3 mb-2">
        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-700">
          {{ task.type }}
        </span>
        <span
          class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
          :class="statusBadgeClass"
        >
          <span v-if="task.status === 'running'" class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1.5 animate-pulse"></span>
          <span v-else-if="task.status === 'completed'" class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
          <span v-else class="w-1.5 h-1.5 rounded-full bg-red-500 mr-1.5"></span>
          {{ task.status }}
        </span>
      </div>
      <h1 class="text-3xl font-bold text-gray-900">{{ task.name }}</h1>
      <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
        <span>by {{ task.author }}</span>
        <span>•</span>
        <span>Started: {{ formatDate(task.startedAt) }}</span>
      </div>
    </div>

    <!-- Data Pipeline -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Data Pipeline</h2>
      <div class="relative">
        <!-- Pipeline Container -->
        <div class="flex items-start gap-0 overflow-x-auto pb-4" ref="pipelineContainer">
          <template v-for="(node, index) in pipelineNodes" :key="node.id">
            <!-- Node Card -->
            <div class="flex-shrink-0 w-[320px] bg-white rounded-lg border border-gray-200 shadow-sm">
              <!-- Node Header -->
              <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100"
                   :class="nodeHeaderClass(node.type)">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-6 rounded flex items-center justify-center" :class="nodeIconClass(node.type)">
                    <svg v-if="node.type === 'dataset'" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
                    </svg>
                    <svg v-else-if="node.type === 'filter'" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
                    </svg>
                    <svg v-else-if="node.type === 'generate'" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                  </div>
                  <div>
                    <div class="text-xs font-medium uppercase tracking-wide" :class="nodeTypeTextClass(node.type)">{{ node.type }}</div>
                    <div class="text-sm font-semibold text-gray-900 truncate max-w-[180px]">{{ node.name }}</div>
                  </div>
                </div>
                <button class="text-gray-400 hover:text-gray-600">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>

              <!-- Node Content -->
              <div class="p-4 space-y-4 max-h-[500px] overflow-y-auto">
                <!-- Init Parameters -->
                <div v-if="node.initParams && Object.keys(node.initParams).length > 0">
                  <h4 class="text-xs font-semibold text-green-600 uppercase tracking-wide mb-2">Init. Parameters</h4>
                  <div class="space-y-2">
                    <div v-for="(value, key) in node.initParams" :key="key" class="text-sm">
                      <div class="text-gray-500 text-xs mb-0.5">{{ formatParamKey(key) }}</div>
                      <div v-if="typeof value === 'string' && value.length > 50" class="text-gray-900 bg-gray-50 p-2 rounded text-xs leading-relaxed">
                        {{ value }}
                      </div>
                      <div v-else class="text-gray-900 font-medium">{{ value }}</div>
                    </div>
                  </div>
                </div>

                <!-- Run Parameters -->
                <div v-if="node.runParams && Object.keys(node.runParams).length > 0">
                  <h4 class="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-2">Run Parameters</h4>
                  <div class="space-y-2">
                    <div v-for="(value, key) in node.runParams" :key="key" class="text-sm">
                      <div class="text-gray-500 text-xs mb-0.5">{{ formatParamKey(key) }}</div>
                      <div class="text-gray-900 font-medium">{{ value }}</div>
                    </div>
                  </div>
                </div>

                <!-- Execution Logs -->
                <div v-if="node.logs && node.logs.length > 0">
                  <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Execution Logs</h4>
                  <div class="bg-gray-900 rounded-lg p-3 text-xs font-mono text-green-400 max-h-[200px] overflow-y-auto">
                    <div v-for="(log, i) in node.logs" :key="i" class="mb-1 leading-relaxed">
                      {{ log }}
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-2 pt-2">
                  <button class="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-orange-100 hover:bg-orange-200 text-orange-700 rounded-lg text-sm font-medium transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    Show Details
                  </button>
                  <button class="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-orange-100 hover:bg-orange-200 text-orange-700 rounded-lg text-sm font-medium transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                    </svg>
                    Download Data
                  </button>
                </div>
              </div>
            </div>

            <!-- Connection Line -->
            <div v-if="index < pipelineNodes.length - 1" class="flex-shrink-0 flex items-center px-2">
              <div class="relative flex items-center">
                <!-- Horizontal line -->
                <div class="w-8 h-0.5 bg-orange-400"></div>
                <!-- Node connector -->
                <div class="absolute left-1/2 -translate-x-1/2 w-8 h-6 bg-orange-400 rounded-full flex items-center justify-center">
                  <span class="text-white text-xs font-medium">Node</span>
                </div>
                <!-- Arrow -->
                <svg class="w-4 h-4 text-orange-400 ml-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Execute Result -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-gray-900">Execute Result</h2>
        <button class="text-gray-400 hover:text-gray-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Task Info -->
      <div class="flex items-center justify-between mb-6">
        <div class="text-sm">
          <span class="text-gray-500">Task ID:</span>
          <span class="font-mono text-gray-900 ml-1">{{ executionResult.taskId }}</span>
        </div>
        <div class="flex items-center gap-1 text-sm text-blue-600">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ executionResult.timeAgo }}
        </div>
      </div>

      <!-- Sample Data and Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Execution Sampled Data -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-3">Execution Sampled Data</h3>
          <div class="border border-gray-200 rounded-lg h-64 flex items-center justify-center bg-gray-50">
            <div class="text-center">
              <svg class="w-12 h-12 text-gray-300 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-gray-400 text-sm">No Data</p>
            </div>
          </div>
        </div>

        <!-- Sample Count Chart -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-3">Sample Count</h3>
          <div class="h-64">
            <canvas ref="sampleChart" class="w-full h-full"></canvas>
          </div>
        </div>
      </div>

      <!-- Logs Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Current Step Logs -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-3">Current Step Logs</h3>
          <div class="bg-gray-900 rounded-lg p-4 h-48 overflow-y-auto">
            <div class="font-mono text-xs space-y-1">
              <div v-for="(log, i) in currentStepLogs" :key="i" class="text-green-400">
                {{ log }}
              </div>
            </div>
          </div>
        </div>

        <!-- Logs -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-3">Logs</h3>
          <div class="bg-gray-900 rounded-lg p-4 h-48 overflow-y-auto">
            <div class="font-mono text-xs space-y-1">
              <div v-for="(log, i) in executionLogs" :key="i" :class="logClass(log)">
                {{ log }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTaskById } from '@/data/tasks.js'
import { getDataProcessingPipeline, getExecutionResult } from '@/data/dataflowTasks.js'

const route = useRoute()
const router = useRouter()
const sampleChart = ref(null)

const task = computed(() => {
  const id = route.params.id
  return getTaskById(id) || {}
})

const pipelineNodes = computed(() => {
  return getDataProcessingPipeline(task.value.id) || []
})

const executionResult = computed(() => {
  return getExecutionResult(task.value.id) || { taskId: '-', timeAgo: '-' }
})

const currentStepLogs = computed(() => {
  const result = executionResult.value
  return result.currentStepLogs || []
})

const executionLogs = computed(() => {
  const result = executionResult.value
  return result.logs || []
})

const statusBadgeClass = computed(() => {
  switch (task.value.status) {
    case 'running': return 'bg-blue-50 text-blue-700'
    case 'completed': return 'bg-green-50 text-green-700'
    case 'failed': return 'bg-red-50 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
})

function nodeHeaderClass(type) {
  switch (type) {
    case 'dataset': return 'bg-purple-50'
    case 'filter': return 'bg-orange-50'
    case 'generate': return 'bg-red-50'
    default: return 'bg-gray-50'
  }
}

function nodeIconClass(type) {
  switch (type) {
    case 'dataset': return 'bg-purple-500'
    case 'filter': return 'bg-orange-500'
    case 'generate': return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

function nodeTypeTextClass(type) {
  switch (type) {
    case 'dataset': return 'text-purple-600'
    case 'filter': return 'text-orange-600'
    case 'generate': return 'text-red-600'
    default: return 'text-gray-600'
  }
}

function formatParamKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

function logClass(log) {
  if (log.includes('Error') || log.includes('error')) return 'text-red-400'
  if (log.includes('Step')) return 'text-yellow-400'
  return 'text-green-400'
}

function goBack() {
  router.push({ name: 'dataflow-tasks' })
}

function formatDate(isoStr) {
  if (!isoStr) return '-'
  const d = new Date(isoStr)
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

function drawSampleChart() {
  const canvas = sampleChart.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  const rect = canvas.parentElement.getBoundingClientRect()
  canvas.width = rect.width * 2
  canvas.height = rect.height * 2
  canvas.style.width = rect.width + 'px'
  canvas.style.height = rect.height + 'px'

  const width = canvas.width
  const height = canvas.height
  const padding = { top: 40, right: 20, bottom: 60, left: 50 }

  // Sample data from screenshot
  const data = [
    { step: 'S1: ReasoningQue...', value: 8, color: '#f8b4b4' },
    { step: 'S2: ReasoningQue...', value: 16, color: '#fde68a' },
    { step: 'S3: ReasoningAns...', value: 16, color: '#bbf7d0' },
    { step: 'S4: ReasoningAns...', value: 16, color: '#bbf7d0' },
    { step: 'S5: ReasoningAns...', value: 16, color: '#bae6fd' },
  ]

  const maxValue = 16
  const barWidth = (width - padding.left - padding.right) / data.length * 0.5
  const spacing = (width - padding.left - padding.right) / data.length

  // Clear canvas
  ctx.clearRect(0, 0, width, height)

  // Draw grid lines
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding.top + (height - padding.top - padding.bottom) * i / 5
    ctx.beginPath()
    ctx.moveTo(padding.left, y)
    ctx.lineTo(width - padding.right, y)
    ctx.stroke()

    // Y-axis labels
    ctx.fillStyle = '#6b7280'
    ctx.font = '20px system-ui'
    ctx.textAlign = 'right'
    const value = Math.round(maxValue - maxValue * i / 5)
    ctx.fillText(value.toString(), padding.left - 10, y + 6)
  }

  // Draw bars
  data.forEach((item, index) => {
    const x = padding.left + spacing * index + spacing * 0.25
    const barHeight = (height - padding.top - padding.bottom) * item.value / maxValue
    const y = height - padding.bottom - barHeight

    // Bar
    ctx.fillStyle = item.color
    ctx.fillRect(x, y, barWidth, barHeight)

    // Value label on top
    if (item.value === 16) {
      ctx.fillStyle = '#4b5563'
      ctx.font = 'bold 24px system-ui'
      ctx.textAlign = 'center'
      ctx.fillText(item.value.toString(), x + barWidth / 2, y - 10)
    }

    // X-axis label
    ctx.fillStyle = '#6b7280'
    ctx.font = '18px system-ui'
    ctx.textAlign = 'center'
    ctx.fillText(item.step, x + barWidth / 2, height - padding.bottom + 30)
  })

  // Draw connecting line for trend
  ctx.strokeStyle = '#6366f1'
  ctx.lineWidth = 4
  ctx.beginPath()
  data.forEach((item, index) => {
    const x = padding.left + spacing * index + spacing * 0.25 + barWidth / 2
    const barHeight = (height - padding.top - padding.bottom) * item.value / maxValue
    const y = height - padding.bottom - barHeight
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  ctx.stroke()

  // Draw dots on the line
  ctx.fillStyle = '#6366f1'
  data.forEach((item, index) => {
    const x = padding.left + spacing * index + spacing * 0.25 + barWidth / 2
    const barHeight = (height - padding.top - padding.bottom) * item.value / maxValue
    const y = height - padding.bottom - barHeight
    ctx.beginPath()
    ctx.arc(x, y, 6, 0, Math.PI * 2)
    ctx.fill()
  })
}

onMounted(() => {
  nextTick(() => {
    drawSampleChart()
  })
})
</script>
