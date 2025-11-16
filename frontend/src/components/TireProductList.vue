<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import DeleteButton from '@/components/DeleteProductButton.vue'

// --- State ---
const products = ref([])
const error = ref(null)
const searchText = ref('')
const loading = ref(true)
const isLoggedIn = ref(false)
const isAdmin = ref(false)

// --- Fetch Products ---
async function fetchProducts(searchTerm = '') {
  error.value = null
  loading.value = true
  const token = localStorage.getItem('authToken')
  const headers = token
  ? { Authorization: `Token ${token}` }
  : {}
  try {
    const url = 'http://localhost:8000/api/tire-products/'
    const params = {}
    if (searchTerm.trim()) {
      params.search = searchTerm.trim()
    }
    const response = await axios.get(url, { 
        params,
        headers 
    })
    products.value = response.data
} catch (err) {
    console.error('Error fetching products:', err)
    // (ตอนนี้ Error 401 จะเกิดเฉพาะ "Token ผิด" เท่านั้น)
    if (err.response?.status === 401) {
        error.value = "Token ไม่ถูกต้อง, กรุณาล็อกอินใหม่ (401)"
    } else {
        error.value = 'ไม่สามารถโหลดข้อมูลได้'
    }
  } finally {
    loading.value = false 
  }
}

// --- ตรวจสอบสิทธิ์ผู้ใช้ ---
async function checkUserRole() {
  const token = localStorage.getItem('authToken')
  if (!token) {
    isAdmin.value = false
    return
  }

  try {
    const response = await axios.get('http://localhost:8000/api/auth/user/', {
      headers: { Authorization: `Token ${token}` }
    })
    // สมมติ Django ส่งข้อมูลกลับเช่น { username: "admin", is_admin: true }
    isAdmin.value = response.data.role === 'admin'
  } catch (err) {
    console.error('Error checking user role:', err)
    isAdmin.value = false
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
  const token = localStorage.getItem('authToken')

  isLoggedIn.value = !!token  
  
 checkUserRole()
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

    <div class="table-scroll-container">
      <table>
        <thead>
          <tr>
            <th>ยี่ห้อ</th>
            <th>ลายดอกยาง</th>
            <th>ขนาด</th>
            <th>คงเหลือ</th>
            <th>สถานะ</th>
            <th class="header-actions">การดำเนินการ</th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="products.length === 0">
            <td colspan="6" class="no-data">ไม่พบข้อมูลสินค้า</td>
          </tr>

          <tr
            v-for="product in products"
            :key="product.product_id"
            :class="{ 'out-of-stock': !product.is_active }"
          >
            <td>{{ product.brand }}</td>
            <td>{{ product.pattern }}</td>
            <td>{{ product.size }}</td>
            <td class="right">{{ product.total_stock_on_hand }}</td>

            <td class="status-cell">
              <span :class="product.is_active ? 'status-in' : 'status-out'">
                {{ product.stock_status }}
              </span>
            </td>

            <td class="actions">
              <RouterLink
                :to="`/product/${product.product_id}`"
                class="button-detail"
              >
                ดูสต็อก
              </RouterLink>

              <DeleteButton
                v-if="isAdmin"
                :product-id="product.product_id"
                endpoint-url="/tire-products/"
                :is-admin="isAdmin"
                @delete-success="onProductDeleted"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
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

/* 2. [เพิ่ม] สไตล์สำหรับกรอบที่ห่อตาราง */
.table-scroll-container {
  max-height: 300px; /*  คุณสามารถปรับความสูงนี้ได้ตามต้องการ */
  overflow-y: auto;  /*  เพิ่ม scrollbar เมื่อเนื้อหาล้น */
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  color: #000;
  /* * ไม่จำเป็นต้องมี margin-top ที่นี่แล้ว 
    * เพราะเราย้ายไปไว้ที่ .table-scroll-container
    */
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

thead {
  background-color: #f4f4f4;

  /* 3. [เพิ่ม] ทำให้หัวตาราง "ติดหนึบ" */
  position: sticky;
  top: 0;
  z-index: 1; /*  เพื่อให้หัวตารางอยู่เหนือเนื้อหา (tbody) เสมอ */
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

/* 1. สไตล์สำหรับแถวที่ "ของหมด" */
tr.out-of-stock {
  background-color: #f8f9fa; /* สีเทาจางๆ */
  color: #6c757d; /* สีตัวอักษรจางลง */
}
/* (เพื่อให้ปุ่มในแถวที่จาง สียังชัด) */
tr.out-of-stock .button-detail {
  color: white;
}

/* 2. สไตล์สำหรับ Cell "สถานะ" */
td.status-cell {
  text-align: center;
  font-weight: bold;
}

/* 3. สไตล์สำหรับสถานะ "มีสินค้า" */
.status-in {
  color: #28a745; /* สีเขียว */
}

/* 4. สไตล์สำหรับสถานะ "ของหมด" */
.status-out {
  color: #dc3545; /* สีแดง */
}
</style>
