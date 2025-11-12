<script setup>
import { ref } from 'vue'
import axios from 'axios'

// --- State ---
const username = ref('')
const password = ref('')
const errorMessage = ref(null)
const isSubmitting = ref(false)

// --- Function Login ---
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

    const token = loginResponse.data.key
    const headers = { 'Authorization': `Token ${token}` }

    // --- ขั้นตอนที่ 2: GET /user/ ---
    const userResponse = await axios.get('http://localhost:8000/api/auth/user/', { headers })
    const userData = userResponse.data

    // --- ขั้นตอนที่ 3: บันทึกข้อมูล ---
    localStorage.setItem('authToken', token)
    localStorage.setItem('userData', JSON.stringify(userData))

    // --- ไปหน้าแรก ---
    window.location.href = '/'

  } catch (error) {
    console.error('Login process failed:', error)

    // --- ถ้าชื่อผู้ใช้หรือรหัสผ่านผิด ---
    if (error.response?.status === 400 || error.response?.status === 401) {
      errorMessage.value = 'ข้อมูลผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
      password.value = '' // ล้างช่องรหัสออก
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
  background-color: #fff; 
  box-sizing: border-box; 
}

.form-group input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.4);
}

.submit-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
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
