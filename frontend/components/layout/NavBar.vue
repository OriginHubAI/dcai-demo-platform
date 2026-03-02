<template>
  <aside 
    class="fixed left-0 top-0 h-full flex flex-col z-50 shadow-lg transition-all duration-300 ease-in-out"
    :class="[
      isCollapsed ? 'w-16' : 'w-60',
      'bg-slate-100 border-r border-slate-200'
    ]"
  >
    <!-- Logo & Toggle -->
    <div 
      class="h-16 flex items-center border-b border-slate-200"
      :class="isCollapsed ? 'justify-center px-2' : 'px-5'"
    >
      <router-link to="/" class="flex items-center gap-3 group" v-if="!isCollapsed">
        <div class="relative">
          <img src="/logo.png" alt="DCAI" class="w-9 h-9 rounded-lg shadow-md group-hover:scale-105 transition-transform duration-300" />
        </div>
        <div class="flex flex-col">
          <span class="text-lg font-bold text-slate-800 tracking-tight">{{ t('app.title') }}</span>
          <span class="text-[10px] text-slate-500 -mt-1">{{ t('app.subtitle') }}</span>
        </div>
      </router-link>
      <router-link to="/" class="flex items-center justify-center" v-else>
        <img src="/logo.png" alt="DCAI" class="w-9 h-9 rounded-lg shadow-md hover:scale-105 transition-transform duration-300" />
      </router-link>
      
      <!-- Collapse Toggle Button (only show when expanded) -->
      <button 
        v-if="!isCollapsed"
        @click="toggleCollapse"
        class="ml-auto p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-all duration-200"
        :title="t('nav.collapseSidebar')"
      >
        <ChevronLeftIcon class="w-4 h-4" />
      </button>
    </div>

    <!-- Expand Toggle Button (only show when collapsed, positioned at top) -->
    <button 
      v-if="isCollapsed"
      @click="toggleCollapse"
      class="absolute -right-3 top-20 w-6 h-6 bg-white border border-slate-200 rounded-full shadow-md flex items-center justify-center text-slate-400 hover:text-slate-600 hover:shadow-lg transition-all duration-200 z-50"
      :title="t('nav.expandSidebar')"
    >
      <ChevronRightIcon class="w-3 h-3" />
    </button>

    <!-- Nav Links -->
    <nav class="flex-1 py-4 overflow-y-auto" :class="isCollapsed ? 'px-2 overflow-x-hidden scrollbar-hide' : 'px-3'">
      <div v-if="!isCollapsed" class="px-3 mb-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">{{ t('nav.menu') }}</div>
      <div v-else class="mb-2 text-center">
        <div class="w-8 h-px bg-slate-200 mx-auto"></div>
      </div>
      
      <template v-for="link in navLinks" :key="link.to">
        <!-- Dropdown for DataFlow -->
        <div v-if="link.children" class="relative">
          <button
            v-if="!isCollapsed"
            @click="toggleDropdown(link.to)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200"
            :class="isActive(link.to) ? 'bg-slate-100 text-slate-900' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'"
          >
            <div class="flex items-center gap-3">
              <component :is="link.icon" class="w-5 h-5" :class="isActive(link.to) ? 'text-dc-primary' : 'text-slate-400'" />
              <span>{{ t(link.labelKey) }}</span>
            </div>
            <svg 
              class="w-4 h-4 transition-transform duration-200 text-slate-400" 
              :class="{ 'rotate-90': dropdownOpen[link.to] }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
          
          <!-- Collapsed: Show children icons -->
          <div v-else class="flex flex-col items-center gap-1">
            <router-link
              :to="link.to"
              class="w-full flex items-center justify-center p-2 rounded-xl transition-all duration-200"
              :class="isActive(link.to) ? 'bg-slate-100 text-dc-primary' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'"
            >
              <component :is="link.icon" class="w-5 h-5" />
            </router-link>
            <!-- Child item icons -->
            <div class="flex flex-col gap-1 py-1">
              <router-link
                v-for="child in link.children"
                :key="child.to"
                :to="child.to"
                class="flex items-center justify-center p-1.5 rounded-lg transition-all duration-200 relative group"
                :class="route.path === child.to ? 'bg-slate-100 text-dc-primary' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-50'"
              >
                <component :is="child.iconComponent" class="w-4 h-4" />
                <!-- Tooltip for collapsed child icons -->
                <div class="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1 bg-slate-800 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
                  {{ t(child.labelKey) }}
                </div>
              </router-link>
            </div>
          </div>
          
          <!-- Dropdown menu (only when expanded) -->
          <div
            v-show="dropdownOpen[link.to] && !isCollapsed"
            class="mt-1 space-y-0.5 pl-4 animate-slideDown"
          >
              <router-link
                v-for="child in link.children"
                :key="child.to"
                :to="child.to"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200"
                :class="route.path === child.to ? 'bg-slate-50 text-dc-primary font-medium' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'"
              >
                <component :is="child.iconComponent" class="w-4 h-4" />
                <span>{{ t(child.labelKey) }}</span>
              </router-link>
          </div>
          
          <!-- Collapsed: Show children on hover -->
          <div
            v-if="isCollapsed && dropdownOpen[link.to]"
            class="absolute left-full top-0 ml-2 w-40 bg-white rounded-xl shadow-xl border border-slate-100 py-2 z-50"
          >
            <div class="px-3 py-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">{{ t(link.labelKey) }}</div>
            <router-link
              v-for="child in link.children"
              :key="child.to"
              :to="child.to"
              class="flex items-center gap-2 px-3 py-2 text-sm transition-all duration-200"
              :class="route.path === child.to ? 'bg-slate-50 text-dc-primary font-medium' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-800'"
              @click="dropdownOpen[link.to] = false"
            >
              <component :is="child.iconComponent" class="w-4 h-4" />
              <span>{{ t(child.labelKey) }}</span>
            </router-link>
          </div>
        </div>
        
        <!-- Regular link -->
        <router-link
          v-if="!link.children"
          :to="link.to"
          class="flex items-center rounded-xl text-sm font-medium transition-all duration-200 group relative"
          :class="[
            isCollapsed ? 'justify-center p-2.5' : 'gap-3 px-3 py-2.5',
            isActive(link.to) ? 'bg-slate-100 text-slate-900' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
          ]"
        >
          <component :is="link.icon" class="w-5 h-5 transition-colors" :class="isActive(link.to) ? 'text-dc-primary' : 'text-slate-400 group-hover:text-slate-500'" />
          <span v-if="!isCollapsed">{{ t(link.labelKey) }}</span>
          <div v-if="isActive(link.to) && !isCollapsed" class="ml-auto w-1.5 h-1.5 rounded-full bg-dc-primary"></div>
          
          <!-- Tooltip for collapsed state -->
          <div v-if="isCollapsed" class="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1 bg-slate-800 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
            {{ t(link.labelKey) }}
          </div>
        </router-link>
      </template>
    </nav>

    <!-- Help & Support -->
    <div class="border-t border-slate-200" :class="isCollapsed ? 'p-2' : 'p-3'">
      <button 
        class="flex items-center rounded-xl transition-all duration-200 group relative"
        :class="[
          isCollapsed ? 'justify-center p-2.5 w-full' : 'gap-3 px-3 py-2.5 w-full text-slate-600 hover:text-slate-900 hover:bg-slate-50',
        ]"
      >
        <div 
          class="flex items-center justify-center rounded-lg transition-colors"
          :class="isCollapsed ? 'w-8 h-8 bg-slate-100 text-slate-500' : 'w-8 h-8 bg-slate-100 text-slate-500 group-hover:bg-slate-200'"
        >
          <QuestionMarkCircleIcon class="w-4 h-4" />
        </div>
        <span v-if="!isCollapsed" class="font-medium text-sm">{{ t('nav.helpSupport') }}</span>
        
        <!-- Tooltip for collapsed state -->
        <div v-if="isCollapsed" class="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1 bg-slate-800 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
          {{ t('nav.helpSupport') }}
        </div>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { reactive, ref, h } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const isCollapsed = ref(false)
