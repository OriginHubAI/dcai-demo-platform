<template>
  <div>
    <HeroSection />
    <TrendingSection />
    <!-- Organizations section -->
    <section class="bg-slate-50 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-center text-sm font-semibold text-slate-400 uppercase tracking-wide mb-8">
          Trusted by leading AI organizations
        </h2>
        <div class="flex flex-wrap items-center justify-center gap-8 sm:gap-12">
          <span v-for="org in orgs" :key="org" class="text-xl font-bold text-slate-300 hover:text-slate-400 transition-colors cursor-default">
            {{ org }}
          </span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import HeroSection from '@/components/home/HeroSection.vue'
import TrendingSection from '@/components/home/TrendingSection.vue'

const orgs = ['Meta AI', 'Google', 'Microsoft', 'NVIDIA', 'Stability AI', 'Mistral AI', 'DeepSeek', 'Alibaba']
</script>
