<template>
  <router-view />
</template>

<script setup lang="ts">
import { watch } from "vue";
import { useTheme } from "vuetify";

const theme = useTheme();

// dynamic favicon based on theme
watch(
  () => theme.global.current.value.dark,
  (isDark) => {
    // update favicon
    const iconName = isDark ? "favicon-darkmode.png" : "favicon.png";
    const links = document.querySelectorAll("link[rel~='icon']");
    links.forEach((link: any) => {
      link.href = `/${iconName}`;
    });

    // update status bar color
    const metaThemeColor = document.querySelector("meta[name='theme-color']");
    if (metaThemeColor) {
      metaThemeColor.setAttribute("content", isDark ? "#1a1a1a" : "#ffffff");
    }
  },
  { immediate: true }
);
</script>

<style>
* {
  box-sizing: border-box;
}

html,
body {
  touch-action: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
  overscroll-behavior: none;

  margin: 0;
  padding: 0;
  font-size: 15px;

  height: 100%;
}

body {
  overflow: hidden;
}

#app {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

svg {
  height: 1.3em;
  width: 1.3em;
  display: block;
  margin: auto;
}

[contenteditable] {
  -webkit-user-select: text;
  user-select: text;
}
</style>
