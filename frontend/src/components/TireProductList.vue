<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// ====== STATE ======
const products = ref([])
const loading = ref(true)
const error = ref(null)

// ====== API CALL ======
async function fetchTireProducts() {
  loading.value = true
  error.value = null

  try {
    const { data } = await axios.get('http://localhost:8000/api/tire-products/')
    products.value = data
  } catch (err) {
    console.error('Error fetching products:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลได้'
  } finally {
    loading.value = false
  }
}

// ====== LIFECYCLE ======
onMounted(fetchTireProducts)
</script>

<template>
  <div class="product-list-container">
    <h1>รายการสต็อกยาง</h1>

    <!-- Loading -->
    <div v-if="loading">กำลังโหลดข้อมูล...</div>

    <!-- Error -->
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <!-- Table -->
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
          <td class="right">{{ product.total_stock_on_hand }}</td>
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
.product-list-container {
  font-family: sans-serif;
  max-width: 900px;
  margin: 30px auto;
  background-color: #fff;
  padding: 24px;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  color: #222;
}

/* Header */
h1 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 1.8em;
}

/* Error */
.error-message {
  color: red;
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}

/* Table */
.stock-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95em;
}

.stock-table th {
  background-color: #f5f5f5;
  color: #333;
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid #ddd;
}

.stock-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
  text-align: center;
}

.stock-table tr:hover {
  background-color: #fafafa;
}

td.right {
  text-align: right;
}

/* Button */
.detail-button {
  display: inline-block;
  background-color: #007bff;
  color: #fff;
  padding: 6px 12px;
  text-decoration: none;
  border-radius: 5px;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.detail-button:hover {
  background-color: #0056b3;
  color: #fff;
}
</style>
