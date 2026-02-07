<template>
  <div class="min-h-screen flex flex-col">
    <NavBar />
    <main class="flex-1">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from './components/layout/NavBar.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>
