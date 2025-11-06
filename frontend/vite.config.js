import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// --- 1. IMPORT เครื่องมือสำหรับสร้าง Path ---
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  
  // (ส่วนแก้ Hot Reload)
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true
    },
    hmr: {
      clientPort: 5173
    }
  },

  // --- 2. เพิ่มส่วนนี้เข้าไป ---
  // ส่วนสำหรับ "แปล" Path (Resolve)
  resolve: {
    alias: {
      // บอก Vite ว่า '@' ให้หมายถึง โฟลเดอร์ 'src'
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})