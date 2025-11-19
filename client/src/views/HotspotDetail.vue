<template>
  <div class="hotspot-detail">
    <h1>Hotspot Detail</h1>
    <p>This is the placeholder for the hotspot detail screen.</p>
    <button class="button" @click="navigateToHotspotSearch">
      <span>Go to hotspot search screen</span>
    </button>
    <!-- Future: graphs, images, lists of birds, etc -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HotspotDetail',
  setup() {
    const router = useRouter();

    const navigateToHotspotSearch = () => {
      // Example: navigate to hotspot with ID 1
      router.push({ name: 'HotspotSearch', params: { id: 1 } });
    };

    return { navigateToHotspotSearch };
  },
});
</script>

<style scoped>
.hotspot-detail {
  padding: 2rem;
  text-align: center;
}
</style>
