const LOCAL_HOSTS = new Set(['127.0.0.1', 'localhost', '0.0.0.0'])

function getBrowserLocation() {
  if (typeof window === 'undefined') return null
  return window.location
}

export function resolveServiceUrl(rawUrl, defaultPort) {
  const location = getBrowserLocation()
  const fallback = location
    ? `${location.protocol}//${location.hostname}:${defaultPort}`
    : `http://127.0.0.1:${defaultPort}`

  try {
    const url = new URL(rawUrl || fallback, fallback)
    if (location && (LOCAL_HOSTS.has(url.hostname) || url.hostname === '::1')) {
      url.hostname = location.hostname
    }
    return url.toString().replace(/\/$/, '')
  } catch {
    return fallback.replace(/\/$/, '')
  }
}

export const config = {
  dataMode: import.meta.env.VITE_DATA_MODE || 'mock',
  apiBaseUrl: '',
  apiVersion: '/api/v2',
}

export function isMockMode() {
  return config.dataMode === 'mock'
}

export function isApiMode() {
  return config.dataMode === 'api'
}

export function setDataMode(mode) {
  if (mode !== 'mock' && mode !== 'api') {
    console.error(`Invalid data mode: ${mode}. Use 'mock' or 'api'`)
    return
  }
  config.dataMode = mode
  console.log(`[Config] Data mode switched to: ${mode}`)
}

export function getApiUrl(endpoint) {
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `${config.apiBaseUrl}${config.apiVersion}${path}`
}

export default config
