<template>
  <header class="h-16 bg-white/80 backdrop-blur-xl border-b border-slate-200/60 flex items-center justify-between px-6 sticky top-0 z-40 shadow-sm">
    <!-- Left: Breadcrumb / Page Title -->
    <div class="flex items-center">
      <nav class="flex items-center text-sm">
        <router-link to="/" class="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100/80 transition-all duration-200">
          <HomeIcon class="w-5 h-5" />
        </router-link>
        <template v-if="pageTitle">
          <ChevronRightIcon class="w-4 h-4 mx-1 text-slate-300" />
          <span class="font-semibold text-slate-800 tracking-tight">{{ pageTitle }}</span>
        </template>
      </nav>
    </div>

    <!-- Center: Global Search -->
    <div class="flex-1 max-w-xl mx-8">
      <div class="relative group">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <SearchIcon class="w-4 h-4 text-slate-400 group-focus-within:text-dc-primary transition-colors" />
        </div>
        <input
          type="text"
          :placeholder="t('header.searchPlaceholder')"
          class="w-full pl-11 pr-12 py-2.5 text-sm bg-slate-50/80 border border-slate-200/60 rounded-xl focus:outline-none focus:ring-2 focus:ring-dc-primary/20 focus:border-dc-primary/50 focus:bg-white transition-all duration-200 placeholder:text-slate-400"
          @keydown.enter="handleSearch"
          v-model="searchQuery"
        />
        <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
          <kbd class="hidden sm:flex items-center gap-0.5 px-2 py-1 text-[10px] font-semibold text-slate-400 bg-slate-100 rounded-md border border-slate-200">
            <span>⌘</span><span>K</span>
          </kbd>
        </div>
      </div>
    </div>

    <!-- Right: Actions & User -->
    <div class="flex items-center gap-2">
      <!-- New Button -->
      <button class="hidden sm:flex items-center gap-2 bg-dc-primary hover:bg-dc-primary-dark text-white text-sm font-semibold px-4 py-2 rounded-xl transition-all duration-200 shadow-lg shadow-dc-primary/25 hover:shadow-xl hover:shadow-dc-primary/30 hover:-translate-y-0.5">
        <PlusIcon class="w-4 h-4" />
        <span>New</span>
      </button>

      <!-- Language Toggle -->
      <div class="relative">
        <button
          @click="showLanguageMenu = !showLanguageMenu"
          class="p-2.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100/80 rounded-xl transition-all duration-200"
          :class="{ 'bg-slate-100/80': showLanguageMenu }"
        >
          <GlobeIcon class="w-5 h-5" />
        </button>

        <!-- Language Dropdown -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          enter-from-class="opacity-0 scale-95 -translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition-all duration-150 ease-in"
          leave-from-class="opacity-100 scale-100 translate-y-0"
          leave-to-class="opacity-0 scale-95 -translate-y-2"
        >
          <div v-if="showLanguageMenu" class="absolute right-0 mt-2 w-40 bg-white rounded-2xl shadow-2xl border border-slate-100 py-2 z-50 overflow-hidden">
            <button
              @click="setLanguage('zh')"
              class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors"
              :class="currentLocale === 'zh' ? 'bg-slate-50 text-dc-primary font-medium' : 'text-slate-700 hover:bg-slate-50 hover:text-dc-primary'"
            >
              简体中文
            </button>
            <button
              @click="setLanguage('zh-Hant')"
              class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors"
              :class="currentLocale === 'zh-Hant' ? 'bg-slate-50 text-dc-primary font-medium' : 'text-slate-700 hover:bg-slate-50 hover:text-dc-primary'"
            >
              繁體中文
            </button>
            <button
              @click="setLanguage('en')"
              class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors"
              :class="currentLocale === 'en' ? 'bg-slate-50 text-dc-primary font-medium' : 'text-slate-700 hover:bg-slate-50 hover:text-dc-primary'"
            >
              English
            </button>
          </div>
        </Transition>
      </div>

      <!-- Notifications -->
      <button class="relative p-2.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100/80 rounded-xl transition-all duration-200">
        <BellIcon class="w-5 h-5" />
        <span class="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full ring-2 ring-white animate-pulse"></span>
      </button>

      <!-- User Menu -->
      <div class="relative ml-1">
        <button 
          @click="showUserMenu = !showUserMenu"
          class="flex items-center gap-2 p-1.5 pr-3 rounded-xl hover:bg-slate-100/80 transition-all duration-200 group"
          :class="{ 'bg-slate-100/80': showUserMenu }"
        >
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-dc-primary via-dc-primary to-dc-accent flex items-center justify-center text-white text-sm font-bold shadow-md group-hover:shadow-lg transition-shadow">
            U
          </div>
          <ChevronDownIcon class="w-4 h-4 text-slate-400 transition-transform duration-200" :class="{ 'rotate-180': showUserMenu }" />
        </button>

        <!-- Dropdown -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          enter-from-class="opacity-0 scale-95 -translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition-all duration-150 ease-in"
          leave-from-class="opacity-100 scale-100 translate-y-0"
          leave-to-class="opacity-0 scale-95 -translate-y-2"
        >
          <div v-if="showUserMenu" class="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl border border-slate-100 py-2 z-50 overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100">
              <p class="text-sm font-bold text-slate-900">User Name</p>
              <p class="text-xs text-slate-500 mt-0.5">user@example.com</p>
            </div>
            <div class="py-1">
              <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-dc-primary transition-colors">
                <UserIcon class="w-4 h-4 text-slate-400" />
                {{ t('header.profile') }}
              </a>
              <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-dc-primary transition-colors">
                <CogIcon class="w-4 h-4 text-slate-400" />
                {{ t('header.settings') }}
              </a>
              <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-dc-primary transition-colors">
                <KeyIcon class="w-4 h-4 text-slate-400" />
                API Keys
              </a>
            </div>
            <div class="border-t border-slate-100 mt-1 pt-1">
              <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors">
                <LogoutIcon class="w-4 h-4" />
                {{ t('header.logout') }}
              </a>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const showUserMenu = ref(false)
