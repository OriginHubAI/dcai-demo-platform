<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="dataset">
      <!-- Breadcrumb -->
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/datasets" class="hover:text-gray-700">Datasets</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ dataset.id }}</span>
      </div>
      <div class="lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- Main content -->
        <div class="lg:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-lg font-bold text-green-700">
              {{ dataset.author.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">{{ dataset.name }}</h1>
              <span class="text-sm text-gray-500">by {{ dataset.author }}</span>
            </div>
          </div>
          <div class="flex items-center flex-wrap gap-2 mb-6">
            <TagBadge :label="dataset.task" :color="taskColorMap[dataset.task] || 'gray'" />
            <TagBadge :label="dataset.modality" color="teal" />
            <TagBadge :label="dataset.language" color="indigo" />
          </div>
          <!-- Dataset Card content -->
          <div class="border border-gray-200 rounded-lg bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Dataset Card</h2>
            </div>
            <div class="p-6 prose prose-sm max-w-none">
              <h3>Dataset Description</h3>
              <p>{{ dataset.description }}</p>
              <h3>Dataset Summary</h3>
              <p>This dataset contains {{ formatRows(dataset.rows) }} rows of {{ dataset.modality }} data, primarily used for {{ dataset.task.replace(/-/g, ' ') }} tasks.</p>
              <h3>Supported Tasks</h3>
              <ul>
                <li>{{ dataset.task.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) }}</li>
              </ul>
              <h3>Languages</h3>
              <p>{{ dataset.language === 'multilingual' ? 'Multiple languages' : dataset.language.toUpperCase() }}</p>
              <h3>How to Use</h3>
              <pre class="bg-gray-50 rounded-lg p-4 text-sm overflow-x-auto"><code>from datasets import load_dataset

dataset = load_dataset("{{ dataset.id }}")
print(dataset)
print(dataset["train"][0])</code></pre>
              <h3>Citation</h3>
              <p class="text-gray-500 italic">Please refer to the original paper for citation information.</p>
            </div>
          </div>
        </div>
        <!-- Sidebar -->
        <aside class="mt-6 lg:mt-0">
          <div class="border border-gray-200 rounded-lg bg-white p-4 space-y-4 sticky top-20">
            <div class="flex items-center justify-between">
              <StatBadge icon="download" :value="dataset.downloads" />
              <StatBadge icon="like" :value="dataset.likes" />
            </div>
            <hr class="border-gray-200" />
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Size</span>
                <span class="font-medium text-gray-900">{{ dataset.size }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Rows</span>
                <span class="font-medium text-gray-900">{{ formatRows(dataset.rows) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Modality</span>
                <span class="font-medium text-gray-900">{{ dataset.modality }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Language</span>
                <span class="font-medium text-gray-900">{{ dataset.language }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">License</span>
                <span class="font-medium text-gray-900">{{ dataset.license }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Last updated</span>
                <span class="font-medium text-gray-900">{{ dataset.lastModified }}</span>
              </div>
            </div>
            <button class="w-full py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
              Use this dataset
            </button>
          </div>
        </aside>
      </div>
    </div>
    <div v-else class="text-center py-20">
      <p class="text-lg text-gray-500">Dataset not found</p>
      <router-link to="/datasets" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Back to Datasets</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getDatasetById } from '@/data/datasets.js'
import { taskColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'

const route = useRoute()
const dataset = computed(() => getDatasetById(route.params.id))

function formatRows(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k'
  return n.toString()
}
</script>
