<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

// ====== STATE ======
const router = useRouter()
const route = useRoute()
const productId = route.params.id

const product = ref(null)
const stockLots = ref([])
const loading = ref(true)
const error = ref(null)

// ====== API CALLS ======
async function fetchProductDetails() {
  loading.value = true
  error.value = null

  try {
    const [productRes, stockRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/tire-products/${productId}/`),
      axios.get(`http://localhost:8000/api/tire-products/${productId}/stock_by_year/`)
    ])

    product.value = productRes.data
    stockLots.value = stockRes.data
  } catch (err) {
    console.error('Error fetching product details:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลสินค้าได้'
  } finally {
    loading.value = false
  }
}

// ====== HANDLERS ======
function goBack() {
  router.back()
}

// ====== LIFECYCLE ======
onMounted(fetchProductDetails)
</script>

<template>
  <div class="tire-detail-container">
    <!-- Loading -->
    <div v-if="loading">กำลังโหลดข้อมูล...</div>

    <!-- Error -->
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Product Info -->
    <div v-else-if="product">
      <h1>{{ product.brand }} {{ product.pattern }}</h1>
      <h2>ขนาด: {{ product.size }}</h2>
      <hr />

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
            <td class="right">{{ lot.quantity_in }}</td>
            <td class="right">{{ lot.total_out }}</td>
            <td class="right"><strong>{{ lot.quantity_remaining }}</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Back Button -->
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
}

td.right {
  text-align: right;
}

td strong {
  font-size: 1.1em;
  color: #0056b3;
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
