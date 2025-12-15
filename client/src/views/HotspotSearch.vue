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

      <!-- Floating filters card -->
      <div class="filters-card">
        <!-- Text search -->
        <div class="filter-group">
          <label for="search">Search by name or location</label>
          <input
            id="search"
            type="text"
            v-model="searchQuery"
            placeholder="Type a hotspot name or location..."
            @keyup.enter="applyFilters"
          />
        </div>

        <!-- Country Autocomplete -->
        <div class="filter-group autocomplete">
          <label>Country</label>

          <input
            type="text"
            v-model="countrySearch"
            placeholder="Search countries..."
            @input="onCountryInput"
            @keyup.enter="applyFilters"
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
            @input="onSubregionInput"
            @keyup.enter="applyFilters"
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
          Showing {{ filteredHotspots.length }} hotspots
        </div>
      </div>
    </div>
    <!-- END LEFT PANEL -->

    <!-- MIDDLE PANEL: Hotspot Cards -->
    <div class="results">

      <!-- Applied filters bar ABOVE cards -->
      <div v-if="hasActiveFilters" class="results-filters">
        <div class="active-filters">
          <div class="chips">
            <!-- Text search -->
            <button
              v-if="searchQuery.trim()"
              class="chip"
              @click="clearSearch"
            >
              {{ searchQuery }}
              <span class="chip-x">×</span>
            </button>

            <!-- Country -->
            <button
              v-if="analyticsStore.selectedCountry || countrySearch.trim()"
              class="chip"
              @click="clearCountry"
            >
              {{ analyticsStore.selectedCountry || countrySearch }}
              <span class="chip-x">×</span>
            </button>

            <!-- Subregion -->
            <button
              v-if="selectedSubregion || subregionSearch.trim()"
              class="chip"
              @click="clearSubregion"
            >
              {{ selectedSubregion || subregionSearch }}
              <span class="chip-x">×</span>
            </button>
          </div>

          <button class="clear-filters" @click="clearAllFilters">
            Delete all
          </button>
        </div>
      </div>

      <div class="cards-container">
        <HotspotCard
        v-for="hotspot in filteredHotspots"
        :key="hotspot.id"
        :id="hotspot.id"
        :name="hotspot.name"
        :country="hotspot.country"
        :subregion1="hotspot.subregion1"
        :subregion2="hotspot.subregion2"
        :species-count="hotspot.speciesCount"
        :is-selected="analyticsStore.selectedHotspot?.id === hotspot.id"
        @click="selectHotspotById"
      />
        <!-- infinite scroll -->
        <div ref="scrollSentinel" style="height: 1px;"></div>
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
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import type { HotspotOverview } from '../types';

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
    BIconHouseFill,
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();

    const hotspots = computed(() => analyticsStore.allHotspots);

    // How many cards to show at once (for infinite scroll in UI)
    const pageSize = 20;
    const visibleCount = ref(pageSize);

    // Filters
    const searchQuery = ref('');
    const countrySearch = ref('');
    const subregionSearch = ref('');
    const selectedSubregion = ref('');

    // Dropdown visibility
    const showCountryDropdown = ref(false);
    const showSubregionDropdown = ref(false);

    // Infinite scroll sentinel + observer
    const scrollSentinel = ref<HTMLElement | null>(null);
    const scrollObserver = ref<IntersectionObserver | null>(null);

    // -------------------------
    // APPLY FILTERS backend search or browse
    // -------------------------
    const applyFilters = () => {
      const hotspotFilter = searchQuery.value.trim();

      // Country: use selected value (from suggestions) if present
      const countryFilter = analyticsStore.selectedCountry ?? '';

      // Subregion: use selected value OR typed text
      const subregionFilter = (selectedSubregion.value || subregionSearch.value).trim();

      // Are we actually filtering?
      const hasAnyFilter =
        !!hotspotFilter ||
        !!countryFilter ||
        !!subregionFilter;

      // Keep store search fields in sync
      analyticsStore.searchHotspotName = hotspotFilter;
      analyticsStore.searchCountry = countryFilter;
      analyticsStore.searchSubregion1 = subregionFilter;
      analyticsStore.searchSubregion2 = '';

      // Whenever filters change, reset how many we show
      visibleCount.value = pageSize;

      if (!hasAnyFilter) {
        //  No filters browse mode
        analyticsStore.countrySuggestions = [];
        analyticsStore.subregion1Suggestions = [];
        analyticsStore.fetchAllHotspots();
        return;
      }

      // Filters active --> use search endpoint (no backend pagination,
      // but we'll infinite-scroll through the returned list)
      analyticsStore.searchHotspots({
        hotspot: hotspotFilter,
        country: countryFilter,
        subregion1: subregionFilter,
        mode: 'hotspot',
      });
    };

    // -------------------------
    // AVAILABLE FILTER VALUES (fallback from current hotspots)
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
    // combine backend suggestions + local fallback
    // -------------------------
    const filteredCountries = computed(() => {
      if (analyticsStore.countrySuggestions?.length > 0) {
        return analyticsStore.countrySuggestions;
      }
      if (!countrySearch.value.trim()) return availableCountries.value;
      return availableCountries.value.filter(c =>
        c.toLowerCase().includes(countrySearch.value.toLowerCase())
      );
    });

    const filteredSubregions = computed(() => {
      if (analyticsStore.subregion1Suggestions?.length > 0) {
        return analyticsStore.subregion1Suggestions;
      }
      if (!subregionSearch.value.trim()) return availableSubregions.value;
      return availableSubregions.value.filter(sr =>
        sr.toLowerCase().includes(subregionSearch.value.toLowerCase())
      );
    });

    // -------------------------
    // INPUT HANDLERS for backend autocomplete
    // -------------------------
    const onCountryInput = () => {
      showCountryDropdown.value = true;
      const q = countrySearch.value.trim();
      if (q) {
        analyticsStore.searchCountries(q);
      } else {
        analyticsStore.countrySuggestions = [];
        analyticsStore.selectedCountry = null;
        applyFilters();
      }
    };

    const onSubregionInput = () => {
  showSubregionDropdown.value = true;
  const q = subregionSearch.value.trim();

  if (q) {
    analyticsStore.fetchSubregion1Suggestions(
      analyticsStore.selectedCountry ?? '', //  allow country to be emopty
      q
    );
  } else {
    analyticsStore.subregion1Suggestions = [];
    selectedSubregion.value = '';
    applyFilters();
  }
};

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
      analyticsStore.subregion1Suggestions = [];

      applyFilters();
    };

    const selectSubregion = (subregion: string) => {
      selectedSubregion.value = subregion;
      subregionSearch.value = subregion;
      showSubregionDropdown.value = false;

      applyFilters();
    };

    // -------------------------
    // WATCHERS: CLEAR FILTERS WHEN INPUT CLEARED
    // -------------------------
    watch(countrySearch, (val) => {
      const v = (val ?? '').toString();
      if (!v.trim()) {
        analyticsStore.selectedCountry = null;
        analyticsStore.countrySuggestions = [];
        applyFilters();
      }
    });

    watch(subregionSearch, (val) => {
      const v = (val ?? '').toString();
      if (!v.trim()) {
        selectedSubregion.value = '';
        analyticsStore.subregion1Suggestions = [];
        applyFilters();
      }
    });

    // If backend result list shrinks (new filter returns fewer),
    // keep visibleCount within range
    watch(hotspots, (newVal) => {
      if (visibleCount.value > newVal.length) {
        visibleCount.value = Math.min(newVal.length, pageSize);
      }
    });

    // -------------------------
    // FILTER HOTSPOTS (UI-side infinite scroll)
    // -------------------------
    const filteredHotspots = computed(() => {
      return hotspots.value.slice(0, visibleCount.value);
    });

    // -------------------------
    // APPLIED FILTERS STATE
    // -------------------------
    const hasActiveFilters = computed(() => {
      return (
        !!searchQuery.value.trim() ||
        !!analyticsStore.selectedCountry ||
        !!countrySearch.value.trim() ||
        !!selectedSubregion.value ||
        !!subregionSearch.value.trim()
      );
    });

    const clearSearch = () => {
      searchQuery.value = '';
      applyFilters();
    };

    const clearCountry = () => {
      analyticsStore.selectedCountry = null;
      countrySearch.value = '';
      analyticsStore.countrySuggestions = [];
      applyFilters();
    };

    const clearSubregion = () => {
      selectedSubregion.value = '';
      subregionSearch.value = '';
      analyticsStore.subregion1Suggestions = [];
      applyFilters();
    };

    const clearAllFilters = () => {
      searchQuery.value = '';
      analyticsStore.selectedCountry = null;
      countrySearch.value = '';
      analyticsStore.countrySuggestions = [];
      selectedSubregion.value = '';
      subregionSearch.value = '';
      analyticsStore.subregion1Suggestions = [];
      applyFilters();
    };

    // -------------------------
    // DROPDOWN HIDING BEHAVIOR
    // -------------------------
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
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

    // -------------------------
    // INFINITE SCROLL OBSERVER
    // -------------------------
    const setupScrollObserver = () => {
      if (!scrollSentinel.value) return;

      const observer = new IntersectionObserver((entries) => {
        const entry = entries[0];
        if (!entry || !entry.isIntersecting) return;

        // Always show more on scroll, up to the number of hotspots we have
        if (visibleCount.value < hotspots.value.length) {
          visibleCount.value += pageSize;
        }

        // In browse mode if we've shown everything we currently have
        // and backend says there is more, request another page.
        if (
          !hasActiveFilters.value &&
          visibleCount.value >= hotspots.value.length &&
          analyticsStore.hotspotsHasMore
        ) {
          analyticsStore.loadMoreHotspots();
        }
      });

      observer.observe(scrollSentinel.value);
      scrollObserver.value = observer;
    };

    onMounted(() => {
      // Initial browse load
      analyticsStore.fetchAllHotspots();

      document.addEventListener('click', handleClickOutside);
      document.addEventListener('keydown', handleEscape);

      setupScrollObserver();
    });

    onBeforeUnmount(() => {
      if (scrollObserver.value && scrollSentinel.value) {
        scrollObserver.value.unobserve(scrollSentinel.value);
        scrollObserver.value.disconnect();
      }
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

      // Handlers
      onCountryInput,
      onSubregionInput,

      // Infinite scroll
      scrollSentinel,

      // Hotspot display
      filteredHotspots,
      selectHotspotById,

      // Applied filters
      hasActiveFilters,
      clearSearch,
      clearCountry,
      clearSubregion,
      clearAllFilters,
      applyFilters,

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
  box-sizing: border-box;
  background: #f9f9f9;     
  overflow-y: auto; 
}

/* floating card for filters */
.filters-card {
  margin-top: 12px;
  padding: 14px 12px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* Dropdown wrapper */
.autocomplete {
  position: relative;
}

/* MIDDLE PANEL: cards */
.results {
  flex: 1.5;
  padding: 20px;
  box-sizing: border-box;
  background: #f9f9f9;
  overflow-y: auto;
}

/* Applied filters bar in middle */
.results-filters {
  margin-bottom: 16px;
}

.active-filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 18px;             
  background: #ffffff;
  border: 1px solid #0066cc;       
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  font-size: 0.95rem;             
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid #0066cc;
  background: #f3f8ff;
  color: #0066cc;
  font-size: 0.95rem;
  cursor: pointer;
}

.chip-x {
  font-weight: 600;
  line-height: 1;
}

.chip:hover {
  background: #e4f0ff;
}

.clear-filters {
  border: none;
  background: transparent;
  color: #0066cc; 
  cursor: pointer;
  padding: 0 4px;
  font-size: 0.9rem;
  white-space: nowrap;
}

/* Dropdown for autocomplete */
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
  margin-top: 16px;
  margin-bottom: 4px;
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

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-content: flex-start;
}

/* RIGHT PANEL: summary */
.summary-panel {
  width: 320px;
  box-sizing: border-box;
  padding: 16px;
  background: #f9f9f9;
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
