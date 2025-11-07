<script setup>
import TireProductList from '@/components/TireProductList.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <div class="page-header">
      <!-- ปุ่มเพิ่มสินค้า -->
      <RouterLink to="/stock-in" class="add-product-button">
        เพิ่มสินค้าใหม่
      </RouterLink>
    </div>

    <!-- แสดงรายการสินค้า -->
    <TireProductList />
  </main>
</template>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  background-color: white;
  
}
main {
  padding: 1rem;
}

.page-header {
  margin-bottom: 1.5rem; /* เว้นระยะห่างระหว่างปุ่มกับ list */
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}
 /*เพิ่ม style สำหรับปุ่ม */
.add-product-button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff; /* สีน้ำเงิน (เปลี่ยนได้) */
  border: none;
  border-radius: 5px;
  text-decoration: none; /* เอาขีดเส้นใต้ของลิงก์ออก */
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-product-button:hover {
  background-color: #0056b3; /* สีเข้มขึ้นตอนชี้ */
}
</style>
