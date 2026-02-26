<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="close">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-6xl mx-4 h-[80vh] flex flex-col">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">{{ kb?.name }} - {{ $t('knowledgeBase.knowledgeGraph') }}</h2>
          <p class="text-sm text-gray-500 mt-1">
            {{ kb?.knowledgeGraph.entityCount }} entities · {{ kb?.knowledgeGraph.relationCount }} relations
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="resetCamera"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            {{ $t('common.reset') }}
          </button>
          <button @click="close" class="text-gray-400 hover:text-gray-600 p-1">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Graph Container -->
      <div class="flex-1 relative">
        <div ref="containerRef" class="w-full h-full"></div>

        <!-- Legend -->
        <div class="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4 border border-gray-200">
          <h4 class="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2">{{ $t('knowledgeBase.graphLegend') }}</h4>
          <div class="space-y-1.5">
            <div v-for="(color, type) in nodeColors" :key="type" class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full" :style="{ backgroundColor: color }"></span>
              <span class="text-xs text-gray-600">{{ type }}</span>
            </div>
          </div>
        </div>

        <!-- Selected Node Info -->
        <div v-if="selectedNode" class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4 border border-gray-200 max-w-xs">
          <h4 class="text-sm font-semibold text-gray-900 mb-2">{{ selectedNode.label }}</h4>
          <div class="space-y-1 text-xs text-gray-600">
            <p><span class="text-gray-400">Type:</span> {{ selectedNode.type }}</p>
            <p><span class="text-gray-400">ID:</span> {{ selectedNode.id }}</p>
            <p v-if="selectedNode.properties?.description"><span class="text-gray-400">Description:</span> {{ selectedNode.properties.description }}</p>
          </div>
          <button @click="selectedNode = null" class="mt-3 text-xs text-indigo-600 hover:text-indigo-700">{{ $t('common.close') }}</button>
        </div>
      </div>

      <!-- Footer with Controls -->
      <div class="px-6 py-3 border-t border-gray-200 bg-gray-50 rounded-b-xl">
        <div class="flex items-center justify-between text-sm text-gray-600">
          <div class="flex items-center gap-4">
            <span>{{ $t('knowledgeBase.graphControls.zoom') }}</span>
            <span class="text-gray-400">|</span>
            <span>{{ $t('knowledgeBase.graphControls.pan') }}</span>
            <span class="text-gray-400">|</span>
            <span>{{ $t('knowledgeBase.graphControls.click') }}</span>
          </div>
          <div class="text-xs text-gray-400">
            Powered by Sigma.js
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import Sigma from 'sigma'
import Graph from 'graphology'
import forceAtlas2 from 'graphology-layout-forceatlas2'

