<template>
  <div class="h-[calc(100vh-57px)] flex overflow-hidden bg-[#f7f8fa]">
    <!-- Main Canvas Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Toolbar -->
      <div class="flex items-center justify-between px-4 py-2.5 bg-white border-b border-gray-200 flex-shrink-0">
      <div class="flex items-center gap-2">
        <button
          v-for="btn in toolbarButtons"
          :key="btn.id"
          @click="onToolbarClick(btn.id)"
          class="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-colors border"
          :class="btn.id === 'execute'
            ? 'bg-[#10b981] text-white border-[#10b981] hover:bg-[#059669] shadow-sm'
            : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50 hover:border-gray-300'"
        >
          <span v-if="btn.icon" class="text-base" v-html="btn.icon" />
          <span>{{ btn.label }}</span>
        </button>
        <!-- Agent 编排按钮 - 仅在侧边栏关闭时显示 -->
        <button
          v-if="!agentSidebarExpanded"
          @click="agentSidebarExpanded = true"
          class="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-colors border bg-gradient-to-r from-blue-500 to-indigo-600 text-white border-transparent hover:from-blue-600 hover:to-indigo-700 shadow-sm"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
          </svg>
          <span>Agent 编排</span>
        </button>
      </div>
      <div class="flex items-center gap-1">
        <button
          title="移动画布"
          @click="activeTool = activeTool === 'pan' ? 'select' : 'pan'"
          class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
          :class="activeTool === 'pan' ? 'bg-gray-200 text-gray-800' : 'text-gray-500 hover:bg-gray-100'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
          </svg>
        </button>
        <button
          title="删除选中"
          @click="deleteSelectedNode"
          class="w-9 h-9 rounded-lg flex items-center justify-center text-gray-500 hover:bg-red-50 hover:text-red-500 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
          </svg>
        </button>
        <button
          title="全屏"
          @click="toggleFullscreen"
          class="w-9 h-9 rounded-lg flex items-center justify-center text-gray-500 hover:bg-gray-100 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Canvas Area -->
    <div class="flex-1 relative overflow-hidden" ref="canvasContainer"
      @mousedown="onCanvasMouseDown"
      @mousemove="onCanvasMouseMove"
      @mouseup="onCanvasMouseUp"
      @wheel.prevent="onWheel"
    >
      <!-- SVG layer for connections -->
      <svg class="absolute inset-0 w-full h-full pointer-events-none" style="z-index: 1;">
        <defs>
          <marker id="arrow-orange" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#f97316" />
          </marker>
        </defs>
        <g :transform="`translate(${pan.x},${pan.y}) scale(${zoom})`">
          <!-- Connection lines -->
          <path
            v-for="edge in edges"
            :key="edge.id"
            :d="getEdgePath(edge)"
            fill="none"
            stroke="#f97316"
            stroke-width="2.5"
            stroke-dasharray="8 6"
            stroke-linecap="round"
            opacity="0.85"
          />
          <!-- Dragging edge preview -->
          <path
            v-if="draggingEdge"
            :d="getDraggingEdgePath()"
            fill="none"
            stroke="#f97316"
            stroke-width="2"
            stroke-dasharray="6 4"
            opacity="0.5"
          />
        </g>
      </svg>

      <!-- Nodes layer -->
      <div class="absolute inset-0" style="z-index: 2;"
        :style="{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`, transformOrigin: '0 0' }"
      >
        <div
          v-for="node in nodes"
          :key="node.id"
          class="absolute node-card"
          :style="{
            left: node.x + 'px',
            top: node.y + 'px',
            width: node.width + 'px',
          }"
          @mousedown.stop="onNodeMouseDown($event, node)"
        >
          <!-- Node Card -->
          <div
            class="bg-white rounded-xl shadow-sm border-2 transition-all duration-150 overflow-hidden"
            :class="selectedNode === node.id ? 'border-blue-400 shadow-md' : 'border-gray-200 hover:shadow-md'"
          >
            <!-- Node Header -->
            <div class="px-4 pt-3 pb-2 flex items-start gap-2.5">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                :style="{ backgroundColor: node.color + '15' }">
                <svg v-if="node.headerIcon === 'doc'" class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <svg v-else-if="node.headerIcon === 'filter'" class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
                </svg>
                <svg v-else-if="node.headerIcon === 'eval'" class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
                </svg>
                <svg v-else-if="node.headerIcon === 'generate'" class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                </svg>
                <svg v-else-if="node.headerIcon === 'expert'" class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                </svg>
                <svg v-else class="w-4 h-4" :style="{ color: node.color }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                </svg>
              </div>
              <div class="min-w-0 flex-1">
                <div class="text-sm font-semibold text-gray-900 leading-tight">{{ node.label }}</div>
                <div class="text-xs mt-0.5" :style="{ color: node.color }">{{ node.subtitle }}</div>
              </div>
              <!-- Delete button -->
              <button
                v-if="selectedNode === node.id"
                @click.stop="deleteNode(node.id)"
                class="w-5 h-5 rounded-full bg-red-500 text-white flex items-center justify-center text-xs hover:bg-red-600 flex-shrink-0"
              >×</button>
            </div>

            <!-- Node Content Sections -->
            <div class="px-4 pb-3">
              <!-- Init params section -->
              <div v-if="node.initParams && node.initParams.length" class="mb-2">
                <div class="text-xs font-semibold text-green-600 mb-1.5">初始化参数</div>
                <div v-for="param in node.initParams" :key="param.key" class="mb-1.5">
                  <div class="flex items-center gap-1">
                    <span class="w-2 h-2 rounded-full flex-shrink-0" :style="{ backgroundColor: param.portColor || '#10b981' }" />
                    <span class="text-xs text-gray-500">{{ param.key }}</span>
                  </div>
                  <div class="ml-3 mt-0.5">
                    <div v-if="param.type === 'select'" class="text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1 flex items-center justify-between">
                      <span class="text-gray-800">{{ param.value }}</span>
                      <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" /></svg>
                    </div>
                    <div v-else-if="param.type === 'textarea'" class="text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1.5 text-gray-800 min-h-[40px] whitespace-pre-wrap break-words">{{ param.value }}</div>
                    <div v-else class="text-xs text-gray-800 pl-0.5">{{ param.value }}</div>
                  </div>
                </div>
              </div>

              <!-- Runtime params section -->
              <div v-if="node.runtimeParams && node.runtimeParams.length">
                <div class="text-xs font-semibold text-blue-600 mb-1.5">运行参数</div>
                <div v-for="param in node.runtimeParams" :key="param.key" class="mb-1.5">
                  <div class="flex items-center gap-1">
                    <span class="w-2 h-2 rounded-full flex-shrink-0" :style="{ backgroundColor: param.portColor || '#3b82f6' }" />
                    <span class="text-xs text-gray-500">{{ param.key }}</span>
                  </div>
                  <div class="ml-3 mt-0.5">
                    <div v-if="param.type === 'select'" class="text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1 flex items-center justify-between">
                      <span class="text-gray-800">{{ param.value }}</span>
                      <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" /></svg>
                    </div>
                    <div v-else class="text-xs text-gray-800 pl-0.5">{{ param.value }}</div>
                  </div>
                </div>
              </div>

              <!-- Config section (for MineruParser style) -->
              <div v-if="node.configSection">
                <div class="text-xs font-semibold mb-1.5" :style="{ color: node.color }">{{ node.configSection.title }}</div>
                <div v-for="param in node.configSection.params" :key="param.key" class="mb-1.5">
                  <div class="text-xs text-gray-500">{{ param.key }}</div>
                  <div class="mt-0.5">
                    <div v-if="param.type === 'select'" class="text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1 flex items-center justify-between">
                      <span class="text-gray-800">{{ param.value }}</span>
                      <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" /></svg>
                    </div>
                    <div v-else class="text-xs text-gray-800 pl-0.5">{{ param.value }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Input ports (left side) -->
            <div v-if="node.inputPorts && node.inputPorts.length" class="absolute left-0 top-0 h-full flex flex-col justify-evenly pointer-events-none" style="transform: translateX(-50%);">
              <div
                v-for="(port, idx) in node.inputPorts"
                :key="'in-' + idx"
                class="w-3 h-3 rounded-full border-2 border-white shadow-sm pointer-events-auto cursor-crosshair"
                :style="{ backgroundColor: port.color || '#3b82f6' }"
                :title="port.label"
              />
            </div>

            <!-- Output ports (right side) -->
            <div v-if="node.outputPorts && node.outputPorts.length" class="absolute right-0 top-0 h-full flex flex-col justify-evenly pointer-events-none" style="transform: translateX(50%);">
              <div
                v-for="(port, idx) in node.outputPorts"
                :key="'out-' + idx"
                class="w-3 h-3 rounded-full border-2 border-white shadow-sm pointer-events-auto cursor-crosshair"
                :style="{ backgroundColor: port.color || '#f97316' }"
                :title="port.label"
                @mousedown.stop="onPortMouseDown($event, node, idx)"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Zoom indicator -->
      <div class="absolute bottom-4 left-4 bg-white rounded-lg shadow-sm border border-gray-200 px-3 py-1.5 flex items-center gap-2 z-10">
        <button @click="zoomOut" class="text-gray-500 hover:text-gray-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M18 12H6" /></svg>
        </button>
        <span class="text-xs text-gray-600 w-10 text-center font-medium">{{ Math.round(zoom * 100) }}%</span>
        <button @click="zoomIn" class="text-gray-500 hover:text-gray-700 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" /></svg>
        </button>
      </div>
    </div>
    </div>

    <!-- Agent Dialog Sidebar -->
    <AgentDialogSidebar
      v-if="agentSidebarExpanded"
      @close="agentSidebarExpanded = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import AgentDialogSidebar from '../components/dataflow/AgentDialogSidebar.vue'

const canvasContainer = ref(null)
const activeTool = ref('select')
const selectedNode = ref(null)
const zoom = ref(0.85)
const pan = reactive({ x: 50, y: 30 })
const viewportSize = reactive({ w: 1200, h: 700 })
const agentSidebarExpanded = ref(true)

const toolbarButtons = [
  { id: 'compute', label: '算力配置', icon: '⚡' },
  { id: 'dataset', label: '数据集', icon: '🗃️' },
  { id: 'operators', label: '算子库', icon: '≡' },
  { id: 'pipeline-lib', label: 'Pipeline库', icon: '🔗' },
  { id: 'save', label: '保存Pipeline', icon: '💾' },
  { id: 'execute', label: '▶ 执行任务', icon: '' },
]

let nodeIdCounter = 10

const nodes = reactive([
  {
    id: 1,
    label: 'MineruParser',
    subtitle: 'parser',
    headerIcon: 'doc',
    color: '#6366f1',
    x: 40,
    y: 80,
    width: 260,
    nodeHeight: 260,
    configSection: {
      title: 'MinerU 配置',
      params: [
        { key: 'dataset_id', value: '02960634-2099-4580-9779-4a2...', type: 'text' },
      ]
    },
    runtimeParams: [
      { key: 'Output Key', value: 'raw_content', type: 'text', portColor: '#3b82f6' },
      { key: '切片模式', value: '按全文切分', type: 'select', portColor: '#3b82f6' },
    ],
    inputPorts: [],
    outputPorts: [
      { color: '#f97316', label: 'raw_content' },
    ],
  },
  {
    id: 2,
    label: 'MinHashTextFilter',
    subtitle: 'external',
    headerIcon: 'filter',
    color: '#10b981',
    x: 360,
    y: 180,
    width: 240,
    nodeHeight: 320,
    initParams: [
      { key: 'Num perm', value: '128', type: 'text', portColor: '#10b981' },
      { key: 'Threshold', value: '0.7', type: 'text', portColor: '#10b981' },
    ],
    runtimeParams: [
      { key: 'Input key', value: 'raw_content', type: 'text', portColor: '#3b82f6' },
      { key: 'Output key', value: 'deduplicated_chunk', type: 'text', portColor: '#3b82f6' },
    ],
    inputPorts: [
      { color: '#3b82f6', label: 'raw_content' },
    ],
    outputPorts: [
      { color: '#f97316', label: 'deduplicated_chunk' },
    ],
  },
  {
    id: 3,
    label: 'PromptedEvaluator',
    subtitle: 'eval',
    headerIcon: 'eval',
    color: '#8b5cf6',
    x: 600,
    y: 30,
    width: 260,
    nodeHeight: 350,
    initParams: [
      { key: 'Use llm', value: '是', type: 'select', portColor: '#10b981' },
      { key: 'System prompt', value: 'Please evaluate the quality of this data on a scale from 1 to 5.', type: 'textarea', portColor: '#10b981' },
      { key: 'User model name', value: 'Qwen3-30B-A3B-Instru...', type: 'select', portColor: '#10b981' },
    ],
    runtimeParams: [
      { key: 'Input key', value: 'deduplicated_chunk', type: 'text', portColor: '#3b82f6' },
      { key: 'Output key', value: 'eval', type: 'text', portColor: '#3b82f6' },
    ],
    inputPorts: [
      { color: '#3b82f6', label: 'deduplicated_chunk' },
    ],
    outputPorts: [
      { color: '#f97316', label: 'eval' },
    ],
  },
  {
    id: 4,
    label: 'Text2QAGenerator',
    subtitle: 'generate',
    headerIcon: 'generate',
    color: '#f59e0b',
    x: 680,
    y: 420,
    width: 260,
    nodeHeight: 460,
    initParams: [
      { key: 'Use llm', value: '是', type: 'select', portColor: '#10b981' },
      { key: 'User model name', value: 'Qwen3-30B-A3B-Instr...', type: 'select', portColor: '#10b981' },
    ],
    runtimeParams: [
      { key: 'Input key', value: 'deduplicated_chunk', type: 'text', portColor: '#3b82f6' },
      { key: 'Output answer key', value: 'generated_answer', type: 'text', portColor: '#3b82f6' },
      { key: 'Output prompt key', value: 'generated_prompt', type: 'text', portColor: '#3b82f6' },
      { key: 'Input question num', value: '1', type: 'text', portColor: '#3b82f6' },
      { key: 'Output question key', value: 'generated_question', type: 'text', portColor: '#3b82f6' },
    ],
    inputPorts: [
      { color: '#3b82f6', label: 'deduplicated_chunk' },
    ],
    outputPorts: [
      { color: '#f97316', label: 'generated_answer' },
      { color: '#f97316', label: 'generated_prompt' },
      { color: '#f97316', label: 'generated_question' },
    ],
  },
  {
    id: 5,
    label: 'QAPairSampleEvaluator',
    subtitle: 'external',
    headerIcon: 'eval',
    color: '#ef4444',
    x: 1020,
    y: 160,
    width: 280,
    nodeHeight: 600,
    initParams: [
      { key: 'Use llm', value: '是', type: 'select', portColor: '#10b981' },
      { key: 'User model name', value: 'Qwen3-30B-A3B-Instruct-25...', type: 'select', portColor: '#10b981' },
    ],
    runtimeParams: [
      { key: 'Input qa key', value: 'generated_answer', type: 'text', portColor: '#3b82f6' },
      { key: 'Output question quality key', value: 'question_quality_grades', type: 'text', portColor: '#3b82f6' },
      { key: 'Output question quality feedback key', value: 'question_quality_feedbacks', type: 'text', portColor: '#3b82f6' },
      { key: 'Output answer alignment key', value: 'answer_alignment_grades', type: 'text', portColor: '#3b82f6' },
      { key: 'Output answer alignment feedback key', value: 'answer_alignment_feedbacks', type: 'text', portColor: '#3b82f6' },
      { key: 'Output answer verifiability key', value: 'answer_verifiability_grades', type: 'text', portColor: '#3b82f6' },
      { key: 'Output answer verifiability feedback key', value: 'answer_verifiability_feedbacks', type: 'text', portColor: '#3b82f6' },
      { key: 'Output downstream value key', value: 'downstream_value_grades', type: 'text', portColor: '#3b82f6' },
      { key: 'Output downstream value feedback key', value: 'downstream_value_feedbacks', type: 'text', portColor: '#3b82f6' },
    ],
    inputPorts: [
      { color: '#3b82f6', label: 'generated_answer' },
    ],
    outputPorts: [
      { color: '#f97316', label: 'question_quality_grades' },
      { color: '#f97316', label: 'answer_alignment_grades' },
      { color: '#f97316', label: 'answer_verifiability_grades' },
      { color: '#f97316', label: 'downstream_value_grades' },
    ],
  },
  {
    id: 6,
    label: 'UniMiner',
    subtitle: 'expert',
    headerIcon: 'expert',
    color: '#ec4899',
    x: 1360,
    y: 200,
    width: 280,
    nodeHeight: 380,
    initParams: [
      { key: 'Annotation type', value: 'Quality Assessment', type: 'select', portColor: '#10b981' },
      { key: 'Expert level', value: 'Senior', type: 'select', portColor: '#10b981' },
      { key: 'Review mode', value: 'Multi-pass', type: 'select', portColor: '#10b981' },
    ],
    runtimeParams: [
      { key: 'Input key', value: 'downstream_value_grades', type: 'text', portColor: '#3b82f6' },
      { key: 'Output annotation key', value: 'expert_annotation', type: 'text', portColor: '#3b82f6' },
      { key: 'Output confidence key', value: 'annotation_confidence', type: 'text', portColor: '#3b82f6' },
      { key: 'Output feedback key', value: 'expert_feedback', type: 'text', portColor: '#3b82f6' },
    ],
    inputPorts: [
      { color: '#3b82f6', label: 'downstream_value_grades' },
    ],
    outputPorts: [
      { color: '#f97316', label: 'expert_annotation' },
      { color: '#f97316', label: 'annotation_confidence' },
      { color: '#f97316', label: 'expert_feedback' },
    ],
  },
])

const edges = reactive([
  { id: 'e1-2', from: 1, to: 2, fromPort: 0, toPort: 0 },
  { id: 'e2-3', from: 2, to: 3, fromPort: 0, toPort: 0 },
  { id: 'e2-4', from: 2, to: 4, fromPort: 0, toPort: 0 },
  { id: 'e4-5', from: 4, to: 5, fromPort: 0, toPort: 0 },
  { id: 'e5-6', from: 5, to: 6, fromPort: 3, toPort: 0 },
])

// Dragging state
const dragging = reactive({ active: false, nodeId: null, offsetX: 0, offsetY: 0 })
const panning = reactive({ active: false, startX: 0, startY: 0, startPanX: 0, startPanY: 0 })
const draggingEdge = ref(null)

const minimapBounds = computed(() => {
  if (!nodes.length) return { minX: 0, minY: 0, width: 800, height: 400 }
  const minX = Math.min(...nodes.map(n => n.x))
  const minY = Math.min(...nodes.map(n => n.y))
  const maxX = Math.max(...nodes.map(n => n.x + n.width))
  const maxY = Math.max(...nodes.map(n => n.y + (n.nodeHeight || 200)))
  return { minX, minY, width: maxX - minX, height: maxY - minY }
})

const minimapViewBox = computed(() => {
  const b = minimapBounds.value
  const padding = 60
  return `${b.minX - padding} ${b.minY - padding} ${b.width + padding * 2} ${b.height + padding * 2}`
})

function getNodeCenter(nodeId) {
  const node = nodes.find(n => n.id === nodeId)
  if (!node) return { x: 0, y: 0 }
  return { x: node.x + node.width / 2, y: node.y + (node.nodeHeight || 200) / 2 }
}

function getPortPosition(node, side, portIndex) {
  const ports = side === 'output' ? node.outputPorts : node.inputPorts
  if (!ports || !ports.length) return { x: 0, y: 0 }
  const nodeH = node.nodeHeight || 200
  const spacing = nodeH / (ports.length + 1)
  const y = node.y + spacing * (portIndex + 1)
  const x = side === 'output' ? node.x + node.width : node.x
  return { x, y }
}

function getEdgePath(edge) {
  const fromNode = nodes.find(n => n.id === edge.from)
  const toNode = nodes.find(n => n.id === edge.to)
  if (!fromNode || !toNode) return ''

  const fromPos = getPortPosition(fromNode, 'output', edge.fromPort || 0)
  const toPos = getPortPosition(toNode, 'input', edge.toPort || 0)

  const dx = Math.abs(toPos.x - fromPos.x) * 0.5
  return `M ${fromPos.x} ${fromPos.y} C ${fromPos.x + dx} ${fromPos.y}, ${toPos.x - dx} ${toPos.y}, ${toPos.x} ${toPos.y}`
}

function getDraggingEdgePath() {
  if (!draggingEdge.value) return ''
  const { x1, y1, x2, y2 } = draggingEdge.value
  const dx = Math.abs(x2 - x1) * 0.5
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
}

function getCanvasPoint(event) {
  const rect = canvasContainer.value.getBoundingClientRect()
  return {
    x: (event.clientX - rect.left - pan.x) / zoom.value,
    y: (event.clientY - rect.top - pan.y) / zoom.value,
  }
}

function onNodeMouseDown(event, node) {
  selectedNode.value = node.id
  dragging.active = true
  dragging.nodeId = node.id
  const pt = getCanvasPoint(event)
  dragging.offsetX = pt.x - node.x
  dragging.offsetY = pt.y - node.y
}

function onPortMouseDown(event, node, portIndex) {
  const pos = getPortPosition(node, 'output', portIndex)
  draggingEdge.value = { fromId: node.id, fromPort: portIndex, x1: pos.x, y1: pos.y, x2: pos.x, y2: pos.y }
}

function onCanvasMouseDown(event) {
  if (event.target === canvasContainer.value || event.target.closest('.node-card') === null) {
    selectedNode.value = null
    panning.active = true
    panning.startX = event.clientX
    panning.startY = event.clientY
    panning.startPanX = pan.x
    panning.startPanY = pan.y
  }
}

function onCanvasMouseMove(event) {
  if (dragging.active) {
    const pt = getCanvasPoint(event)
    const node = nodes.find(n => n.id === dragging.nodeId)
    if (node) {
      node.x = pt.x - dragging.offsetX
      node.y = pt.y - dragging.offsetY
    }
  } else if (panning.active) {
    pan.x = panning.startPanX + (event.clientX - panning.startX)
    pan.y = panning.startPanY + (event.clientY - panning.startY)
  } else if (draggingEdge.value) {
    const pt = getCanvasPoint(event)
    draggingEdge.value.x2 = pt.x
    draggingEdge.value.y2 = pt.y
  }
}

function onCanvasMouseUp(event) {
  if (draggingEdge.value) {
    const pt = getCanvasPoint(event)
    const targetNode = nodes.find(n =>
      n.inputPorts && n.inputPorts.length &&
      n.id !== draggingEdge.value.fromId &&
      pt.x >= n.x - 15 && pt.x <= n.x + 15 &&
      pt.y >= n.y && pt.y <= n.y + (n.nodeHeight || 200)
    )
    if (targetNode) {
      const exists = edges.some(e => e.from === draggingEdge.value.fromId && e.to === targetNode.id)
      if (!exists) {
        edges.push({
          id: `e${draggingEdge.value.fromId}-${targetNode.id}`,
          from: draggingEdge.value.fromId,
          to: targetNode.id,
          fromPort: draggingEdge.value.fromPort || 0,
          toPort: 0,
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
  zoom.value = Math.max(0.2, Math.min(2, zoom.value + delta))
}

function zoomIn() {
  zoom.value = Math.min(2, zoom.value + 0.1)
}

function zoomOut() {
  zoom.value = Math.max(0.2, zoom.value - 0.1)
}

function deleteNode(nodeId) {
  const idx = nodes.findIndex(n => n.id === nodeId)
  if (idx !== -1) nodes.splice(idx, 1)
  for (let i = edges.length - 1; i >= 0; i--) {
    if (edges[i].from === nodeId || edges[i].to === nodeId) {
      edges.splice(i, 1)
    }
  }
  selectedNode.value = null
}

function deleteSelectedNode() {
  if (selectedNode.value) {
    deleteNode(selectedNode.value)
  }
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    canvasContainer.value?.parentElement?.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

function onToolbarClick(id) {
  if (id === 'execute') {
    alert('Pipeline 执行任务已提交！')
  }
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
})

onUnmounted(() => {
  window.removeEventListener('resize', updateViewportSize)
})
</script>

<style scoped>
.node-card {
  position: absolute;
  user-select: none;
}
</style>
