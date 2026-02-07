<template>
  <div class="space-y-3">
    <div v-for="group in groups" :key="group.label">
      <button
        @click="group.open = !group.open"
        class="flex items-center justify-between w-full text-sm font-semibold text-gray-700 py-1"
      >
        {{ group.label }}
        <svg
          class="w-4 h-4 transition-transform"
          :class="{ 'rotate-180': group.open }"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <div v-show="group.open" class="mt-1 space-y-1 max-h-48 overflow-y-auto">
        <label
          v-for="option in group.options"
          :key="option.value"
          class="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 cursor-pointer py-0.5"
        >
          <input
            type="checkbox"
            :checked="isSelected(group.key, option.value)"
            @change="toggle(group.key, option.value)"
            class="rounded border-gray-300 text-hf-yellow focus:ring-hf-yellow"
          />
          <span class="truncate">{{ option.label }}</span>
          <span v-if="option.count !== undefined" class="text-gray-400 text-xs ml-auto">{{ option.count }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  filterGroups: { type: Array, required: true },
  selected: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:selected'])

const groups = reactive(
  props.filterGroups.map(g => ({ ...g, open: g.open !== false }))
)

function isSelected(key, value) {
  return (props.selected[key] || []).includes(value)
}

function toggle(key, value) {
  const current = [...(props.selected[key] || [])]
  const idx = current.indexOf(value)
  if (idx >= 0) current.splice(idx, 1)
  else current.push(value)
  emit('update:selected', { ...props.selected, [key]: current })
}
</script>
