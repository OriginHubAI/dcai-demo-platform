<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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
        <span
          class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
          :class="typeBadgeClass"
        >
          {{ task.type }}
        </span>
        <span
          class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
          :class="statusBadgeClass"
        >
          <span v-if="task.status === 'running'" class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1.5 animate-pulse"></span>
          <span v-else-if="task.status === 'completed'" class="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
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

    <!-- Export Model Section (for running and completed tasks) -->
    <div v-if="task.status === 'completed' || task.status === 'running'" class="mt-8 mb-8 bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Export Model</h2>
          <p class="text-sm text-gray-500 mt-1">Export the LoRA checkpoint to Models page</p>
        </div>
        <button
          v-if="!isModelExported"
          @click="exportModel"
          class="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
          </svg>
          Export to Models
        </button>
        <div v-else class="inline-flex items-center px-4 py-2 bg-green-50 text-green-700 rounded-lg">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          Already Exported
        </div>
      </div>
      <div v-if="isModelExported" class="mt-4 p-4 bg-gray-50 rounded-lg">
        <div class="text-sm text-gray-500 mb-2">Exported model details:</div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div><span class="text-gray-500">Model ID:</span> <span class="font-medium text-gray-900">{{ exportedModelId }}</span></div>
          <div><span class="text-gray-500">Type:</span> <span class="font-medium text-gray-900">LoRA ({{ task.type }})</span></div>
        </div>
      </div>
    </div>

    <!-- Training Loss Chart -->
    <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Training Loss</h2>
      <div class="h-64 relative">
        <canvas ref="lossChart" class="w-full h-full"></canvas>
      </div>
    </div>

    <!-- SFT Training Parameters -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">SFT Training Parameters</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Model</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.model }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Base Model</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.baseModel }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Dataset</div>
          <div class="text-base font-medium text-gray-900">{{ task.dataset }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Learning Rate</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.learningRate }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Batch Size</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.batchSize }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Epochs</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.epochs }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Warmup Steps</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.warmupSteps }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Max Sequence Length</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.maxSeqLength }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Gradient Accumulation</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.gradientAccumulation }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Optimizer</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.optimizer }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Weight Decay</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.weightDecay }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Training Steps</div>
          <div class="text-base font-medium text-gray-900">{{ trainingParams.trainingSteps }}</div>
        </div>
      </div>
    </div>

    <!-- Progress Section (for running tasks) -->
    <div v-if="task.status === 'running'" class="mt-6 bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-900">Training Progress</h2>
        <span class="text-sm text-gray-500">{{ task.progress }}%</span>
      </div>
      <div class="w-full bg-gray-100 rounded-full h-2">
        <div
          class="h-2 rounded-full bg-blue-500 transition-all"
          :style="{ width: task.progress + '%' }"
        ></div>
      </div>
      <div class="mt-4 grid grid-cols-3 gap-4 text-center">
        <div>
          <div class="text-2xl font-bold text-gray-900">1,234</div>
          <div class="text-sm text-gray-500">Tokens/Step</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900">{{ currentLoss }}</div>
          <div class="text-sm text-gray-500">Current Loss</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900">~2h</div>
          <div class="text-sm text-gray-500">Est. Remaining</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { tasks } from '@/data/tasks.js'
import { models } from '@/data/models.js'

const route = useRoute()
const router = useRouter()
const lossChart = ref(null)

// Track exported models for this session
const exportedModels = ref([])

const task = computed(() => {
  const id = route.params.id
  return tasks.find(t => t.id === id) || tasks[0]
})

// Generate a unique model ID based on task
const exportedModelId = computed(() => {
  if (!task.value) return ''
  return `lora/${task.value.id}-${task.value.name.replace(/\s+/g, '-')}`
})

// Check if model is already exported
const isModelExported = computed(() => {
  const modelId = exportedModelId.value
  return models.some(m => m.id === modelId) || exportedModels.value.includes(modelId)
})

function exportModel() {
  const modelId = exportedModelId.value
  const newModel = {
    id: modelId,
    author: task.value.author,
    name: `${task.value.name} (LoRA)`,
    pipeline_tag: 'text-generation',
    downloads: 0,
    likes: 0,
    lastModified: new Date().toISOString().split('T')[0],
    tags: ['lora', 'fine-tuned', task.value.type?.toLowerCase().replace(/\s+/g, '-') || 'model-tuning'],
    library: 'transformers',
    language: 'multilingual',
    license: 'apache-2.0',
    featured: false,
    description: `LoRA checkpoint exported from ${task.value.name} training task. Base model: ${trainingParams.value.baseModel}. Dataset: ${task.value.dataset}.`,
    isExported: true,
    baseModel: trainingParams.value.baseModel,
    taskId: task.value.id
  }
  
  models.unshift(newModel)
  exportedModels.value.push(modelId)
  
  // Optionally navigate to the models page
  // router.push({ name: 'models' })
}

