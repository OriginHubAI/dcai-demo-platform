<template>
  <div class="relative">
    <button
      @click="open = !open"
      class="flex items-center space-x-1 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg px-3 py-1.5"
    >
      <span>Sort: {{ currentLabel }}</span>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>
    <div
      v-if="open"
      class="absolute right-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
    >
      <button
        v-for="opt in options"
        :key="opt.value"
        @click="select(opt.value)"
        class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
        :class="modelValue === opt.value ? 'text-dc-primary font-medium' : 'text-gray-700'"
      >
        {{ opt.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array, required: true }
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const currentLabel = computed(() => {
  const opt = props.options.find(o => o.value === props.modelValue)
  return opt ? opt.label : ''
})

function select(val) {
  emit('update:modelValue', val)
  open.value = false
}
</script>
