<template>
  <div class="min-h-screen bg-slate-50/50">
    <!-- Hero Section -->
    <div class="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-dc-primary/20">
      <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%23ffffff%22%20fill-opacity%3D%220.03%22%3E%3Cpath%20d%3D%22M36%2034v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6%2034v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6%204V0H4v4H0v2h4v4h2V6h4V4H6z%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')] opacity-20"></div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div class="text-center">
          <!-- MCP Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 mb-6">
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            <span class="text-sm font-medium text-white/90">Model Context Protocol</span>
          </div>
          
          <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 tracking-tight">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-white via-white to-white/70">
              让 AI 智能体
            </span>
            <br />
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-dc-primary to-dc-accent">
              安全访问您的数据
            </span>
          </h1>
          
          <p class="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-10 leading-relaxed">
            通过 MCP (Model Context Protocol) 协议，AI 助手可以标准化地访问 Dataset 和 Knowledge Base，
            实现智能化的数据查询、分析和知识管理。
          </p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button 
              @click="scrollToTools"
              class="inline-flex items-center gap-2 px-6 py-3 bg-dc-primary text-white rounded-xl font-medium hover:bg-dc-primary-dark transition-all duration-200 shadow-lg shadow-dc-primary/25"
            >
              <BoltIcon class="w-5 h-5" />
              探索 MCP 工具
            </button>
            <button 
              @click="showConfigModal = true"
              class="inline-flex items-center gap-2 px-6 py-3 bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-xl font-medium hover:bg-white/20 transition-all duration-200"
            >
              <Cog6ToothIcon class="w-5 h-5" />
              配置连接
            </button>
          </div>
        </div>
        
        <!-- Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 max-w-4xl mx-auto">
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-3xl font-bold text-white mb-1">17</div>
            <div class="text-sm text-slate-400">可用工具</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-3xl font-bold text-white mb-1">2</div>
            <div class="text-sm text-slate-400">数据源类型</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-3xl font-bold text-white mb-1">2</div>
            <div class="text-sm text-slate-400">传输协议</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-3xl font-bold text-green-400 mb-1">Ready</div>
            <div class="text-sm text-slate-400">服务状态</div>
          </div>
        </div>
      </div>
    </div>

    <!-- What is MCP Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold text-slate-900 mb-4">什么是 MCP?</h2>
        <p class="text-lg text-slate-600 max-w-3xl mx-auto">
          Model Context Protocol (模型上下文协议) 是 Anthropic 提出的开放协议，
          用于标准化 AI 模型与外部数据源和工具之间的通信。
        </p>
      </div>
      
      <div class="grid md:grid-cols-3 gap-8">
        <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200/60 hover:shadow-lg hover:border-dc-primary/20 transition-all duration-300">
          <div class="w-14 h-14 bg-gradient-to-br from-dc-primary to-dc-primary-dark rounded-xl flex items-center justify-center mb-6">
            <ShieldCheckIcon class="w-7 h-7 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-slate-900 mb-3">安全可靠</h3>
          <p class="text-slate-600 leading-relaxed">
            MCP 提供标准化的安全机制，确保 AI 助手只能访问授权的数据，
            保护您的敏感信息。
          </p>
        </div>
        
        <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200/60 hover:shadow-lg hover:border-dc-primary/20 transition-all duration-300">
          <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-6">
            <PuzzlePieceIcon class="w-7 h-7 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-slate-900 mb-3">即插即用</h3>
          <p class="text-slate-600 leading-relaxed">
            一次配置，多处使用。支持 Claude、Cursor、ChatGPT 等主流 AI 助手，
            实现真正的跨平台兼容。
          </p>
        </div>
        
        <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200/60 hover:shadow-lg hover:border-dc-primary/20 transition-all duration-300">
          <div class="w-14 h-14 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center mb-6">
            <BoltIcon class="w-7 h-7 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-slate-900 mb-3">实时数据</h3>
          <p class="text-slate-600 leading-relaxed">
            AI 助手可以实时查询 Dataset 和 Knowledge Base，获取最新数据，
            不再受限于训练数据的时效性。
          </p>
        </div>
      </div>
    </div>

    <!-- Tools Section -->
    <div id="tools" class="bg-white py-20 border-t border-slate-200/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-slate-900 mb-4">MCP 工具库</h2>
          <p class="text-lg text-slate-600">为 AI 助手提供的标准化工具接口</p>
        </div>
        
        <!-- Tabs -->
        <div class="flex justify-center mb-10">
          <div class="inline-flex bg-slate-100 rounded-xl p-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                activeTab === tab.id
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              <span class="flex items-center gap-2">
                <component :is="tab.icon" class="w-4 h-4" />
                {{ tab.label }}
              </span>
            </button>
          </div>
        </div>
        
        <!-- Dataset Tools -->
        <div v-if="activeTab === 'dataset'" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="tool in datasetTools"
            :key="tool.name"
            class="group bg-slate-50 rounded-2xl p-6 border border-slate-200/60 hover:border-dc-primary/30 hover:bg-white hover:shadow-lg transition-all duration-300"
          >
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <component :is="tool.icon" class="w-5 h-5 text-white" />
              </div>
              <div class="flex-1 min-w-0 overflow-hidden">
                <h4 class="font-semibold text-slate-900 mb-1 break-all">{{ tool.name }}</h4>
                <p class="text-sm text-slate-600 mb-3">{{ tool.description }}</p>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="param in tool.params"
                    :key="param"
                    class="px-2 py-1 bg-slate-200 text-slate-600 rounded text-xs font-mono"
                  >
                    {{ param }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Knowledge Base Tools -->
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="tool in knowledgeBaseTools"
            :key="tool.name"
            class="group bg-slate-50 rounded-2xl p-6 border border-slate-200/60 hover:border-purple-500/30 hover:bg-white hover:shadow-lg transition-all duration-300"
          >
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <component :is="tool.icon" class="w-5 h-5 text-white" />
              </div>
              <div class="flex-1 min-w-0 overflow-hidden">
                <h4 class="font-semibold text-slate-900 mb-1 break-all">{{ tool.name }}</h4>
                <p class="text-sm text-slate-600 mb-3">{{ tool.description }}</p>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="param in tool.params"
                    :key="param"
                    class="px-2 py-1 bg-slate-200 text-slate-600 rounded text-xs font-mono"
                  >
                    {{ param }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Architecture Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-slate-900 mb-4">系统架构</h2>
        <p class="text-lg text-slate-600">MCP 服务与后端的无缝集成</p>
      </div>
      
      <div class="bg-white rounded-3xl p-8 shadow-lg border border-slate-200/60">
        <div class="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-6">
          <!-- AI Assistant -->
          <div class="text-center flex-shrink-0">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl flex items-center justify-center mb-4 shadow-xl">
              <SparklesIcon class="w-10 h-10 text-white" />
            </div>
            <h4 class="font-semibold text-slate-900 mb-1">AI 助手</h4>
            <p class="text-sm text-slate-500">Claude / Cursor / ChatGPT</p>
          </div>

          <!-- Arrow -->
          <div class="hidden md:flex items-center justify-center flex-shrink-0">
            <div class="flex items-center gap-2 text-slate-400">
              <div class="h-0.5 w-12 bg-gradient-to-r from-slate-300 to-dc-primary"></div>
              <ArrowRightIcon class="w-5 h-5 text-dc-primary" />
            </div>
          </div>

          <!-- MCP Server -->
          <div class="text-center flex-shrink-0">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-dc-primary to-dc-primary-dark rounded-2xl flex items-center justify-center mb-4 shadow-xl shadow-dc-primary/25">
              <ServerIcon class="w-10 h-10 text-white" />
            </div>
            <h4 class="font-semibold text-slate-900 mb-1">MCP 服务器</h4>
            <p class="text-sm text-slate-500">SSE / STDIO 双模式</p>
          </div>

          <!-- Arrow -->
          <div class="hidden md:flex items-center justify-center flex-shrink-0">
            <div class="flex items-center gap-2 text-slate-400">
              <div class="h-0.5 w-12 bg-gradient-to-r from-dc-primary to-purple-500"></div>
              <ArrowRightIcon class="w-5 h-5 text-purple-500" />
            </div>
          </div>

          <!-- Backend -->
          <div class="text-center flex-shrink-0">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-4 shadow-xl">
              <CircleStackIcon class="w-10 h-10 text-white" />
            </div>
            <h4 class="font-semibold text-slate-900 mb-1">后端 API</h4>
            <p class="text-sm text-slate-500">Dataset / Knowledge Base</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Start Section -->
    <div class="bg-gradient-to-br from-slate-900 to-slate-800 py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-white mb-4">快速开始</h2>
          <p class="text-lg text-slate-300">三步即可让 AI 助手连接您的数据</p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8 items-stretch">
          <div class="relative h-full">
            <div class="absolute -top-4 -left-4 w-12 h-12 bg-dc-primary rounded-full flex items-center justify-center text-white font-bold text-xl z-10">1</div>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 h-full flex flex-col">
              <div class="h-10 mb-4 flex items-center">
                <TerminalIcon class="w-10 h-10 text-dc-primary" />
              </div>
              <h3 class="text-xl font-semibold text-white mb-3">启动 MCP 服务</h3>
              <p class="text-slate-300 mb-6 flex-grow">运行 MCP 服务器，支持 SSE 或 STDIO 传输模式</p>
              <div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-green-400 overflow-x-auto">
                python server.py --port 8080
              </div>
            </div>
          </div>

          <div class="relative h-full">
            <div class="absolute -top-4 -left-4 w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl z-10">2</div>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 h-full flex flex-col">
              <div class="h-10 mb-4 flex items-center">
                <Cog6ToothIcon class="w-10 h-10 text-purple-400" />
              </div>
              <h3 class="text-xl font-semibold text-white mb-3">配置 AI 助手</h3>
              <p class="text-slate-300 mb-6 flex-grow">在 Claude Desktop 或 Cursor 中添加 MCP 配置</p>
              <div class="bg-slate-900 rounded-lg p-4">
                <button
                  @click="showConfigModal = true"
                  class="text-purple-400 hover:text-purple-300 font-medium inline-flex items-center gap-1"
                >
                  查看配置示例
                  <ArrowRightIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <div class="relative h-full">
            <div class="absolute -top-4 -left-4 w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-xl z-10">3</div>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10 h-full flex flex-col">
              <div class="h-10 mb-4 flex items-center">
                <ChatBubbleLeftRightIcon class="w-10 h-10 text-green-400" />
              </div>
              <h3 class="text-xl font-semibold text-white mb-3">开始对话</h3>
              <p class="text-slate-300 mb-6 flex-grow">向 AI 助手提问，自动调用 MCP 工具获取数据</p>
              <div class="bg-slate-900 rounded-lg p-4 text-sm text-slate-400 italic">
                "帮我找一下生物学领域的数据集"
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Config Modal -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="showConfigModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showConfigModal = false"></div>
        
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-200/60 flex items-center justify-between bg-slate-50">
            <h3 class="text-lg font-semibold text-slate-900">MCP 配置示例</h3>
            <button @click="showConfigModal = false" class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-200 rounded-lg transition-colors">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <div class="p-6">
            <div class="mb-6">
              <label class="block text-sm font-medium text-slate-700 mb-2">选择您的 AI 助手</label>
              <div class="flex gap-3">
                <button
                  v-for="client in clients"
                  :key="client.id"
                  @click="selectedClient = client.id"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                    selectedClient === client.id
                      ? 'bg-dc-primary text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  ]"
                >
                  {{ client.name }}
                </button>
              </div>
            </div>
            
            <div class="bg-slate-900 rounded-xl p-4 overflow-x-auto">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs text-slate-400 uppercase tracking-wider">配置文件</span>
                <button 
                  @click="copyConfig"
                  class="text-xs text-dc-primary hover:text-dc-primary-dark flex items-center gap-1"
                >
                  <ClipboardIcon class="w-3 h-3" />
                  复制
                </button>
              </div>
              <pre class="text-sm text-green-400 font-mono"><code>{{ getConfigExample() }}</code></pre>
            </div>
            
            <div class="mt-4 text-sm text-slate-600">
              <p class="flex items-start gap-2">
                <InformationCircleIcon class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
                <span>配置文件位置：{{ getConfigPath() }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, h } from 'vue'

// Icons
const BoltIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
])

