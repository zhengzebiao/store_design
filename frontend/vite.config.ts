import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

function hasPath(id: string, value: string) {
  return id.indexOf(value) >= 0
}

function vendorChunk(id: string) {
  if (!hasPath(id, 'node_modules')) return undefined
  if (hasPath(id, '/react/') || hasPath(id, '/react-dom/') || hasPath(id, '/react-router-dom/')) return 'react-vendor'
  if (hasPath(id, '/@tanstack/') || hasPath(id, '/zustand/') || hasPath(id, '/immer/')) return 'query-vendor'
  if (hasPath(id, '/@dnd-kit/')) return 'dnd-vendor'
  if (hasPath(id, '/antd/') || hasPath(id, '/@ant-design/') || hasPath(id, '/rc-') || hasPath(id, '/@rc-component/')) return 'antd-vendor'
  return undefined
}

export default defineConfig(({ command }) => ({
  base: command === 'serve' ? '/store_design/' : '/micro-apps/store_design/',
  plugins: [react()],
  server: {
    port: 5174,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/api': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
  build: {
    target: 'es2018',
    outDir: 'dist',
    chunkSizeWarningLimit: 800,
    rollupOptions: {
      output: {
        manualChunks: vendorChunk,
      },
    },
  },
}))
