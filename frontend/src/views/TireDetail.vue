<script setup>
import { ref, onMounted } from 'vue'
import { useRoute,useRouter} from 'vue-router' 
import axios from 'axios'

// (2) สร้าง State สำหรับเก็บข้อมูล
const router = useRouter()
const product = ref(null) // สำหรับเก็บข้อมูลหลัก (ชื่อ, ยี่ห้อ)
const stockLots = ref([]) // สำหรับเก็บข้อมูลสต็อก (แยกล็อต/ปี)
const loading = ref(true)
const error = ref(null)

// (3) ดึง ID ของสินค้าจาก URL
const route = useRoute()
const productId = route.params.id // (id นี้ต้องตรงกับที่ตั้งใน router)

// (4) สร้าง Function สำหรับดึงข้อมูล 2 ส่วน
async function fetchProductDetails() {
  loading.value = true
  error.value = null
  try {
    // (4A) ดึงข้อมูลหลักของสินค้า
    const productUrl = `http://localhost:8000/api/tire-products/${productId}/`
    const productResponse = await axios.get(productUrl)
    product.value = productResponse.data

    // (4B) ดึงข้อมูลสต็อกแยกตามปี (จาก Endpoint ที่คุณต้องการ)
    const stockUrl = `http://localhost:8000/api/tire-products/${productId}/stock_by_year/`
    const stockResponse = await axios.get(stockUrl)
    stockLots.value = stockResponse.data

  } catch (err) {
    console.error('Error fetching details:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลสินค้าได้'
  } finally {
    loading.value = false
  }
}

// (5) สั่งให้ดึงข้อมูลทันทีเมื่อเปิดหน้านี้
onMounted(() => {
  fetchProductDetails()
})
// (6) สร้าง Function สำหรับปุ่มย้อนกลับ 
function goBack() {
  // สั่งให้ router ย้อนกลับไป 1 หน้า 
  router.back() 
}
</script>

<template>
  <div class="tire-detail-container">
    
    <div v-if="loading">
      กำลังโหลดข้อมูล...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else-if="product">
      
      <h1>{{ product.brand }} {{ product.pattern }}</h1>
      <h2>ขนาด: {{ product.size }}</h2>
      <hr>

      <h3>รายละเอียดสต็อกคงเหลือ (แยกตามล็อต)</h3>

      <div v-if="stockLots.length === 0" class="no-stock">
        * ไม่พบข้อมูลสต็อกสำหรับสินค้ารายการนี้ *
      </div>
      
      <table v-else>
        <thead>
          <tr>
            <th>ปีผลิต</th>
            <th>วันที่รับเข้า</th>
            <th>จำนวนรับเข้า</th>
            <th>จำนวนเบิกออก</th>
            <th>จำนวนคงเหลือ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in stockLots" :key="lot.lot_id">
            <td>{{ lot.year_manufactured }}</td>
            <td>{{ lot.date_in }}</td>
            <td>{{ lot.quantity_in }}</td>
            <td>{{ lot.total_out }}</td>
            <td><strong>{{ lot.quantity_remaining }}</strong></td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>

  <div class="tire-detail-container">
    
    <button @click="goBack" class="back-button">&larr; ย้อนกลับ</button>

  </div>
</template>

<style scoped>
.tire-detail-container {
  font-family: sans-serif;
  color: #000; /* เพิ่มตรงนี้ให้ข้อความทั้งหมดเป็นสีดำ */
}

.error-message {
  color: red;
  font-weight: bold;
}

.no-stock {
  color: #777;
  font-style: italic;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

thead {
  background-color: #f4f4f4;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  color: #000; 
}

td:nth-child(3),
td:nth-child(4),
td:nth-child(5) {
  text-align: right;
}

td strong {
  font-size: 1.1em;
  color: #0056b3; 
}

/* ปุ่มย้อนกลับ */
.back-button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  margin-bottom: 1.5rem;
  color: #000; 
}
.back-button:hover {
  background-color: #e0e0e0;
}
</style>
