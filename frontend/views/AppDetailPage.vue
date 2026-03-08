<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="loading" class="text-center py-20">
      <p class="text-lg text-gray-500">Loading...</p>
    </div>
    <div v-else-if="app">
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/apps" class="hover:text-gray-700">Apps</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ app.id }}</span>
      </div>

      <div v-if="app.type === 'proxied'" class="space-y-6">
        <div class="rounded-xl h-32 flex items-center justify-center" :style="gradientStyle">
          <div class="text-center text-white">
            <span class="text-5xl block">{{ app.emoji }}</span>
            <p class="text-lg font-semibold mt-2">{{ app.title }}</p>
          </div>
        </div>
        <component :is="appComponent" v-if="appComponent" :app="app" />
      </div>

      <div v-else>
        <div class="rounded-xl h-40 flex items-center justify-center mb-6" :style="gradientStyle">
          <span class="text-6xl">{{ app.emoji }}</span>
        </div>
        <div class="lg:grid lg:grid-cols-3 lg:gap-8">
          <div class="lg:col-span-2">
            <div class="flex items-center space-x-3 mb-2">
              <h1 class="text-2xl font-bold text-gray-900">{{ app.title }}</h1>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                :class="app.status === 'running' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'"
              >
                {{ app.status === 'running' ? 'Running' : 'Offline' }}
              </span>
            </div>
            <p class="text-sm text-gray-500 mb-6">by {{ app.author }}</p>
            <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
              <div class="border-b border-gray-200 px-4 py-3 flex items-center justify-between">
                <h2 class="font-semibold text-gray-900">App</h2>
                <span class="text-xs text-gray-400">{{ app.sdk }} · {{ app.hardware }}</span>
              </div>
              <div class="bg-gray-50 flex items-center justify-center h-80">
                <div class="text-center">
                  <span class="text-5xl block mb-4">{{ app.emoji }}</span>
                  <p class="text-gray-500 text-sm">Interactive app preview</p>
                  <p class="text-gray-400 text-xs mt-1">This app does not expose an embedded workspace yet.</p>
                </div>
              </div>
            </div>
          </div>
          <aside class="mt-6 lg:mt-0">
            <div class="border border-gray-200 rounded-lg bg-white p-4 space-y-4 sticky top-20">
              <div class="text-sm text-slate-700">{{ app.description }}</div>
              <div class="text-xs text-slate-500">{{ app.tags?.join(' · ') }}</div>
            </div>
          </aside>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-20">
      <p class="text-lg text-gray-500">App not found</p>
      <router-link to="/apps" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Back to Apps</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { appApi } from '@/services/api.js'
import DFAgentApp from '@/components/apps/DFAgentApp.vue'
import LoopAIApp from '@/components/apps/LoopAIApp.vue'
import PackageEditorApp from '@/components/apps/PackageEditorApp.vue'

const route = useRoute()
const app = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    app.value = await appApi.getAppById(route.params.id)
  } catch (error) {
    console.error('Failed to load app:', error)
  } finally {
    loading.value = false
  }
})

const colorValues = {
  red: '#ef4444', orange: '#f97316', yellow: '#eab308', green: '#22c55e',
  emerald: '#10b981',
  teal: '#14b8a6', cyan: '#06b6d4', blue: '#3b82f6', indigo: '#6366f1',
  purple: '#a855f7', pink: '#ec4899', slate: '#475569',
}

const gradientStyle = computed(() => {
  if (!app.value) return {}
  const from = colorValues[app.value.colorFrom] || '#6366f1'
  const to = colorValues[app.value.colorTo] || '#3b82f6'
  return { background: `linear-gradient(135deg, ${from}, ${to})` }
})

const appComponent = computed(() => {
  if (!app.value?.integration?.kind) return null
  if (app.value.integration.kind === 'loopai') return LoopAIApp
  if (app.value.integration.kind === 'dfagent') return DFAgentApp
  if (app.value.integration.kind === 'package-editor') return PackageEditorApp
  return null
})
</script>
