<template>
  <!-- top navigation bar -->
  <nav class="top-nav">
    <!-- left group: logo -->
    <div class="nav-left-group">
      <!-- logo -->
      <div class="logo-wrapper">
        <router-link to="/" class="logo-link">
          <img
            class="header-logo"
            :src="currentLogo"
            alt="FeatherWeight Logo"
          />
        </router-link>
      </div>
    </div>

    <!-- center group: links (desktop only) -->
    <div class="nav-center-group desktop-only">
      <button class="nav-item" @click="handleNav('home')">Home</button>
      <button class="nav-item" @click="handleNav('about')">About</button>
      <button class="nav-item" @click="handleNav('how-to')">Tutorial</button>
      <button class="nav-item" @click="handleNav('learn')">
        Documentation
      </button>
    </div>

    <!-- right group: back + search + theme toggle (desktop only) -->
    <div class="nav-right-group desktop-only">
      <!-- back button (desktop only) -->
      <div v-if="showBack" class="back-btn-wrapper">
        <button
          class="nav-back-icon-btn"
          @click="handleBack"
          aria-label="Go Back"
          title="Go Back"
        >
          <i class="bi bi-arrow-left"></i>
        </button>
      </div>

      <button
        v-if="!showBack"
        class="nav-search"
        @click="goToHotspotSearch"
        aria-label="Search Hotspots"
      >
        <span>Search Hotspots</span>
      </button>

      <div class="desktop-theme-toggle">
        <ThemeToggle />
      </div>
    </div>
  </nav>

  <!-- mobile drawer -->
  <div class="mobile-drawer" :class="{ open: navStore.mobileNavOpen }">
    <button class="nav-item mobile-item" @click="handleNav('home')">
      Home
    </button>
    <button class="nav-item mobile-item" @click="handleNav('about')">
      About
    </button>
    <button class="nav-item mobile-item" @click="handleNav('how-to')">
      Tutorial
    </button>

    <!-- documentation + theme toggle row -->
    <div class="mobile-item doc-row">
      <button class="nav-item mobile-link-btn" @click="handleNav('learn')">
        Documentation
      </button>
      <div class="mobile-toggle-wrapper">
        <ThemeToggle />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useTheme } from "vuetify";
import { useNavigationStore } from "../stores/useNavigationStore";
import ThemeToggle from "./ThemeToggle.vue";
import logoLight from "../assets/logo.png";
import logoDark from "../assets/logo-darkmode.png";

const router = useRouter();
const route = useRoute();
const navStore = useNavigationStore();
const theme = useTheme();

const isSearchPage = computed(() => route.path === "/hotspot-search");
const isDetailPage = computed(() => route.path.includes("/hotspot/"));
const showBack = computed(() => isSearchPage.value || isDetailPage.value);

// theme logic
const isDark = computed(() => theme.global.current.value?.dark);
const currentLogo = computed(() => (isDark.value ? logoDark : logoLight));

// auto-close drawer on mount
onMounted(() => {
  if (navStore.mobileNavOpen) {
    // delay for render
    setTimeout(() => {
      navStore.closeMobileNav();
    }, 300);
  }
});

function goToHotspotSearch() {
  router.push("/hotspot-search");
  // keep dock lifted
}

function handleBack() {
  if (isDetailPage.value) {
    router.push("/hotspot-search");
  } else {
    router.push("/");
  }
}

function handleNav(sectionId: string) {
  navStore.closeMobileNav();
  if (route.path !== "/") {
    router.push("/").then(() => {
      if (sectionId === "home") {
        forceScrollTop();
      } else {
        // wait for mount
        setTimeout(() => scrollToSection(sectionId), 100);
      }
    });
  } else {
    if (sectionId === "home") {
      forceScrollTop();
    } else {
      scrollToSection(sectionId);
    }
  }
}

function forceScrollTop() {
  // try window first
  window.scrollTo({ top: 0, behavior: "smooth" });

  // try known scroll containers
  const containers = [
    ".page-shell", // HomeScreen
    ".hotspot-detail", // Generic wrapper
    ".content", // Generic content
    ".page-layout", // Search screen
  ];

  containers.forEach((selector) => {
    const el = document.querySelector(selector);
    if (el) {
      el.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
}

function scrollToSection(id: string) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  }
}
</script>

<style scoped>
/* top nav container */
.top-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--color-bg-panel);
  display: flex;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid var(--color-border-light);
  width: 100%;
  height: 68px; /* fixed height */
  box-sizing: border-box;
}

