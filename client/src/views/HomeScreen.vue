<template>
  <div class="homescreen-container">
    <div class="page-shell">
      <!-- PAGE TITLE BAR -->
      <header class="title-bar">
        <h1>ebird Hotspot Overview</h1>
      </header>

      <!-- TOP NAV / MENU -->
      <nav class="top-nav">
        <div class="nav-left">
          <button class="nav-item nav-item-active">
            Home
          </button>
          <button class="nav-item" @click="goToHotspotSearch">
            Hotspot Search
          </button>
        </div>

        <div class="nav-right">
          <button class="nav-item" @click="openDocs">
            Documentation
          </button>
        </div>
      </nav>

      <!-- MAIN CONTENT -->
      <main class="main-layout">
        <section class="content">
          <h2 class="section-heading">Welcome!</h2>

          <p class="lead">
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something here! 
            This is where steve will write something! This is where steve will write something!
            This is where steve will write something
          </p>

          <p>
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something here! 
            This is where steve will write something! This is where steve will write something!
            This is where steve will write something
          </p>

          <p>
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something
            This is where steve will write something! This is where steve will write something here! 
            This is where steve will write something! This is where steve will write something!
            This is where steve will write something
          </p>

          <h3 class="section-subheading">
            Notes from steve:
          </h3>
          <ol class="feature-list">
            <li>
              This is where steve will write something! This is where steve will write something
            </li>
            <li>
              This is where steve will write something! This is where steve will write something
            </li>
            <li>
              This is where steve will write something! This is where steve will write something
            </li>
            <li>
              This is where steve will write something! This is where steve will write something
            </li>
            <li>
             This is where steve will write something! This is where steve will write something
            </li>
          </ol>

          <p class="footer-note">
            All of this text is just placeholder content. We will soon replace this with real text lol
          </p>
        </section>

        <!-- RIGHT-SIDE IMAGE -->
        <aside class="image-panel">
          <img
            :src="birdImage"
            alt="Bird illustration"
            class="circle-image"
          />
        </aside>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import birdImage from '../assets/bird.jpeg'  

const router = useRouter()

function goToHotspotSearch() {
  router.push('/hotspot-search')
}

function openDocs() {
  console.log('Docs placeholder')
}
</script>


<style>
/* ---- App Colors ---- */
:root {
  --color-charcoal: #1a1a1a;
  --color-offwhite: #f9fafb;
  --color-lightgray: #e5e7eb;

  --color-accent-red: #d64545;
  --color-accent-green: #57a773;
  --color-accent-teal: #3cafaf;

  --color-border: #d1d5db;
  --color-muted: #6b7280;
}
</style>

<style scoped>
/* Outer blue margins similar to the ECM page */
.homescreen-container {
  min-height: 100vh;
  background: #457999; 
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
}

/* White central panel */
.page-shell {
  width: min(1500px, 100% - 48px);
  min-height: 90vh;
  background: white;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
}

/* Title bar */
.title-bar {
  padding: 32px 40px 24px;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
}

.title-bar h1 {
  margin: 0;
  font-family: 'Georgia', serif;
  font-size: 32px;
  letter-spacing: 0.03em;
}

/* Top blue strip */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #296239;
  padding: 0 40px;
}

.nav-left,
.nav-right {
  display: flex;
  gap: 12px;
}

.nav-item {
  border: none;
  background: transparent;
  color: #e5e7eb;
  padding: 12px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-item:hover {
  background: #374151;
}

.nav-item-active {
  background: #296239;
  border-bottom: 3px solid #f3f4f6;
  border-radius: 0;
}

.main-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  padding: 32px 40px 40px;
}

.content {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: black;
}

.section-heading {
  font-family: 'Georgia', serif;
  font-size: 26px;
  margin: 0 0 16px;
}

.lead {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.section-subheading {
  font-size: 18px;
  margin-top: 24px;
  margin-bottom: 12px;
}

.feature-list {
  padding-left: 20px;
  margin: 0 0 16px;
  line-height: 1.6;
}

.footer-note {
  font-size: 14px;
  color: var(--color-muted);
  margin-top: 16px;
}

/* Right-side image panel */
.image-panel {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* Circular bird image */
.circle-image {
  margin-top: 20px;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  object-fit: cover;
 object-position: 80% 50%;

  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  border: 3px solid #296239;
}

/* Responsive tweaks */
@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
  }

  .image-panel {
    justify-content: center;
  }
}
</style>
