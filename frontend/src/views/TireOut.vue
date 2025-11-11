<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router' // (1) Import useRouter
import axios from 'axios'

// --- (2) Setup Router ---
const router = useRouter()
const lotId = useRoute().params.lotId

// --- State ---
const lotDetails = ref(null)
const loading = ref(true)
const errorMessage = ref(null)
const isSubmitting = ref(false)

// --- (3) ลบ employee_id ออกไปเลย ---
const defaults = {
  quantity: 1,
  date: new Date().toISOString().split('T')[0],
  remarks: ''
}
const quantity_out = ref(defaults.quantity)
const date_out = ref(defaults.date)
const remarks = ref(defaults.remarks)
// (ลบ loadedDefaultQuantity ทิ้งไป เราจะใช้แค่ router.back())

// --- (4) เพิ่ม Function สำหรับดึง Headers (สำคัญมาก) ---
// (เราจะใช้ Token จาก localStorage ที่ LoginView.vue เก็บไว้)
function getAuthHeaders() {
  const token = localStorage.getItem('authToken')
  if (!token) {
    errorMessage.value = "คุณยังไม่ได้ล็อกอิน!"
    // (ทางเลือก) พาไปหน้า Login
    router.push('/login') 
    return null
  }
  return {
    'Authorization': `Token ${token}`
  }
}

// --- (5) แก้ไข Fetch Lot Details (ให้แนบ Token) ---
async function fetchLotDetails() {
  const headers = getAuthHeaders()
  if (!headers) {
      loading.value = false
      return // ถ้าไม่มี Token ก็ไม่ต้องทำต่อ
  }

  try {
    loading.value = true
    const { data } = await axios.get(
      `http://localhost:8000/api/tire-lots/${lotId}/`,
      { headers } // <-- (สำคัญ) แนบ Token ไปด้วย
    )
    
    lotDetails.value = data
    const remaining = data.quantity_remaining
    quantity_out.value = remaining > 0 ? 1 : 0

  } catch (err) {
    console.error(err)
    if (err.response?.status === 401) {
        errorMessage.value = "คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้ (401)"
    } else {
        errorMessage.value = 'ไม่พบข้อมูลล็อต หรือไม่สามารถเชื่อมต่อ API ได้'
    }
  } finally {
    loading.value = false
  }
}

// --- (6) แก้ไข Submit Form (ลบ employee, แนบ Token) ---
async function handleStockOut() {
  const headers = getAuthHeaders()
  if (!headers) return // ถ้าไม่มี Token ก็ไม่ต้องทำต่อ

  const qty = +quantity_out.value

  // (ลบการตรวจสอบ employee_name ออก)
  if (!qty || qty <= 0)
    return (errorMessage.value = 'จำนวนที่เบิกต้องมากกว่า 0')

  if (qty > lotDetails.value.quantity_remaining)
    return (errorMessage.value = `เบิกเกิน! คงเหลือ ${lotDetails.value.quantity_remaining} เส้น`)

  // (7) แก้ไข Payload (เอา employee ออก)
  const payload = {
    lot: +lotId,
    // (ลบ) employee: ...  <-- Backend ไม่ต้องการแล้ว!
    quantity_out: qty,
    date_out: date_out.value,
    remarks: remarks.value
  }

  try {
    isSubmitting.value = true
    // (สำคัญ) แนบ Headers ไปด้วย
    await axios.post('http://localhost:8000/api/stock-out/', payload, { headers })
    
    // (เราควรใช้ Modal ที่เราทำไว้ใน App.vue หรือสร้างใหม่)
    alert('เบิกสินค้าสำเร็จ!') // (ชั่วคราว)
    router.back() // กลับไปหน้า List
    
  } catch (error) {
    console.error(error)
    if (error.response?.data) {
        const data = error.response.data;
        // ดึง Error แรกที่เจอ
        const firstErrorKey = Object.keys(data)[0];
        const firstErrorMessage = Array.isArray(data[firstErrorKey]) ? data[firstErrorKey][0] : data[firstErrorKey];
        errorMessage.value = firstErrorMessage || 'เกิดข้อผิดพลาดในการบันทึก';
    } else {
        errorMessage.value = 'เกิดข้อผิดพลาดในการบันทึก'
    }
  } finally {
    isSubmitting.value = false
  }
}

// --- (8) แก้ไข Cancel / Back (ให้ง่ายขึ้น) ---
function goBack() {
  // (ลบ `confirm` ที่อาจถูกบล็อก และ `isDirty` ที่พังแล้ว)
  router.back()
}

onMounted(fetchLotDetails)
</script>

