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
        }
        ,
        '/embedded/dataflow-webui': {
          target: 'http://127.0.0.1:8002',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/embedded\/dataflow-webui/, ''),
        },
        '/embedded/dataflow-backend': {
          target: 'http://127.0.0.1:8002',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/embedded\/dataflow-backend/, ''),
        }
      }
    }
  }
})
