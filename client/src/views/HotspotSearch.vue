<template>
  <div class="hotspot-search">

    <!-- LEFT PANEL -->
    <div class="filters">

      <!-- Buttons container -->
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

      <!-- Country Autocomplete -->
      <div class="filter-group autocomplete">
        <label>Country</label>

        <input
          type="text"
          v-model="countrySearch"
          placeholder="Search countries..."
          @input="showCountryDropdown = true"
        />

        <!-- Autocomplete dropdown -->
        <div
          v-if="showCountryDropdown && filteredCountries.length > 0"
          class="dropdown"
        >
          <div
            class="dropdown-item"
            v-for="country in filteredCountries"
            :key="country"
            @click="selectCountry(country)"
          >
            {{ country }}
          </div>
        </div>
      </div>

      <!-- Subregion Autocomplete -->
      <div class="filter-group autocomplete">
        <label>Subregion</label>

        <input
          type="text"
          v-model="subregionSearch"
          placeholder="Search subregions..."
          @input="showSubregionDropdown = true"
        />

        <!-- Autocomplete dropdown -->
        <div
          v-if="showSubregionDropdown && filteredSubregions.length > 0"
          class="dropdown"
        >
          <div
            class="dropdown-item"
            v-for="subregion in filteredSubregions"
            :key="subregion"
            @click="selectSubregion(subregion)"
          >
            {{ subregion }}
          </div>
        </div>
      </div>

      <div class="filter-summary">
        Showing {{ filteredHotspots.length }} of {{ hotspots.length }} hotspots
      </div>

    </div>
    <!-- END LEFT PANEL -->


    <!-- MIDDLE PANEL: Hotspot Cards -->
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
          :is-selected="
            analyticsStore.selectedHotspot &&
            analyticsStore.selectedHotspot.id === hotspot.id
          "
          @click="selectHotspotById"
        />
      </div>
    </div>


    <!-- RIGHT PANEL -->
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
            {{ analyticsStore.selectedHotspot.isSaved ? "Yes" : "No" }}
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
import {
  defineComponent,
  ref,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
} from 'vue';
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
    const analyticsStore = useAnalyticsStore();

    // Fetch hotspot list
    analyticsStore.fetchAllHotspots();
    const hotspots = computed(() => analyticsStore.allHotspots);

    // Filters
    const searchQuery = ref('');
    const countrySearch = ref('');
    const subregionSearch = ref('');
    const selectedSubregion = ref('');

    // Dropdown visibility
    const showCountryDropdown = ref(false);
    const showSubregionDropdown = ref(false);

    // -------------------------
    // AVAILABLE FILTER VALUES
    // -------------------------
    const availableCountries = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach(h => set.add(h.country));
      return Array.from(set).sort();
    });

    const availableSubregions = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach(h => {
        if (!analyticsStore.selectedCountry || h.country === analyticsStore.selectedCountry) {
          set.add(h.subregion1);
        }
      });
      return Array.from(set).sort();
    });

    // -------------------------
    // AUTOCOMPLETE FILTERING
    // -------------------------
    const filteredCountries = computed(() => {
      if (!countrySearch.value.trim()) return availableCountries.value;
      return availableCountries.value.filter(c =>
        c.toLowerCase().includes(countrySearch.value.toLowerCase())
      );
    });

    const filteredSubregions = computed(() => {
      if (!subregionSearch.value.trim()) return availableSubregions.value;
      return availableSubregions.value.filter(sr =>
        sr.toLowerCase().includes(subregionSearch.value.toLowerCase())
      );
    });

    // -------------------------
    // SELECTING FILTER VALUES
    // -------------------------
    const selectCountry = (country: string) => {
      analyticsStore.selectedCountry = country;
      countrySearch.value = country;
      showCountryDropdown.value = false;

      // Reset subregion when country changes
      selectedSubregion.value = '';
      subregionSearch.value = '';
    };

    const selectSubregion = (subregion: string) => {
      selectedSubregion.value = subregion;
      subregionSearch.value = subregion;
      showSubregionDropdown.value = false;
    };

    // -------------------------
    // WATCHERS: CLEAR FILTERS WHEN INPUT CLEARED
    // -------------------------
    watch(countrySearch, (val) => {
      if (!val.trim()) {
        analyticsStore.selectedCountry = null;
      }
    });

    watch(subregionSearch, (val) => {
      if (!val.trim()) {
        selectedSubregion.value = '';
      }
    });

    // -------------------------
    // FILTER HOTSPOTS
    // -------------------------
    const filteredHotspots = computed(() => {
      const q = searchQuery.value.trim().toLowerCase();
      const country = analyticsStore.selectedCountry;
      const subregion = selectedSubregion.value;

      return hotspots.value.filter(h => {
        const matchesSearch =
          !q ||
          h.name.toLowerCase().includes(q) ||
          h.subregion1.toLowerCase().includes(q);

        const matchesCountry =
          !country || h.country === country;

        const matchesSubregion =
          !subregion || h.subregion1 === subregion;

        return matchesSearch && matchesCountry && matchesSubregion;
      });
    });

    // -------------------------
    // DROPDOWN HIDING BEHAVIOR
    // -------------------------
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      // if click is not inside an element with .autocomplete, close both dropdowns
      if (!target.closest('.autocomplete')) {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
      document.addEventListener('keydown', handleEscape);
    });

    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    });

    // -------------------------
    // HOTSPOT SELECTION
    // -------------------------
    const selectHotspotById = (id: HotspotOverview['id']) => {
      analyticsStore.setHotspot(id);
    };

    const goToSelectedHotspotDetail = () => {
      if (!analyticsStore.selectedHotspot) return;
      router.push({
        name: "HotspotDetail",
        params: { id: analyticsStore.selectedHotspot.id },
      });
    };

    const redirectToHomeScreen = () => {
      router.push({ name: "HomeScreen" });
    };

    // -------------------------
    // RETURN TO TEMPLATE
    // -------------------------
    return {
      // Data
      hotspots,
      analyticsStore,
      searchQuery,

      // Autocomplete input + dropdown state
      countrySearch,
      subregionSearch,
      showCountryDropdown,
      showSubregionDropdown,

      // Filters & options
      availableCountries,
      availableSubregions,
      filteredCountries,
      filteredSubregions,
      selectedSubregion,
      selectCountry,
      selectSubregion,

      // Hotspot display
      filteredHotspots,
      selectHotspotById,

      // Navigation
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

.autocomplete {
  position: relative;
}

.active-filters {
  margin-top: 8px;
  font-size: 0.8rem;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 6px;
}

.chip {
  padding: 4px 8px;
  border-radius: 999px;
  background: #eee;
}

.clear-filters {
  border: none;
  background: transparent;
  color: #0066cc;
  cursor: pointer;
  padding: 0;
  font-size: 0.8rem;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 180px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12);
  z-index: 20;
}

.dropdown-item {
  padding: 8px 10px;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: #f2f2f2;
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
  background: #385b74;
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
