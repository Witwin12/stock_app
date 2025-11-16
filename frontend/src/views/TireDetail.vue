<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from 'axios'
import LotDeleteButton from '@/components/DeleteTireLotButton.vue'

const router = useRouter()
const productId = useRoute().params.id

// --- State ---
const product = ref(null)
const stockLots = ref([])
const loading = ref(true)
const error = ref(null)
const isLoggedIn = ref(false)

// 1. เพิ่มฟังก์ชันจัดรูปแบบราคา
function formatPrice(value) {
  const price = parseFloat(value)
  if (isNaN(price)) {
    return '-'
  }
  // จัดรูปแบบเป็นเลขทศนิยม 2 ตำแหน่ง (เช่น 1200.50)
  return price.toLocaleString('th-TH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// --- ฟังก์ชันดึง Token + Headers ---
function getAuthHeaders() {
  const token = localStorage.getItem('authToken')
  isLoggedIn.value = !!token
  const headers = {}
  if (token) {
    headers['Authorization'] = `Token ${token}`
  }
  return headers
}

// --- ดึงข้อมูลสินค้าและสต็อก ---
async function fetchProductDetails() {
  try {
    loading.value = true
    const headers = getAuthHeaders()

    const [productRes, stockRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/tire-products/${productId}/`, { headers }),
      axios.get(`http://localhost:8000/api/tire-products/${productId}/stock_by_year/`, { headers })
    ])

    product.value = productRes.data
    stockLots.value = stockRes.data
  } catch (err) {
    console.error('Error fetching product details:', err)
    if (err.response?.status === 401) {
      error.value = 'คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้ (401)'
    } else {
      error.value = 'ไม่สามารถโหลดข้อมูลสินค้าได้'
    }
  } finally {
    loading.value = false
  }
}

// --- ตรวจสอบ login แล้วค่อยดึงข้อมูล ---
function checkLoginAndFetch() {
  const token = localStorage.getItem('authToken')
  isLoggedIn.value = !!token
  fetchProductDetails()
}

// --- ฟังก์ชันเมื่อ Lot ถูกลบ ---
function onLotDeleted(deletedLotId) {
  stockLots.value = stockLots.value.filter((lot) => lot.lot_id !== deletedLotId)
}

// --- ปุ่มย้อนกลับ ---
const goBack = () => router.back()

// --- Lifecycle ---
onMounted(checkLoginAndFetch)
</script>

<template>
  <div class="tire-detail-container">
    <div v-if="loading">กำลังโหลดข้อมูล...</div>

    <div v-else-if="error" class="error-message">{{ error }}</div>

    <template v-else-if="product">
      <div class="page-header">
        <div class="header-info">
          <h1>{{ product.brand }} {{ product.pattern }}</h1>
          <h2>ขนาด: {{ product.size }}</h2>
        </div>
        <div class="header-actions">
          <button @click="$router.go(-1)" class="back-button">&larr; ย้อนกลับ</button>
        </div>
      </div>

      <h3>รายละเอียดสต็อก</h3>

      <div v-if="!stockLots.length" class="no-stock">* ไม่พบข้อมูลสต็อก *</div>

      <div v-else class="table-scroll-container">
        <table>
          <thead>
            <tr>
              <th>ปีผลิต</th>
              <th>วันที่รับเข้า</th>
              <th>ราคา(บาท)</th>
              <th>จำนวนรับเข้า</th>
              <th>จำนวนเบิกออก</th>
              <th>คงเหลือ</th>
              <th v-if="isLoggedIn">การดำเนินการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in stockLots" :key="lot.lot_id">
              <td>{{ lot.year_manufactured }}</td>
              <td>{{ lot.date_in }}</td>
              
              <td class="right">{{ formatPrice(lot.price) }}</td>
              <td class="right">{{ lot.quantity_in }}</td>
              <td class="right">{{ lot.total_out }}</td>
              <td class="right">
                <strong>{{ lot.quantity_remaining }}</strong>
              </td>
              <td class="action-cell" v-if="isLoggedIn">
                <RouterLink :to="`/stock-out-form/${lot.lot_id}`" class="stock-out-button">
                  เบิกออก
                </RouterLink>
                <LotDeleteButton
                  v-if="isLoggedIn"
                  :lot-id="lot.lot_id"
                  endpoint-url="/api/tire-lots/"
                  @delete-success="onLotDeleted"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* --- 1. The Card UI --- */
.tire-detail-container {
 background-color: #ffffff;
 padding: 1.5rem 2rem;
 border-radius: 8px;
 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  color: #000;
  font-family: sans-serif;
}

/* --- 2. New Page Header (Flexbox) --- */
.page-header {
 display: flex;
 justify-content: space-between;
 align-items: flex-start; /* จัดให้อยู่ด้านบน */
 border-bottom: 2px solid #f0f0f0;
 padding-bottom: 1rem;
 margin-bottom: 1.5rem;
}
.header-info h1 {
 margin: 0 0 0.25rem 0;
  color: #000;
}
.header-info h2 {
 margin: 0;
 font-size: 1.2rem;
 font-weight: normal;
 color: #555;
}
.back-button {
 background-color: #f0f0f0;
 border: 1px solid #ccc;
 padding: 8px 16px;
 border-radius: 5px;
 cursor: pointer;
 font-size: 0.9em;
 color: #000;
 transition: background-color 0.2s ease;
  flex-shrink: 0; /* ป้องกันปุ่มหด */
}
.back-button:hover {
 background-color: #e0e0e0;
}

/* --- 3. Table and Content Styles --- */
h3 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
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

.table-scroll-container {
 max-height: 400px; /* คุณปรับความสูงนี้ได้ */
 overflow-y: auto;
 border: 1px solid #ddd;
 border-radius: 4px;
}
table {
 width: 100%;
 border-collapse: collapse;
}
thead {
 background-color: #f4f4f4;
 position: sticky;
 top: 0;
 z-index: 1;
}
th, td {
 border: 1px solid #ddd;
 padding: 12px;
 text-align: left;
 color: #000;
 vertical-align: middle;
}
td.right {
 text-align: right;
}
td.action-cell {
 text-align: center;
}
td strong {
 font-size: 1.1em;
 color: #0056b3;
}
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
</style>