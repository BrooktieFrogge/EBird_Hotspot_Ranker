<template>
  <button
    class="theme-toggle"
    @click="toggleTheme"
    :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    aria-label="Toggle Dark Mode"
  >
    <!-- sun icon (dark -> light) -->
    <svg
      v-if="isDark"
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="feather feather-sun"
    >
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>

    <!-- moon icon (light -> dark) -->
    <svg
      v-else
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="feather feather-moon"
    >
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
  </button>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from "vue";
import { useTheme } from "vuetify";

export default defineComponent({
  name: "ThemeToggle",
  setup() {
    const theme = useTheme();

    const isDark = computed(() => theme.global.name.value === "dark");

    // update Safari/iOS status bar theme color
    const updateThemeColor = (isDarkMode: boolean) => {
      const color = isDarkMode ? "#1e1e1e" : "#ffffff";

      document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
        meta.setAttribute("content", color);
      });
    };

    const toggleTheme = () => {
      const newTheme = isDark.value ? "light" : "dark";

      if ((theme as any).change) {
        (theme as any).change(newTheme);
      } else {
        theme.global.name.value = newTheme;
      }

      if (newTheme === "dark") {
        document.body.classList.add("theme--dark");
        localStorage.setItem("user-theme", "dark");
      } else {
        document.body.classList.remove("theme--dark");
        localStorage.setItem("user-theme", "light");
      }

      updateThemeColor(newTheme === "dark");
    };

    // init from local storage
    onMounted(() => {
      const savedTheme = localStorage.getItem("user-theme");
      const isDarkMode =
        savedTheme === "dark" ||
        (!savedTheme &&
          window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);

      if (isDarkMode) {
        document.body.classList.add("theme--dark");
      }

      // set initial Safari status bar color
      updateThemeColor(isDarkMode);
    });

    return {
      isDark,
      toggleTheme,
    };
  },
});
</script>

<style scoped>
.theme-toggle {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: inherit;
  transition: all 0.2s ease;
  padding: 0;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
}

/* adjust for dark mode */
:global(body.theme--dark) .theme-toggle {
  background: rgba(255, 255, 255, 0.1);
  color: #fb8c00; /* orange for sun */
}

:global(body.theme--dark) .theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffa726;
}

/* specific overrides handled by parent */
</style>
