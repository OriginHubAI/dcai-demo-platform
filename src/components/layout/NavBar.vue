<template>
  <aside class="fixed left-0 top-0 h-full w-56 bg-white border-r border-gray-200 flex flex-col z-50">
    <!-- Logo -->
    <div class="h-14 flex items-center px-4 border-b border-gray-200">
      <router-link to="/" class="flex items-center space-x-2 text-lg font-bold text-gray-900 hover:text-dc-primary">
        <img src="/logo.png" alt="DCAI" class="w-8 h-8" />
        <span>Sci-DCAI</span>
      </router-link>
    </div>

    <!-- Search -->
    <div class="p-4 border-b border-gray-200">
      <div class="relative">
        <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          type="text"
          placeholder="Search..."
          class="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-dc-primary focus:border-transparent"
          @keydown.enter="handleSearch"
          v-model="searchQuery"
        />
      </div>
    </div>

    <!-- Nav Links -->
    <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
      <template v-for="link in navLinks" :key="link.to">
        <!-- Dropdown for DataFlow -->
        <div v-if="link.children" class="relative">
          <button
            @click="toggleDropdown(link.to)"
            class="w-full flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
          >
            <span>{{ link.label }}</span>
            <svg 
              class="w-4 h-4 transition-transform" 
              :class="{ 'rotate-90': dropdownOpen[link.to] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
          <div
            v-show="dropdownOpen[link.to]"
            class="ml-3 mt-1 space-y-1 border-l-2 border-gray-100 pl-3"
          >
            <router-link
              v-for="child in link.children"
              :key="child.to"
              :to="child.to"
              class="flex items-center gap-2 px-3 py-1.5 rounded-md text-sm transition-colors"
              :class="route.path === child.to ? 'bg-gray-100 text-dc-primary font-medium' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
            >
              <svg v-if="child.icon === 'package'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
              </svg>
              <svg v-else-if="child.icon === 'canvas'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"/>
              </svg>
              <svg v-else-if="child.icon === 'tasks'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
              </svg>
              {{ child.label }}
            </router-link>
          </div>
        </div>
        <!-- Regular link -->
        <router-link
          v-else
          :to="link.to"
          class="flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors"
          :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
        >
          {{ link.label }}
        </router-link>
      </template>
    </nav>

    <!-- Auth buttons -->
    <div class="p-4 border-t border-gray-200 space-y-2">
      <button class="w-full text-sm text-gray-600 hover:text-gray-900 font-medium px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors text-left">Log In</button>
      <button class="w-full text-sm bg-dc-primary text-white font-medium px-3 py-1.5 rounded-lg hover:bg-dc-primary-dark transition-colors">Sign Up</button>
    </div>
  </aside>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const dropdownOpen = reactive({
  '/dataflow': true, // DataFlow dropdown open by default
})

const navLinks = [
  { to: '/datasets', label: 'Datasets' },
  {
    to: '/dataflow',
    label: 'DataFlow',
    children: [
      { to: '/dataflow', label: 'Packages', icon: 'package' },
      { to: '/dataflow/canvas', label: 'Canvas', icon: 'canvas' },
      { to: '/dataflow/tasks', label: 'Tasks', icon: 'tasks' },
    ],
  },
  { to: '/spaces', label: 'Spaces' },
  { to: '/models', label: 'Models' },
]

function toggleDropdown(key) {
  dropdownOpen[key] = !dropdownOpen[key]
}

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/models', query: { search: searchQuery.value.trim() } })
    searchQuery.value = ''
  }
}
</script>
