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
  <div class="app-container">
    <header class="app-header">
      <div class="logo">
        <RouterLink to="/">ระบบสต็อกยาง</RouterLink>
      </div>

      <nav class="navigation"></nav>

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

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* --------------------- GLOBAL --------------------- */
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  overflow-x: hidden; /* ป้องกันขอบขาวทางขวา */
}

* {
  box-sizing: border-box; /* ป้องกัน element ด้านในล้นขนาด */
}
</style>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* เต็มจอแนวตั้ง */
  width: 100%;   /* เต็มจอแนวนอน */
}

/* Header ด้านบน */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #333;
  color: #fff;
  border-bottom: 2px solid #007bff;
  flex-shrink: 0;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
}

/* ส่วนเนื้อหา (RouterView) */
.main-content {
  flex: 1;
  width: 100%;
  max-width: 100vw; /* ป้องกันล้นขอบแนวนอน */
  height: 100%;
  padding: 2rem;
  background-color: #ffffff;
  overflow-y: auto;
}
</style>