<template>
  <!-- 
    (Template เกือบเหมือนเดิม)
    (เราแค่ "ลบ" ช่องกรอก "ชื่อพนักงาน" ออก)
  -->
  <main class="stock-out-form-container">
    <div class="form-header">
      <button @click="goBack" class="back-button">&larr; ย้อนกลับ</button>
      <h1>ฟอร์มเบิกสินค้า (Stock-Out)</h1>
    </div>

    <!-- (ข้อความ Error จะแสดงที่นี่) -->
    <div v-if="loading" class="loading-message">กำลังโหลดข้อมูล...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <form v-if="lotDetails" @submit.prevent="handleStockOut" class="stock-out-form">
      <fieldset class="lot-details">
        <legend>รายละเอียดล็อต (Lot ID: {{ lotId }})</legend>
        <h3>{{ lotDetails.product.brand }} {{ lotDetails.product.pattern }}</h3>
        <p><strong>ขนาด:</strong> {{ lotDetails.product.size }}</p>
        <p><strong>ปีผลิต:</strong> {{ lotDetails.year_manufactured }}</p>
        <p><strong>วันที่รับเข้า:</strong> {{ lotDetails.date_in }}</p>
        <p class="remaining-highlight">คงเหลือ: <strong>{{ lotDetails.quantity_remaining }}</strong> เส้น</p>
      </fieldset>

      <fieldset>
        <legend>ข้อมูลการเบิก</legend>

        <!-- --- (9) ลบช่องกรอก "ชื่อพนักงาน" ออกจากที่นี่ --- -->
        <!-- <div class="form-group"> ... </div> -->

        <div class="form-group">
          <label for="quantity">จำนวนที่เบิก</label>
          <input
            id="quantity" 
            v-model.number="quantity_out"
            type="number"
            min="1"
            :max="lotDetails.quantity_remaining"
            :disabled="lotDetails.quantity_remaining <= 0"
            required
          />
        </div>

        <div class="form-group">
          <label for="date_out">วันที่เบิกออก</label>
          <input id="date_out" v-model="date_out" type="date" required />
        </div>

        <div class="form-group">
          <label for="remarks">หมายเหตุ</label>
          <textarea id="remarks" v-model="remarks" rows="3"></textarea>
        </div>
      </fieldset>

      <button type="submit" class="submit-button" :disabled="isSubmitting || lotDetails.quantity_remaining <= 0">
        {{ isSubmitting ? 'กำลังบันทึก...' : 'ยืนยันการเบิกออก' }}
      </button>
      <button type="button" class="cancel-button" @click="goBack" :disabled="isSubmitting">ยกเลิก</button>
    </form>
  </main>
</template>

<style scoped>
.stock-out-form-container {
 max-width: 800px;
 margin: 2rem auto;
 padding: 2rem;
 border-radius: 8px;
 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
 background-color: #ffffff;
 color: #000; /* ตัวอักษรสีดำทั้งหมด */
}

.form-header {
 display: flex;
 align-items: center;
 justify-content: space-between;
 border-bottom: 2px solid #f0f0f0;
 padding-bottom: 1rem;
 margin-bottom: 1.5rem;
 color: #000;
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
 color: #000;
}
.back-button:hover {
 background-color: #f4f4f4;
}

.stock-out-form {
 display: flex;
 flex-direction: column;
 gap: 1.5rem; /* (หมายเหตุ: gap ระหว่าง fieldset กับปุ่ม submit) */
 color: #000;
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

/* ส่วนแสดงรายละเอียด Lot */
.lot-details {
 background-color: #f9f9f9;
 color: #000;
}
.lot-details h3 {
 margin: 0 0 0.5rem 0;
 color: #0056b3;
}
.remaining-highlight {
 margin-top: 1rem;
 font-size: 1.2rem;
 font-weight: bold;
 color: #000;
}
.remaining-highlight strong {
 font-size: 1.5rem;
 color: #dc3545;
}

.form-group {
 display: flex;
 flex-direction: column;
 color: #000;
}
.form-group label {
 font-weight: 600;
 margin-bottom: 0.5rem;
}
.form-group input,
.form-group textarea {
 padding: 0.75rem;
 border: 1px solid #ccc;
 border-radius: 4px;
 font-size: 1rem;
 color: #000;
 background-color: #fff; 
}

/* ปุ่ม Submit (สีแดง) */
.submit-button {
 padding: 1rem;
 font-size: 1.1rem;
 font-weight: bold;
 color: #fff;
 background-color: #dc3545;
 border: none;
 border-radius: 5px;
 cursor: pointer;
 transition: background-color 0.2s;
  width: 100%;
}
.submit-button:hover {
 background-color: #c82333;
}
.submit-button:disabled {
 background-color: #ccc;
 cursor: not-allowed;
}

/* (เพิ่ม) ปุ่มยกเลิก (สีเทา) */
.cancel-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333; /* สีตัวอักษรเข้ม */
  background-color: #f8f9fa; /* สีเทาอ่อน */
  border: 1px solid #ccc; /* เส้นขอบ */
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  /* (แก้ไข) ลบ gap ของ form ออก แล้วมาใช้ margin แทน */
  margin-top: 0.5rem; 
  /* (หมายเหตุ: .stock-out-form จะมี gap: 1.5rem ทำให้ปุ่มนี้ห่างจาก fieldset อยู่แล้ว) */
}

.cancel-button:hover {
  background-color: #e2e6ea; /* สีเทาเข้มขึ้น */
}
.cancel-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message, .loading-message {
 padding: 1rem;
 background-color: #f8d7da;
 color: #721c24;
 border: 1px solid #f5c6cb;
 border-radius: 5px;
 margin-bottom: 1.5rem;
}
.loading-message {
 background-color: #e2e3e5;
 color: #383d41;
 border-color: #d6d8db;
}
</style>
