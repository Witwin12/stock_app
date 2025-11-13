<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import TireProductList from '@/components/TireProductList.vue'

// สร้าง state สำหรับตรวจว่าล็อกอินอยู่ไหม
const isLoggedIn = ref(false)

onMounted(() => {
  const token = localStorage.getItem('authToken')
  isLoggedIn.value = !!token // ถ้ามี token = true
})
</script>

<template>
  <div class="page-container">
    <main>
      <div class="page-header">
        <RouterLink
          v-if="isLoggedIn"
          to="/stock-in"
          class="add-product-button"
        >
          เพิ่มสินค้าใหม่
        </RouterLink>
      </div>
      <TireProductList />
    </main>
  </div>
</template>


<style scoped>
.page-container {
  width: 100%;
  min-height: 100%;
  background-color: #fff;
  padding: 0;
  margin: 0;
  overflow-x: hidden;
}

main {
  box-sizing: border-box;
  background-color: #fff;
}

.page-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

/* ปุ่มเพิ่มสินค้า */
.add-product-button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-product-button:hover {
  background-color: #0056b3;
}
</style>
