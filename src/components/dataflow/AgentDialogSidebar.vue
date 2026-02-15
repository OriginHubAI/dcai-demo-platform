<template>
  <div
    class="flex-shrink-0 w-[420px] bg-white border-l border-gray-200 transition-all duration-300 ease-in-out overflow-hidden flex flex-col relative z-50"
  >
    <!-- Close Button -->
    <button
      @click="$emit('close')"
      class="absolute right-3 top-3 z-20 w-8 h-8 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors"
      title="关闭"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <!-- Content -->
    <div class="flex flex-col h-full">
      <!-- Header -->
      <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between bg-gradient-to-r from-white to-gray-50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-bold text-gray-900">AI 智能编排</h3>
            <div class="flex items-center gap-1.5 mt-0.5">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              <span class="text-xs text-green-600 font-medium">运行中</span>
            </div>
          </div>
        </div>
        <button
          @click="showSettings = !showSettings"
          class="w-8 h-8 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
          </svg>
        </button>
      </div>

      <!-- Scrollable Content -->
      <div class="flex-1 overflow-y-auto px-3 py-3 space-y-3 custom-scrollbar">
        <!-- Welcome Message -->
        <div class="flex gap-3">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-md">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl rounded-tl-sm px-4 py-3 border border-blue-100 shadow-sm">
              <p class="text-sm text-gray-700 leading-relaxed">
                感谢您的信息！我们已经有足够的细节来开始创建您的视频数据处理流水线。马上为您准备执行！
              </p>
            </div>
            <span class="text-xs text-gray-400 mt-1.5 block">17:20:13</span>
          </div>
        </div>

        <!-- Requirements Summary Card -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="px-4 py-3 bg-gradient-to-r from-slate-50 to-gray-50 border-b border-gray-100 flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-bold text-gray-900">需求总结</h4>
              <span class="text-xs text-gray-500 font-mono">wf_mult_pipeline_recommand_agent</span>
            </div>
          </div>
          <div class="p-4">
            <div class="flex items-center gap-2 mb-4">
              <span class="text-xs text-gray-500">当前阶段:</span>
              <span class="px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-700 text-xs font-semibold">需求收集</span>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-gray-50 rounded-lg p-3">
                <div class="text-xs text-gray-500 mb-1.5">描述任务目标 <span class="text-red-500">*</span></div>
                <div class="text-xs text-gray-800 font-medium">视频中数据的提取</div>
                <div class="text-xs text-gray-400 mt-2 text-right">8 / 200</div>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <div class="text-xs text-gray-500 mb-1.5">描述数据集特征</div>
                <div class="text-xs text-gray-800 font-medium">视频格式为mp4</div>
                <div class="text-xs text-gray-400 mt-2 text-right">8 / 200</div>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <div class="text-xs text-gray-500 mb-1.5">描述数据处理规则</div>
                <div class="text-xs text-gray-800 font-medium">提取视频音频、识别画面信息及字幕</div>
                <div class="text-xs text-gray-400 mt-2 text-right">16 / 200</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Analysis Card -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="px-4 py-3 bg-gradient-to-r from-indigo-50 to-blue-50 border-b border-indigo-100 flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </div>
            <h4 class="text-sm font-bold text-gray-900">开始分析</h4>
          </div>
          <div class="p-4">
            <div class="text-xs text-gray-500 mb-3">任务:</div>
            <div class="text-sm font-semibold text-gray-800 mb-4">用户输入:</div>
            <div class="bg-gray-50 rounded-lg p-3 mb-4">
              <div class="text-xs text-gray-500 mb-2">已收集的需求:</div>
              <ul class="space-y-2 text-xs text-gray-700">
                <li class="flex items-start gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-1.5 flex-shrink-0"></span>
                  <span><span class="font-mono text-indigo-600">task_goal:</span> 视频中数据的提取</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-1.5 flex-shrink-0"></span>
                  <span><span class="font-mono text-indigo-600">dataset_info:</span> 视频格式为mp4</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-1.5 flex-shrink-0"></span>
                  <span><span class="font-mono text-indigo-600">processing_rules:</span> 提取视频音频、识别画面信息及字幕</span>
                </li>
              </ul>
            </div>
            <div class="flex items-center gap-2 text-xs text-indigo-600">
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>正在分析中...</span>
            </div>
          </div>
        </div>

        <!-- Plan Decision Card -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="px-4 py-3 bg-gradient-to-r from-emerald-50 to-teal-50 border-b border-emerald-100 flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
            </div>
            <h4 class="text-sm font-bold text-gray-900">计划决策</h4>
          </div>
          <div class="p-4">
            <div class="text-xs text-gray-500 mb-2">原因:</div>
            <p class="text-sm text-gray-700 leading-relaxed">
              正在分析与理解用户需求，我决定选择合适的工具处理该需求
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-2 pt-2">
          <button class="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-sm font-medium py-2.5 px-4 rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 flex items-center justify-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
            </svg>
            生成 Pipeline
          </button>
          <button class="px-4 py-2.5 border border-gray-200 text-gray-700 text-sm font-medium rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all duration-200">
            重置
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['close'])

const showSettings = ref(false)
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