const Cog6ToothIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const ShieldCheckIcon = () => h('svg', { class: 'w-7 h-7', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
])

const PuzzlePieceIcon = () => h('svg', { class: 'w-7 h-7', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z' })
])

const SparklesIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z' })
])

const ServerIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01' })
])

const CircleStackIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' })
])

const ArrowRightIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 7l5 5m0 0l-5 5m5-5H6' })
])

const TerminalIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
])

const ChatBubbleLeftRightIcon = () => h('svg', { class: 'w-10 h-10', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' })
])

const XMarkIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M6 18L18 6M6 6l12 12' })
])

const ClipboardIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3' })
])

const InformationCircleIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const ListBulletIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 6h16M4 12h16M4 18h16' })
])

const DocumentIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
])

const MagnifyingGlassIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
])

const ChartBarIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const FireIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z' })
])

const TagIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z' })
])

const ArrowsRightLeftIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4' })
])

const BookOpenIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const CheckCircleIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const FolderOpenIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z' })
])

// State
const activeTab = ref('dataset')
const showConfigModal = ref(false)
const selectedClient = ref('claude')

const tabs = [
  { id: 'dataset', label: 'Dataset 工具', icon: CircleStackIcon },
  { id: 'knowledgebase', label: 'Knowledge Base 工具', icon: BookOpenIcon }
]

