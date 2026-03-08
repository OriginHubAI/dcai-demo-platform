<template>
  <div class="dataset-files">
    <!-- Files Header -->
    <div class="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
      <div class="flex items-center space-x-4">
        <!-- Branch Selector -->
        <div class="relative">
          <button
            @click="showBranchDropdown = !showBranchDropdown"
            class="flex items-center space-x-2 px-3 py-1.5 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span>{{ currentBranch }}</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <!-- Branch Dropdown -->
          <div v-if="showBranchDropdown" class="absolute top-full left-0 mt-1 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-10">
            <div class="py-1">
              <button
                v-for="branch in branches"
                :key="branch"
                @click="selectBranch(branch)"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                :class="{ 'bg-blue-50 text-blue-600': branch === currentBranch }"
              >
                {{ branch }}
              </button>
            </div>
          </div>
        </div>

        <!-- Dataset Name & Size -->
        <div class="flex items-center space-x-2 text-sm">
          <span class="font-semibold text-gray-900">{{ datasetId }}</span>
          <span class="px-2 py-0.5 bg-gray-200 rounded text-gray-600 text-xs font-mono">{{ totalSize }}</span>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <!-- Contributors -->
        <div class="flex items-center space-x-2 text-sm text-gray-600">
          <div class="flex -space-x-2">
            <div
              v-for="(contributor, index) in contributors.slice(0, 3)"
              :key="index"
              class="w-6 h-6 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 border-2 border-white flex items-center justify-center text-xs text-white font-medium"
              :title="contributor"
            >
              {{ contributor.charAt(0).toUpperCase() }}
            </div>
          </div>
          <span>{{ contributors.length }} contributors</span>
        </div>

        <!-- History Button -->
        <button class="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50 bg-white">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>History: {{ commitCount }} commits</span>
        </button>

        <!-- Contribute Button -->
        <button class="flex items-center space-x-1 px-3 py-1.5 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-md">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Contribute</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Breadcrumb Navigation -->
    <div class="flex items-center space-x-2 text-sm text-gray-600 mb-4">
      <button
        @click="navigateToFolder('')"
        class="hover:text-blue-600 flex items-center space-x-1"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      </button>
      <template v-for="(segment, index) in breadcrumbSegments" :key="index">
        <span class="text-gray-400">/</span>
        <button
          @click="navigateToBreadcrumb(index)"
          class="hover:text-blue-600"
          :class="{ 'text-gray-900 font-medium': index === breadcrumbSegments.length - 1 }"
        >
          {{ segment }}
        </button>
      </template>
    </div>

    <!-- Files Table -->
    <div class="border border-gray-200 rounded-lg overflow-hidden">
      <!-- Table Header -->
      <div class="bg-gray-50 px-4 py-2 border-b border-gray-200 flex items-center text-sm font-medium text-gray-700">
        <div class="flex-1">Name</div>
        <div class="w-32 text-right">Size</div>
        <div class="w-48 text-left ml-8">Last commit</div>
        <div class="w-32 text-right">Updated</div>
      </div>

      <!-- Parent Directory Link -->
      <div v-if="currentPath" class="border-b border-gray-100">
        <button
          @click="navigateToParent"
          class="w-full px-4 py-3 flex items-center text-sm text-gray-600 hover:bg-gray-50"
        >
          <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
          <span>..</span>
        </button>
      </div>

      <!-- File List -->
      <div v-for="item in sortedFiles" :key="item.path" class="border-b border-gray-100 last:border-b-0">
        <button
          @click="handleItemClick(item)"
          class="w-full px-4 py-3 flex items-center text-sm hover:bg-gray-50 text-left"
        >
          <!-- Icon -->
          <div class="flex-shrink-0 mr-3">
            <svg v-if="item.type === 'directory'" class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
            </svg>
            <svg v-else class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>

          <!-- Name -->
          <div class="flex-1 min-w-0">
            <span class="text-gray-900 font-medium truncate" :class="{ 'text-blue-600': item.type === 'directory' }">
              {{ item.name }}
            </span>
            <span v-if="item.isSafe" class="ml-2 inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
              Safe
            </span>
          </div>

          <!-- Size -->
          <div class="w-32 text-right text-gray-600">
            {{ item.type === 'directory' ? '-' : formatFileSize(item.size) }}
          </div>

          <!-- Last Commit -->
          <div class="w-48 ml-8 flex items-center space-x-2 text-gray-600 truncate">
            <span class="font-mono text-xs text-gray-500">{{ item.lastCommitHash }}</span>
            <span class="truncate">{{ item.lastCommitMessage }}</span>
          </div>

          <!-- Updated Time -->
          <div class="w-32 text-right text-gray-500">
            {{ formatRelativeTime(item.lastModified) }}
          </div>

          <!-- Download Button for Files -->
          <button
            v-if="item.type === 'file'"
            @click.stop="downloadFile(item)"
            class="ml-4 p-1 text-gray-400 hover:text-gray-600"
            title="Download"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="sortedFiles.length === 0" class="px-4 py-8 text-center text-gray-500">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <p>This folder is empty</p>
      </div>
    </div>

    <!-- README Preview -->
    <div v-if="readmeContent" class="mt-6 border border-gray-200 rounded-lg overflow-hidden">
      <div class="bg-gray-50 px-4 py-2 border-b border-gray-200 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="text-sm font-medium text-gray-700">README.md</span>
        </div>
        <button class="text-sm text-blue-600 hover:underline">View raw</button>
      </div>
      <div class="p-4 prose prose-sm max-w-none">
        <pre class="whitespace-pre-wrap text-sm text-gray-700">{{ readmeContent }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  datasetId: {
    type: String,
    required: true
  }
})