const trainingParams = computed(() => {
  if (task.value.name && task.value.name.includes('VL')) {
    return {
      model: 'Qwen2-VL-2B-Instruct',
      baseModel: 'Qwen2-VL-2B',
      learningRate: '1e-5',
      batchSize: 8,
      epochs: 3,
      warmupSteps: 100,
      maxSeqLength: 4096,
      gradientAccumulation: 4,
      optimizer: 'AdamW',
      weightDecay: 0.01,
      trainingSteps: 1500
    }
  }
  return {
    model: 'Qwen3-8B',
    baseModel: 'Qwen3-8B-Base',
    learningRate: '2e-5',
    batchSize: 16,
    epochs: 3,
    warmupSteps: 500,
    maxSeqLength: 8192,
    gradientAccumulation: 2,
    optimizer: 'AdamW',
    weightDecay: 0.01,
    trainingSteps: 3000
  }
})

const currentLoss = computed(() => {
  if (task.value.status === 'completed') return '0.234'
  if (task.value.name && task.value.name.includes('VL')) {
    return (1.5 - task.value.progress * 0.01).toFixed(3)
  }
  return (2.0 - task.value.progress * 0.012).toFixed(3)
})

const typeBadgeClass = computed(() => {
  return task.value.type === 'Model Tuning' 
    ? 'bg-purple-100 text-purple-700' 
    : 'bg-blue-100 text-blue-700'
})

const statusBadgeClass = computed(() => {
  switch (task.value.status) {
    case 'running': return 'bg-blue-50 text-blue-700'
    case 'completed': return 'bg-green-50 text-green-700'
    case 'failed': return 'bg-red-50 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
})

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

function drawChart() {
  const canvas = lossChart.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const rect = canvas.parentElement.getBoundingClientRect()
  canvas.width = rect.width * 2
  canvas.height = rect.height * 2
  canvas.style.width = rect.width + 'px'
  canvas.style.height = rect.height + 'px'
  
  const width = canvas.width
  const height = canvas.height
  const padding = 60
  
  // Generate loss data
  const isVL = task.value.name && task.value.name.includes('VL')
  const steps = isVL ? 50 : 80
  const data = []
  for (let i = 0; i < steps; i++) {
    const baseLoss = isVL ? 2.5 : 3.0
    const noise = Math.random() * 0.1
    const decay = Math.exp(-i * 0.05)
    data.push(baseLoss * decay + 0.2 + noise)
  }
  
  // Clear canvas
  ctx.clearRect(0, 0, width, height)
  
  // Draw grid
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height - 2 * padding) * i / 5
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(width - padding, y)
    ctx.stroke()
  }
  
  // Y-axis labels
  ctx.fillStyle = '#6b7280'
  ctx.font = '24px system-ui'
  ctx.textAlign = 'right'
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height - 2 * padding) * i / 5
    const val = (3 - i * 0.6).toFixed(1)
    ctx.fillText(val, padding - 10, y + 8)
  }
  
  // X-axis labels
  ctx.textAlign = 'center'
  const xSteps = 5
  for (let i = 0; i <= xSteps; i++) {
    const x = padding + (width - 2 * padding) * i / xSteps
    const val = Math.round(steps * i / xSteps)
    ctx.fillText(val.toString(), x, height - padding + 30)
  }
  
  // Draw loss line
  ctx.strokeStyle = '#8b5cf6'
  ctx.lineWidth = 4
  ctx.lineJoin = 'round'
  ctx.lineCap = 'round'
  ctx.beginPath()
  
  const maxLoss = Math.max(...data)
  const minLoss = Math.min(...data)
  const lossRange = maxLoss - minLoss || 1
  
  for (let i = 0; i < data.length; i++) {
    const x = padding + (width - 2 * padding) * i / (data.length - 1)
    // Invert Y: higher loss at top (smaller y), lower loss at bottom (larger y)
    const y = padding + (height - 2 * padding) * (maxLoss - data[i]) / lossRange
    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  }
  ctx.stroke()
  
  // Draw dots
  ctx.fillStyle = '#8b5cf6'
  for (let i = 0; i < data.length; i += Math.ceil(data.length / 10)) {
    const x = padding + (width - 2 * padding) * i / (data.length - 1)
    // Invert Y: higher loss at top (smaller y), lower loss at bottom (larger y)
    const y = padding + (height - 2 * padding) * (maxLoss - data[i]) / lossRange
    ctx.beginPath()
    ctx.arc(x, y, 6, 0, Math.PI * 2)
    ctx.fill()
  }
  
  // Axis labels
  ctx.fillStyle = '#374151'
  ctx.font = 'bold 28px system-ui'
  ctx.textAlign = 'center'
  ctx.fillText('Training Steps', width / 2, height - 15)
  
  ctx.save()
  ctx.translate(20, height / 2)
  ctx.rotate(-Math.PI / 2)
  ctx.fillText('Loss', 0, 0)
  ctx.restore()
}

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})
</script>
