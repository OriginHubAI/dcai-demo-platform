<template>
  <div class="min-h-screen flex">
    <NavBar />
    <main class="flex-1 ml-56 flex flex-col">
      <div class="p-6 flex-1">
        <router-view />
      </div>
      <AppFooter />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/layout/NavBar.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>
