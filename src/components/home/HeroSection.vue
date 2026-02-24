<template>
  <section class="relative overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <div class="absolute inset-0 opacity-30">
      <div class="absolute top-10 left-10 w-72 h-72 bg-blue-200 rounded-full blur-3xl"></div>
      <div class="absolute bottom-10 right-10 w-96 h-96 bg-purple-200 rounded-full blur-3xl"></div>
    </div>
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28 text-center">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 text-slate-800">
        Empowering Industries with Data-Centric AI.
      </h1>
      <p class="text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto mb-10">
        The Data-Centric AI platform where AI developers, data scientists, and domain experts collaborate around data to build professional models, agents, and applications.
      </p>

      <div class="inline-flex flex-col w-full max-w-2xl mx-auto">
        <!-- ChatGPT-style Dialog -->
        <div class="mb-6 w-full">
          <div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-4 min-h-[120px] flex flex-col justify-between">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <div class="flex-1 pt-1">
                <p class="text-slate-400 text-left text-lg">
                  Just tell about your data needs, and DataMaster will help you get things done.
                </p>
              </div>
            </div>
            <div class="flex justify-end mt-2">
              <button class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-white hover:bg-slate-300 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Example Queries Section -->
        <div class="w-full text-left">
          <h3 class="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <span class="w-1 h-4 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></span>
            Try these queries
          </h3>
          <div class="space-y-3">
            <button
              v-for="(query, index) in exampleQueries"
              :key="index"
              @click="handleQueryClick(query)"
              class="w-full text-left bg-white rounded-xl shadow-md border border-slate-100 p-4 hover:shadow-lg hover:border-blue-200 transition-all duration-200 group"
            >
              <p class="text-slate-700 text-sm sm:text-base group-hover:text-slate-900">
                {{ query }}
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const exampleQueries = [
  '@arxiv-stem-papers what are recent advances on superconductivity',
  'Generate SFT data from @k12-science-textbooks',
  'Extract knowledge graphs from @chemistry-books',
  'Finetune a model on @math-proofs-corpus'
]

const handleQueryClick = (query) => {
  // Handle query click - could emit event or navigate
  console.log('Selected query:', query)
}
</script>
