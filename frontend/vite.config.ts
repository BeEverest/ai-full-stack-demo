import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
    },
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'unplagiarized-emmie-coroplastic.ngrok-free.dev', // 你的 ngrok 域名
    ]    
  },
})
