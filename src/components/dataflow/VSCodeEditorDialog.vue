<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
        @click="handleBackdropClick"
      >
        <div
          class="w-full h-full max-w-[1400px] max-h-[90vh] bg-white rounded-lg shadow-2xl overflow-hidden flex flex-col"
          @click.stop
        >
          <!-- VSCode Header -->
          <div class="h-9 bg-[#f3f3f3] flex items-center justify-between px-3 select-none">
            <div class="flex items-center gap-2">
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 rounded-full bg-[#ff5f57]"></div>
                <div class="w-3 h-3 rounded-full bg-[#febc2e]"></div>
                <div class="w-3 h-3 rounded-full bg-[#28c840]"></div>
              </div>
              <span class="text-xs text-gray-600 ml-3">{{ pkg.name }} - OpenVSCode Server</span>
            </div>
            <button
              @click="close"
              class="w-8 h-8 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-200 rounded transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- VSCode Main Layout -->
          <div class="flex-1 flex overflow-hidden">
            <!-- Activity Bar (Left) -->
            <div class="w-12 bg-[#f6f6f6] flex flex-col items-center py-2 gap-1">
              <button class="w-12 h-12 flex items-center justify-center text-gray-700 border-l-2 border-blue-500 bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
                </svg>
              </button>
              <button class="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                </svg>
              </button>
              <button class="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.25 9.75L16.5 12l-2.25 2.25m-4.5 0L7.5 12l2.25-2.25M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z" />
                </svg>
              </button>
              <button class="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 010 1.972l-11.54 6.347a1.125 1.125 0 01-1.667-.986V5.653z" />
                </svg>
              </button>
              <div class="flex-1"></div>
              <button class="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </button>
              <button class="w-12 h-12 flex items-center justify-center text-gray-500 hover:text-gray-800 hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.212 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>

            <!-- Sidebar (Explorer) -->
            <div class="w-64 bg-[#f8f8f8] flex flex-col border-r border-[#e0e0e0]">
              <!-- Explorer Header -->
              <div class="h-9 flex items-center px-3">
                <span class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Explorer</span>
                <div class="flex-1"></div>
                <button class="p-1 hover:bg-gray-200 rounded">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM12.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM18.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                  </svg>
                </button>
              </div>

              <!-- File Tree -->
              <div class="flex-1 overflow-y-auto py-1">
                <!-- DATAFLOW Folder -->
                <div class="px-1">
                  <button
                    @click="toggleFolder('dataflow')"
                    class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-700 text-[13px]"
                  >
                    <svg
                      class="w-4 h-4 transition-transform"
                      :class="{ 'rotate-90': expandedFolders.dataflow }"
                      fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                    <span class="font-bold uppercase text-[11px] tracking-wide">{{ pkg.name.toUpperCase() }}</span>
                  </button>
                  <div v-show="expandedFolders.dataflow" class="ml-4">
                    <!-- .github folder -->
                    <div>
                      <button
                        @click="toggleFolder('github')"
                        class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                      >
                        <svg
                          class="w-4 h-4 transition-transform"
                          :class="{ 'rotate-90': expandedFolders.github }"
                          fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                        >
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                        </svg>
                        <span>.github</span>
                      </button>
                    </div>
                    <!-- dataflow folder -->
                    <div>
                      <button
                        @click="toggleFolder('dataflow_pkg')"
                        class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                      >
                        <svg
                          class="w-4 h-4 transition-transform"
                          :class="{ 'rotate-90': expandedFolders.dataflow_pkg }"
                          fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                        >
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                        </svg>
                        <span>dataflow</span>
                      </button>
                      <div v-show="expandedFolders.dataflow_pkg" class="ml-4">
                        <div v-for="folder in ['cli_funcs', 'core', 'example', 'operators']" :key="folder">
                          <button
                            @click="toggleFolder(folder)"
                            class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                          >
                            <svg
                              class="w-4 h-4 transition-transform"
                              :class="{ 'rotate-90': expandedFolders[folder] }"
                              fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                            >
                              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                            </svg>
                            <span>{{ folder }}</span>
                          </button>
                          <div v-show="expandedFolders[folder]" class="ml-4">
                            <!-- Subfolders for operators -->
                            <template v-if="folder === 'operators'">
                              <div v-for="sub in ['agentic_rag', 'chemistry', 'code', 'conversations', 'core_speech', 'core_text']" :key="sub">
                                <button
                                  @click="toggleFolder(sub)"
                                  class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                                >
                                  <svg
                                    class="w-4 h-4 transition-transform"
                                    :class="{ 'rotate-90': expandedFolders[sub] }"
                                    fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                                  >
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                                  </svg>
                                  <span>{{ sub }}</span>
                                </button>
                                <div v-show="expandedFolders[sub] && sub === 'core_text'" class="ml-4">
                                  <div v-for="file in ['eval', 'filter', 'generate', 'refine']" :key="file">
                                    <button
                                      @click="toggleFolder(file)"
                                      class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                                    >
                                      <svg
                                        class="w-4 h-4 transition-transform"
                                        :class="{ 'rotate-90': expandedFolders[file] }"
                                        fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
                                      >
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                                      </svg>
                                      <span>{{ file }}</span>
                                    </button>
                                    <div v-show="expandedFolders[file] && file === 'eval'" class="ml-4">
                                      <button
                                        v-for="pyFile in ['bench_dataset_evaluator_question.py', 'bench_dataset_evaluator.py', 'prompted_eval.py', 'text2qa_sample_evaluator.py', 'unified_bench_dataset_evaluator.py']"
                                        :key="pyFile"
                                        @click="openFile(pyFile)"
                                        class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                                        :class="{ 'bg-blue-100 text-blue-800': activeFile === pyFile }"
                                      >
                                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                                          <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                                        </svg>
                                        <span class="truncate">{{ pyFile }}</span>
                                      </button>
                                    </div>
                                    <div v-show="expandedFolders[file] && file === 'generate'" class="ml-4">
                                      <button
                                        v-for="pyFile in ['bench_answer_generator.py', 'chunked_prompted_generator.py', 'embedding_generator.py', 'format_str_prompted_generator.py', 'prompted_generator.py', 'random_domain_knowledge_row_generator.py', 'retrieval_generator.py', 'text2multihopqa_generator.py', 'text2qa_generator.py']"
                                        :key="pyFile"
                                        @click="openFile(pyFile)"
                                        class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]"
                                        :class="{ 'bg-blue-100 text-blue-800': activeFile === pyFile }"
                                      >
                                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                                          <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                                        </svg>
                                        <span class="truncate">{{ pyFile }}</span>
                                      </button>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </template>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- OUTLINE Section -->
                <div class="mt-4 px-1">
                  <button class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                    <span class="font-bold uppercase text-[11px] tracking-wide">Outline</span>
                  </button>
                </div>

                <!-- TIMELINE Section -->
                <div class="px-1">
                  <button class="w-full flex items-center gap-1 px-2 py-1 hover:bg-gray-100 text-gray-600 text-[13px]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                    <span class="font-bold uppercase text-[11px] tracking-wide">Timeline</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Editor Area -->
            <div class="flex-1 flex flex-col bg-white">
              <!-- Tabs -->
              <div class="h-9 bg-[#fafafa] flex items-center">
                <div class="flex items-center h-full">
                  <div
                    v-for="tab in openTabs"
                    :key="tab"
                    @click="activeFile = tab"
                    class="h-full px-3 flex items-center gap-2 text-[13px] min-w-[120px] max-w-[200px] border-r border-[#e0e0e0] cursor-pointer"
                    :class="activeFile === tab ? 'bg-white text-gray-800' : 'bg-[#fafafa] text-gray-600 hover:bg-gray-100'"
                  >
                    <svg class="w-4 h-4 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
                    </svg>
                    <span class="truncate flex-1">{{ tab }}</span>
                    <span
                      @click.stop="closeTab(tab)"
                      class="w-4 h-4 flex items-center justify-center rounded hover:bg-gray-200 cursor-pointer"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                  </div>
                </div>
              </div>

              <!-- Editor Content -->
              <div class="flex-1 overflow-auto p-8">
                <!-- Welcome Page -->
                <div v-if="!activeFile" class="max-w-4xl mx-auto">
                  <h1 class="text-4xl font-light text-gray-700 mb-2">OpenVSCode Server</h1>
                  <p class="text-lg text-gray-500 mb-12">Editing evolved</p>

                  <div class="grid grid-cols-2 gap-12">
                    <!-- Start Section -->
                    <div>
                      <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wide">Start</h2>
                      <div class="space-y-2">
                        <button class="w-full flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded text-[13px] group">
                          <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                          </svg>
                          New File...
                        </button>
                        <button class="w-full flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded text-[13px] group">
                          <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V5.25A2.25 2.25 0 016.375 3h6.375" />
                          </svg>
                          Open File...
                        </button>
                        <button class="w-full flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded text-[13px] group">
                          <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z" />
                          </svg>
                          Clone Git Repository...
                        </button>
                      </div>
                    </div>

                    <!-- Walkthroughs Section -->
                    <div>
                      <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wide">Walkthroughs</h2>
                      <div class="space-y-3">
                        <button class="w-full flex items-start gap-3 p-3 bg-gray-100 hover:bg-gray-200 rounded text-left group">
                          <div class="w-8 h-8 bg-blue-500 rounded flex items-center justify-center flex-shrink-0">
                            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                            </svg>
                          </div>
                          <div>
                            <div class="text-[13px] text-gray-700 font-medium group-hover:text-gray-900">Get Started with VS Code: for the Web</div>
                            <div class="text-xs text-gray-500 mt-0.5">Customize your editor, learn the basics, and start coding</div>
                          </div>
                        </button>
                        <button class="w-full flex items-start gap-3 p-3 hover:bg-gray-100 rounded text-left group">
                          <div class="w-8 h-8 bg-gray-500 rounded flex items-center justify-center flex-shrink-0">
                            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                          </div>
                          <div class="text-[13px] text-gray-700 group-hover:text-gray-900">Learn the Fundamentals</div>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Recent Section -->
                  <div class="mt-12">
                    <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wide">Recent</h2>
                    <p class="text-[13px] text-gray-500">You have no recent folders, <span class="text-blue-500 hover:underline cursor-pointer">open a folder</span> to start.</p>
                  </div>
                </div>

                <!-- Code Editor -->
                <div v-else class="font-mono text-[13px] leading-6">
                  <div class="text-gray-500 mb-4">// {{ activeFile }}</div>
                  <pre class="text-gray-800"><code>{{ getFileContent(activeFile) }}</code></pre>
                </div>
              </div>

              <!-- Status Bar -->
              <div class="h-6 bg-[#007acc] flex items-center px-2 text-[11px] text-white">
                <div class="flex items-center gap-3">
                  <button class="flex items-center gap-1 hover:bg-blue-400/30 px-1.5 py-0.5 rounded">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 010 1.972l-11.54 6.347a1.125 1.125 0 01-1.667-.986V5.653z" />
                    </svg>
                    main
                  </button>
                  <span class="flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                    </svg>
                    0
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                    </svg>
                    0
                  </span>
                </div>
                <div class="flex-1"></div>
                <div class="flex items-center gap-3">
                  <span>Ln 12, Col 34</span>
                  <span>UTF-8</span>
                  <span>Python</span>
                  <span>Prettier</span>
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                  </svg>
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  pkg: { type: Object, required: true }
})

