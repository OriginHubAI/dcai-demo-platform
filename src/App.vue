<template>
  <div class="min-h-screen flex bg-slate-50">
    <!-- Sidebar -->
    <NavBar />
    
    <!-- Main Content Area -->
    <main 
      class="flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out"
      :class="sidebarCollapsed ? 'ml-16' : 'ml-60'"
    >
      <!-- Top Header -->
      <AppHeader />
      
      <!-- Page Content -->
      <div class="flex-1 p-6">
        <router-view />
      </div>
      
      <!-- Footer -->
      <AppFooter />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import NavBar from './components/layout/NavBar.vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'

const sidebarCollapsed = ref(false)

function handleSidebarToggle(e) {
  sidebarCollapsed.value = e.detail.collapsed
}

onMounted(() => {
  window.addEventListener('sidebar-toggle', handleSidebarToggle)
})

onUnmounted(() => {
  window.removeEventListener('sidebar-toggle', handleSidebarToggle)
})
</script>
