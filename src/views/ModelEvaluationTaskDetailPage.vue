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

    <!-- Evaluation Metrics Summary Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="text-sm text-gray-500 mb-1">Accuracy</div>
        <div class="text-2xl font-bold text-gray-900">{{ evaluationMetrics.accuracy }}</div>
        <div class="text-xs text-green-600 mt-1">↑ 5.2% vs baseline</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="text-sm text-gray-500 mb-1">Precision</div>
        <div class="text-2xl font-bold text-gray-900">{{ evaluationMetrics.precision }}</div>
        <div class="text-xs text-green-600 mt-1">↑ 4.5% vs baseline</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="text-sm text-gray-500 mb-1">Recall</div>
        <div class="text-2xl font-bold text-gray-900">{{ evaluationMetrics.recall }}</div>
        <div class="text-xs text-green-600 mt-1">↑ 6.8% vs baseline</div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="text-sm text-gray-500 mb-1">F1 Score</div>
        <div class="text-2xl font-bold text-gray-900">{{ evaluationMetrics.f1 }}</div>
        <div class="text-xs text-green-600 mt-1">↑ 4.2% vs baseline</div>
      </div>
    </div>

    <!-- Evaluation Results Visualization -->
    <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Evaluation Metrics Comparison</h2>
      <div class="h-96 relative">
        <canvas ref="metricsChart" class="w-full h-full"></canvas>
      </div>
    </div>

    <!-- Additional Metrics -->
    <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Detailed Metrics</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">AUC-ROC</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.auc }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Perplexity</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.perplexity }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">BLEU Score</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.bleu }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">ROUGE-L</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.rouge }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Latency (ms)</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.latency }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Throughput (samples/s)</div>
          <div class="text-base font-medium text-gray-900">{{ detailedMetrics.throughput }}</div>
        </div>
      </div>
    </div>

    <!-- Evaluation Parameters -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Evaluation Configuration</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Model</div>
          <div class="text-base font-medium text-gray-900">{{ evaluationConfig.model }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Dataset</div>
          <div class="text-base font-medium text-gray-900">{{ task.dataset }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Evaluation Package</div>
          <div class="text-base font-medium text-gray-900">{{ task.package }}</div>
        </div>
        <div class="p-4 bg-gray-50 rounded-lg">
          <div class="text-sm text-gray-500 mb-1">Test Split</div>
          <div class="text-base font-medium text-gray-900">{{ evaluationConfig.testSplit }}</div>
        </div>
      </div>
    </div>

    <!-- Progress Section (for running tasks) -->
    <div v-if="task.status === 'running'" class="mt-6 bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-900">Evaluation Progress</h2>
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
          <div class="text-2xl font-bold text-gray-900">{{ samplesProcessed }}</div>
          <div class="text-sm text-gray-500">Samples Processed</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900">{{ currentAccuracy }}</div>
          <div class="text-sm text-gray-500">Current Accuracy</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900">~15m</div>
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

const route = useRoute()
const router = useRouter()
const metricsChart = ref(null)

const task = computed(() => {
  const id = route.params.id
  return tasks.find(t => t.id === id) || tasks[0]
})

const evaluationMetrics = computed(() => {
  // Different metrics based on task name
  if (task.value.name && task.value.name.includes('Math')) {
    return {
      accuracy: '78.5%',
      precision: '76.2%',
      recall: '80.1%',
      f1: '78.1%'
    }
  }
  if (task.value.name && task.value.name.includes('LLaMA')) {
    return {
      accuracy: '85.3%',
      precision: '84.1%',
      recall: '86.5%',
      f1: '85.3%'
    }
  }
  // Default metrics for Qwen3
  return {
    accuracy: '82.7%',
    precision: '81.4%',
    recall: '84.2%',
    f1: '82.8%'
  }
})

const detailedMetrics = computed(() => {
  if (task.value.name && task.value.name.includes('Math')) {
    return {
      auc: '0.923',
      perplexity: '4.56',
      bleu: '32.1',
      rouge: '0.45',
      latency: '125',
      throughput: '45.2'
    }
  }
  if (task.value.name && task.value.name.includes('LLaMA')) {
    return {
      auc: '0.951',
      perplexity: '3.21',
      bleu: '38.7',
      rouge: '0.52',
      latency: '180',
      throughput: '32.5'
    }
  }
  return {
    auc: '0.938',
    perplexity: '3.87',
    bleu: '35.4',
    rouge: '0.48',
    latency: '156',
    throughput: '38.7'
  }
})

const evaluationConfig = computed(() => {
  return {
    model: task.value.name && task.value.name.includes('LLaMA') ? 'LLaMA3-70B-Instruct' : 
           task.value.name && task.value.name.includes('Mistral') ? 'Mistral-7B-Instruct' :
           task.value.name && task.value.name.includes('Med-SFT') ? 'Qwen3 8B Med-SFT' : 'Qwen3-8B',
    testSplit: '20%',
    batchSize: 32,
    evalFramework: 'PyTorch'
  }
})

const samplesProcessed = computed(() => {
  const total = 10000
  return Math.round(total * task.value.progress / 100).toLocaleString()
})

const currentAccuracy = computed(() => {
  const base = task.value.status === 'completed' ? 82.7 : 75
  const progress = task.value.progress || 0
  const current = base + (progress * 0.1)
  return current.toFixed(1) + '%'
})

const typeBadgeClass = computed(() => {
  return task.value.type === 'Model Evaluation' 
    ? 'bg-emerald-100 text-emerald-700' 
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
  const canvas = metricsChart.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const rect = canvas.parentElement.getBoundingClientRect()
  canvas.width = rect.width * 2
  canvas.height = rect.height * 2
  canvas.style.width = rect.width + 'px'
  canvas.style.height = rect.height + 'px'
  
  const width = canvas.width
  const height = canvas.height
  const centerX = width / 2
  const centerY = height / 2 + 30  // Slightly lower to make room for top labels
  const radius = Math.min(width, height) / 2 - 100  // Larger radius for bigger chart
  
  // Metrics data
  const labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC-ROC']
  const values = [
    parseFloat(evaluationMetrics.value.accuracy),
    parseFloat(evaluationMetrics.value.precision),
    parseFloat(evaluationMetrics.value.recall),
    parseFloat(evaluationMetrics.value.f1),
    parseFloat(detailedMetrics.value.auc) * 100
  ]
  
  const numAxes = labels.length
  const angleStep = (2 * Math.PI) / numAxes
  
  // Clear canvas
  ctx.clearRect(0, 0, width, height)
  
  // Draw concentric grid circles
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  for (let i = 1; i <= 5; i++) {
    ctx.beginPath()
    const r = (radius * i) / 5
    for (let j = 0; j <= numAxes; j++) {
      const angle = j * angleStep - Math.PI / 2
      const x = centerX + r * Math.cos(angle)
      const y = centerY + r * Math.sin(angle)
      if (j === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    }
    ctx.closePath()
    ctx.stroke()
  }
  
  // Draw axis lines and labels
  ctx.strokeStyle = '#9ca3af'
  ctx.fillStyle = '#6b7280'
  ctx.font = '24px system-ui'
  ctx.textAlign = 'center'
  
  for (let i = 0; i < numAxes; i++) {
    const angle = i * angleStep - Math.PI / 2
    const xEnd = centerX + radius * Math.cos(angle)
    const yEnd = centerY + radius * Math.sin(angle)
    
    // Draw axis line
    ctx.beginPath()
    ctx.moveTo(centerX, centerY)
    ctx.lineTo(xEnd, yEnd)
    ctx.stroke()
    
    // Draw labels with adjusted positioning
    const labelRadius = radius + 70
    const labelX = centerX + labelRadius * Math.cos(angle)
    const labelY = centerY + labelRadius * Math.sin(angle)
    
    // Adjust text alignment based on position
    if (Math.abs(angle - (-Math.PI / 2)) < 0.1) {
      // Top label (Accuracy)
      ctx.textAlign = 'center'
      ctx.fillText(labels[i], labelX, labelY)
    } else if (angle > -Math.PI / 2 && angle < Math.PI / 2) {
      // Right side labels
      ctx.textAlign = 'left'
      ctx.fillText(labels[i], labelX + 15, labelY + 8)
    } else {
      // Left side labels
      ctx.textAlign = 'right'
      ctx.fillText(labels[i], labelX - 15, labelY + 8)
    }
  }
  
  
  // Draw data polygon
  ctx.beginPath()
  for (let i = 0; i <= numAxes; i++) {
    const idx = i % numAxes
    const angle = idx * angleStep - Math.PI / 2
    const r = (values[idx] / 100) * radius
    const x = centerX + r * Math.cos(angle)
    const y = centerY + r * Math.sin(angle)
    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  }
  ctx.closePath()
  
  // Fill the polygon
  ctx.fillStyle = 'rgba(16, 185, 129, 0.2)'
  ctx.fill()
  
  // Stroke the polygon
  ctx.strokeStyle = '#10b981'
  ctx.lineWidth = 3
  ctx.stroke()
  
  // Draw data points and value labels
  for (let i = 0; i < numAxes; i++) {
    const angle = i * angleStep - Math.PI / 2
    const r = (values[i] / 100) * radius
    const x = centerX + r * Math.cos(angle)
    const y = centerY + r * Math.sin(angle)
    
    ctx.beginPath()
    ctx.arc(x, y, 8, 0, 2 * Math.PI)
    ctx.fillStyle = '#10b981'
    ctx.fill()
    ctx.strokeStyle = '#ffffff'
    ctx.lineWidth = 2
    ctx.stroke()
    
    // Draw value labels with better positioning
    ctx.fillStyle = '#374151'
    ctx.font = 'bold 20px system-ui'
    
    // Position value labels further out to avoid overlap
    const valueOffset = 50
    let valueX, valueY
    
    if (Math.abs(angle - (-Math.PI / 2)) < 0.1) {
      // Top value (Accuracy) - position above
      ctx.textAlign = 'center'
      valueX = x
      valueY = y - valueOffset
    } else if (angle > -Math.PI / 2 && angle < Math.PI / 2) {
      // Right side values - position to the right
      ctx.textAlign = 'left'
      valueX = x + valueOffset
      valueY = y + 6
    } else {
      // Left side values - position to the left
      ctx.textAlign = 'right'
      valueX = x - valueOffset
      valueY = y + 6
    }
    
    ctx.fillText(values[i].toFixed(1) + '%', valueX, valueY)
  }
}

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})
</script>
