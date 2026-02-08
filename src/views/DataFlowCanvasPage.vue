<template>
  <div class="h-[calc(100vh-57px)] flex overflow-hidden bg-gray-50">
    <!-- Left Toolbar -->
    <div class="w-12 bg-white border-r border-gray-200 flex flex-col items-center py-3 gap-1 flex-shrink-0">
      <button
        v-for="tool in tools"
        :key="tool.id"
        @click="activeTool = tool.id"
        :title="tool.label"
        class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
        :class="activeTool === tool.id ? 'bg-dc-primary text-white' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-700'"
      >
        <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" :d="tool.icon" />
        </svg>
      </button>
      <div class="flex-1" />
      <button
        title="Zoom In"
        @click="zoomIn"
        class="w-9 h-9 rounded-lg flex items-center justify-center text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
        </svg>
      </button>
      <button
        title="Zoom Out"
        @click="zoomOut"
        class="w-9 h-9 rounded-lg flex items-center justify-center text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M18 12H6" />
        </svg>
      </button>
      <button
        title="Fit View"
        @click="fitView"
        class="w-9 h-9 rounded-lg flex items-center justify-center text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5" />
        </svg>
      </button>
    </div>

    <!-- Canvas Area -->
    <div class="flex-1 relative overflow-hidden" ref="canvasContainer">
      <!-- Top bar -->
      <div class="absolute top-0 left-0 right-0 z-10 bg-white/80 backdrop-blur-sm border-b border-gray-200 px-4 py-2 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <h2 class="text-sm font-semibold text-gray-900">DataFlow Canvas</h2>
          <span class="text-xs text-gray-400">|</span>
          <span class="text-xs text-gray-500">{{ nodes.length }} nodes</span>
          <span class="text-xs text-gray-400">{{ edges.length }} connections</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-400">{{ Math.round(zoom * 100) }}%</span>
          <button
            @click="addNode"
            class="text-xs bg-dc-primary text-white px-3 py-1.5 rounded-md hover:bg-dc-primary-dark transition-colors font-medium"
          >
            + Add Node
          </button>
        </div>
      </div>

      <!-- SVG Canvas -->
      <svg
        ref="svgCanvas"
        class="w-full h-full"
        @mousedown="onCanvasMouseDown"
        @mousemove="onCanvasMouseMove"
        @mouseup="onCanvasMouseUp"
        @wheel.prevent="onWheel"
      >
        <defs>
          <pattern id="grid-small" width="20" height="20" patternUnits="userSpaceOnUse"
            :patternTransform="`translate(${pan.x},${pan.y}) scale(${zoom})`">
            <circle cx="10" cy="10" r="0.5" fill="#d1d5db" />
          </pattern>
          <pattern id="grid-large" width="100" height="100" patternUnits="userSpaceOnUse"
            :patternTransform="`translate(${pan.x},${pan.y}) scale(${zoom})`">
            <circle cx="50" cy="50" r="1" fill="#9ca3af" opacity="0.3" />
          </pattern>
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" :fill="'#9ca3af'" />
          </marker>
        </defs>

        <!-- Grid background -->
        <rect width="100%" height="100%" fill="url(#grid-small)" />
        <rect width="100%" height="100%" fill="url(#grid-large)" />

        <g :transform="`translate(${pan.x},${pan.y}) scale(${zoom})`">
          <!-- Edges -->
          <g v-for="edge in edges" :key="edge.id">
            <path
              :d="getEdgePath(edge)"
              fill="none"
              stroke="#94a3b8"
              stroke-width="2"
              marker-end="url(#arrowhead)"
              class="transition-colors"
            />
          </g>

          <!-- Dragging edge preview -->
          <path
            v-if="draggingEdge"
            :d="getDraggingEdgePath()"
            fill="none"
            stroke="#3b82f6"
            stroke-width="2"
            stroke-dasharray="6 3"
            opacity="0.6"
          />

          <!-- Nodes -->
          <g
            v-for="node in nodes"
            :key="node.id"
            :transform="`translate(${node.x},${node.y})`"
            @mousedown.stop="onNodeMouseDown($event, node)"
            class="cursor-move"
          >
            <!-- Node shadow -->
            <rect
              x="1" y="1"
              :width="node.width" :height="node.height"
              rx="8" ry="8"
              fill="black" opacity="0.05"
            />
            <!-- Node body -->
            <rect
              x="0" y="0"
              :width="node.width" :height="node.height"
              rx="8" ry="8"
              fill="white"
              :stroke="selectedNode === node.id ? '#1a56db' : '#e5e7eb'"
              :stroke-width="selectedNode === node.id ? 2 : 1"
            />
            <!-- Color accent bar -->
            <rect
              x="0" y="0"
              :width="node.width" height="4"
              :rx="8" :ry="8"
              :fill="node.color"
            />
            <rect
              x="0" y="2"
              :width="node.width" height="2"
              :fill="node.color"
            />

            <!-- Node icon -->
            <circle :cx="20" :cy="28" r="12" :fill="node.color" opacity="0.1" />
            <text :x="20" :y="33" text-anchor="middle" :fill="node.color" font-size="14">
              {{ node.emoji }}
            </text>

            <!-- Node title -->
            <text :x="40" :y="32" font-size="12" font-weight="600" fill="#1f2937">
              {{ node.label }}
            </text>

            <!-- Node description -->
            <text :x="12" :y="54" font-size="10" fill="#6b7280">
              {{ node.description }}
            </text>

            <!-- Input port -->
            <circle
              v-if="node.hasInput"
              :cx="0" :cy="node.height / 2"
              r="5"
              fill="white"
              stroke="#94a3b8"
              stroke-width="1.5"
              class="cursor-crosshair"
            />

            <!-- Output port -->
            <circle
              v-if="node.hasOutput"
              :cx="node.width" :cy="node.height / 2"
              r="5"
              fill="white"
              stroke="#94a3b8"
              stroke-width="1.5"
              class="cursor-crosshair"
              @mousedown.stop="onPortMouseDown($event, node, 'output')"
            />
          </g>
        </g>
      </svg>

      <!-- Minimap -->
      <div class="absolute bottom-4 right-4 w-44 h-28 bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
        <svg class="w-full h-full" :viewBox="minimapViewBox">
          <rect :x="minimapBounds.minX - 20" :y="minimapBounds.minY - 20"
            :width="minimapBounds.width + 40" :height="minimapBounds.height + 40"
            fill="#f9fafb" />
          <g v-for="edge in edges" :key="'mm-' + edge.id">
            <line
              :x1="getNodeCenter(edge.from).x" :y1="getNodeCenter(edge.from).y"
              :x2="getNodeCenter(edge.to).x" :y2="getNodeCenter(edge.to).y"
              stroke="#d1d5db" stroke-width="2"
            />
          </g>
          <rect
            v-for="node in nodes" :key="'mm-' + node.id"
            :x="node.x" :y="node.y"
            :width="node.width" :height="node.height"
            rx="3" ry="3"
            :fill="node.color" opacity="0.3"
            :stroke="node.color" stroke-width="2"
          />
          <!-- Viewport indicator -->
          <rect
            :x="(-pan.x / zoom)" :y="(-pan.y / zoom)"
            :width="viewportSize.w / zoom" :height="viewportSize.h / zoom"
            fill="none" stroke="#1a56db" stroke-width="3" rx="2"
            opacity="0.5"
          />
        </svg>
      </div>
    </div>

    <!-- Right Panel (Node Properties) -->
    <transition name="slide">
      <div v-if="selectedNodeData" class="w-64 bg-white border-l border-gray-200 flex-shrink-0 overflow-y-auto">
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-semibold text-gray-900">Properties</h3>
            <button @click="selectedNode = null" class="text-gray-400 hover:text-gray-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <!-- Node color indicator -->
          <div class="flex items-center gap-2 mb-4">
            <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: selectedNodeData.color }" />
            <span class="text-sm font-medium text-gray-700">{{ selectedNodeData.label }}</span>
          </div>
          <!-- Properties -->
          <div class="space-y-3">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Type</label>
              <div class="text-sm text-gray-900 bg-gray-50 rounded-md px-3 py-1.5">{{ selectedNodeData.type }}</div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Description</label>
              <div class="text-sm text-gray-700 bg-gray-50 rounded-md px-3 py-1.5">{{ selectedNodeData.description }}</div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Position</label>
              <div class="grid grid-cols-2 gap-2">
                <div class="text-xs text-gray-500 bg-gray-50 rounded-md px-2 py-1.5">X: {{ Math.round(selectedNodeData.x) }}</div>
                <div class="text-xs text-gray-500 bg-gray-50 rounded-md px-2 py-1.5">Y: {{ Math.round(selectedNodeData.y) }}</div>
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Connections</label>
              <div class="text-sm text-gray-700 bg-gray-50 rounded-md px-3 py-1.5">
                {{ getNodeConnectionCount(selectedNodeData.id) }} connection(s)
              </div>
            </div>
          </div>
          <!-- Actions -->
          <div class="mt-6 space-y-2">
            <button
              @click="duplicateNode(selectedNodeData)"
              class="w-full text-xs text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-md px-3 py-2 transition-colors text-left"
            >
              Duplicate Node
            </button>
            <button
              @click="deleteNode(selectedNodeData.id)"
              class="w-full text-xs text-red-600 bg-red-50 hover:bg-red-100 rounded-md px-3 py-2 transition-colors text-left"
            >
              Delete Node
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

