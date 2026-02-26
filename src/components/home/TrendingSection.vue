<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-8">Trending on DCAI Platform</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Trending Datasets -->
      <div>
        <div class="flex items-center space-x-2 mb-4">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
          </svg>
          <h3 class="font-semibold text-gray-700">Datasets</h3>
          <router-link to="/datasets" class="ml-auto text-sm text-gray-500 hover:text-gray-700">See all →</router-link>
        </div>
        <div class="space-y-2">
          <router-link
            v-for="(ds, i) in trendingDatasets"
            :key="ds.id"
            :to="`/datasets/${ds.id}`"
            class="flex items-center space-x-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <span class="text-xs text-gray-400 w-4">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate group-hover:text-blue-600">{{ ds.id }}</div>
              <div class="flex items-center space-x-3 mt-0.5">
                <TagBadge :label="ds.task" :color="taskColorMap[ds.task] || 'gray'" />
                <StatBadge icon="like" :value="ds.likes" />
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Trending Apps -->
      <div>
        <div class="flex items-center space-x-2 mb-4">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
          </svg>
          <h3 class="font-semibold text-gray-700">Apps</h3>
          <router-link to="/apps" class="ml-auto text-sm text-gray-500 hover:text-gray-700">See all →</router-link>
        </div>
        <div class="space-y-2">
          <router-link
            v-for="(app, i) in trendingApps"
            :key="app.id"
            :to="`/apps/${app.id}`"
            class="flex items-center space-x-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <span class="text-xs text-gray-400 w-4">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate group-hover:text-blue-600">
                <span class="mr-1">{{ app.emoji }}</span>{{ app.title }}
              </div>
              <div class="flex items-center space-x-3 mt-0.5">
                <span class="text-xs text-gray-500">{{ app.author }}</span>
                <StatBadge icon="like" :value="app.likes" />
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Trending Models -->
      <div>
        <div class="flex items-center space-x-2 mb-4">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
          <h3 class="font-semibold text-gray-700">Models</h3>
          <router-link to="/models" class="ml-auto text-sm text-gray-500 hover:text-gray-700">See all →</router-link>
        </div>
        <div class="space-y-2">
          <router-link
            v-for="(model, i) in trendingModels"
            :key="model.id"
            :to="`/models/${model.id}`"
            class="flex items-center space-x-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <span class="text-xs text-gray-400 w-4">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate group-hover:text-blue-600">{{ model.id }}</div>
              <div class="flex items-center space-x-3 mt-0.5">
                <TagBadge :label="model.pipeline_tag" :color="taskColorMap[model.pipeline_tag] || 'gray'" />
                <StatBadge icon="like" :value="model.likes" />
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { models } from '@/data/models.js'
import { datasets } from '@/data/datasets.js'
import { apps } from '@/data/apps.js'
import { taskColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'

const trendingModels = computed(() =>
  [...models].sort((a, b) => b.likes - a.likes).slice(0, 5)
)
const trendingDatasets = computed(() =>
  [...datasets].sort((a, b) => b.likes - a.likes).slice(0, 5)
)
const trendingApps = computed(() =>
  [...apps].sort((a, b) => b.likes - a.likes).slice(0, 5)
)
</script>
