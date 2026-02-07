<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="model">
      <!-- Header -->
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/models" class="hover:text-gray-700">Models</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ model.id }}</span>
      </div>
      <div class="lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- Main content -->
        <div class="lg:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-lg font-bold text-gray-600">
              {{ model.author.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">{{ model.name }}</h1>
              <span class="text-sm text-gray-500">by {{ model.author }}</span>
            </div>
          </div>
          <div class="flex items-center flex-wrap gap-2 mb-6">
            <TagBadge :label="model.pipeline_tag" :color="taskColorMap[model.pipeline_tag] || 'gray'" />
            <TagBadge v-for="tag in model.tags" :key="tag" :label="tag" color="gray" />
          </div>
          <!-- Model Card content -->
          <div class="border border-gray-200 rounded-lg bg-white">
            <div class="border-b border-gray-200 px-4 py-3">
              <h2 class="font-semibold text-gray-900">Model Card</h2>
            </div>
            <div class="p-6 prose prose-sm max-w-none">
              <h3>Model Description</h3>
              <p>{{ model.description }}</p>
              <h3>Intended Uses</h3>
              <p>This model is designed for {{ model.pipeline_tag.replace(/-/g, ' ') }} tasks. It can be used directly with the Transformers library or through the Inference API.</p>
              <h3>Training Data</h3>
              <p>The model was trained on a large corpus of publicly available data. Please refer to the original paper for detailed training information.</p>
              <h3>How to Use</h3>
              <pre class="bg-gray-50 rounded-lg p-4 text-sm overflow-x-auto"><code>from transformers import pipeline

pipe = pipeline("{{ model.pipeline_tag }}", model="{{ model.id }}")
result = pipe("Your input here")
print(result)</code></pre>
              <h3>Limitations</h3>
              <p>This model may produce inaccurate or biased outputs. Users should evaluate the model's suitability for their specific use case and implement appropriate safeguards.</p>
            </div>
          </div>
        </div>
        <!-- Sidebar -->
        <aside class="mt-6 lg:mt-0">
          <div class="border border-gray-200 rounded-lg bg-white p-4 space-y-4 sticky top-20">
            <div class="flex items-center justify-between">
              <StatBadge icon="download" :value="model.downloads" />
              <StatBadge icon="like" :value="model.likes" />
            </div>
            <hr class="border-gray-200" />
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Library</span>
                <span class="font-medium text-gray-900">{{ model.library }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Language</span>
                <span class="font-medium text-gray-900">{{ model.language }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">License</span>
                <span class="font-medium text-gray-900">{{ model.license }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Last updated</span>
                <span class="font-medium text-gray-900">{{ model.lastModified }}</span>
              </div>
            </div>
            <hr class="border-gray-200" />
            <div>
              <h4 class="text-sm font-semibold text-gray-700 mb-2">Tags</h4>
              <div class="flex flex-wrap gap-1">
                <TagBadge v-for="tag in model.tags" :key="tag" :label="tag" color="gray" />
              </div>
            </div>
            <button class="w-full py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
              Use this model
            </button>
          </div>
        </aside>
      </div>
    </div>
    <div v-else class="text-center py-20">
      <p class="text-lg text-gray-500">Model not found</p>
      <router-link to="/models" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Back to Models</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getModelById } from '@/data/models.js'
import { taskColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'

const route = useRoute()
const model = computed(() => getModelById(route.params.id))
</script>