const showLanguageMenu = ref(false)

const { locale, t } = useI18n()
const currentLocale = computed(() => locale.value)

function setLanguage(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
  showLanguageMenu.value = false
}

// Icon components
const HomeIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
])

const ChevronRightIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5l7 7-7 7' })
])

const SearchIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
])

const PlusIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4v16m8-8H4' })
])

const BellIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' })
])

const ChevronDownIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 9l-7 7-7-7' })
])

const UserIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
])

const CogIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const KeyIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z' })
])

const LogoutIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1' })
])

const GlobeIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9' })
])

// Page title based on route
const pageTitle = computed(() => {
  const titleKeys = {
    '/': '',
    '/datasets': 'nav.datasets',
    '/datasets/': 'nav.datasets',
    '/models': 'nav.models',
    '/models/': 'nav.models',
    '/spaces': 'nav.spaces',
    '/spaces/': 'nav.spaces',
    '/dataflow': 'nav.packages',
    '/dataflow/canvas': 'nav.canvas',
    '/dataflow/tasks': 'nav.tasks',
  }
  
  if (titleKeys[route.path]) {
    return titleKeys[route.path] ? t(titleKeys[route.path]) : ''
  }
  
  for (const [path, key] of Object.entries(titleKeys)) {
    if (path.endsWith('/') && route.path.startsWith(path)) {
      return key ? t(key) : ''
    }
  }
  
  return ''
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/datasets', query: { search: searchQuery.value.trim() } })
    searchQuery.value = ''
  }
}

// Close menus when clicking outside
function handleClickOutside(e) {
  if (!e.target.closest('.relative')) {
    showUserMenu.value = false
    showLanguageMenu.value = false
  }
}

// Close menus on escape key
function handleKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    document.querySelector('input[type="text"]')?.focus()
  }
  if (e.key === 'Escape') {
    showUserMenu.value = false
    showLanguageMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('click', handleClickOutside)
})
</script>
