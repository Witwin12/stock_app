<script setup>
// (1) Import เครื่องมือที่จำเป็น
import { ref, onMounted } from 'vue'
import axios from 'axios'
// *** ไม่ต้อง Import อะไรเพิ่มสำหรับ <router-link> ***

// (2) สร้าง "State" (กล่องเปล่า) สำหรับเก็บข้อมูล
const products = ref([])
const loading = ref(true)
const error = ref(null)

// (3) สร้าง Function สำหรับดึงข้อมูล (เหมือนเดิม)
async function fetchTireProducts() {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:8000/api/tire-products/')
    products.value = response.data
    
  } catch (err) {
    console.error('Error fetching data:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลได้'
  } finally {
    loading.value = false
  }
}

// (8) สั่งให้ Function นี้ทำงาน (เหมือนเดิม)
onMounted(() => {
  fetchTireProducts()
})

</script>

<template>
  <div class="product-list">
    <h1>รายการสต็อกยาง</h1>

    <div v-if="loading">
      กำลังโหลดข้อมูล...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <table v-else class="stock-table">
      <thead>
        <tr>
          <th>ยี่ห้อ</th>
          <th>ลายดอกยาง</th>
          <th>ขนาด</th>
          <th>ยอดคงเหลือรวม (เส้น)</th>
          
          <th>รายละเอียด</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.product_id">
          <td>{{ product.brand }}</td>
          <td>{{ product.pattern }}</td>
          <td>{{ product.size }}</td>
          <td>{{ product.total_stock_on_hand }}</td>
          
          <td>
            <router-link 
              :to="`/product/${product.product_id}`" 
              class="detail-button"
            >
              ดูสต็อก
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.product-list {
  font-family: sans-serif;
  max-width: 800px;
  margin: 20px auto;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  color: #222;
}
/* (Style อื่นๆ เหมือนเดิม) */
h1 {
  text-align: center;
  margin-bottom: 20px;
}
.error {
  color: red;
  text-align: center;
}
.stock-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
}
.stock-table th {
  background-color: #f5f5f5;
  color: #333;
  text-align: left;
  padding: 10px;
  border-bottom: 2px solid #ddd;
}
.stock-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  /* (ทางเลือก) จัดให้ปุ่มอยู่ตรงกลาง Cell */
  vertical-align: middle;
  text-align: center;
}
.stock-table tr:hover {
  background-color: #f9f9f9;
}

/* (4) เพิ่ม Style สำหรับปุ่มลิงก์ */
.detail-button {
  display: inline-block;
  background-color: #007bff; /* สีฟ้า */
  color: white;
  padding: 6px 12px;
  text-align: center;
  text-decoration: none; /* ลบขีดเส้นใต้ของลิงก์ */
  border-radius: 4px;
  font-size: 0.9em;
  transition: background-color 0.2s;
  white-space: nowrap; /* กันไม่ให้ปุ่มตกบรรทัด */
}

.detail-button:hover {
  background-color: #0056b3; /* สีฟ้าเข้มขึ้น */
  color: white;
}
</style>