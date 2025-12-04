<template>
  <div class="hotspot-search">

    <!-- LEFT PANEL -->
    <div class="filters">

      <!-- Buttons container  -->
      <div class="buttons-container">
        <div id="home-button" @click="redirectToHomeScreen">
          <div class="back-button-wrapper">
            <BIconHouseFill />
          </div>
        </div>
      </div>

      <h1 class="panel-title">Hotspot Browser</h1>

      <!-- Text search -->
      <div class="filter-group">
        <label for="search">Search by name or location</label>
        <input
          id="search"
          type="text"
          v-model="searchQuery"
          placeholder="Type a hotspot name or location..."
        />
      </div>

      <!-- Country filter -->
      <div class="filter-group">
        <label for="country">Country</label>
        <select id="country" v-model="analyticsStore.selectedCountry">
          <option value="">All countries</option>
          <option
            v-for="country in availableCountries"
            :key="country"
            :value="country"
          >
            {{ country }}
          </option>
        </select>
      </div>

      <!-- Subregion filter -->
      <div class="filter-group">
        <label for="subregion">Subregion</label>
        <select id="subregion" v-model="selectedSubregion">
          <option value="">All subregions</option>
          <option
            v-for="subregion in availableSubregions"
            :key="subregion"
            :value="subregion"
          >
            {{ subregion }}
          </option>
        </select>
      </div>

      <div class="filter-summary">
        Showing {{ filteredHotspots.length }} of {{ hotspots.length }} hotspots
      </div>
    </div>

    <!-- MIDDLE PANEL: Hotspot Cards (scrollable) -->
    <div class="results">
      <div class="cards-container">
        <HotspotCard
          v-for="hotspot in filteredHotspots"
          :key="hotspot.id"
          :id="hotspot.id"
          :name="hotspot.name"
          :country="hotspot.country"
          :subregion1="hotspot.subregion1"
          :species-count="hotspot.speciesCount"
          :is-selected="analyticsStore.selectedHotspot && analyticsStore.selectedHotspot.id === hotspot.id"
          @click="selectHotspotById"
        />
      </div>
    </div>

    <!-- RIGHT PANEL: Selected Hotspot Summary -->
    <div class="summary-panel">
      <div class="summary-header">
        <h2 v-if="analyticsStore.selectedHotspot">Selected Hotspot</h2>
        <h2 v-else>No Hotspot Selected</h2>
      </div>

      <div class="summary-body" v-if="analyticsStore.selectedHotspot">
        <div class="summary-name">
          {{ analyticsStore.selectedHotspot.name }}
        </div>

        <div class="summary-row">
          <span class="summary-label">Country:</span>
          <span class="summary-value">
            {{ analyticsStore.selectedHotspot.country }}
          </span>
        </div>

        <div class="summary-row">
          <span class="summary-label">Location:</span>
          <span class="summary-value">
            {{ analyticsStore.selectedHotspot.subregion1 }}
          </span>
        </div>

        <div class="summary-row">
          <span class="summary-label">Saved:</span>
          <span class="summary-value">
            {{ analyticsStore.selectedHotspot.isSaved ? 'Yes' : 'No' }}
          </span>
        </div>
      </div>

      <div class="summary-body" v-else>
        <p>Select a hotspot card to see details here.</p>
      </div>

      <div class="summary-footer">
        <button
          class="detail-button"
          @click="goToSelectedHotspotDetail"
          :disabled="!analyticsStore.selectedHotspot"
        >
          Go to hotspot detail
        </button>
      </div>
    </div>

  </div>
</template>



