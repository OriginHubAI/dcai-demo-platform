import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiTarget = env.VITE_API_PROXY_TARGET || env.VITE_API_BASE_URL || 'http://127.0.0.1:18000'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': '/frontend'
      }
    },
    server: {
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
        },
        // In ASGI-integrated mode, /embedded/* is served by the same uvicorn ASGI
        // server as the Django/FastAPI backend (no separate DataFlow-WebUI process).
        '/embedded/dataflow-webui': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/embedded/dataflow-backend': {
          target: apiTarget,
          changeOrigin: true,
        }
      }
    }
  }
})
