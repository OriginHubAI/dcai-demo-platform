<template>
  <FilterSidebar
    :filter-groups="filterGroups"
    :selected="selected"
    @update:selected="$emit('update:selected', $event)"
  />
</template>

<script setup>
import FilterSidebar from '@/components/common/FilterSidebar.vue'
import { taskFilters, libraryFilters, languageFilters, licenseFilters } from '@/data/filters.js'

defineProps({
  selected: { type: Object, default: () => ({}) }
})
defineEmits(['update:selected'])

const filterGroups = [
  { key: 'pipeline_tag', label: 'Tasks', options: taskFilters, open: true },
  { key: 'library', label: 'Libraries', options: libraryFilters, open: false },
  { key: 'language', label: 'Languages', options: languageFilters, open: false },
  { key: 'license', label: 'Licenses', options: licenseFilters, open: false },
]
</script>
