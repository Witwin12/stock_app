import { createRouter, createWebHistory } from 'vue-router';

import Home from '@/views/Home.vue'; 
import TireDetail from '@/views/TireDetail.vue';

// 2. "routes" ต้องเป็น Array (วงเล็บเหลี่ยม)
const routes = [
  {
    path: '/',          // URL ที่ต้องการ
    name: 'home',       // ชื่อของ Route
    component: Home     // Component ที่จะแสดงผล (ที่เรา import มา)
  },

  {
    // `:id` คือ "ตัวแปร" ที่จะถูกส่งไปให้ component
    path: '/product/:id', 
    name: 'product-detail',
    component: TireDetail
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes, // ส่ง Array routes เข้าไป
});

export default router;