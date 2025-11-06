<script setup>
// (1) Import เครื่องมือที่จำเป็น
import { ref, onMounted } from 'vue'
import axios from 'axios'

// (2) สร้าง "State" (กล่องเปล่า) สำหรับเก็บข้อมูล
// ref() ทำให้ตัวแปรนี้ "Reactive" (ถ้าข้อมูลเปลี่ยน HTML จะอัปเดตตาม)
const products = ref([])
const loading = ref(true)
const error = ref(null)

// (3) สร้าง Function สำหรับดึงข้อมูล
// เราจะใช้ `async/await` เพื่อให้โค้ดอ่านง่าย
async function fetchTireProducts() {
  loading.value = true
  try {
    // (4) ยิง Request ไปยัง Backend (นี่คือ URL ที่เราสร้างใน urls.py)
    const response = await axios.get('http://localhost:8000/api/tire-products/')
    
    // (5) เอาข้อมูล (response.data) มาใส่ใน "State"
    products.value = response.data
    
  } catch (err) {
    // (6) จัดการ Error
    console.error('Error fetching data:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลได้'
  } finally {
    // (7) ไม่ว่าจะสำเร็จหรือล่ม ให้หยุด Loading
    loading.value = false
  }
}

// (8) สั่งให้ Function นี้ทำงาน "อัตโนมัติ" 
// เมื่อ Component ถูกสร้างขึ้น (Mounted)
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
          <th>รุ่น</th>
          <th>ขนาด</th>
          <th>ยอดคงเหลือรวม (เส้น)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.product_id">
          <td>{{ product.brand }}</td>
          <td>{{ product.pattern }}</td>
          <td>{{ product.size }}</td>
          <td>{{ product.total_stock_on_hand }}</td>
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
}

.stock-table tr:hover {
  background-color: #f9f9f9;
}
</style>
