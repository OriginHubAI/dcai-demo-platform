/**
 * API Service Layer
 * Provides unified interface for both mock data and backend API
 */

import { isMockMode, isApiMode, getApiUrl } from '@/config/index.js'

/**
 * Generic fetch wrapper with error handling
 */
async function fetchWithAuth(url, options = {}) {
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      // Add auth token if available
      ...(localStorage.getItem('token') && {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      })
    },
  }
  
  try {
    const response = await fetch(url, { ...defaultOptions, ...options })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('[API] Fetch error:', error)
    throw error
  }
}

/**
 * Task API Service
 */
export const taskApi = {
  /**
   * Get all tasks
   * @param {Object} params - Query params (page, page_size, type, status, search)
   */
  async getTasks(params = {}) {
    if (isMockMode()) {
      const { tasks } = await import('@/data/tasks.js')
      return { list: tasks, total: tasks.length }
    }
    
    const queryParams = new URLSearchParams(params)
    const url = getApiUrl(`/tasks?${queryParams}`)
    const response = await fetchWithAuth(url)
    return response.data || { list: [], total: 0 }
  },
  
  /**
   * Get task by ID
   * @param {string} taskId
   */
  async getTaskById(taskId) {
    if (isMockMode()) {
      const { getTaskById } = await import('@/data/tasks.js')
      return getTaskById(taskId)
    }
    
    const url = getApiUrl(`/tasks/${taskId}`)
    const response = await fetchWithAuth(url)
    return response.data
  },
  
  /**
   * Get task status
   * @param {string} taskId
   */
  async getTaskStatus(taskId) {
    if (isMockMode()) {
      const { getTaskById } = await import('@/data/tasks.js')
      const task = getTaskById(taskId)
      return { status: task?.status || 'pending', progress: task?.progress || 0 }
    }
    
    const url = getApiUrl(`/task/${taskId}/status`)
    const response = await fetchWithAuth(url)
    return response.data
  },
}

/**
 * Dataset API Service
 */
export const datasetApi = {
  /**
   * Get all datasets
   */
  async getDatasets() {
    if (isMockMode()) {
      const { datasets } = await import('@/data/datasets.js')
      return datasets
    }
    
    const url = getApiUrl('/datasets')
    const response = await fetchWithAuth(url)
    return response.data?.list || []
  },
  
  /**
   * Get dataset by ID
   * @param {string} datasetId
   */
  async getDatasetById(datasetId) {
    if (isMockMode()) {
      const { getDatasetById } = await import('@/data/datasets.js')
      return getDatasetById(datasetId)
    }
    
    const url = getApiUrl(`/datasets/${datasetId}`)
    const response = await fetchWithAuth(url)
    return response.data
  },
}

/**
 * DataFlow API Service
 */
export const dataflowApi = {
  /**
   * Get all DataFlow packages
   */
  async getPackages() {
    if (isMockMode()) {
      const { dataflowPackages } = await import('@/data/dataflow.js')
      return dataflowPackages
    }
    
    const url = getApiUrl('/dataflow/packages')
    const response = await fetchWithAuth(url)
    return response.data?.list || []
  },
  
  /**
   * Get package by ID
   * @param {string} packageId
   */
  async getPackageById(packageId) {
    if (isMockMode()) {
      const { getDataflowPackageById } = await import('@/data/dataflow.js')
      return getDataflowPackageById(packageId)
    }
    
    const url = getApiUrl(`/dataflow/packages/${packageId}`)
    const response = await fetchWithAuth(url)
    return response.data
  },
  
  /**
   * Get data processing pipeline for a task
   * @param {string} taskId
   */
  async getPipeline(taskId) {
    if (isMockMode()) {
      const { getDataProcessingPipeline } = await import('@/data/dataflowTasks.js')
      return getDataProcessingPipeline(taskId)
    }
    
    const url = getApiUrl(`/dataflow/pipeline/${taskId}`)
    const response = await fetchWithAuth(url)
    return response.data?.nodes || []
  },
  
  /**
   * Get execution results for a task
   * @param {string} taskId
   */
  async getExecutionResult(taskId) {
    if (isMockMode()) {
      const { getExecutionResult } = await import('@/data/dataflowTasks.js')
      return getExecutionResult(taskId)
    }
    
    const url = getApiUrl(`/dataflow/execution/${taskId}`)
    const response = await fetchWithAuth(url)
    return response.data
  },
}

/**
 * Knowledge Base API Service
 */
export const knowledgeBaseApi = {
  /**
   * Get all knowledge bases
   */
  async getKnowledgeBases() {
    if (isMockMode()) {
      const { knowledgeBases } = await import('@/data/knowledgeBase.js')
      return knowledgeBases
    }
    
    const url = getApiUrl('/knowledgebase')
    const response = await fetchWithAuth(url)
    return response.data?.list || []
  },
}

/**
 * Model API Service
 */
export const modelApi = {
  /**
   * Get all models
   */
  async getModels() {
    if (isMockMode()) {
      const { models } = await import('@/data/models.js')
      return models
    }
    
    const url = getApiUrl('/models')
    const response = await fetchWithAuth(url)
    return response.data?.list || []
  },
}

/**
 * Space API Service
 */
export const spaceApi = {
  /**
   * Get all spaces
   */
  async getSpaces() {
    if (isMockMode()) {
      const { spaces } = await import('@/data/spaces.js')
      return spaces
    }
    
    const url = getApiUrl('/spaces')
    const response = await fetchWithAuth(url)
    return response.data?.list || []
  },
}

// Export all APIs
export default {
  task: taskApi,
  dataset: datasetApi,
  dataflow: dataflowApi,
  knowledgeBase: knowledgeBaseApi,
  model: modelApi,
  space: spaceApi,
}