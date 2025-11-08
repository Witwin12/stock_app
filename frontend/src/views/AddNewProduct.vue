<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// --- Defaults ---
const defaults = {
  brand: '',
  pattern: '',
  size: '',
  year: new Date().getFullYear(),
  date: new Date().toISOString().split('T')[0],
  quantity: 1
}

// --- Form State ---
const brand = ref(defaults.brand)
const pattern = ref(defaults.pattern)
const size = ref(defaults.size)
const year_manufactured = ref(defaults.year)
const date_in = ref(defaults.date)
const quantity_in = ref(defaults.quantity)

const isLoading = ref(false)
const errorMessage = ref(null)

// --- Submit Handler ---
async function addNewProduct() {
  if (quantity_in.value <= 0)
    return (errorMessage.value = 'จำนวนรับเข้าต้องมากกว่า 0')

  const payload = {
    brand: brand.value,
    pattern: pattern.value,
    size: size.value,
    year_manufactured: +year_manufactured.value,
    date_in: date_in.value,
    quantity_in: +quantity_in.value
  }

  try {
    isLoading.value = true
    await axios.post('http://localhost:8000/api/stock-in/', payload)
    alert('เพิ่มสินค้าเรียบร้อย!')
    router.push('/')
  } catch (error) {
    console.error(error)
    errorMessage.value = error.response?.data
      ? JSON.stringify(error.response.data)
      : 'เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์'
  } finally {
    isLoading.value = false
  }
}

// --- Back Button ---
function goBackHome() {
  const isDirty =
    brand.value ||
    pattern.value ||
    size.value ||
    year_manufactured.value !== defaults.year ||
    date_in.value !== defaults.date ||
    quantity_in.value !== defaults.quantity

  if (!isDirty || confirm('คุณแน่ใจหรือไม่ว่าจะออกโดยไม่บันทึก?'))
    router.push('/')
}
</script>

<template>
  <main class="stock-in-form-container">
    <div class="form-header">
      <button @click="goBackHome" class="back-button">&larr; กลับหน้าหลัก</button>
      <h1>เพิ่มสินค้าเข้าสต็อก (Stock-In)</h1>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <form @submit.prevent="addNewProduct" class="stock-in-form">
      <fieldset>
        <legend>ข้อมูลสินค้า</legend>
        <div class="form-group"><label>ยี่ห้อ</label><input v-model="brand" required /></div>
        <div class="form-group"><label>ลายดอกยาง</label><input v-model="pattern" required /></div>
        <div class="form-group"><label>ขนาด</label><input v-model="size" required /></div>
      </fieldset>

      <fieldset>
        <legend>ข้อมูลล็อต</legend>
        <div class="form-group">
          <label>ปีที่ผลิต</label>
          <input v-model.number="year_manufactured" type="number" min="2000" :max="new Date().getFullYear() + 1" required />
        </div>
        <div class="form-group">
          <label>วันที่รับเข้า</label>
          <input v-model="date_in" type="date" required />
        </div>
        <div class="form-group">
          <label>จำนวนรับเข้า</label>
          <input v-model.number="quantity_in" type="number" min="1" required />
        </div>
      </fieldset>

      <button type="submit" class="submit-button" :disabled="isLoading">
        {{ isLoading ? 'กำลังบันทึก...' : 'บันทึกข้อมูล' }}
      </button>
      <button type="button" @click="goBackHome">ย้อนกลับ</button>
    </form>
  </main>
</template>

<style scoped>

.stock-in-form-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  color: #000; 
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.form-header h1 {
  margin: 0;
  font-size: 1.75rem;
  color: #000; 
}

.back-button {
  background: none;
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #000; 
}
.back-button:hover {
  background-color: #f4f4f4;
  border-color: #aaa;
}

.stock-in-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

fieldset {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #000; 
}

legend {
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0 0.5rem;
  color: #000;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #000;
}

/* ช่อง input ทั่วไป */
.form-group input {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  background-color: #fff;
  color: #000;
}

/*  ปรับสไตล์ช่องวันที่ + ใส่ไอคอนตกแต่ง */
.form-group input[type="date"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;

  background-color: #fff;
  color: #000;
  padding: 0.75rem 2.5rem 0.75rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;

  /* ไอคอนตกแต่งทางขวา */
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='gray' viewBox='0 0 24 24'><path d='M19 4h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z'/></svg>");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 20px;
  cursor: pointer;
  position: relative;
}

/*  ทำให้ปฏิทินของ browser ยังคงกดได้ */
.form-group input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 1; /* ให้แสดงปกติ */
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  cursor: pointer;
  background: transparent;
  color: transparent;
}


.submit-button {
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: #28a745; /* สีเขียว */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.submit-button:hover {
  background-color: #218838;
}
.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  padding: 1rem;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  margin-bottom: 1.5rem;
}

</style>
