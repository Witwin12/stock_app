import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    // 1. ให้ Vite รับการเชื่อมต่อจากภายนอก Container (สำคัญมาก)
    host: '0.0.0.0', 
    
    // 2. ระบุพอร์ตให้ตรง
    port: 5173, 
    
    // 3. (นี่คือตัวแก้ Hot Reload) บังคับให้ใช้ Polling
    watch: {
      usePolling: true
    },

    // 4. (ทางเลือก) ช่วยให้ HMR (การแทนที่โมดูล) ทำงานดีขึ้น
    hmr: {
      clientPort: 5173
    }
  }
})