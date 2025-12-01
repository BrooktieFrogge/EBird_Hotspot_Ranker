<template>
  <div class="homescreen-container">
    <!-- TOP MENU -->
    <div class="menu-grid">
     <div class="menu-item" @click="goToHotspotSearch">
        Hotspot Search
      </div>

      <div class="menu-item" @click="openDocs">
        Documentation
      </div>
    </div>
    <!-- MAIN CONTENT-->
    <div class="main-section">
      <h1 style="text-align: center; padding: 20px; font-family:serif"> Welcome! </h1>
      <p style="text-align: center; padding: 20px; font-family:serif"> </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>
        <p>Lorem ipsum dolor sit amet... </p>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()

function goToHotspotSearch() {
  router.push('/hotspot-search')
}

function openDocs() {
  console.log("Docs placeholder")
}
</script>

<style>
/* ---- App Colors ---- */
:root {
  --color-charcoal: #1A1A1A;
  --color-offwhite: #F9FAFB;
  --color-lightgray: #E5E7EB;

  --color-accent-red: #D64545;
  --color-accent-green: #57A773;
  --color-accent-teal: #3CAFAF;

  --color-border: #D1D5DB;
  --color-muted: #6B7280;

  --color-error: #B91C1C;
  --color-success: #198754;
}
</style>

<style scoped>

.homescreen-container {
  display: flex;
  gap: 24px;
  padding: 40px;
  height: 115vh;
  overflow: scroll;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, 180px);
  gap: 32px;
  padding: 25px;
  background-color: var(--color-success);
  justify-content: center;
  width: 1200px;
}

.menu-item {
  height: 50px;
  width: 180px;
  border-radius: 16px;
  padding: 24px;
  font-size: 18px;
  font-weight: 500;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  background-color: var(--color-accent-green);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.151);

  cursor: pointer;
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.menu-item:hover {
  transform: translateY(-4px);
  background-color: var(--color-muted);
}

.main-section {
  overflow: scroll;
  min-height: 900px;
  width: 1200px;
  background-color: var(--color-lightgray);
}
</style>
