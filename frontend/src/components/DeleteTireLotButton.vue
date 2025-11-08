<script setup>
import axios from 'axios'

// 1. รับ ID และ URL มาจาก Parent
const props = defineProps({
  lotId: {
    type: [Number, String],
    required: true
  },
  endpointUrl: {
    type: String,
    required: true // (เช่น /api/tire-lots/)
  }
})

// 2. สร้าง 'emit' เพื่อส่งสัญญาณบอก Parent
const emit = defineEmits(['delete-success'])

// 3. ฟังก์ชันสำหรับลบ (Hard Delete)
async function handleDelete() {
  
  // 3.1. ถามยืนยัน (พร้อมคำเตือน)
  const confirmed = confirm(
    'คุณแน่ใจหรือไม่ว่าต้องการลบล็อตนี้?\n(ข้อควรระวัง: จะลบได้เฉพาะล็อตที่ยังไม่เคยมีการเบิกออกเท่านั้น)'
  )
  if (!confirmed) return

  try {
    // 3.2. ยิง DELETE request (ตามที่คุณต้องการ)
    await axios.delete(
      `http://localhost:8000${props.endpointUrl}${props.lotId}/`
    )
    
    // 3.3. ส่งสัญญาณ 'delete-success' บอก Parent
    alert('ลบล็อตสำเร็จ')
    emit('delete-success', props.lotId)

  } catch (err) {
    // 3.4. (สำคัญ) จัดการ Error 400 จาก Django
    console.error('Error deleting lot:', err)
    if (err.response && err.response.status === 400) {
      // แสดง Error ที่ Django ส่งกลับมา (เช่น "ลบไม่ได้: ล็อตนี้มีประวัติ...")
      alert(`ลบล้มเหลว: ${err.response.data.error}`)
    } else {
      alert('เกิดข้อผิดพลาด: ไม่สามารถลบได้')
    }
  }
}
</script>

<template>
  <button @click="handleDelete" class="button-delete-lot">
    ลบ
  </button>
</template>

<style scoped>
/* 5. สไตล์สำหรับปุ่มนี้  */
.button-delete-lot {
  display: inline-block;
  padding: 6px 14px;
  font-size: 0.9em;
  font-weight: bold;
  color: #fff;
  background-color: #dc3545; /* สีแดง */
  border: none;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-left: 0.5rem; /* เว้นระยะห่างจากปุ่ม "เบิกออก" */
}
.button-delete-lot:hover {
  background-color: #5a6268;
}
</style>