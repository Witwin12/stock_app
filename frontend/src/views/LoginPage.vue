<script setup>
import { ref } from 'vue'
// (ลบ useRouter ออก เพราะเราจะใช้ window.location)
import axios from 'axios'

// --- State ---
const username = ref('')
const password = ref('')
const errorMessage = ref(null)
const isSubmitting = ref(false)

// --- (นี่คือ Function ที่แก้ไขใหม่ทั้งหมด) ---
async function handleLogin() {
  isSubmitting.value = true
  errorMessage.value = null

  const payload = {
    username: username.value,
    password: password.value
  }

  try {
    // --- ขั้นตอนที่ 1: POST ไปที่ /login/ เพื่อเอา "Key" ---
    const loginResponse = await axios.post('http://localhost:8000/api/auth/login/', payload)
    
    // (ถ้ามาถึงตรงนี้ = Login สำเร็จ)
    const token = loginResponse.data.key
    
    // (เก็บ Token ไว้ใน Headers สำหรับการยิงครั้งต่อไป)
    const headers = {
      'Authorization': `Token ${token}`
    }

    // --- ขั้นตอนที่ 2: GET ไปที่ /user/ (โดยใช้ Key) เพื่อเอา "User Data" ---
    const userResponse = await axios.get('http://localhost:8000/api/auth/user/', { headers })
    
    // (ถ้ามาถึงตรงนี้ = ได้ข้อมูล User สำเร็จ)
    const userData = userResponse.data // นี่คือ { id: ..., role: ... }

    // --- ขั้นตอนที่ 3: บันทึก "ทั้งสองอย่าง" ลง localStorage ---
    
    // 1. บันทึก Key (Token)
    localStorage.setItem('authToken', token)
    
    // 2. บันทึก User Data (ที่ตอนนี้เป็น JSON ที่ถูกต้อง)
    localStorage.setItem('userData', JSON.stringify(userData))

    // 4. สั่งให้ Vue โหลดหน้าเว็บใหม่ (ไปที่หน้าหลัก)
    //    (App.vue จะอ่านค่าใหม่นี้ และ JSON.parse จะไม่พังแล้ว!)
    window.location.href = '/' 

  } catch (error) {
    // 5. ถ้า Error (เช่น รหัสผิด หรือ 401)
    console.error('Login process failed:', error)
    
    if (error.response?.data?.non_field_errors) {
      errorMessage.value = error.response.data.non_field_errors[0]
    } else if (error.response?.status === 401) {
        errorMessage.value = "Token ไม่ถูกต้อง (401)"
    } else {
      errorMessage.value = 'เกิดข้อผิดพลาดในการล็อกอิน (กรุณาลองใหม่)'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>เข้าสู่ระบบ</h1>
      <p>กรุณาป้อน Username และ Password ของคุณ</p>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div class="form-group">
        <label for="username">Username</label>
        <input 
          id="username" 
          v-model="username" 
          type="text" 
          placeholder="ระบุ Username" 
          required 
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input 
          id="password" 
          v-model="password" 
          type="password" 
          placeholder="ระบุ Password" 
          required 
        />
      </div>

      <button type="submit" class="submit-button" :disabled="isSubmitting">
        {{ isSubmitting ? 'กำลังล็อกอิน...' : 'ล็อกอิน' }}
      </button>
    </form>
  </main>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f4f4f4;
  color: #000;
}

.login-form {
  background: #fff;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin-bottom: 0.5rem;
  color: #000;
}

p {
  margin-bottom: 1.5rem;
  color: #555;
}

.form-group {
  text-align: left;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #000;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  color: #000;
  box-sizing: border-box; 
}

.submit-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff; /* สีน้ำเงิน (เปลี่ยนได้) */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.submit-button:hover {
  background-color: #0056b3;
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
  text-align: center;
  font-weight: bold;
}
</style>