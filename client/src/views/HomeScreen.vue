<template>
  <div class="homescreen-container">
    <div class="page-shell">
      <!-- PAGE TITLE BAR -->
      <header class="title-bar">
        <div class="title-content">
          <img class="header-logo" :src="logo" alt="FeatherWeight Logo" />
        </div>
      </header>

      <!-- TOP NAV / MENU -->
      <nav class="top-nav">
        <div class="nav-left">
          <button class="nav-item nav-item-active">Home</button>
          <button class="nav-item" @click="goToHotspotSearch">
            Hotspot Search
          </button>
        </div>

        <div class="nav-right">
          <button class="nav-item" @click="openDocs">Documentation</button>
        </div>
      </nav>

      <!-- MAIN CONTENT -->
      <main class="main-layout">
        <section class="content">
          <h2 class="section-heading">Welcome!</h2>

          <p class="lead">
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>
          <!-- RIGHT-SIDE IMAGE -->
          <aside class="image-panel">
            <figure>
              <img
                :src="birdImage"
                alt="Bird illustration"
                class="square-image"
              />
              <figcaption>© Luis Alberto Salagaje Muela</figcaption>
            </figure>
          </aside>

          <p class="lead">
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>
          <p class="lead">
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <p class="standout">
            Q: At the Copalinga Lodge (Ecuador), what is the likelihood of
            seeing the rare, reclusive Gray Tinamou?! Is it a “sure-bet”, or
            not, to see the stunning Green-and-gold Tanager?
          </p>

          <!-- LEFT-SIDE IMAGE -->
          <aside class="left-image-panel">
            <figure>
              <img
                :src="birdImage2"
                alt="Bird illustration"
                class="square-image"
              />
              <figcaption>© Brandon Nidiffer</figcaption>
            </figure>
          </aside>

          <p>
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <p class="lead">
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <p class="lead">
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <p>
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <h3 class="section-subheading">Notes from steve:</h3>
          <p>
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>
          <p>
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>
          <p>
            This is where steve will write something! This is where steve will
            write something This is where steve will write something! This is
            where steve will write something This is where steve will write
            something! This is where steve will write something here! This is
            where steve will write something! This is where steve will write
            something! This is where steve will write something
          </p>

          <p class="footer-note">
            All of this text is just placeholder content. We will soon replace
            this with real text lol
          </p>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import birdImage from "../assets/bird.jpg";
import birdImage2 from "../assets/bird2.jpg";
import logo from "../assets/logo.jpg";

const router = useRouter();

function goToHotspotSearch() {
  router.push("/hotspot-search");
}

function openDocs() {
  console.log("Docs placeholder");
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
  background: white;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
}

/* White central panel */
.page-shell {
  width: 100vh);
  height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scrollbar-width: none;
}

.page-shell::-webkit-scrollbar {
  display: none;
}

/* Title bar */
.title-bar {
  background-color: white;
  padding: 25px 40px 29x;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
}

.title-bar h1 {
  margin: 0;
  font-family: "Monospace", monaco;
  font-size: 32px;
  letter-spacing: 0.03em;
}

.title-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.header-logo {
  margin: 20px 0 0 0;
  width: auto;
  height: 125px;
  border-radius: 5px;
}

/* Top blue strip */
.top-nav {
  position: sticky;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 10px 40px;
  box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.35);
}

.nav-left,
.nav-right {
  display: flex;
  gap: 12px;
}

.nav-item {
  border: none;
  background: transparent;
  color: black;
  padding: 12px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  font-weight: lighter;
  font-size: 16px;
  font-family: "Sans-serif", verdana;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-item:hover {
  background: #e5e7eb;
}

.nav-item-active {
  background: #e5e7eb;
  border-bottom: 3px solid #f3f4f6;
  border-radius: 0;
}

.main-layout {
  display: grid;
  //grid-template-columns: 2fr 1fr;
  gap: 32px;
  padding: 32px 40px 40px;
}

.content {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
  color: black;
}

.section-heading {
  font-family: "Sans-serif", verdana;
  font-weight: lighter;
  font-size: 28px;
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
  color: #f9fafb;
}

.feature-list {
  padding-left: 20px;
  margin: 0 0 16px;
  line-height: 1.6;
  align-items: center;
  flex-direction: column;
  color: #f9fafb;
}

.footer-note {
  font-size: 14px;
  color: #f9fafb;
  margin-top: 16px;
}

/* Right-side image panel */
.image-panel {
  display: flex;
  justify-content: right;
  align-items: flex-start;
  float: right;
  margin: 0 10px 20px 40px;
}

/* Left-side image panel */
.left-image-panel {
  float: left;
  margin: 0 60px 20px 10px;
  display: flex;
  justify-content: left;
  align-items: flex-start;
}

.standout {
  font-family: "Sans-serif", verdana;
  font-weight: bold;
  font-size: 16px;
  margin: 0 0 16px;
  color: #b31b1b;
}

/* Square bird image */
.square-image {
  margin-top: 20px;
  width: 350px;
  height: 350px;
  object-fit: cover;
  object-position: 80% 50%;
  box-shadow: 0px 5px 40px rgba(0, 0, 0, 0.35);
}

.split-h {
  background-color: #1a1a1a;
  z-index: 1;
  width: 100%;
  margin: 0;
  padding: 0;
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
