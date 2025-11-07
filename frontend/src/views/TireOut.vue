<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

// --- 1. State และ Router ---
const router = useRouter()
const route = useRoute()
const lotId = route.params.lotId 

// --- 2. State สำหรับแสดงข้อมูล Lot ---
const lotDetails = ref(null) 
const loading = ref(true)
const errorMessage = ref(null)

// --- 3. State สำหรับ Form (v-model) และเก็บค่า Default ---
const defaultEmployeeId = ''
const defaultQuantityOut = 1 
const defaultDateOut = new Date().toISOString().split('T')[0]
const defaultRemarks = ''
const employee_id = ref(defaultEmployeeId)
const quantity_out = ref(defaultQuantityOut)
const date_out = ref(defaultDateOut)
const remarks = ref(defaultRemarks)
const isSubmitting = ref(false)
const loadedDefaultQuantity = ref(defaultQuantityOut)

// --- 4. ดึงข้อมูล Lot เมื่อเปิดหน้า ---
async function fetchLotDetails() {
 loading.value = true
 errorMessage.value = null
 try {
  const response = await axios.get(`http://localhost:8000/api/tire-lots/${lotId}/`)
  lotDetails.value = response.data
  if (lotDetails.value.quantity_remaining <= 0) {
   quantity_out.value = 0
   loadedDefaultQuantity.value = 0
  } else {
   loadedDefaultQuantity.value = 1
  }
 } catch (err) {
  console.error('Error fetching lot details:', err)
  errorMessage.value = 'ไม่พบข้อมูลล็อต หรือไม่สามารถเชื่อมต่อ API ได้'
 } finally {
  loading.value = false
 }
}

// --- 5. Logic การเบิกออก (Submit Form) ---
async function handleStockOut() {
  // ... (โค้ดส่วนนี้เหมือนเดิม) ...
 isSubmitting.value = true
 errorMessage.value = null
 const qty = parseInt(quantity_out.value)
 if (qty <= 0) {
  errorMessage.value = 'จำนวนที่เบิกต้องมากกว่า 0'
  isSubmitting.value = false
  return
 }
 if (qty > lotDetails.value.quantity_remaining) {
  errorMessage.value = `เบิกเกิน! ยอดคงเหลือมี ${lotDetails.value.quantity_remaining} เส้น`
  isSubmitting.value = false
  return
 }
 if (employee_id.value === '') {
   errorMessage.value = 'กรุณาระบุ ID พนักงาน'
  isSubmitting.value = false
  return
 }
 const payload = {
  lot: parseInt(lotId),
  employee: parseInt(employee_id.value),
  quantity_out: qty,
  date_out: date_out.value,
  remarks: remarks.value
 }
 try {
  await axios.post('http://localhost:8000/api/stock-out/', payload)
  alert('เบิกสินค้าสำเร็จ!')
    
    // (แก้ไข) เปลี่ยนเป็น router.back()
  router.back(); 

 } catch (error) {
  console.error('Error submitting stock out:', error)
  if (error.response && error.response.data) {
   errorMessage.value = JSON.stringify(error.response.data)
  } else {
   errorMessage.value = 'เกิดข้อผิดพลาดในการบันทึก'
  }
 } finally {
  isSubmitting.value = false
 }
}

// --- 6. (แก้ไข) ฟังก์ชันสำหรับปุ่ม "ย้อนกลับ" (ปุ่มยกเลิก) ---
function goBack() {

 // 1. ตรวจสอบว่าฟอร์มมีการแก้ไขหรือไม่ (Is Dirty?)
 const isDirty = employee_id.value !== defaultEmployeeId ||
         quantity_out.value !== loadedDefaultQuantity.value || 
         date_out.value !== defaultDateOut ||
         remarks.value !== defaultRemarks;
 
 if (isDirty) {
  // 2. ถ้ามีการแก้ไข ให้ถามยืนยัน
  const confirmed = confirm(
   'คุณมีการเปลี่ยนแปลงที่ยังไม่ได้บันทึก คุณแน่ใจหรือไม่ว่าต้องการออกจากหน้านี้?'
  );
  
  if (!confirmed) {
   return; // ถ้ากด Cancel ก็ไม่ต้องทำอะไร
  }
 }

 // 3. (จุดที่แก้ไข)
  //    เปลี่ยนจาก router.push(targetPath) เป็น router.back()
 router.back(); // กลับไปหน้าก่อนหน้า (คือ /product/1)
}

// --- 7. Lifecycle ---
onMounted(fetchLotDetails)
</script>

<template>
 <main class="stock-out-form-container">
  
  <div class="form-header">
   <button @click="goBack" class="back-button">
    &larr; ย้อนกลับ
   </button>
   <h1>ฟอร์มเบิกสินค้า (Stock-Out)</h1>
  </div>

    <div v-if="loading" class="loading-message">กำลังโหลดข้อมูลล็อต...</div>
  
    <div v-if="errorMessage" class="error-message">
   <strong>Error:</strong> {{ errorMessage }}
  </div>

    <form v-if="lotDetails && !loading" @submit.prevent="handleStockOut" class="stock-out-form">
   
   <fieldset class="lot-details">
    <legend>รายละเอียดล็อต (Lot ID: {{ lotId }})</legend>
    <h3>{{ lotDetails.product.brand }} {{ lotDetails.product.pattern }}</h3>
    <div><strong>ขนาด:</strong> {{ lotDetails.product.size }}</div>
    <div><strong>ปีผลิต:</strong> {{ lotDetails.year_manufactured }}</div>
    <div><strong>วันที่รับเข้า:</strong> {{ lotDetails.date_in }}</div>
    
    <div class="remaining-highlight"> ยอดคงเหลือ: <strong>{{ lotDetails.quantity_remaining }}</strong> เส้น
    </div>
   </fieldset>

   <fieldset>
    <legend>ข้อมูลการเบิก</legend>
    
    <div class="form-group">
     <label for="employee">ID พนักงาน (Employee ID)</label>
     <input id="employee" v-model="employee_id" type="number" placeholder="เช่น 1 หรือ 2" required>
    </div>

    <div class="form-group">
     <label for="quantity">จำนวนที่เบิก (Quantity)</label>
     <input 
      id="quantity" 
      v-model.number="quantity_out" 
      type="number" 
      min="1"
      :max="lotDetails.quantity_remaining" 
      :disabled="lotDetails.quantity_remaining <= 0"
      required
     >
    </div>

    <div class="form-group">
     <label for="date_out">วันที่เบิกออก (Date Out)</label>
     <input id="date_out" v-model="date_out" type="date" required>
    </div>

    <div class="form-group">
     <label for="remarks">หมายเหตุ (Remarks)</label>
     <textarea id="remarks" v-model="remarks" rows="3"></textarea>
    </div>
   </fieldset>

      <button 
    type="submit" 
    class="submit-button" 
    :disabled="isSubmitting || lotDetails.quantity_remaining <= 0"
   >
    {{ isSubmitting ? 'กำลังบันทึก...' : 'ยืนยันการเบิกออก' }}
   </button>
   
      <button 
        type="button" 
        class="cancel-button"
        @click="goBack"
        :disabled="isSubmitting"
      >
        ยกเลิก
      </button>

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