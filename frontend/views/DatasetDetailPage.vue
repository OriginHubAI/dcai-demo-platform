<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div v-if="dataset">
      <!-- Breadcrumb -->
      <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
        <router-link to="/datasets" class="hover:text-gray-700">Datasets</router-link>
        <span>/</span>
        <span class="text-gray-900">{{ dataset.id }}</span>
      </div>
      
      <!-- Tab Navigation for Autodriving Datasets -->
      <div v-if="showDataStudioTab" class="mb-6 border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'card'"
            :class="[
              activeTab === 'card'
                ? 'border-dc-primary text-dc-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2'
            ]"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>Dataset Card</span>
          </button>
          <button
            @click="activeTab = 'datastudio'"
            :class="[
              activeTab === 'datastudio'
                ? 'border-dc-primary text-dc-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2'
            ]"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
            <span>Data Studio</span>
          </button>
        </nav>
      </div>
      
      <!-- Readonly Warning Banner -->
      <div v-if="dataset.readonly" class="mb-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <div class="flex items-center space-x-2">
          <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <span class="text-amber-800 font-medium">Read-only Derived Dataset</span>
        </div>
        <p class="text-sm text-amber-700 mt-1">
          This is a processed dataset derived from <router-link :to="`/datasets/${dataset.parentDataset}`" class="underline">{{ dataset.parentDataset }}</router-link>. 
          It cannot be modified directly. To make changes, process the original dataset through a DataFlow-MM pipeline.
        </p>
      </div>

      <div class="lg:grid lg:gap-8" :class="activeTab === 'datastudio' ? 'lg:grid-cols-1' : 'lg:grid-cols-3'">
        <!-- Main content -->
        <div :class="activeTab === 'datastudio' ? 'lg:col-span-1' : 'lg:col-span-2'">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-lg font-bold text-green-700">
              {{ dataset.author.charAt(0).toUpperCase() }}
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h1 class="text-xl font-bold text-gray-900">{{ dataset.name }}</h1>
                <TagBadge v-if="dataset.datasetType" :label="dataset.datasetType === 'original' ? 'Original' : 'Derived'" :color="datasetTypeColorMap[dataset.datasetType] || 'gray'" />
              </div>
              <span class="text-sm text-gray-500">by {{ dataset.author }}</span>
            </div>
          </div>

          <div class="flex items-center flex-wrap gap-2 mb-6">
            <TagBadge :label="dataset.task" :color="taskColorMap[dataset.task] || 'gray'" />
            <TagBadge :label="dataset.modality" color="teal" />
            <TagBadge :label="dataset.language" color="indigo" />
          </div>

          <!-- Autonomous Driving Metadata - only show in Dataset Card tab -->
          <div v-if="activeTab === 'card' && dataset.domain === 'autonomous-driving' && dataset.metadata" class="mb-6">
            <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
              <div class="border-b border-gray-200 px-4 py-3 bg-gray-50">
                <h2 class="font-semibold text-gray-900 flex items-center space-x-2">
                  <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0121 18.382V7.618a1 1 0 01-.447-.894L15 7m0 13V7m0 0L9.553 4.553A1 1 0 009 4.118v.004" />
                  </svg>
                  <span>Spatial & Temporal Metadata</span>
                </h2>
              </div>
              <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Time Range -->
                <div v-if="dataset.metadata.timeRange" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700 flex items-center space-x-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>Time Range</span>
                  </h4>
                  <div class="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                    <div>{{ dataset.metadata.timeRange.start }} to {{ dataset.metadata.timeRange.end }}</div>
                    <div class="text-xs text-gray-500">Timezone: {{ dataset.metadata.timeRange.timezone }}</div>
                  </div>
                </div>

                <!-- Spatial Coverage -->
                <div v-if="dataset.metadata.spatial" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700 flex items-center space-x-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>Spatial Coverage</span>
                  </h4>
                  <div class="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                    <div>Regions: {{ dataset.metadata.spatial.regions.join(', ') }}</div>
                    <div class="text-xs text-gray-500">{{ dataset.metadata.spatial.coverage }}</div>
                    <div v-if="dataset.metadata.spatial.coordinates" class="text-xs text-gray-400 mt-1">
                      Lat: {{ dataset.metadata.spatial.coordinates.lat.join(' to ') }}<br>
                      Lon: {{ dataset.metadata.spatial.coordinates.lon.join(' to ') }}
                    </div>
                  </div>
                </div>

                <!-- Sensors -->
                <div v-if="dataset.metadata.sensors" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700">Sensors</h4>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="sensor in dataset.metadata.sensors" :key="sensor" class="text-xs bg-teal-50 text-teal-700 px-2 py-1 rounded">
                      {{ sensor }}
                    </span>
                  </div>
                </div>

                <!-- Conditions -->
                <div v-if="dataset.metadata.conditions" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700">Conditions</h4>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="condition in dataset.metadata.conditions" :key="condition" class="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                      {{ condition }}
                    </span>
                  </div>
                </div>

                <!-- Annotations -->
                <div v-if="dataset.metadata.annotations" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700">Annotations</h4>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="ann in dataset.metadata.annotations" :key="ann" class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded">
                      {{ ann }}
                    </span>
                  </div>
                </div>

                <!-- Processing Pipeline -->
                <div v-if="dataset.processingPipeline" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700">Processing Pipeline</h4>
                  <div class="text-sm text-gray-600 font-mono bg-gray-100 px-2 py-1 rounded">
                    {{ dataset.processingPipeline }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Semantic Index - only show in Dataset Card tab -->
          <div v-if="activeTab === 'card' && dataset.semanticIndex" class="mb-6">
            <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
              <div class="border-b border-gray-200 px-4 py-3 bg-gray-50">
                <h2 class="font-semibold text-gray-900 flex items-center space-x-2">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  <span>Semantic Search Index</span>
                </h2>
              </div>
              <div class="p-4 space-y-3">
                <div v-for="(values, key) in dataset.semanticIndex" :key="key" class="space-y-1">
                  <h4 class="text-sm font-medium text-gray-700 capitalize">{{ key.replace(/-/g, ' ') }}</h4>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="value in values" :key="value" class="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded hover:bg-purple-100 cursor-pointer transition-colors">
                      {{ value }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Data Studio Tab Content -->
          <div v-if="activeTab === 'datastudio'" class="data-studio-container border border-gray-200 rounded-lg bg-white p-4">
            <DataStudio :dataset-id="dataset.id" />
          </div>

          <!-- Dataset Card content -->
          <div v-else class="border border-gray-200 rounded-lg bg-white">
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
              
              <!-- Time/Space/Label/Semantic Search Examples for Autodriving -->
              <div v-if="dataset.domain === 'autonomous-driving'">
                <h3>Advanced Search Examples</h3>
                <div class="space-y-2 text-sm">
                  <div class="bg-gray-50 p-3 rounded">
                    <strong>Time-based Search:</strong>
                    <code class="block mt-1 text-xs">dataset.filter(lambda x: x['timestamp'] >= '2025-01-01' and x['timestamp'] <= '2025-03-15')</code>
                  </div>
                  <div class="bg-gray-50 p-3 rounded">
                    <strong>Spatial Search:</strong>
                    <code class="block mt-1 text-xs">dataset.filter(lambda x: 1.2 <= x['latitude'] <= 42.4 and 71.1 <= x['longitude'] <= 103.8)</code>
                  </div>
                  <div class="bg-gray-50 p-3 rounded">
                    <strong>Label-based Search:</strong>
                    <code class="block mt-1 text-xs">dataset.filter(lambda x: 'car' in x['objects'] and x['weather'] == 'clear')</code>
                  </div>
                  <div class="bg-gray-50 p-3 rounded">
                    <strong>Semantic Search:</strong>
                    <code class="block mt-1 text-xs">dataset.semantic_search("vehicles at intersection during nighttime")</code>
                  </div>
                </div>
              </div>
              
              <h3>Citation</h3>
              <p class="text-gray-500 italic">Please refer to the original paper for citation information.</p>
            </div>
          </div>
        </div>

        <!-- Sidebar - hidden in Data Studio tab -->
        <aside v-if="activeTab === 'card'" class="mt-6 lg:mt-0">
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
              <div v-if="dataset.datasetType" class="flex justify-between">
                <span class="text-gray-500">Type</span>
                <span class="font-medium" :class="dataset.datasetType === 'original' ? 'text-green-600' : 'text-blue-600'">{{ dataset.datasetType }}</span>
              </div>
            </div>
            <button 
              class="w-full py-2 text-white text-sm font-medium rounded-lg transition-colors"
              :class="dataset.readonly ? 'bg-gray-400 cursor-not-allowed' : 'bg-gray-900 hover:bg-gray-800'"
              :disabled="dataset.readonly"
            >
              {{ dataset.readonly ? 'Read-only Dataset' : 'Use this dataset' }}
            </button>
          </div>

          <!-- Dataset Relationships -->
          <div v-if="dataset.parentDataset || (dataset.derivedDatasets && dataset.derivedDatasets.length)" class="mt-4 p-4 bg-gray-50 rounded-lg">
            <h3 class="text-sm font-semibold text-gray-700 mb-2">{{ $t('datasets.relationships.title') }}</h3>
            <div v-if="dataset.parentDataset" class="text-sm text-gray-600 mb-3">
              <span class="text-gray-500">{{ $t('datasets.relationships.parentDataset') }}:</span>
              <router-link :to="`/datasets/${dataset.parentDataset}`" class="text-blue-600 hover:underline ml-1 font-medium">{{ dataset.parentDataset }}</router-link>
            </div>
            <div v-if="dataset.derivedDatasets && dataset.derivedDatasets.length" class="text-sm text-gray-600">
              <span class="text-gray-500">{{ $t('datasets.relationships.derivedDatasets') }}:</span>
              <div class="flex flex-wrap gap-2 mt-1">
                <router-link 
                  v-for="derivedId in dataset.derivedDatasets" 
                  :key="derivedId"
                  :to="`/datasets/${derivedId}`"
                  class="text-blue-600 hover:underline text-xs bg-blue-50 px-2 py-1 rounded border border-blue-100 hover:bg-blue-100 transition-colors"
                >
                  {{ derivedId }}
                </router-link>
              </div>
            </div>
          </div>

          <!-- Related Tasks -->
          <div v-if="dataset.relatedTasks && dataset.relatedTasks.length" class="mt-4 p-4 bg-gray-50 rounded-lg">
            <h3 class="text-sm font-semibold text-gray-700 mb-2">{{ $t('datasets.relatedTasks.title') }}</h3>
            <div class="space-y-2">
              <router-link
                v-for="task in dataset.relatedTasks"
                :key="task.id"
                :to="`/dataflow/tasks/${task.id}`"
                class="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-sm transition-all group"
              >
                <div class="flex items-center gap-3">
                  <!-- Status Icon -->
                  <div class="flex-shrink-0">
                    <div v-if="task.status === 'running'" class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <div v-else-if="task.status === 'completed'" class="w-2 h-2 rounded-full bg-blue-500"></div>
                    <div v-else-if="task.status === 'failed'" class="w-2 h-2 rounded-full bg-red-500"></div>
                    <div v-else class="w-2 h-2 rounded-full bg-gray-400"></div>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900 group-hover:text-blue-600">{{ task.name }}</div>
                    <div class="text-xs text-gray-500">
                      <span v-if="task.isInput" class="text-blue-600">{{ $t('datasets.relatedTasks.generatedBy') }}</span>
                      <span v-else-if="task.isOutput" class="text-green-600">{{ $t('datasets.relatedTasks.generates') }}</span>
                      <span v-if="task.duration" class="ml-2">• {{ task.duration }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <!-- Status Badge -->
                  <span 
                    class="text-xs px-2 py-1 rounded-full font-medium"
                    :class="{
                      'bg-green-100 text-green-700': task.status === 'running',
                      'bg-blue-100 text-blue-700': task.status === 'completed',
                      'bg-red-100 text-red-700': task.status === 'failed',
                      'bg-gray-100 text-gray-600': !['running', 'completed', 'failed'].includes(task.status)
                    }"
                  >
                    {{ task.status === 'running' ? $t('tasks.status.running') : task.status === 'completed' ? $t('tasks.status.completed') : task.status === 'failed' ? $t('tasks.status.failed') : task.status }}
                  </span>
                  <!-- Progress Bar for Running Tasks -->
                  <div v-if="task.status === 'running' && task.progress" class="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-green-500 rounded-full transition-all"
                      :style="{ width: `${task.progress}%` }"
                    ></div>
                  </div>
                  <svg class="w-4 h-4 text-gray-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </router-link>
            </div>
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
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getDatasetById } from '@/data/datasets.js'
import { taskColorMap, domainColorMap, datasetTypeColorMap } from '@/data/filters.js'
import TagBadge from '@/components/common/TagBadge.vue'
import StatBadge from '@/components/common/StatBadge.vue'
import DataStudio from '@/components/datasets/DataStudio.vue'

const route = useRoute()
const dataset = computed(() => getDatasetById(route.params.id))

// Tab state - only show DataStudio for autodrive-derived-nuscenes-filtered
const activeTab = ref('card')
const showDataStudioTab = computed(() => {
  return dataset.value?.id === 'autodrive-derived-nuscenes-filtered'
})

function formatRows(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k'
  return n.toString()
}
</script>
