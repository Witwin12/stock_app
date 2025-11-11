<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from 'axios'
import LotDeleteButton from '@/components/DeleteTireLotButton.vue'

const router = useRouter()
const productId = useRoute().params.id

const product = ref(null)
const stockLots = ref([])
const loading = ref(true)
const error = ref(null)

function getAuthHeaders() {
  const token = localStorage.getItem('authToken')
  if (!token) {
    error.value = "คุณยังไม่ได้ล็อกอิน!"
    return null
  }
  return {
    'Authorization': `Token ${token}`
  }
}

async function fetchProductDetails() {
  try {
    loading.value = true
    const headers = getAuthHeaders()
    if (!headers) {
      loading.value = false
      return
    }

    const [productRes, stockRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/tire-products/${productId}/`, { headers }),
      axios.get(`http://localhost:8000/api/tire-products/${productId}/stock_by_year/`, { headers })
    ])
    product.value = productRes.data
    stockLots.value = stockRes.data

  } catch (err) {
    if (err.response?.status === 401) {
      error.value = "คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้ (401)"
    } else {
      error.value = 'ไม่สามารถโหลดข้อมูลสินค้าได้'
    }
  } finally {
    loading.value = false
  }
}

//สร้างฟังก์ชันรับ emit 'delete-success'
function onLotDeleted(deletedLotId) {
  // ลบ Lot นั้นออกจาก Array (เพื่ออัปเดต UI)
  stockLots.value = stockLots.value.filter(
    lot => lot.lot_id !== deletedLotId
  )
}

const goBack = () => router.back()

onMounted(fetchProductDetails)
</script>

<template>
 <div class="tire-detail-container">
  
    <div v-if="loading">กำลังโหลดข้อมูล...</div>
  
    <div v-else-if="error" class="error-message">{{ error }}</div>

      <template v-else-if="product">
   <h1>{{ product.brand }} {{ product.pattern }}</h1>
   <h2>ขนาด: {{ product.size }}</h2>
   <hr />
   <h3>รายละเอียดสต็อก (ตามล็อต)</h3>

   <div v-if="!stockLots.length" class="no-stock">* ไม่พบข้อมูลสต็อก *</div>

         <table v-else>
    <thead>
     <tr>
      <th>ปีผลิต</th>
      <th>วันที่รับเข้า</th>
      <th>จำนวนรับเข้า</th>
      <th>จำนวนเบิกออก</th>
      <th>คงเหลือ</th>
      <th>การดำเนินการ</th>
     </tr>
    </thead>
    <tbody>
     <tr v-for="lot in stockLots" :key="lot.lot_id">
      <td>{{ lot.year_manufactured }}</td>
      <td>{{ lot.date_in }}</td>
      <td class="right">{{ lot.quantity_in }}</td>
      <td class="right">{{ lot.total_out }}</td>
      <td class="right"><strong>{{ lot.quantity_remaining }}</strong></td>
      
            <td class="action-cell">
                     <RouterLink :to="`/stock-out-form/${lot.lot_id}`" class="stock-out-button">
                เบิกออก
              </RouterLink>

              <LotDeleteButton 
                :lot-id="lot.lot_id"
                endpoint-url="/api/tire-lots/"
                @delete-success="onLotDeleted"
              />
      </td>
     </tr>
    </tbody>
   </table>
  </template>

      <button @click="goBack" class="back-button">&larr; ย้อนกลับ</button>
 </div>
</template>
<style scoped>
.tire-detail-container {
  font-family: sans-serif;
  color: #000;
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

/* Table styling */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

thead {
  background-color: #f4f4f4;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  color: #000;
  vertical-align: middle; 
}

td.right {
  text-align: right;
}

th.action-header {
  text-align: center;
}

td.action-cell {
  text-align: center;
}

td strong {
  font-size: 1.1em;
  color: #0056b3;
}

/* style ปุ่มเบิกสินค้า */
.stock-out-button {
  display: inline-block;
  padding: 6px 14px;
  font-size: 0.9em;
  font-weight: bold;
  color: #fff;
  background-color: #dc3545; 
  border: none;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.stock-out-button:hover {
  background-color: #c82333; 
}

/* Back button */
.back-button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  margin-top: 1.5rem;
  color: #000;
  transition: background-color 0.2s ease;
}

.back-button:hover {
  background-color: #e0e0e0;
}
</style>