const clients = [
  { id: 'claude', name: 'Claude Desktop' },
  { id: 'cursor', name: 'Cursor' },
  { id: 'vscode', name: 'VSCode' }
]

const datasetTools = [
  { name: 'list_datasets', description: '获取数据集列表，支持分页和筛选', icon: ListBulletIcon, params: ['page', 'page_size', 'domain'] },
  { name: 'get_dataset_detail', description: '获取指定数据集的详细信息', icon: DocumentIcon, params: ['dataset_id'] },
  { name: 'search_datasets', description: '按关键词搜索数据集', icon: MagnifyingGlassIcon, params: ['keyword', 'page'] },
  { name: 'get_dataset_statistics', description: '获取数据集的统计信息', icon: ChartBarIcon, params: [] },
  { name: 'get_popular_datasets', description: '获取热门数据集排行', icon: FireIcon, params: ['limit'] },
  { name: 'get_datasets_by_domain', description: '按领域筛选数据集', icon: TagIcon, params: ['domain'] },
  { name: 'compare_datasets', description: '对比多个数据集', icon: ArrowsRightLeftIcon, params: ['dataset_ids'] }
]

const knowledgeBaseTools = [
  { name: 'list_knowledge_bases', description: '获取知识库列表，支持状态筛选', icon: ListBulletIcon, params: ['status', 'kb_type'] },
  { name: 'get_knowledge_base_detail', description: '获取知识库的详细信息', icon: DocumentIcon, params: ['kb_id'] },
  { name: 'search_knowledge_bases', description: '按关键词搜索知识库', icon: MagnifyingGlassIcon, params: ['keyword', 'status'] },
  { name: 'get_knowledge_base_statistics', description: '获取知识库的统计信息', icon: ChartBarIcon, params: [] },
  { name: 'get_knowledge_base_sources', description: '获取知识库的数据源', icon: FolderOpenIcon, params: ['kb_id'] },
  { name: 'get_ready_knowledge_bases', description: '获取就绪状态的知识库', icon: CheckCircleIcon, params: [] },
  { name: 'check_knowledge_base_status', description: '检查知识库处理状态', icon: InformationCircleIcon, params: ['kb_id'] },
  { name: 'compare_knowledge_bases', description: '对比多个知识库', icon: ArrowsRightLeftIcon, params: ['kb_ids'] },
  { name: 'find_knowledge_bases_by_source', description: '根据数据源查找知识库', icon: TagIcon, params: ['source_type', 'source_id'] },
  { name: 'get_knowledge_base_document_summary', description: '获取文档处理摘要', icon: DocumentIcon, params: ['kb_id'] }
]