const props = defineProps({
  visible: { type: Boolean, default: false },
  kb: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const { t } = useI18n()
const containerRef = ref(null)
const selectedNode = ref(null)
let sigmaInstance = null
let graph = null

// Node colors by type
const nodeColors = {
  'Concept': '#6366f1',
  'Entity': '#10b981',
  'Relation': '#f59e0b',
  'Document': '#ef4444',
  'Keyword': '#8b5cf6',
  'Topic': '#ec4899'
}

// Generate sample graph data based on knowledge base
function generateGraphData(kb) {
  const g = new Graph()
  const entityCount = kb?.knowledgeGraph?.entityCount || 50
  const relationCount = kb?.knowledgeGraph?.relationCount || 80

  const types = Object.keys(nodeColors)
  const labels = {
    'Concept': ['Machine Learning', 'Deep Learning', 'Neural Network', 'Algorithm', 'Data Structure', 'Optimization', 'Regression', 'Classification', 'Clustering', 'Embedding'],
    'Entity': ['Model A', 'Dataset B', 'Framework C', 'Tool D', 'Library E', 'API F', 'Service G', 'Platform H'],
    'Relation': ['implements', 'extends', 'uses', 'requires', 'produces', 'consumes', 'references', 'contains'],
    'Document': ['Paper 1', 'Article 2', 'Report 3', 'Guide 4', 'Manual 5', 'Tutorial 6'],
    'Keyword': ['AI', 'ML', 'DL', 'NLP', 'CV', 'RL', 'GAN', 'Transformer'],
    'Topic': ['Research', 'Development', 'Production', 'Testing', 'Deployment', 'Monitoring']
  }

  // Add nodes
  const nodeCount = Math.min(entityCount, 80)
  for (let i = 0; i < nodeCount; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const typeLabels = labels[type]
    const label = typeLabels[Math.floor(Math.random() * typeLabels.length)] + (i > 0 ? ` ${i}` : '')

    g.addNode(`node-${i}`, {
      label: label,
      nodeType: type,
      size: 6 + Math.random() * 8,
      color: nodeColors[type],
      x: Math.random() * 100 - 50,
      y: Math.random() * 100 - 50,
      properties: {
        description: `This is a ${type.toLowerCase()} node in the knowledge graph.`
      }
    })
  }

  // Add edges
  const edgeCount = Math.min(relationCount, nodeCount * 1.5)
  for (let i = 0; i < edgeCount; i++) {
    const source = `node-${Math.floor(Math.random() * nodeCount)}`
    const target = `node-${Math.floor(Math.random() * nodeCount)}`

    if (source !== target && !g.hasEdge(source, target)) {
      g.addEdge(source, target, {
        label: labels['Relation'][Math.floor(Math.random() * labels['Relation'].length)],
        size: 1 + Math.random(),
        color: '#94a3b8'
      })
    }
  }

  return g
}

function initSigma() {
  if (!containerRef.value || !props.kb) return

  // Clean up existing instance
  if (sigmaInstance) {
    sigmaInstance.kill()
    sigmaInstance = null
  }

  // Generate graph
  graph = generateGraphData(props.kb)

  // Apply force atlas layout
  const settings = {
    iterations: 150,
    settings: {
      gravity: 0.5,
      scalingRatio: 3,
      strongGravityMode: false,
      slowDown: 3
    }
  }
  forceAtlas2.assign(graph, settings)

  // Create sigma instance with standard settings
  sigmaInstance = new Sigma(graph, containerRef.value, {
    renderLabels: true,
    labelSize: 11,
    labelWeight: '500',
    labelColor: { color: '#374151' },
    defaultNodeColor: '#6366f1',
    defaultEdgeColor: '#94a3b8',
    edgeColor: 'color',
    minCameraRatio: 0.05,
    maxCameraRatio: 20,
    allowInvalidContainer: true,
    enableNodeClickEvents: true,
    enableNodeHoverEvents: true,
    enableEdgeClickEvents: false,
    enableEdgeHoverEvents: false
  })

  // Handle node click
  sigmaInstance.on('clickNode', ({ node }) => {
    const attrs = graph.getNodeAttributes(node)
    selectedNode.value = {
      id: node,
      label: attrs.label,
      type: attrs.nodeType,
      properties: attrs.properties
    }
  })

  // Handle stage click (deselect)
  sigmaInstance.on('clickStage', () => {
    selectedNode.value = null
  })
}

function resetCamera() {
  if (sigmaInstance) {
    sigmaInstance.getCamera().animatedReset({ duration: 500 })
  }
}

function close() {
  selectedNode.value = null
  emit('close')
}

// Watch for visibility changes
watch(() => props.visible, async (newVisible) => {
  if (newVisible) {
    await nextTick()
    // Small delay to ensure container is rendered
    setTimeout(() => {
      initSigma()
    }, 100)
  } else {
    if (sigmaInstance) {
      sigmaInstance.kill()
      sigmaInstance = null
    }
  }
})

// Watch for knowledge base changes
watch(() => props.kb, async (newKb) => {
  if (newKb && props.visible) {
    await nextTick()
    initSigma()
  }
}, { deep: true })

onUnmounted(() => {
  if (sigmaInstance) {
    sigmaInstance.kill()
    sigmaInstance = null
  }
})
</script>

<style scoped>
:deep(.sigma-mouse) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

:deep(.sigma-labels) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

:deep(.sigma-label) {
  position: absolute;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
  pointer-events: none;
  transform: translate(-50%, -50%);
}

:deep(.sigma-hovers) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
