<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' 
import axios from 'axios'

// 2. สร้าง Refs สำหรับ v-model
// --- Product Fields ---
const brand = ref('')
const pattern = ref('')
const size = ref('')

// --- (แก้ไข) 1. เก็บค่าเริ่มต้นไว้เปรียบเทียบ ---
const defaultYear = new Date().getFullYear()
const defaultDate = new Date().toISOString().split('T')[0]
const defaultQuantity = 1

// --- Lot Fields ---
const year_manufactured = ref(defaultYear) 
const date_in = ref(defaultDate) 
const quantity_in = ref(defaultQuantity) 

// 3. สร้าง state สำหรับการโหลดและ error
const isLoading = ref(false)
const errorMessage = ref(null)

// 4. Import Router สำหรับการนำทาง
const router = useRouter()

// 5. เขียนฟังก์ชัน 'เพิ่มสินค้า' (โค้ดเดิม)
async function add_new_product() {
// ตรวจสอบค่าเบื้องต้น
 if (quantity_in.value <= 0) {
 errorMessage.value = 'จำนวนรับเข้าต้องมากกว่า 0'
  return
 }
 
 isLoading.value = true
 errorMessage.value = null

 const payload = {
  brand: brand.value,
  pattern: pattern.value,
  size: size.value,
  year_manufactured: parseInt(year_manufactured.value),
  date_in: date_in.value,
  quantity_in: parseInt(quantity_in.value)
 }

 try {
  await axios.post('http://localhost:8000/api/stock-in/', payload)
  
  alert('เพิ่มสินค้าและล็อตใหม่สำเร็จ!')
  router.push('/') 

 } catch (error) {
  console.error('Error adding product:', error)
  if (error.response && error.response.data) {
   errorMessage.value = JSON.stringify(error.response.data)
  } else {
   errorMessage.value = 'เกิดข้อผิดพลาด ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้'
  }
 } finally {
  isLoading.value = false
 }
}

// 10. (แก้ไข) ฟังก์ชันสำหรับปุ่ม "ย้อนกลับ"
function goBackHome() {
  
  // --- 2. ตรวจสอบว่าฟอร์มมีการแก้ไขหรือไม่ (Is Dirty?) ---
  const isDirty = brand.value !== '' ||
                  pattern.value !== '' ||
                  size.value !== '' ||
                  year_manufactured.value !== defaultYear ||
                  date_in.value !== defaultDate ||
                  quantity_in.value !== defaultQuantity;

  if (isDirty) {
    // --- 3. ถ้ามีการแก้ไข ให้ถามยืนยัน ---
    const confirmed = confirm(
      'คุณมีการเปลี่ยนแปลงที่ยังไม่ได้บันทึก คุณแน่ใจหรือไม่ว่าต้องการออกจากหน้านี้?'
    );
    
    // ถ้าผู้ใช้กดยืนยัน (OK) ถึงจะกลับไป
    if (confirmed) {
      router.push('/');
    }
    // ถ้ากด Cancel ก็ไม่ต้องทำอะไร
  } else {
    // --- 4. ถ้าฟอร์มสะอาด ไม่ต้องถาม ---
    router.push('/');
  }
}
</script>

<template>
  <main class="stock-in-form-container">
    
    <div class="form-header">
      <button @click="goBackHome" class="back-button">
        &larr; กลับหน้าหลัก
      </button>
      <h1>เพิ่มสินค้าเข้าสต็อก (Stock-In)</h1>
    </div>

    <div v-if="errorMessage" class="error-message">
      <strong>Error:</strong> {{ errorMessage }}
    </div>

    <form @submit.prevent="add_new_product" class="stock-in-form">

      <fieldset>
        <legend>ข้อมูลสินค้า (Product Info)</legend>
        <div class="form-group">
          <label for="brand">ยี่ห้อ (Brand)</label>
          <input id="brand" v-model="brand" type="text" placeholder="เช่น Michelin" required>
        </div>
        <div class="form-group">
          <label for="pattern">ลายดอกยาง (Pattern)</label>
          <input id="pattern" v-model="pattern" type="text" placeholder="เช่น Pilot Sport 5" required>
        </div>
        <div class="form-group">
          <label for="size">ขนาด (Size)</label>
          <input id="size" v-model="size" type="text" placeholder="เช่น 225/45R18" required>
        </div>
      </fieldset>

      <fieldset>
        <legend>ข้อมูลล็อต (Lot Info)</legend>
        <div class="form-group">
          <label for="year">ปีที่ผลิต (Year)</label>
          <input id="year" v-model.number="year_manufactured" type="number" min="2000" :max="new Date().getFullYear() + 1" required>
        </div>
        <div class="form-group">
          <label for="date_in">วันที่รับเข้า (Date In)</label>
          <input id="date_in" v-model="date_in" type="date" required>
        </div>
        <div class="form-group">
          <label for="quantity">จำนวนรับเข้า (Quantity)</label>
          <input id="quantity" v-model.number="quantity_in" type="number" min="1" required>
        </div>
      </fieldset>

      <button type="submit" class="submit-button" :disabled="isLoading">
        {{ isLoading ? 'กำลังบันทึก...' : 'บันทึกข้อมูล' }}
      </button>

        <button type="button" @click="goBackHome">
          ย้อนกลับ
        </button>
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
}

.back-button {
  background: none;
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
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
}

legend {
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0 0.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
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
