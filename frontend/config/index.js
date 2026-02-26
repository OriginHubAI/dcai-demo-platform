/**
 * Global Configuration
 * Controls whether to use mock data or backend API
 */

// Global config object
export const config = {
  /**
   * Data source mode
   * - 'mock': Use local mock data (default)
   * - 'api': Use backend Django API
   */
  dataMode: import.meta.env.VITE_DATA_MODE || 'mock',
  
  /**
   * Backend API base URL
   */
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  /**
   * API version prefix
   */
  apiVersion: '/api/v2',
}

/**
 * Check if currently using mock data mode
 */
export function isMockMode() {
  return config.dataMode === 'mock'
}

/**
 * Check if currently using API mode
 */
export function isApiMode() {
  return config.dataMode === 'api'
}

/**
 * Set data mode dynamically
 * @param {'mock' | 'api'} mode
 */
export function setDataMode(mode) {
  if (mode !== 'mock' && mode !== 'api') {
    console.error(`Invalid data mode: ${mode}. Use 'mock' or 'api'`)
    return
  }
  config.dataMode = mode
  console.log(`[Config] Data mode switched to: ${mode}`)
}

/**
 * Get full API URL
 * @param {string} endpoint - API endpoint path (e.g., '/tasks')
 */
export function getApiUrl(endpoint) {
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `${config.apiBaseUrl}${config.apiVersion}${path}`
}

export default config