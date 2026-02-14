<template>
  <aside class="fixed left-0 top-0 h-full w-60 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 flex flex-col z-50 shadow-2xl">
    <!-- Logo -->
    <div class="h-16 flex items-center px-5 border-b border-slate-700/50">
      <router-link to="/" class="flex items-center gap-3 group">
        <div class="relative">
          <img src="/logo.png" alt="DCAI" class="w-9 h-9 rounded-lg shadow-lg group-hover:scale-105 transition-transform duration-300" />
          <div class="absolute inset-0 rounded-lg bg-dc-primary/20 blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
        <div class="flex flex-col">
          <span class="text-lg font-bold text-white tracking-tight">Sci-DCAI</span>
          <span class="text-[10px] text-slate-400 -mt-1">AI Platform</span>
        </div>
      </router-link>
    </div>

    <!-- Nav Links -->
    <nav class="flex-1 py-4 px-3 space-y-0.5 overflow-y-auto">
      <div class="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Menu</div>
      <template v-for="link in navLinks" :key="link.to">
        <!-- Dropdown for DataFlow -->
        <div v-if="link.children" class="relative">
          <button
            @click="toggleDropdown(link.to)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200"
            :class="isActive(link.to) ? 'bg-gradient-to-r from-dc-primary/20 to-transparent text-white shadow-sm' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'"
          >
            <div class="flex items-center gap-3">
              <component :is="link.icon" class="w-5 h-5" :class="isActive(link.to) ? 'text-dc-primary' : 'text-slate-400'" />
              <span>{{ link.label }}</span>
            </div>
            <svg 
              class="w-4 h-4 transition-transform duration-200" 
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
            class="mt-1 space-y-0.5 pl-4 animate-slideDown"
          >
            <router-link
              v-for="child in link.children"
              :key="child.to"
              :to="child.to"
              class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200"
              :class="route.path === child.to ? 'bg-dc-primary/10 text-dc-primary font-medium' : 'text-slate-400 hover:bg-slate-700/30 hover:text-slate-200'"
            >
              <component :is="child.iconComponent" class="w-4 h-4" />
              <span>{{ child.label }}</span>
            </router-link>
          </div>
        </div>
        <!-- Regular link -->
        <router-link
          v-else
          :to="link.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group"
          :class="isActive(link.to) ? 'bg-gradient-to-r from-dc-primary/20 to-transparent text-white shadow-sm' : 'text-slate-300 hover:text-white hover:bg-slate-700/50'"
        >
          <component :is="link.icon" class="w-5 h-5 transition-colors" :class="isActive(link.to) ? 'text-dc-primary' : 'text-slate-400 group-hover:text-slate-300'" />
          <span>{{ link.label }}</span>
          <div v-if="isActive(link.to)" class="ml-auto w-1.5 h-1.5 rounded-full bg-dc-primary shadow-lg shadow-dc-primary/50"></div>
        </router-link>
      </template>
    </nav>

    <!-- Help & Support -->
    <div class="p-3 border-t border-slate-700/50">
      <button class="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-xl transition-all duration-200 group">
        <div class="w-8 h-8 rounded-lg bg-slate-700/50 flex items-center justify-center group-hover:bg-slate-600/50 transition-colors">
          <QuestionMarkCircleIcon class="w-4 h-4" />
        </div>
        <span class="font-medium">Help & Support</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { reactive, h } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const dropdownOpen = reactive({
  '/dataflow': true,
})

// Icon components
const DatabaseIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4' })
])

const FlowIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
])

const RocketIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16 8l2-2' })
])

const CubeIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' })
])

const PackageIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' })
])

const CanvasIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10 0a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z' })
])

const TasksIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' })
])

const QuestionMarkCircleIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const navLinks = [
  { to: '/datasets', label: 'Datasets', icon: DatabaseIcon },
  {
    to: '/dataflow',
    label: 'DataFlow',
    icon: FlowIcon,
    children: [
      { to: '/dataflow', label: 'Packages', iconComponent: PackageIcon },
      { to: '/dataflow/canvas', label: 'Canvas', iconComponent: CanvasIcon },
      { to: '/dataflow/tasks', label: 'Tasks', iconComponent: TasksIcon },
    ],
  },
  { to: '/spaces', label: 'Spaces', icon: RocketIcon },
  { to: '/models', label: 'Models', icon: CubeIcon },
]

function toggleDropdown(key) {
  dropdownOpen[key] = !dropdownOpen[key]
}

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style scoped>
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideDown {
  animation: slideDown 0.2s ease-out;
}
</style>
