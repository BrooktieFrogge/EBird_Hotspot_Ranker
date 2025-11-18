<template>
  <router-view/>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>
  
<style>
* {
  box-sizing: border-box;
}
  
html, body {
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
  