import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Export a function so we can tweak the base path depending on whether
// we're building for production (GitHub Pages) or running the dev server.
export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === 'build' ? './' : '/',
  server: {
    port: 5173,
    host: '0.0.0.0'
  }
}))
