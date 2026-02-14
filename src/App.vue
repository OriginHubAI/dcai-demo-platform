<template>
  <div class="min-h-screen flex bg-slate-50/50">
    <!-- Sidebar -->
    <NavBar />
    
    <!-- Main Content Area -->
    <main class="flex-1 ml-60 flex flex-col min-h-screen">
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
import NavBar from './components/layout/NavBar.vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>
