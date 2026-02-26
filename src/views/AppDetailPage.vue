<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="loading" class="text-center py-20">
      <p class="text-lg text-gray-500">Loading...</p>
    </div>
    <div v-else-if="app">
      <!-- Breadcrumb -->
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/apps" class="hover:text-gray-700">Apps</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ app.id }}</span>
      </div>
      <!-- Gradient header -->
      <div
        class="rounded-xl h-40 flex items-center justify-center mb-6"
        :style="gradientStyle"
      >
        <span class="text-6xl">{{ app.emoji }}</span>
      </div>
      <div class="lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- Main content -->
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
          <!-- App preview placeholder -->
          <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
            <div class="border-b border-gray-200 px-4 py-3 flex items-center justify-between">
              <h2 class="font-semibold text-gray-900">App</h2>
              <span class="text-xs text-gray-400">{{ app.sdk }} · {{ app.hardware }}</span>
            </div>
            <div class="bg-gray-50 flex items-center justify-center h-80">
              <div class="text-center">
                <span class="text-5xl block mb-4">{{ app.emoji }}</span>
                <p class="text-gray-500 text-sm">Interactive app preview</p>
                <p class="text-gray-400 text-xs mt-1">This is a demo clone — the actual app would be embedded here</p>
                <button class="mt-4 px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-800 transition-colors">
                  Open in new tab
                </button>
              </div>
            </div>
          </div>
          <!-- Description -->
          <div class="border border-gray-200 rounded-lg bg-white mt-6">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">About</h2>
            </div>
            <div class="p-6 prose prose-sm max-w-none">
              <p>{{ app.description }}</p>
              <h3>How to Use</h3>
              <p>Visit this App to interact with the application directly in your browser. No installation or setup required.</p>
              <h3>Technical Details</h3>
              <ul>
                <li><strong>SDK:</strong> {{ app.sdk }}</li>
                <li><strong>Hardware:</strong> {{ app.hardware }}</li>
                <li><strong>Category:</strong> {{ app.category.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) }}</li>
              </ul>
            </div>
          </div>
        </div>
        <!-- Sidebar -->
        <aside class="mt-6 lg:mt-0">
          <div class="border border-gray-200 rounded-lg bg-white p-4 space-y-4 sticky top-20">
            <div class="flex items-center justify-between">
              <StatBadge icon="like" :value="app.likes" />
              <span
                class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                :class="app.status === 'running' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'"
              >
                {{ app.status === 'running' ? 'Running' : 'Offline' }}
              </span>
            </div>
            <hr class="border-gray-200" />
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Author</span>
                <span class="font-medium text-gray-900">{{ app.author }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">SDK</span>
                <span class="font-medium text-gray-900">{{ app.sdk }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Hardware</span>
                <span class="font-medium text-gray-900">{{ app.hardware }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Category</span>
                <span class="font-medium text-gray-900">{{ app.category.replace(/-/g, ' ') }}</span>
              </div>
            </div>
            <hr class="border-gray-200" />
            <button class="w-full py-2 bg-dc-primary text-white text-sm font-semibold rounded-lg hover:bg-dc-primary-dark transition-colors">
              ❤️ Like
            </button>
            <button class="w-full py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
              Duplicate this App
            </button>
          </div>
        </aside>
      </div>
    </div>
    <div v-else class="text-center py-20">
      <p class="text-lg text-gray-500">App not found</p>
      <router-link to="/apps" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Back to Apps</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { appApi } from '@/services/api.js'
import StatBadge from '@/components/common/StatBadge.vue'

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
  teal: '#14b8a6', cyan: '#06b6d4', blue: '#3b82f6', indigo: '#6366f1',
  purple: '#a855f7', pink: '#ec4899',
}

const gradientStyle = computed(() => {
  if (!app.value) return {}
  const from = colorValues[app.value.colorFrom] || '#6366f1'
  const to = colorValues[app.value.colorTo] || '#3b82f6'
  return { background: `linear-gradient(135deg, ${from}, ${to})` }
})
</script>
