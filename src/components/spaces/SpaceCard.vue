<template>
  <router-link
    :to="`/apps/${space.id}`"
    class="block rounded-lg overflow-hidden hover:shadow-lg transition-all border border-gray-200"
  >
    <!-- Gradient header -->
    <div
      class="h-24 flex items-center justify-center text-4xl"
      :style="gradientStyle"
    >
      {{ space.emoji }}
    </div>
    <!-- Content -->
    <div class="bg-white p-4">
      <div class="flex items-center space-x-2 mb-1">
        <span class="text-sm font-semibold text-gray-900 truncate">{{ space.title }}</span>
        <span
          class="w-2 h-2 rounded-full flex-shrink-0"
          :class="space.status === 'running' ? 'bg-green-400' : 'bg-gray-300'"
        ></span>
      </div>
      <p class="text-xs text-gray-500 mb-2">{{ space.author }}</p>
      <p class="text-xs text-gray-600 line-clamp-2">{{ space.description }}</p>
      <div class="flex items-center mt-3">
        <StatBadge icon="like" :value="space.likes" />
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import StatBadge from '@/components/common/StatBadge.vue'

const props = defineProps({
  space: { type: Object, required: true }
})

const colorValues = {
  red: '#ef4444', orange: '#f97316', yellow: '#eab308', green: '#22c55e',
  teal: '#14b8a6', cyan: '#06b6d4', blue: '#3b82f6', indigo: '#6366f1',
  purple: '#a855f7', pink: '#ec4899',
}

const gradientStyle = computed(() => {
  const from = colorValues[props.space.colorFrom] || '#6366f1'
  const to = colorValues[props.space.colorTo] || '#3b82f6'
  return { background: `linear-gradient(135deg, ${from}, ${to})` }
})
</script>