<script lang="ts">
import { defineComponent, onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import HotspotCard from "../components/HotspotCard.vue";
import { BIconHouseFill } from 'bootstrap-icons-vue';
import { useAnalyticsStore } from "../stores/useAnalyticsStore.ts"
import type { HotspotOverview } from '../types/index.ts';

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
    BIconHouseFill,
  },

  setup() {
    const router = useRouter();

    const searchQuery = ref('');

    const analyticsStore = useAnalyticsStore();

    analyticsStore.fetchAllHotspots();
    
    const hotspots = computed(() => analyticsStore.allHotspots);

    const selectedSubregion = ref('');  // local state for subregion filter


    const availableCountries = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach(h => set.add(h.country));
      return Array.from(set).sort();
    });

     const filteredHotspots = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  const country = analyticsStore.selectedCountry;

  return hotspots.value.filter(h => {
    const matchesSearch =
      !q ||
      h.name.toLowerCase().includes(q) ||
      h.subregion1.toLowerCase().includes(q);

    const matchesCountry =
      !country || h.country === country;

    return matchesSearch && matchesCountry;
  });
});


    const availableSubregions = computed(() => {
  const set = new Set<string>();

  hotspots.value.forEach(h => {
    // only include subregions for the currently selected country
    if (!analyticsStore.selectedCountry || h.country === analyticsStore.selectedCountry) {
      set.add(h.subregion1);
    }
  });

  return Array.from(set).sort();
});

    const selectHotspotById = (id: HotspotOverview['id']) => {
  analyticsStore.setHotspot(id);
};

  
    const goToSelectedHotspotDetail = () => {
      if (!analyticsStore.selectedHotspot) return;
      router.push({ name: 'HotspotDetail', params: { id: analyticsStore.selectedHotspot.id } });
    };

    const redirectToHomeScreen = () => {
      router.push({ name: 'HomeScreen' });
    };

    return {
      hotspots,
      analyticsStore,
      searchQuery,
      availableCountries,
      filteredHotspots,
      availableSubregions,
      selectHotspotById,
      goToSelectedHotspotDetail,
      redirectToHomeScreen,
    };
  },
});
</script>


<style scoped>
.hotspot-search {
  display: flex;
  height: 100vh;
  background: #fafafa;
  color: #222;
  font-family: Arial, sans-serif;
  overflow: hidden; 
}

/* LEFT PANEL */
.filters {
  width: 280px;
  padding: 16px;
  border-right: 1px solid #ddd;
  box-sizing: border-box;
  background: #fafafa;
  overflow-y: auto; 
}

/* Buttons container  */
.buttons-container {
  display: flex;
  justify-content: center; 
  align-items: center;
  width: 100%;
  height: 60px;
  border-top: 1px solid #ffffffc9;
  border-bottom: 1px solid #ffffffc9;
  padding-top: 20px;
  padding-inline: 40px;
  padding-bottom: 20px;
}

.back-button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: fit-content;
  border: 1px solid #000000;
  padding: 15px;
  border-radius: 10px;
  background-color: #ffffff;
  color: #000000;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button-wrapper:hover {
  background-color: #d2d2d2;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 20px;
  margin-bottom: 20px;
}

.filter-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #333;
}

.filter-group input,
.filter-group select {
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #bfbfbf;
  background-color: #ffffff;
  color: #000000;
}

.filter-summary {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #555;
}

/* MIDDLE PANEL: cards */
.results {
  flex: 1.5;
  padding: 20px;
  box-sizing: border-box;
  background: white;
  overflow-y: auto;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-content: flex-start;
}

/* RIGHT PANEL: summary */
.summary-panel {
  width: 320px;
  border-left: 1px solid #ddd;
  box-sizing: border-box;
  padding: 16px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.summary-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.summary-body {
  font-size: 0.95rem;
  color: #333;
  margin: 0 0 0px 0;
}

.summary-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.summary-row {
  display: flex;
  margin-bottom: 6px;
}

.summary-label {
  width: 110px;
  font-weight: 500;
  color: #666;
}

.summary-value {
  flex: 1;
}

.summary-footer {
  margin-top: auto; 
  padding-top: 12px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.detail-button {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #000;
  background: #fff;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
}

.detail-button:disabled {
  border-color: #ccc;
  color: #999;
  cursor: not-allowed;
  background: #f5f5f5;
}

.detail-button:not(:disabled):hover {
  background: #000;
  color: #fff;
}
</style>