/* left group */
.nav-left-group {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 10;
}

/* logo */
.logo-wrapper {
  display: block;
  flex-shrink: 0;
}
.header-logo {
  height: 48px;
  width: auto;
  object-fit: contain;
  display: block;
}

/* back button (icon only) */
.nav-back-icon-btn {
  background: transparent;
  border: 1px solid var(--color-border-light);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  color: var(--color-text-primary);
  transition: all 0.2s ease;
}
.nav-back-icon-btn:hover {
  background: rgba(125, 125, 125, 0.15);
  transform: scale(1.05);
}

/* center group (absolute centering) */
.nav-center-group {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 30px;
  align-items: center;
  justify-content: center;
}

/* right group */
.nav-right-group {
  margin-left: auto; /* push to right */
  display: flex;
  align-items: center;
  gap: 15px;
  flex-shrink: 0;
  z-index: 10;
}

/* desktop (regular) */
@media (min-width: 769px) {
  .mobile-drawer {
    display: none;
  }
}

/* compact desktop (769px - 1100px) */
@media (min-width: 769px) and (max-width: 1100px) {
  .top-nav {
    padding: 10px 15px;
  }
  .header-logo {
    height: 36px;
  }
  .nav-center-group {
    gap: 15px;
  }
  .nav-item {
    font-size: 15px !important;
    padding: 5px !important;
  }
  .nav-search {
    font-size: 14px !important;
    padding: 6px 12px !important;
    height: 36px !important;
  }
  .desktop-theme-toggle {
    transform: scale(0.85);
  }
}

/* nav link items */
.nav-item {
  border: none;
  background: transparent;
  color: var(--color-text-primary);
  padding: 7px;
  font-size: 20px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s ease, color 0.15s ease;
}
.nav-item:hover {
  text-decoration: underline;
  text-decoration-color: var(--color-danger);
  text-decoration-thickness: 3px;
  text-underline-offset: 0.4em;
}

/* search button */
.nav-search {
  width: auto;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  background: var(--color-danger);
  border: black;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 16px;
  font-weight: 500;
  font-size: 18px;
  line-height: 1.2;
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.35);
  transition: background 0.15s ease, color 0.15s ease;
  white-space: nowrap;
}
.nav-search:hover {
  filter: brightness(0.9);
}

/* mobile styles */
@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }

  .top-nav {
    /* mobile absolute centering */
    display: flex;
    align-items: center;
    position: relative;
    height: 54px !important; /* compact fixed height */
    padding: 0 10px;
  }

  .logo-wrapper {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: auto;
  }

  .header-logo {
    height: 32px; /* small logo */
  }

  /* hidden on mobile */

  /* mobile drawer (fixed overlay) */
  .mobile-drawer {
    display: flex;
    flex-direction: column;
    position: fixed;
    bottom: 0; /* anchor to bottom */
    height: var(--drawer-lift-height); /* match lift height */
    left: 0;
    right: 0;
    background: var(--color-bg-panel);
    padding: 16px;
    box-shadow: none;
    border-top: none; /* remove border */
    border-radius: 0; /* square corners */
    align-items: flex-start;
    justify-content: flex-end; /* push items to bottom */
    z-index: 90; /* behind dock */

    /* animation props */
    transform: translateY(100%); /* start hidden */
    visibility: hidden;
    transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1), visibility 0.5s;
  }

  .mobile-drawer.open {
    transform: translateY(0); /* slide up */
    visibility: visible;
  }

  .mobile-item {
    font-size: 18px;
    padding: 12px 0;
    width: 100%;
    text-align: left;
    border-bottom: 1px solid var(--color-border-light);
  }
  .doc-row {
    border-bottom: none; /* only doc row has no border */
  }

  /* combined row styles */
  .doc-row {
    display: flex;
    align-items: center;
    justify-content: space-between; /* space out */
    padding-right: 2px;
  }

  .mobile-link-btn {
    background: transparent;
    border: none;
    color: var(--color-text-primary);
    font-size: 18px;
    text-align: left;
    padding: 0;
    margin: 0;
    cursor: pointer;
    flex: 1; /* take leftover space */
  }

  .mobile-toggle-wrapper {
    margin-right: 2px; /* alignment */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* override ThemeToggle styles */
  .mobile-toggle-wrapper :deep(.theme-toggle) {
    width: 44px;
    height: 44px;
    border-radius: 12px; /* match dock shape */
  }
}
</style>