const dropdownOpen = reactive({
  '/dataflow/canvas': true,
})

const { t } = useI18n()

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
  // Emit event to parent to adjust main content
  window.dispatchEvent(new CustomEvent('sidebar-toggle', { detail: { collapsed: isCollapsed.value } }))
}

// Icon components
const ChevronLeftIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 19l-7-7 7-7' })
])

const ChevronRightIcon = () => h('svg', { class: 'w-3 h-3', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5l7 7-7 7' })
])

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

const TasksIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' })
])

const BookOpenIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const SparklesIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z' })
])

const QuestionMarkCircleIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const navLinks = [
  { to: '/datasets', labelKey: 'nav.datasets', icon: DatabaseIcon },
  { to: '/knowledge-base', labelKey: 'nav.knowledgeBase', icon: BookOpenIcon },
  {
    to: '/dataflow/canvas',
    labelKey: 'nav.dataflow',
    icon: FlowIcon,
    children: [
      { to: '/dataflow/canvas', labelKey: 'nav.canvas', iconComponent: CanvasIcon },
      { to: '/dataflow', labelKey: 'nav.packages', iconComponent: PackageIcon },
    ],
  },
  { to: '/dataflow/tasks', labelKey: 'nav.tasks', icon: TasksIcon },
  { to: '/apps', labelKey: 'nav.apps', icon: RocketIcon },
  { to: '/models', labelKey: 'nav.models', icon: CubeIcon },
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

/* Hide scrollbars when sidebar is collapsed */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
