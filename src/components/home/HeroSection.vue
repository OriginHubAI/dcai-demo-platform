<template>
  <section class="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
    <div class="absolute inset-0 opacity-10">
      <div class="absolute top-10 left-10 w-72 h-72 bg-hf-yellow rounded-full blur-3xl"></div>
      <div class="absolute bottom-10 right-10 w-96 h-96 bg-blue-500 rounded-full blur-3xl"></div>
    </div>
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28 text-center">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6">
        The AI community building the future.
      </h1>
      <p class="text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto mb-10">
        The platform where the machine learning community collaborates on models, datasets, and applications.
      </p>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <router-link
          to="/models"
          class="inline-flex items-center px-6 py-3 bg-hf-yellow text-gray-900 font-semibold rounded-lg hover:bg-hf-yellow-dark transition-colors text-sm"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
          Explore Models
        </router-link>
        <router-link
          to="/spaces"
          class="inline-flex items-center px-6 py-3 bg-white/10 text-white font-semibold rounded-lg hover:bg-white/20 transition-colors border border-white/20 text-sm"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
          </svg>
          Browse Spaces
        </router-link>
      </div>
      <!-- Stats -->
      <div class="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-6 max-w-3xl mx-auto">
        <div v-for="stat in stats" :key="stat.label">
          <div class="text-2xl sm:text-3xl font-bold text-hf-yellow">{{ stat.value }}</div>
          <div class="text-sm text-gray-400 mt-1">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const stats = [
  { value: '900K+', label: 'Models' },
  { value: '200K+', label: 'Datasets' },
  { value: '400K+', label: 'Spaces' },
  { value: '50K+', label: 'Organizations' },
]
</script>
