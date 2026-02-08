<template>
  <nav class="sticky top-0 z-50 bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14">
        <!-- Logo -->
        <div class="flex items-center space-x-6">
          <router-link to="/" class="flex items-center space-x-2 text-lg font-bold text-gray-900 hover:text-dc-primary">
            <img src="/logo.png" alt="DCAI" class="w-8 h-8" />
            <span class="hidden sm:inline">DCAI Platform</span>
          </router-link>
          <!-- Nav Links -->
          <div class="hidden md:flex items-center space-x-1">
            <router-link
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
            >
              {{ link.label }}
            </router-link>
          </div>
        </div>

        <!-- Right side -->
        <div class="flex items-center space-x-3">
          <!-- Search -->
          <div class="hidden sm:block relative">
            <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              type="text"
              placeholder="Search models, datasets, users..."
              class="w-64 pl-8 pr-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-dc-primary focus:border-transparent"
              @keydown.enter="handleSearch"
              v-model="searchQuery"
            />
          </div>
          <!-- Auth buttons -->
          <button class="text-sm text-gray-600 hover:text-gray-900 font-medium px-3 py-1.5">Log In</button>
          <button class="text-sm bg-dc-primary text-white font-medium px-3 py-1.5 rounded-lg hover:bg-dc-primary-dark transition-colors">Sign Up</button>
          <!-- Mobile menu button -->
          <button @click="mobileOpen = !mobileOpen" class="md:hidden p-1.5 rounded-md text-gray-500 hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <!-- Mobile menu -->
    <div v-if="mobileOpen" class="md:hidden border-t border-gray-200 bg-white px-4 py-3 space-y-1">
      <router-link
        v-for="link in navLinks"
        :key="link.to"
        :to="link.to"
        class="block px-3 py-2 rounded-md text-sm font-medium"
        :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50'"
        @click="mobileOpen = false"
      >
        {{ link.label }}
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const mobileOpen = ref(false)
const searchQuery = ref('')

const navLinks = [
  { to: '/models', label: 'Models' },
  { to: '/datasets', label: 'Datasets' },
  { to: '/spaces', label: 'Spaces' },
]

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
