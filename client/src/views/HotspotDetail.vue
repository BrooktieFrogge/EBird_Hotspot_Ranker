<template>
  <div :class="['hotspot-detail']">
    <div class="content">

      <!-- Config Panel -->
      <div class="config-panel">
        <AnalyticsConfigPanel />
      </div>

      <!-- Hotspot Analytics Report -->
      <div class="analytics-report">
        <HotspotAnalyticsReport />
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import HotspotAnalyticsReport from '../components/HotspotAnalyticsReport.vue';
import AnalyticsConfigPanel from '../components/AnalyticsConfigPanel.vue';

export default defineComponent({
  name: 'HotspotDetail',

  components: {
    AnalyticsConfigPanel,
    HotspotAnalyticsReport
  },

  setup() {
    const store = useAnalyticsStore();
    const route = useRoute();

    // trigger fetch on load instead of search page
    onMounted(() => {
      const id = route.params.id as string;

      if (id) {
          store.selectedHotspotId = id
          store.fetchHotspotDetail();
      }
    });

    return { store };
  }

});
</script>

<style scoped>
.hotspot-detail {
  padding: none;
  text-align: center;
}

.content {
  display: flex;
  flex: 1;
}

.config-panel {
  flex: 1;
  max-width: 30%;
  background-color: #181818;
  padding: none;
  box-sizing: border-box;
}

.analytics-report {
  flex: 2;
  min-width: 40%;
  background: #181818;
  padding: none;
  box-sizing: border-box;
}

</style>