const canvasContainer = ref(null)
const svgCanvas = ref(null)

const activeTool = ref('select')
const selectedNode = ref(null)
const zoom = ref(1)
const pan = reactive({ x: 0, y: 0 })
const viewportSize = reactive({ w: 1200, h: 700 })

const tools = [
  { id: 'select', label: 'Select', icon: 'M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122' },
  { id: 'pan', label: 'Pan', icon: 'M7 11.5V14m0-2.5v-6a1.5 1.5 0 113 0m-3 6a1.5 1.5 0 00-3 0v2a7.5 7.5 0 0015 0v-5a1.5 1.5 0 00-3 0m-6-3V11m0-5.5v-1a1.5 1.5 0 013 0v1m0 0V11m0-5.5a1.5 1.5 0 013 0v3m0 0V11' },
  { id: 'connect', label: 'Connect', icon: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1' },
]

let nodeIdCounter = 7

const nodes = reactive([
  { id: 1, label: 'Data Source', type: 'source', description: 'Load raw data', emoji: '\u{1F4E5}', x: 80, y: 180, width: 180, height: 68, color: '#3b82f6', hasInput: false, hasOutput: true },
  { id: 2, label: 'Data Cleaning', type: 'transform', description: 'Clean & validate', emoji: '\u{1F9F9}', x: 340, y: 100, width: 180, height: 68, color: '#10b981', hasInput: true, hasOutput: true },
  { id: 3, label: 'Feature Engineering', type: 'transform', description: 'Extract features', emoji: '\u2699\uFE0F', x: 340, y: 260, width: 180, height: 68, color: '#8b5cf6', hasInput: true, hasOutput: true },
  { id: 4, label: 'Model Training', type: 'model', description: 'Train ML model', emoji: '\u{1F9E0}', x: 600, y: 180, width: 180, height: 68, color: '#f59e0b', hasInput: true, hasOutput: true },
  { id: 5, label: 'Model Evaluation', type: 'evaluation', description: 'Evaluate metrics', emoji: '\u{1F4CA}', x: 860, y: 120, width: 180, height: 68, color: '#ef4444', hasInput: true, hasOutput: true },
  { id: 6, label: 'Data Export', type: 'export', description: 'Export results', emoji: '\u{1F4E4}', x: 860, y: 260, width: 180, height: 68, color: '#06b6d4', hasInput: true, hasOutput: false },
])

const edges = reactive([
  { id: 'e1-2', from: 1, to: 2 },
  { id: 'e1-3', from: 1, to: 3 },
  { id: 'e2-4', from: 2, to: 4 },
  { id: 'e3-4', from: 3, to: 4 },
  { id: 'e4-5', from: 4, to: 5 },
  { id: 'e4-6', from: 4, to: 6 },
])

// Dragging state
const dragging = reactive({ active: false, nodeId: null, offsetX: 0, offsetY: 0 })
const panning = reactive({ active: false, startX: 0, startY: 0, startPanX: 0, startPanY: 0 })
const draggingEdge = ref(null)

const selectedNodeData = computed(() => {
  if (!selectedNode.value) return null
  return nodes.find(n => n.id === selectedNode.value) || null
})

const minimapBounds = computed(() => {
  if (!nodes.length) return { minX: 0, minY: 0, width: 800, height: 400 }
  const minX = Math.min(...nodes.map(n => n.x))
  const minY = Math.min(...nodes.map(n => n.y))
  const maxX = Math.max(...nodes.map(n => n.x + n.width))
  const maxY = Math.max(...nodes.map(n => n.y + n.height))
  return { minX, minY, width: maxX - minX, height: maxY - minY }
})

const minimapViewBox = computed(() => {
  const b = minimapBounds.value
  const padding = 40
  return `${b.minX - padding} ${b.minY - padding} ${b.width + padding * 2} ${b.height + padding * 2}`
})

function getNodeCenter(nodeId) {
  const node = nodes.find(n => n.id === nodeId)
  if (!node) return { x: 0, y: 0 }
  return { x: node.x + node.width / 2, y: node.y + node.height / 2 }
}

function getEdgePath(edge) {
  const fromNode = nodes.find(n => n.id === edge.from)
  const toNode = nodes.find(n => n.id === edge.to)
  if (!fromNode || !toNode) return ''

  const x1 = fromNode.x + fromNode.width
  const y1 = fromNode.y + fromNode.height / 2
  const x2 = toNode.x
  const y2 = toNode.y + toNode.height / 2
  const dx = Math.abs(x2 - x1) * 0.5

  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
}

function getDraggingEdgePath() {
  if (!draggingEdge.value) return ''
  const { x1, y1, x2, y2 } = draggingEdge.value
  const dx = Math.abs(x2 - x1) * 0.5
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
}

function getNodeConnectionCount(nodeId) {
  return edges.filter(e => e.from === nodeId || e.to === nodeId).length
}

function getSVGPoint(event) {
  const rect = svgCanvas.value.getBoundingClientRect()
  return {
    x: (event.clientX - rect.left - pan.x) / zoom.value,
    y: (event.clientY - rect.top - pan.y) / zoom.value,
  }
}

// Node interactions
function onNodeMouseDown(event, node) {
  if (activeTool.value === 'connect') {
    onPortMouseDown(event, node, 'output')
    return
  }
  selectedNode.value = node.id
  dragging.active = true
  dragging.nodeId = node.id
  const pt = getSVGPoint(event)
  dragging.offsetX = pt.x - node.x
  dragging.offsetY = pt.y - node.y
}

function onPortMouseDown(event, node, portType) {
  if (portType === 'output' && node.hasOutput) {
    const x1 = node.x + node.width
    const y1 = node.y + node.height / 2
    draggingEdge.value = { fromId: node.id, x1, y1, x2: x1, y2: y1 }
  }
}

// Canvas interactions
function onCanvasMouseDown(event) {
  if (event.target === svgCanvas.value || event.target.tagName === 'rect') {
    if (activeTool.value === 'pan' || event.button === 1) {
      panning.active = true
      panning.startX = event.clientX
      panning.startY = event.clientY
      panning.startPanX = pan.x
      panning.startPanY = pan.y
    } else {
      selectedNode.value = null
      panning.active = true
      panning.startX = event.clientX
      panning.startY = event.clientY
      panning.startPanX = pan.x
      panning.startPanY = pan.y
    }
  }
}

function onCanvasMouseMove(event) {
  if (dragging.active) {
    const pt = getSVGPoint(event)
    const node = nodes.find(n => n.id === dragging.nodeId)
    if (node) {
      node.x = pt.x - dragging.offsetX
      node.y = pt.y - dragging.offsetY
    }
  } else if (panning.active) {
    pan.x = panning.startPanX + (event.clientX - panning.startX)
    pan.y = panning.startPanY + (event.clientY - panning.startY)
  } else if (draggingEdge.value) {
    const pt = getSVGPoint(event)
    draggingEdge.value.x2 = pt.x
    draggingEdge.value.y2 = pt.y
  }
}

function onCanvasMouseUp(event) {
  if (draggingEdge.value) {
    // Check if dropped on a node input
    const pt = getSVGPoint(event)
    const targetNode = nodes.find(n =>
      n.hasInput &&
      n.id !== draggingEdge.value.fromId &&
      pt.x >= n.x - 10 && pt.x <= n.x + 10 &&
      pt.y >= n.y && pt.y <= n.y + n.height
    )
    if (targetNode) {
      const exists = edges.some(e => e.from === draggingEdge.value.fromId && e.to === targetNode.id)
      if (!exists) {
        edges.push({
          id: `e${draggingEdge.value.fromId}-${targetNode.id}`,
          from: draggingEdge.value.fromId,
          to: targetNode.id,
        })
      }
    }
    draggingEdge.value = null
  }
  dragging.active = false
  panning.active = false
}

function onWheel(event) {
  const delta = event.deltaY > 0 ? -0.05 : 0.05
  const newZoom = Math.max(0.3, Math.min(2, zoom.value + delta))
  zoom.value = newZoom
}

function zoomIn() {
  zoom.value = Math.min(2, zoom.value + 0.1)
}

function zoomOut() {
  zoom.value = Math.max(0.3, zoom.value - 0.1)
}

function fitView() {
  zoom.value = 1
  pan.x = 50
  pan.y = 30
}

const nodeTemplates = [
  { label: 'Data Source', type: 'source', description: 'Load raw data', emoji: '\u{1F4E5}', color: '#3b82f6', hasInput: false, hasOutput: true },
  { label: 'Transform', type: 'transform', description: 'Transform data', emoji: '\u2699\uFE0F', color: '#8b5cf6', hasInput: true, hasOutput: true },
  { label: 'Model', type: 'model', description: 'ML model', emoji: '\u{1F9E0}', color: '#f59e0b', hasInput: true, hasOutput: true },
  { label: 'Evaluation', type: 'evaluation', description: 'Evaluate results', emoji: '\u{1F4CA}', color: '#ef4444', hasInput: true, hasOutput: true },
  { label: 'Export', type: 'export', description: 'Export data', emoji: '\u{1F4E4}', color: '#06b6d4', hasInput: true, hasOutput: false },
]

function addNode() {
  const template = nodeTemplates[Math.floor(Math.random() * nodeTemplates.length)]
  const id = nodeIdCounter++
  nodes.push({
    id,
    ...template,
    label: `${template.label} ${id}`,
    x: (-pan.x / zoom.value) + 200 + Math.random() * 200,
    y: (-pan.y / zoom.value) + 150 + Math.random() * 150,
    width: 180,
    height: 68,
  })
  selectedNode.value = id
}

function duplicateNode(node) {
  const id = nodeIdCounter++
  nodes.push({
    ...node,
    id,
    label: `${node.label} (copy)`,
    x: node.x + 30,
    y: node.y + 30,
  })
  selectedNode.value = id
}

function deleteNode(nodeId) {
  const idx = nodes.findIndex(n => n.id === nodeId)
  if (idx !== -1) nodes.splice(idx, 1)
  // Remove connected edges
  for (let i = edges.length - 1; i >= 0; i--) {
    if (edges[i].from === nodeId || edges[i].to === nodeId) {
      edges.splice(i, 1)
    }
  }
  selectedNode.value = null
}

function updateViewportSize() {
  if (canvasContainer.value) {
    viewportSize.w = canvasContainer.value.clientWidth
    viewportSize.h = canvasContainer.value.clientHeight
  }
}

onMounted(() => {
  updateViewportSize()
  window.addEventListener('resize', updateViewportSize)
  // Center the initial view
  fitView()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateViewportSize)
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
