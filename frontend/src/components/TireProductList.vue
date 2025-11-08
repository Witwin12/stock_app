<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import DeleteButton from '@/components/DeleteProductButton.vue'

// --- State ---
const products = ref([])
const error = ref(null)
const searchText = ref('')

// --- Fetch Products ---
async function fetchProducts(searchTerm = '') {
  error.value = null
  try {
    let url = 'http://localhost:8000/api/tire-products/'
    if (searchTerm.trim()) {
      url += `?search=${encodeURIComponent(searchTerm.trim())}`
    }
    const response = await axios.get(url)
    products.value = response.data
  } catch (err) {
    console.error('Error fetching products:', err)
    error.value = 'ไม่สามารถโหลดข้อมูลได้'
  }
}

// --- Search Functions ---
function triggerSearch() {
  fetchProducts(searchText.value)
}

function clearSearch() {
  searchText.value = ''
  fetchProducts()
}

// --- Delete Event Handler ---
function onProductDeleted(deletedProductId) {
  products.value = products.value.filter(
    (product) => product.product_id !== deletedProductId
  )
}

// --- Lifecycle ---
onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="tire-stock-container">
    <h1 class="page-title">รายการสต็อกยาง</h1>

    <div class="search-container">
      <input 
        v-model="searchText"
        @keyup.enter="triggerSearch"
        type="text"
        placeholder="ค้นหา (ยี่ห้อ, ลาย, หรือขนาด)"
      />
      <button @click="triggerSearch">ค้นหา</button>
      <button @click="clearSearch" class="button-clear">ล้าง</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>ยี่ห้อ</th>
          <th>ลายดอกยาง</th>
          <th>ขนาด</th>
          <th>คงเหลือ</th>
          <th class="header-actions">การดำเนินการ</th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="products.length === 0">
          <td colspan="5" class="no-data">ไม่พบข้อมูลสินค้า</td>
        </tr>

        <tr v-for="product in products" :key="product.product_id">
          <td>{{ product.brand }}</td>
          <td>{{ product.pattern }}</td>
          <td>{{ product.size }}</td>
          <td class="right">{{ product.total_stock_on_hand }}</td>

          <td class="actions">
            <RouterLink 
              :to="`/product/${product.product_id}`"
              class="button-detail"
            >
              ดูสต็อก
            </RouterLink>

            <DeleteButton 
              :product-id="product.product_id"
              endpoint-url="/api/tire-products/"
              @delete-success="onProductDeleted"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.tire-stock-container {
  font-family: sans-serif;
  color: #000;
}

/* ===== Title ===== */
.page-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #000;
}

/* ===== Search Box ===== */
.search-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.search-container input {
  flex-grow: 1;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  color: #000;
}

.search-container button {
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-container button:hover {
  opacity: 0.9;
}

.search-container button:not(.button-clear) {
  background-color: #007bff;
}

.search-container .button-clear {
  background-color: #6c757d;
}

/* ===== Table ===== */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  color: #000;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

thead {
  background-color: #f4f4f4;
}

td.right {
  text-align: right;
  font-weight: bold;
}

.no-data {
  text-align: center;
  color: #777;
  font-style: italic;
}

th.header-actions {
  text-align: center;
}

/* ===== Action Buttons ===== */
.actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
}

.button-detail {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.9em;
  transition: background-color 0.2s;
}

.button-detail:hover {
  background-color: #0056b3;
}
</style>
