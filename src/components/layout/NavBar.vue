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
            <template v-for="link in navLinks" :key="link.to">
              <!-- Dropdown for DataFlow -->
              <div v-if="link.children" class="relative" @mouseenter="openDropdown(link.to)" @mouseleave="closeDropdown(link.to)">
                <router-link
                  :to="link.to"
                  class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors inline-flex items-center gap-1"
                  :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
                >
                  {{ link.label }}
                  <svg class="w-3.5 h-3.5 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </router-link>
                <div
                  v-show="dropdownOpen[link.to]"
                  class="absolute left-0 top-full mt-0.5 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50"
                >
                  <router-link
                    v-for="child in link.children"
                    :key="child.to"
                    :to="child.to"
                    class="flex items-center gap-2 px-4 py-2 text-sm transition-colors"
                    :class="route.path === child.to ? 'bg-gray-50 text-dc-primary font-medium' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
                  >
                    <svg v-if="child.icon === 'package'" class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                    <svg v-else-if="child.icon === 'canvas'" class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"/>
                    </svg>
                    <svg v-else-if="child.icon === 'tasks'" class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
                :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
              >
                {{ link.label }}
              </router-link>
            </template>
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
      <template v-for="link in navLinks" :key="link.to">
        <template v-if="link.children">
          <div class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">{{ link.label }}</div>
          <router-link
            v-for="child in link.children"
            :key="child.to"
            :to="child.to"
            class="block px-3 py-2 pl-6 rounded-md text-sm font-medium"
            :class="route.path === child.to ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50'"
            @click="mobileOpen = false"
          >
            {{ child.label }}
          </router-link>
        </template>
        <router-link
          v-else
          :to="link.to"
          class="block px-3 py-2 rounded-md text-sm font-medium"
          :class="isActive(link.to) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50'"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const mobileOpen = ref(false)
const searchQuery = ref('')
const dropdownOpen = reactive({})
let dropdownTimer = null

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

function openDropdown(key) {
  clearTimeout(dropdownTimer)
  dropdownOpen[key] = true
}

function closeDropdown(key) {
  dropdownTimer = setTimeout(() => {
    dropdownOpen[key] = false
  }, 150)
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
