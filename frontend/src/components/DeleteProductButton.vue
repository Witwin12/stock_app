<script setup>
import api from '@/api/axios'
import { useAuth } from '@/composables/useAuth'

// --- รับ props จาก parent ---
const props = defineProps({
  productId: {
    type: [Number, String],
    required: true
  },
  endpointUrl: {
    type: String,
    required: true
  }
})

// --- ใช้ useAuth() เพื่อดึงข้อมูล user ---
const { userData, isLoggedIn } = useAuth()

// --- emit event กลับไปเมื่อสำเร็จ ---
const emit = defineEmits(['delete-success'])

async function handleDelete() {
  if (!confirm('ยืนยันการลบถาวร?\nข้อมูลนี้จะหายไปอย่างถาวรและกู้คืนไม่ได้')) return

  if (!isLoggedIn.value) {
    alert('กรุณาเข้าสู่ระบบก่อนทำรายการนี้')
    return
  }

  if (userData.value?.role !== 'admin') {
    alert('คุณไม่มีสิทธิ์ในการลบข้อมูลนี้')
    return
  }

  try {
    await api.delete(`${props.endpointUrl}${props.productId}/`)
    emit('delete-success', props.productId)
  } catch (err) {
    console.error('Error hard deleting item:', err)
    const msg = err.response?.status === 403
      ? 'คุณไม่มีสิทธิ์ในการลบข้อมูลนี้'
      : 'เกิดข้อผิดพลาด: ไม่สามารถลบถาวรได้'
    alert(msg)
  }
}
</script>

<template>
  <!-- แสดงเฉพาะเมื่อเป็นแอดมิน -->
  <button
    v-if="userData?.role === 'admin'"
    @click="handleDelete"
    class="button-delete"
  >
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