const emit = defineEmits(['update:visible', 'close'])

const expandedFolders = ref({
  dataflow: true,
  dataflow_pkg: true,
  operators: true,
  core_text: true,
  eval: true,
  generate: false,
})

const activeFile = ref('')
const openTabs = ref([])

function toggleFolder(folder) {
  expandedFolders.value[folder] = !expandedFolders.value[folder]
}

function openFile(filename) {
  activeFile.value = filename
  if (!openTabs.value.includes(filename)) {
    openTabs.value.push(filename)
  }
}

function closeTab(tab) {
  openTabs.value = openTabs.value.filter(t => t !== tab)
  if (activeFile.value === tab) {
    activeFile.value = openTabs.value[openTabs.value.length - 1] || ''
  }
}

function close() {
  emit('update:visible', false)
  emit('close')
}

function handleBackdropClick() {
  close()
}

function getFileContent(filename) {
  const contents = {
    'bench_dataset_evaluator.py': `# Bench Dataset Evaluator for ${props.pkg.name}

import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class EvaluationResult:
    score: float
    metrics: Dict[str, float]
    details: List[Dict[str, Any]]

class BenchDatasetEvaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics = []
        
    def evaluate(self, predictions: List[str], references: List[str]) -> EvaluationResult:
        scores = []
        for pred, ref in zip(predictions, references):
            score = self._compute_score(pred, ref)
            scores.append(score)
            
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        return EvaluationResult(
            score=avg_score,
            metrics={'accuracy': avg_score, 'count': len(scores)},
            details=[]
        )
    
    def _compute_score(self, prediction: str, reference: str) -> float:
        # Implementation here
        return 0.95

if __name__ == '__main__':
    evaluator = BenchDatasetEvaluator({})
    result = evaluator.evaluate(['pred1'], ['ref1'])
    print(f'Score: {result.score}')`,
    'prompted_eval.py': `# Prompted Evaluation Module

class PromptedEvaluator:
    def __init__(self, prompt_template: str):
        self.template = prompt_template
        
    def format_prompt(self, **kwargs) -> str:
        return self.template.format(**kwargs)
        
    def evaluate_with_prompt(self, context: str, question: str) -> dict:
        prompt = self.format_prompt(
            context=context,
            question=question
        )
        return {
            'prompt': prompt,
            'result': None
        }`,
    'text2qa_sample_evaluator.py': `# Text2QA Sample Evaluator

class Text2QASampleEvaluator:
    def __init__(self):
        self.samples = []
        
    def add_sample(self, text: str, question: str, answer: str):
        self.samples.append({
            'text': text,
            'question': question,
            'answer': answer
        })
        
    def evaluate(self, model_predictions: list) -> dict:
        correct = sum(1 for p in model_predictions if p['correct'])
        total = len(model_predictions)
        return {
            'accuracy': correct / total if total > 0 else 0,
            'total': total,
            'correct': correct
        }`,
    'bench_answer_generator.py': `# Bench Answer Generator

from typing import List, Dict

class BenchAnswerGenerator:
    def __init__(self, model_config: Dict):
        self.config = model_config
        
    def generate(self, questions: List[str], contexts: List[str]) -> List[str]:
        answers = []
        for q, c in zip(questions, contexts):
            answer = self._generate_answer(q, c)
            answers.append(answer)
        return answers
    
    def _generate_answer(self, question: str, context: str) -> str:
        # Answer generation logic
        return f'Generated answer for: {question}'`,
    'embedding_generator.py': `# Embedding Generator

import numpy as np
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'default'):
        self.model_name = model_name
        self.dimension = 768
        
    def generate(self, texts: List[str]) -> np.ndarray:
        # Generate embeddings
        embeddings = np.random.randn(len(texts), self.dimension)
        return embeddings
    
    def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))`,
    'retrieval_generator.py': `# Retrieval Generator

class RetrievalGenerator:
    def __init__(self, index_path: str = None):
        self.index_path = index_path
        self.documents = []
        
    def add_documents(self, docs: list):
        self.documents.extend(docs)
        
    def retrieve(self, query: str, top_k: int = 5) -> list:
        # Simple retrieval logic
        return self.documents[:top_k]`,
  }
  
  return contents[filename] || `# ${filename}
# This is a placeholder file for ${props.pkg.name} package.

class ${filename.replace('.py', '').split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('')}:
    def __init__(self):
        pass
    
    def process(self):
        pass`
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    // Auto-open a file for demo
    if (!activeFile.value) {
      openFile('bench_dataset_evaluator.py')
    }
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar for light theme */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f0f0f0;
}

::-webkit-scrollbar-thumb {
  background: #c0c0c0;
}

::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}

::-webkit-scrollbar-corner {
  background: #f0f0f0;
}
</style>
