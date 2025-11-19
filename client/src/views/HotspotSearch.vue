<template>
  <div class="hotspot-search">
    <h1>Hotspot Search</h1>
    <p>This is the placeholder for the hotspot search screen.</p>
    <button class="button" @click="navigateToHotspotDetail">
      <span>Go to hotspot detail screen</span>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HotspotSearch',
  setup() {
    const router = useRouter();

    const navigateToHotspotDetail = () => {
      // Example: navigate to hotspot with ID 1
      router.push({ name: 'HotspotDetail', params: { id: 1 } });
    };

    return { navigateToHotspotDetail };
  },
});
</script>

<style scoped>
.hotspot-search {
  padding: 2rem;
  text-align: center;
}
</style>
