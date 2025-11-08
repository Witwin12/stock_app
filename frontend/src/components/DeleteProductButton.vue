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
  }
})

// 2. สร้าง 'emit' เพื่อส่งสัญญาณบอก Parent ว่าลบสำเร็จ
const emit = defineEmits(['delete-success'])

// 3. ฟังก์ชันสำหรับลบ (Soft Delete)
async function handleDelete() {
  // 3.1. ถามยืนยัน
  const confirmed = confirm(
    'คุณแน่ใจหรือไม่ว่าต้องการลบรายการนี้? (ข้อมูลจะถูกซ่อนจากระบบ)'
  )
  if (!confirmed) return

  try {
    // 3.2. ยิง PATCH request
    await axios.patch(
      `http://localhost:8000${props.endpointUrl}${props.productId}/`,
      {
        "is_active": false 
      }
    )
    
    // 3.3. ส่งสัญญาณ 'delete-success' บอก Parent
    emit('delete-success', props.productId)

  } catch (err) {
    console.error('Error deleting item:', err)
    alert('เกิดข้อผิดพลาด: ไม่สามารถลบได้')
  }
}
</script>

<template>
  <button @click="handleDelete" class="button-delete">
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