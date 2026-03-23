<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
    <div class="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ $t('notebook.title') }}</h1>
        <p class="text-sm text-gray-500 mt-1">{{ $t('notebook.subtitle') }}</p>
      </div>
      <router-link
        to="/knowledge-base"
        class="inline-flex items-center gap-2 px-4 py-2 border border-slate-200 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
      >
        {{ $t('notebook.backToKnowledgeBase') }}
      </router-link>
    </div>

    <OpenNotebookApp />
  </div>
</template>

<script setup>
import OpenNotebookApp from '@/components/apps/OpenNotebookApp.vue'
</script>
