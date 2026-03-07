<template>
  <span
    class="inline-flex items-center px-2 py-0.5 rounded-full font-medium whitespace-nowrap"
    :class="[colorClass, sizeClass]"
  >
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  color: { type: String, default: 'blue' },
  size: { type: String, default: 'xs' }
})

const colorMap = {
  blue: 'bg-blue-100 text-blue-800',
  green: 'bg-green-100 text-green-800',
  purple: 'bg-purple-100 text-purple-800',
  orange: 'bg-orange-100 text-orange-800',
  red: 'bg-red-100 text-red-800',
  yellow: 'bg-yellow-100 text-yellow-800',
  gray: 'bg-gray-100 text-gray-700',
  pink: 'bg-pink-100 text-pink-800',
  indigo: 'bg-indigo-100 text-indigo-800',
  teal: 'bg-teal-100 text-teal-800',
}

const colorClass = computed(() => colorMap[props.color] || colorMap.blue)

const sizeMap = {
  xs: 'text-xs',
  '2xs': 'text-[10px]'
}

const sizeClass = computed(() => sizeMap[props.size] || sizeMap.xs)
</script>