// Methods
function scrollToTools() {
  document.getElementById('tools').scrollIntoView({ behavior: 'smooth' })
}

function getConfigExample() {
  const basePath = '/path/to/mcp-server'
  
  if (selectedClient.value === 'claude') {
    return JSON.stringify({
      "mcpServers": {
        "hf-frontend": {
          "command": "python",
          "args": ["server.py", "--transport", "stdio"],
          "cwd": basePath,
          "env": {
            "BACKEND_API_URL": "http://localhost:8000/api/v2"
          }
        }
      }
    }, null, 2)
  } else if (selectedClient.value === 'cursor') {
    return JSON.stringify({
      "mcpServers": {
        "hf-frontend": {
          "command": "python",
          "args": ["server.py", "--transport", "stdio"],
          "env": {
            "BACKEND_API_URL": "http://localhost:8000/api/v2"
          }
        }
      }
    }, null, 2)
  } else {
    return JSON.stringify({
      "servers": {
        "hf-frontend": {
          "type": "stdio",
          "command": "python",
          "args": ["server.py", "--transport", "stdio"],
          "env": {
            "BACKEND_API_URL": "http://localhost:8000/api/v2"
          }
        }
      }
    }, null, 2)
  }
}

function getConfigPath() {
  const paths = {
    claude: '~/Library/Application Support/Claude/claude_desktop_config.json (macOS)',
    cursor: '~/.cursor/mcp.json',
    vscode: '.vscode/mcp.json (项目目录)'
  }
  return paths[selectedClient.value]
}

function copyConfig() {
  navigator.clipboard.writeText(getConfigExample())
  alert('配置已复制到剪贴板')
}
</script>
