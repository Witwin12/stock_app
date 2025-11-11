<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

// --- Auth State ---
const isLoggedIn = ref(false)
const userData = ref(null)

// --- Functions ---
function handleLogout() {
  // ลบ Token และ ข้อมูล User ออกจากหน่วยความจำ
  localStorage.removeItem('authToken')
  localStorage.removeItem('userData')

  // สั่งโหลดหน้าเว็บใหม่
  window.location.href = '/' // กลับไปหน้าหลัก (ซึ่งตอนนี้จะกลายเป็นสถานะ Logout)
}

// --- Lifecycle ---
// onMounted() จะทำงาน 1 ครั้ง ตอน Component โหลดเสร็จ
onMounted(() => {
  // ตรวจสอบว่ามี Token ล็อกอินค้างอยู่หรือไม่
  const token = localStorage.getItem('authToken')
  const userJson = localStorage.getItem('userData')
  
  if (token && userJson) {
    isLoggedIn.value = true
    userData.value = JSON.parse(userJson)
    console.log('User is logged in:', userData.value)
  } else {
    isLoggedIn.value = false
    console.log('User is not logged in.')
  }
})
</script>

<template>
  <header class="app-header">
    <div class="logo">
      <RouterLink to="/">ระบบสต็อกยาง</RouterLink>
    </div>
    
    <nav class="navigation">
      </nav>

    <div class="auth-buttons">
      
      <template v-if="isLoggedIn">
        <span class="welcome-user">
          สวัสดี, {{ userData?.username }} ({{ userData?.role }})
        </span>
        <button @click="handleLogout" class="logout-button">
          ออกจากระบบ
        </button>
      </template>

      <template v-else>
        <RouterLink to="/login" class="login-button">
          เข้าสู่ระบบ
        </RouterLink>
      </template>

    </div>
  </header>

  <div class="main-content">
    <RouterView />
  </div>

</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #333;
  color: #fff;
  border-bottom: 2px solid #007bff;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
}

.navigation a {
  margin: 0 1rem;
  color: #eee;
  text-decoration: none;
  font-size: 1rem;
}
.navigation a:hover {
  color: #007bff;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-user {
  font-size: 0.9rem;
  color: #ccc;
}

/* ปุ่ม Login (ที่เป็น Link) */
.login-button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}
.login-button:hover {
  background-color: #0056b3;
}

/* ปุ่ม Logout (ที่เป็น button) */
.logout-button {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}
.logout-button:hover {
  background-color: #c82333;
}

.main-content {
  width: 100%;
  height: 100%;
  padding: 2rem;
}
</style>