// Mock data - In real implementation, these would come from API
const currentBranch = ref('main')
const branches = ['main', 'dev', 'v1.0', 'v2.0']
const showBranchDropdown = ref(false)
const currentPath = ref('')

const contributors = ['OmniLottie', 'contributor1', 'contributor2']
const commitCount = 19
const totalSize = '93.5 GB'

// Mock file structure
const fileStructure = [
  {
    name: 'data',
    path: 'data',
    type: 'directory',
    lastCommitMessage: 'Add Lottie_SVG split',
    lastCommitHash: 'b53c397',
    lastModified: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000),
    children: [
      {
        name: 'train',
        path: 'data/train',
        type: 'directory',
        lastCommitMessage: 'Add training data',
        lastCommitHash: 'a1b2c3d',
        lastModified: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
        children: []
      },
      {
        name: 'validation',
        path: 'data/validation',
        type: 'directory',
        lastCommitMessage: 'Add validation data',
        lastCommitHash: 'e4f5g6h',
        lastModified: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
        children: []
      }
    ]
  },
  {
    name: '.gitattributes',
    path: '.gitattributes',
    type: 'file',
    size: 130,
    lastCommitMessage: 'Initial commit: Upload MMLottie...',
    lastCommitHash: 'f7g8h9i',
    lastModified: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000),
    isSafe: true
  },
  {
    name: 'README.md',
    path: 'README.md',
    type: 'file',
    size: 8350,
    lastCommitMessage: 'Update README.md',
    lastCommitHash: 'b53c397',
    lastModified: new Date(Date.now() - 22 * 60 * 60 * 1000),
    isSafe: true
  },
  {
    name: 'dataset_info.json',
    path: 'dataset_info.json',
    type: 'file',
    size: 2048,
    lastCommitMessage: 'Add dataset metadata',
    lastCommitHash: 'c4d5e6f',
    lastModified: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    isSafe: true
  },
  {
    name: 'LICENSE',
    path: 'LICENSE',
    type: 'file',
    size: 11357,
    lastCommitMessage: 'Add license',
    lastCommitHash: 'd6e7f8g',
    lastModified: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000)
  }
]

const readmeContent = ref(`# ${props.datasetId}

This dataset contains 2M Lottie animations for multi-modal learning.

## Dataset Structure

- data/: Contains train and validation splits
- dataset_info.json: Metadata about the dataset

## Usage

\`\`\`python
from datasets import load_dataset

dataset = load_dataset("${props.datasetId}")
\`\`\``)

// Computed
const breadcrumbSegments = computed(() => {
  return currentPath.value ? currentPath.value.split('/').filter(Boolean) : []
})

const currentFiles = computed(() => {
  if (!currentPath.value) {
    return fileStructure
  }
  
  // Navigate to current path
  const parts = currentPath.value.split('/').filter(Boolean)
  let current = fileStructure
  
  for (const part of parts) {
    const folder = current.find(item => item.name === part && item.type === 'directory')
    if (folder && folder.children) {
      current = folder.children
    } else {
      return []
    }
  }
  
  return current
})

const sortedFiles = computed(() => {
  // Directories first, then files
  return [...currentFiles.value].sort((a, b) => {
    if (a.type === 'directory' && b.type !== 'directory') return -1
    if (a.type !== 'directory' && b.type === 'directory') return 1
    return a.name.localeCompare(b.name)
  })
})

// Methods
function selectBranch(branch) {
  currentBranch.value = branch
  showBranchDropdown.value = false
}

function navigateToFolder(path) {
  currentPath.value = path
}

function navigateToParent() {
  const parts = currentPath.value.split('/').filter(Boolean)
  parts.pop()
  currentPath.value = parts.join('/')
}

function navigateToBreadcrumb(index) {
  const parts = breadcrumbSegments.value.slice(0, index + 1)
  currentPath.value = parts.join('/')
}

function handleItemClick(item) {
  if (item.type === 'directory') {
    currentPath.value = item.path
  } else {
    // Preview file or navigate to file view
    console.log('Open file:', item.path)
  }
}

function downloadFile(item) {
  console.log('Download file:', item.path)
  // Implement download logic
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatRelativeTime(date) {
  const now = new Date()
  const diff = now - new Date(date)
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) {
    return days === 1 ? '1 day ago' : days + ' days ago'
  }
  if (hours > 0) {
    return hours === 1 ? 'about 1 hour ago' : 'about ' + hours + ' hours ago'
  }
  if (minutes > 0) {
    return minutes === 1 ? '1 minute ago' : minutes + ' minutes ago'
  }
  return 'just now'
}
</script>

<style scoped>
.dataset-files {
  width: 100%;
}
</style>