import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// change target if backend is not on localhost:8000
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
