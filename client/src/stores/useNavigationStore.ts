import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useNavigationStore = defineStore('navigation', () => {
  const mobileNavOpen = ref(false);

  function toggleMobileNav() {
    mobileNavOpen.value = !mobileNavOpen.value;
  }

  function closeMobileNav() {
    mobileNavOpen.value = false;
  }

  return {
    mobileNavOpen,
    toggleMobileNav,
    closeMobileNav
  };
});
