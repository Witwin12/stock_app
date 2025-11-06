import { createRouter, createWebHistory } from 'vue-router';
// 1. แก้ไข Path ให้อ้างอิงจาก @ (ซึ่งปกติคือ src/)
import Home from '@/views/Home.vue'; 

// 2. "routes" ต้องเป็น Array (วงเล็บเหลี่ยม)
const routes = [
  {
    path: '/',          // URL ที่ต้องการ
    name: 'home',       // ชื่อของ Route
    component: Home     // Component ที่จะแสดงผล (ที่เรา import มา)
  }

];

const router = createRouter({
  history: createWebHistory(),
  routes, // ส่ง Array routes เข้าไป
});

export default router;