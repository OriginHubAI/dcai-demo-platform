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
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <router-link
          to="/datasets"
          class="inline-flex items-center px-6 py-3 bg-dc-primary text-white font-semibold rounded-lg hover:bg-dc-primary-dark transition-colors text-sm shadow-lg shadow-dc-primary/20"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
          </svg>
          Explore Datasets
        </router-link>
        <router-link
          to="/dataflow/tasks"
          class="inline-flex items-center px-6 py-3 bg-dc-primary text-white font-semibold rounded-lg hover:bg-dc-primary-dark transition-colors text-sm shadow-lg shadow-dc-primary/20"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          View Tasks
        </router-link>
        <router-link
          to="/spaces"
          class="inline-flex items-center px-6 py-3 bg-dc-primary text-white font-semibold rounded-lg hover:bg-dc-primary-dark transition-colors text-sm shadow-lg shadow-dc-primary/20"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
          </svg>
          Browse Spaces
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>
