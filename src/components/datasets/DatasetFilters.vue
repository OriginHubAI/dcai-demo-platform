<template>
  <FilterSidebar
    :filter-groups="filterGroups"
    :selected="selected"
    @update:selected="$emit('update:selected', $event)"
  />
</template>

<script setup>
import FilterSidebar from '@/components/common/FilterSidebar.vue'
import { taskFilters, modalityFilters, languageFilters, licenseFilters } from '@/data/filters.js'

defineProps({
  selected: { type: Object, default: () => ({}) }
})
defineEmits(['update:selected'])

const filterGroups = [
  { key: 'task', label: 'Tasks', options: taskFilters, open: true },
  { key: 'modality', label: 'Modality', options: modalityFilters, open: true },
  { key: 'language', label: 'Languages', options: languageFilters, open: false },
  { key: 'license', label: 'Licenses', options: licenseFilters, open: false },
]
</script>
