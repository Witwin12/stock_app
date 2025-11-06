<script setup>
// (ในอนาคต เราอาจจะ import Navbar มาไว้ที่นี่)
// import NavBar from './components/NavBar.vue'
</script>

<template>
  <main>
    <router-view />
  </main>
  
  </template>

<style scoped>
/* Style ในนี้คือ Style ที่ใช้ "ร่วมกันทุกหน้า" 
*/
main {
  width: 100%;
  height: 100%;
  padding: 2rem;
}
</style>