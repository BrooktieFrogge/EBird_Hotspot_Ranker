<template>
  <router-view />
</template>

<script setup lang="ts">
import { watch } from "vue";
import { useRoute } from "vue-router";
import { useTheme } from "vuetify";

const theme = useTheme();
const route = useRoute();

// enforce correct theme color
const updateThemeColor = () => {
  const isDark = theme.global.current.value.dark;
  const color = isDark ? "#1e1e1e" : "#ffffff";

  const metaTags = document.querySelectorAll("meta[name='theme-color']");
  if (metaTags.length > 0) {
    metaTags.forEach((meta) => {
      meta.setAttribute("content", color);
    });
  } else {
    const meta = document.createElement("meta");
    meta.name = "theme-color";
    meta.content = color;
    document.head.appendChild(meta);
  }
};

// watch theme changes
watch(
  () => theme.global.current.value.dark,
  (isDark) => {
    // update favicon
    const iconName = isDark ? "favicon-darkmode.png" : "favicon.png";
    const links = document.querySelectorAll("link[rel~='icon']");
    links.forEach((link: any) => {
      link.href = `/${iconName}`;
    });

    updateThemeColor();
  },
  { immediate: true }
);

// watch route changes to re-enforce theme color (nuclear option)
watch(
  () => route.path,
  () => {
    // small delay to override any component-level changes
    setTimeout(updateThemeColor, 50);
  }
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

@media all and (display-mode: standalone) {
  #app {
    background-color: var(--color-bg-panel);
  }

  body.theme--dark #app {
    background-color: var(--color-bg-panel);
  }
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
