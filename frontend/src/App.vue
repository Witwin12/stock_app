<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { isLoggedIn, userData, logout } = useAuth()
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
          <button @click="logout" class="logout-button">
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
  overflow-x: hidden; /* ป้องกัน scroll แนวนอน */
}

* {
  box-sizing: border-box;
}
</style>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: hidden;
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
}

/* เนื้อหาหลัก */
.main-content {
  flex: 1;
  width: 100%;
  height: calc(100vh - 70px); /* ปรับตามความสูง header */
  padding: 2rem;
  background-color: #ffffff;
  overflow-y: auto;
}
</style>
