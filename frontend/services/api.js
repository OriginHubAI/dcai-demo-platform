import { config, getApiUrl, isMockMode } from '@/config/index.js'

function getStoredToken() {
  return localStorage.getItem('access_token') || localStorage.getItem('token') || ''
}

function buildHeaders(headers = {}, includeJson = true) {
  const token = getStoredToken()
  return {
    ...(includeJson ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...headers,
  }
}

async function requestJson(url, options = {}) {
  const includeJson = options.body === undefined || !(options.body instanceof FormData)
  const response = await fetch(url, {
    ...options,
    headers: buildHeaders(options.headers, includeJson),
  })

  let payload = {}
  try {
    payload = await response.json()
  } catch (error) {
    payload = {}
  }

  if (!response.ok) {
    const message = payload?.msg || payload?.message || `HTTP error ${response.status}`
    throw new Error(message)
  }

  return payload
}

export const taskApi = {
  async getTasks(params = {}) {
    if (isMockMode()) {
      const { tasks } = await import('@/data/tasks.js')
      return { list: tasks, total: tasks.length }
    }

    const queryParams = new URLSearchParams(params)
    const url = getApiUrl(`/tasks?${queryParams}`)
    const response = await requestJson(url)
    return response.data || { list: [], total: 0 }
  },

  async getTaskById(taskId) {
    if (isMockMode()) {
      const { getTaskById } = await import('@/data/tasks.js')
      return getTaskById(taskId)
    }

    const url = getApiUrl(`/tasks/${taskId}`)
    const response = await requestJson(url)
    return response.data
  },

  async getTaskStatus(taskId) {
    if (isMockMode()) {
      const { getTaskById } = await import('@/data/tasks.js')
      const task = getTaskById(taskId)
      return { status: task?.status || 'pending', progress: task?.progress || 0 }
    }

    const url = getApiUrl(`/task/${taskId}/status`)
    const response = await requestJson(url)
    return response.data
  },
}

export const datasetApi = {
  async getDatasets() {
    if (isMockMode()) {
      const { datasets } = await import('@/data/datasets.js')
      return datasets
    }

    const url = getApiUrl('/datasets')
    const response = await requestJson(url)
    return response.data?.list || []
  },

  async getDatasetById(datasetId) {
    if (isMockMode()) {
      const { getDatasetById } = await import('@/data/datasets.js')
      return getDatasetById(datasetId)
    }

    const url = getApiUrl(`/datasets/${datasetId}`)
    const response = await requestJson(url)
    return response.data
  },

  async getDatasetRelationships(datasetId) {
    if (isMockMode()) {
      const { getDatasetById } = await import('@/data/datasets.js')
      const dataset = getDatasetById(datasetId)
      if (!dataset) return null
      return {
        parent: dataset.parentDataset ? { id: dataset.parentDataset } : null,
        derived: dataset.derivedDatasets?.map((id) => ({ id })) || [],
      }
    }

    const url = getApiUrl(`/datasets/${datasetId}/relationships`)
    const response = await requestJson(url)
    return response.data
  },
}

export const dataflowApi = {
  async getPackages() {
    if (isMockMode()) {
      const { dataflowPackages } = await import('@/data/dataflow.js')
      return dataflowPackages
    }

    const url = getApiUrl('/dataflow/packages')
    const response = await requestJson(url)
    return response.data?.list || []
  },

  async getPackageById(packageId) {
    if (isMockMode()) {
      const { getDataflowPackageById } = await import('@/data/dataflow.js')
      return getDataflowPackageById(packageId)
    }

    const url = getApiUrl(`/dataflow/packages/${packageId}`)
    const response = await requestJson(url)
    return response.data
  },

  async getPackageFiles(packageId) {
    const url = getApiUrl(`/dataflow/packages/${packageId}/files`)
    const response = await requestJson(url)
    return response.data
  },

  async getPackageFileContent(packageId, path) {
    const queryParams = new URLSearchParams({ path })
    const url = getApiUrl(`/dataflow/packages/${packageId}/file?${queryParams}`)
    const response = await requestJson(url)
    return response.data
  },

  async startPackageEditor(packageId) {
    const url = getApiUrl(`/dataflow/packages/${packageId}/editor/start`)
    const response = await requestJson(url, { method: 'POST' })
    return response.data
  },

  async stopPackageEditor(packageId) {
    const url = getApiUrl(`/dataflow/packages/${packageId}/editor/stop`)
    const response = await requestJson(url, { method: 'POST' })
    return response.data
  },

  async runPackageTest(packageId) {
    const url = getApiUrl(`/dataflow/packages/${packageId}/test`)
    const response = await requestJson(url, { method: 'POST' })
    return response.data
  },

  async getPipeline(taskId) {
    if (isMockMode()) {
      const { getDataProcessingPipeline } = await import('@/data/dataflowTasks.js')
      return getDataProcessingPipeline(taskId)
    }

    const url = getApiUrl(`/dataflow/pipeline/${taskId}`)
    const response = await requestJson(url)
    return response.data?.nodes || []
  },

  async getExecutionResult(taskId) {
    if (isMockMode()) {
      const { getExecutionResult } = await import('@/data/dataflowTasks.js')
      return getExecutionResult(taskId)
    }

    const url = getApiUrl(`/dataflow/execution/${taskId}`)
    const response = await requestJson(url)
    return response.data
  },
}

export const knowledgeBaseApi = {
  async getKnowledgeBases() {
    if (isMockMode()) {
      const { knowledgeBases } = await import('@/data/knowledgeBase.js')
      return knowledgeBases
    }

    const url = getApiUrl('/knowledgebase')
    const response = await requestJson(url)
    return response.data?.list || []
  },
}

export const modelApi = {
  async getModels() {
    if (isMockMode()) {
      const { models } = await import('@/data/models.js')
      return models
    }

    const url = getApiUrl('/models')
    const response = await requestJson(url)
    return response.data?.list || []
  },
}

export const appApi = {
  async getApps(params = {}) {
    if (isMockMode()) {
      const { apps } = await import('@/data/apps.js')
      return apps
    }

    const queryParams = new URLSearchParams(params)
    const url = getApiUrl(`/apps?${queryParams}`)
    const response = await requestJson(url)
    return response.data?.list || []
  },

  async getAppById(appId) {
    if (isMockMode()) {
      const { getAppById } = await import('@/data/apps.js')
      return getAppById(appId)
    }

    const url = getApiUrl(`/apps/${appId}`)
    const response = await requestJson(url)
    return response.data
  },
}

export const chatApi = {
  async getModels() {
    const url = `${config.apiBaseUrl}/api/v1/chat/models`
    const response = await requestJson(url)
    return response.data || { models: [], default_model: '' }
  },

  async sendMessage(payload) {
    const url = `${config.apiBaseUrl}/api/v1/chat`
    const response = await requestJson(url, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    return response.data
  },

  async streamMessage(payload) {
    const url = `${config.apiBaseUrl}/api/v1/chat/stream`
    return fetch(url, {
      method: 'POST',
      headers: buildHeaders(),
      body: JSON.stringify(payload),
    })
  },
}

export const loopaiApi = {
  async getConfig() {
    const url = getApiUrl('/loopai/config/config')
    const response = await requestJson(url)
    return response.data
  },

  async createTask({ name, system, states }) {
    const url = getApiUrl('/loopai/task/task')
    const response = await requestJson(url, {
      method: 'POST',
      body: JSON.stringify({
        name,
        config: JSON.stringify({ system, states }),
      }),
    })
    return response.data
  },

  async startAgent(taskId) {
    const queryParams = new URLSearchParams({ task_id: taskId })
    const url = getApiUrl(`/loopai/starter/agent/start?${queryParams}`)
    return requestJson(url, { method: 'POST' })
  },

  async sendInput(text) {
    const queryParams = new URLSearchParams({ text })
    const url = getApiUrl(`/loopai/starter/agent/input?${queryParams}`)
    return requestJson(url, { method: 'POST' })
  },

  async stopAgent() {
    const url = getApiUrl('/loopai/starter/agent/stop')
    return requestJson(url, { method: 'POST' })
  },

  async getStatus() {
    const url = getApiUrl('/loopai/starter/agent/status')
    const response = await requestJson(url)
    return response.data
  },

  async getMessages() {
    const url = getApiUrl('/loopai/starter/agent/messages')
    const response = await requestJson(url)
    return response.data
  },

  getStreamUrl() {
    return getApiUrl('/loopai/starter/agent/message/stream')
  },
}

export const systemApi = {
  async getServicesHealth() {
    const url = getApiUrl('/services/health')
    const response = await requestJson(url)
    return response.data
  },
}

export default {
  task: taskApi,
  dataset: datasetApi,
  dataflow: dataflowApi,
  knowledgeBase: knowledgeBaseApi,
  model: modelApi,
  app: appApi,
  chat: chatApi,
  loopai: loopaiApi,
  system: systemApi,
}
