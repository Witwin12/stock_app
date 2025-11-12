<script setup>
import axios from 'axios'

// 1. รับ productId และ endpoint มาจาก Parent
const props = defineProps({
  productId: {
    type: [Number, String],
    required: true
  },
  //ทำให้ใช้ลบอย่างอื่นได้ด้วย
  endpointUrl: {
    type: String,
    required: true // เช่น /api/tire-products/
  },
  isAdmin: {
    type: Boolean,
    default: false
  }
})

// 2. สร้าง 'emit' เพื่อส่งสัญญาณบอก Parent ว่าลบสำเร็จ
const emit = defineEmits(['delete-success'])

// 3. ฟังก์ชันสำหรับลบ
async function handleDelete() {
  // 3.1. ถามยืนยัน
 const confirmed = confirm(
    '!!! ยืนยันการลบถาวร !!!\nข้อมูลนี้จะหายไปจากฐานข้อมูลอย่างถาวรและกู้คืนไม่ได้ คุณแน่ใจหรือไม่?'
  )
  if (!confirmed) return
// 3.2. [เพิ่ม] ดึง Token มาจาก localStorage
  const token = localStorage.getItem('authToken')

  // 3.3. [เพิ่ม] ตรวจสอบว่ามี Token หรือไม่
  if (!token) {
    alert('ไม่พบข้อมูลการยืนยันตัวตน, กรุณาล็อกอินใหม่')
    return
  }

  // 3.4. [เพิ่ม] สร้าง headers
  const headers = {
    Authorization: `Token ${token}`
  }
  try {
    // 4.2. ยิง DELETE request (ไม่ใช่ PATCH และไม่ต้องมี body)
    await axios.delete(
      `http://localhost:8000${props.endpointUrl}${props.productId}/`,{ headers: headers }
    )
    
    // 4.3. ส่งสัญญาณ 'delete-success' บอก Parent
    emit('delete-success', props.productId)

  } catch (err) {
    console.error('Error hard deleting item:', err)
    
    // 4.4. ดักจับ Error หากไม่ใช่ Admin (เผื่อไว้)
    if (err.response && err.response.status === 403) {
      alert('คุณไม่มีสิทธิ์ในการลบข้อมูลนี้')
    } else {
      alert('เกิดข้อผิดพลาด: ไม่สามารถลบถาวรได้')
    }
  }
}
</script>

<template>
  <button @click="handleDelete" class="button-delete" v-if="isAdmin">
    ลบ
  </button>
</template>

<style scoped>
/* 5. สไตล์สำหรับปุ่มนี้โดยเฉพาะ */
.button-delete {
  background-color: #dc3545; /* สีแดง */
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9em;
}

.button-delete:hover {
  background-color: #c82333;
}
</style>