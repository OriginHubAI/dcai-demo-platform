<template>
  <component :is="detailComponent" />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getTaskById } from '@/data/tasks.js'
import ModelTuningTaskDetailPage from './ModelTuningTaskDetailPage.vue'
import DataProcessingTaskDetailPage from './DataProcessingTaskDetailPage.vue'
import ModelEvaluationTaskDetailPage from './ModelEvaluationTaskDetailPage.vue'

const route = useRoute()

const task = computed(() => {
  const id = route.params.id
  return getTaskById(id) || {}
})

const detailComponent = computed(() => {
  if (task.value.type === 'Model Tuning') {
    return ModelTuningTaskDetailPage
  } else if (task.value.type === 'Model Evaluation') {
    return ModelEvaluationTaskDetailPage
  } else if (task.value.type === 'Data Processing') {
    return DataProcessingTaskDetailPage
  }
  // Default to DataProcessing for unknown types
  return DataProcessingTaskDetailPage
})
</script>
