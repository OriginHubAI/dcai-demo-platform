import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomePage.vue') },
  { path: '/models', name: 'models', component: () => import('../views/ModelsPage.vue') },
  { path: '/models/:id(.*)', name: 'model-detail', component: () => import('../views/ModelDetailPage.vue') },
  { path: '/datasets', name: 'datasets', component: () => import('../views/DatasetsPage.vue') },
  { path: '/datasets/:id(.*)', name: 'dataset-detail', component: () => import('../views/DatasetDetailPage.vue') },
  { path: '/dataflow', name: 'dataflow', component: () => import('../views/DataFlowPage.vue') },
  { path: '/dataflow/canvas', name: 'dataflow-canvas', component: () => import('../views/DataFlowCanvasPage.vue') },
  { path: '/dataflow/tasks', name: 'dataflow-tasks', component: () => import('../views/DataFlowTasksPage.vue') },
  { path: '/dataflow/tasks/:id', name: 'task-detail', component: () => import('../views/TaskDetailRouter.vue') },
  { path: '/spaces', name: 'spaces', component: () => import('../views/SpacesPage.vue') },
  { path: '/spaces/:id(.*)', name: 'space-detail', component: () => import('../views/SpaceDetailPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
