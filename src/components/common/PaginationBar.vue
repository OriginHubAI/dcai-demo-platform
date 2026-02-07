<template>
  <div v-if="totalPages > 1" class="flex items-center justify-center space-x-1 mt-6">
    <button
      @click="$emit('update:modelValue', modelValue - 1)"
      :disabled="modelValue <= 1"
      class="px-3 py-1.5 text-sm rounded-md border border-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      Previous
    </button>
    <button
      v-for="page in visiblePages"
      :key="page"
      @click="$emit('update:modelValue', page)"
      class="px-3 py-1.5 text-sm rounded-md border"
      :class="page === modelValue ? 'bg-hf-yellow border-hf-yellow text-gray-900 font-medium' : 'border-gray-300 hover:bg-gray-50'"
    >
      {{ page }}
    </button>
    <span v-if="totalPages > 7 && modelValue < totalPages - 2" class="px-2 text-gray-400">...</span>
    <button
      @click="$emit('update:modelValue', modelValue + 1)"
      :disabled="modelValue >= totalPages"
      class="px-3 py-1.5 text-sm rounded-md border border-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50"
    >
      Next
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 1 },
  totalPages: { type: Number, required: true }
})
defineEmits(['update:modelValue'])

const visiblePages = computed(() => {
  const pages = []
  const total = props.totalPages
  const current = props.modelValue
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})
</script>
