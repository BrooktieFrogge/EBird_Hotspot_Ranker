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

      <h1 class="panel-title">Browse Hotspots</h1>

      <!-- Floating filters card -->
      <div class="filters-card">

        <!-- Filters heading row -->
        <div class="row">
          <span class="label">
            <BIconFilter class="icon" />
            <strong>Filters</strong>
          </span>
        </div>

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

        <!-- Subregion 1 Autocomplete -->
        <div class="filter-group autocomplete">
          <label>States/Provinces</label>

          <input
            type="text"
            v-model="subregionSearch"
            placeholder="Search states or provinces..."
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

        <!-- Subregion 2 Autocomplete -->
        <div class="filter-group autocomplete">
          <label>Counties/ Districts</label>

          <input
            type="text"
            v-model="subregion2Search"
            placeholder="Search counties or districts..."
            @input="onSubregion2Input"
            @keyup.enter="applyFilters"
          />

          <div
            v-if="showSubregion2Dropdown && filteredSubregions2.length > 0"
            class="dropdown"
          >
            <div
              class="dropdown-item"
              v-for="sr2 in filteredSubregions2"
              :key="sr2"
              @click="selectSubregion2(sr2)"
            >
              {{ sr2 }}
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

            <!-- Subregion 1 -->
            <button
              v-if="selectedSubregion || subregionSearch.trim()"
              class="chip"
              @click="clearSubregion"
            >
              {{ selectedSubregion || subregionSearch }}
              <span class="chip-x">×</span>
            </button>

            <!-- Subregion 2 -->
            <button
              v-if="selectedSubregion2 || subregion2Search.trim()"
              class="chip"
              @click="clearSubregion2"
            >
              {{ selectedSubregion2 || subregion2Search }}
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
          :is-selected="analyticsStore.selectedHotspotId === hotspot.id"
          @click="selectHotspotById(hotspot.id)"
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
          <span class="summary-label">Region:</span>
          <span class="summary-value">
            {{ analyticsStore.selectedHotspot.subregion1 }}
          </span>
        </div>

        <div class="summary-row">
          <span class="summary-label">Local Region:</span>
          <span class="summary-value">
            {{ analyticsStore.selectedHotspot.subregion2 || '—' }}
          </span>
        </div>

        <!-- Species Count -->
        <div class="summary-row">
          <span class="summary-label">Species Count:</span>

          <span
            class="summary-value species-with-dot"
            v-if="selectedSpeciesCount !== null"
          >
            <span
              class="color-dot"
              :style="{ backgroundColor: getSpeciesCountColor(selectedSpeciesCount) }"
              aria-hidden="true"
            />
            {{ selectedSpeciesCount }}
          </span>

          <span class="summary-value" v-else>—</span>
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
          Get Report
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
import { storeToRefs } from "pinia";
import { useRouter } from 'vue-router';
import HotspotCard from "../components/HotspotCard.vue";
import { BIconHouseFill, BIconFilter } from 'bootstrap-icons-vue';
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import { useHotspotSearchUIStore } from "../stores/useHotspotSearchUIStore";
import type { HotspotOverview } from '../types';

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
    BIconHouseFill,
    BIconFilter,
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();

    // UI state store (persists across route changes)
    const uiStore = useHotspotSearchUIStore();
    const {
      searchQuery,
      countrySearch,
      subregionSearch,
      selectedSubregion,
      subregion2Search,
      selectedSubregion2,
      selectedHotspotId,
    } = storeToRefs(uiStore);

    const hotspots = computed(() => analyticsStore.allHotspots);

    // -------------------------
    // PAGINATION (UI-side)
    // -------------------------
    const pageSize = 20;
    const visibleCount = ref(pageSize);

    // Dropdown visibility
    const showCountryDropdown = ref(false);
    const showSubregionDropdown = ref(false);
    const showSubregion2Dropdown = ref(false);

    // -------------------------
    // SCROLL OBSERVER
    // -------------------------
    const scrollSentinel = ref<HTMLElement | null>(null);
    const scrollObserver = ref<IntersectionObserver | null>(null);

    // -------------------------
    // SPECIES COUNT COLOR LOGIC
    // -------------------------
    function getSpeciesCountColor(speciesCount: number): string {
      if (speciesCount >= 600) return '#eb463c';
      if (speciesCount >= 500) return '#eb5f50';
      if (speciesCount >= 400) return '#eb8769';
      if (speciesCount >= 300) return '#f0b46e';
      if (speciesCount >= 250) return '#fadc73';
      if (speciesCount >= 200) return '#faf078';
      if (speciesCount >= 150) return '#fafa8c';
      if (speciesCount >= 100) return '#f0f596';
      if (speciesCount >= 50)  return '#e1ebb4';
      if (speciesCount >= 15)  return '#e1ebeb';
      return '#e6f0eb';
    }

    // -------------------------
    // RIGHT PANEL SAFE SPECIES COUNT
    // -------------------------
    const selectedSpeciesCount = computed<number | null>(() => {
      const selected: any = analyticsStore.selectedHotspot;

      if (typeof selected?.speciesCount === 'number') {
        return selected.speciesCount;
      }

      const id = analyticsStore.selectedHotspotId;
      if (!id) return null;

      const overview = analyticsStore.allHotspots.find(h => h.id === id);
      return typeof overview?.speciesCount === 'number'
        ? overview.speciesCount
        : null;
    });

    // -------------------------
    // APPLY FILTERS (BACKEND)
    // -------------------------
    const applyFilters = () => {
      const hotspotFilter = searchQuery.value.trim();
      const countryFilter = analyticsStore.selectedCountry ?? '';
      const subregion1Filter = (selectedSubregion.value || subregionSearch.value).trim();
      const subregion2Filter = (selectedSubregion2.value || subregion2Search.value).trim();

      const hasAnyFilter =
        !!hotspotFilter ||
        !!countryFilter ||
        !!subregion1Filter ||
        !!subregion2Filter;

      // Keep store search fields in sync
      analyticsStore.searchHotspotName = hotspotFilter;
      analyticsStore.searchCountry = countryFilter;
      analyticsStore.searchSubregion1 = subregion1Filter;
      analyticsStore.searchSubregion2 = subregion2Filter;

      visibleCount.value = pageSize;

      // persist UI state whenever filters are applied
      uiStore.persist();

      if (!hasAnyFilter) {
        analyticsStore.countrySuggestions = [];
        analyticsStore.subregion1Suggestions = [];
        (analyticsStore as any).subregion2Suggestions = [];
        analyticsStore.fetchAllHotspots();
        return;
      }

      analyticsStore.searchHotspots({
        hotspot: hotspotFilter,
        country: countryFilter,
        subregion1: subregion1Filter,
        subregion2: subregion2Filter,
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
          if (h.subregion1) set.add(h.subregion1);
        }
      });
      return Array.from(set).sort();
    });

    const availableSubregions2 = computed(() => {
      const set = new Set<string>();
      const sr1Filter = (selectedSubregion.value || subregionSearch.value).trim();

      hotspots.value.forEach(h => {
        if (sr1Filter && h.subregion1?.toLowerCase() !== sr1Filter.toLowerCase()) return;

        const sr2 = (h.subregion2 ?? '').toString().trim();
        if (sr2 && sr2.toLowerCase() !== 'none' && sr2.toLowerCase() !== 'null') {
          set.add(sr2);
        }
      });

      return Array.from(set).sort();
    });

    // -------------------------
    // AUTOCOMPLETE FILTERING
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

    const filteredSubregions2 = computed(() => {
      const backend = (analyticsStore as any).subregion2Suggestions as string[] | undefined;
      if (backend && backend.length > 0) return backend;

      if (!subregion2Search.value.trim()) return availableSubregions2.value;

      return availableSubregions2.value.filter(sr2 =>
        sr2.toLowerCase().includes(subregion2Search.value.toLowerCase())
      );
    });

    // -------------------------
    // INPUT HANDLERS
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
          analyticsStore.selectedCountry ?? '',
          q
        );
      } else {
        analyticsStore.subregion1Suggestions = [];
        selectedSubregion.value = '';
        applyFilters();
      }
    };

    const onSubregion2Input = () => {
      showSubregion2Dropdown.value = true;
      const q = subregion2Search.value.trim();
      const sr1Filter = (selectedSubregion.value || subregionSearch.value).trim();

      if (q) {
        if (typeof (analyticsStore as any).fetchSubregion2Suggestions === 'function') {
          (analyticsStore as any).fetchSubregion2Suggestions(sr1Filter, q);
        }
      } else {
        (analyticsStore as any).subregion2Suggestions = [];
        selectedSubregion2.value = '';
        applyFilters();
      }
    };

    // -------------------------
    // SELECT FILTER VALUES
    // -------------------------
    const selectCountry = (country: string) => {
      analyticsStore.selectedCountry = country;
      countrySearch.value = country;
      showCountryDropdown.value = false;

      selectedSubregion.value = '';
      subregionSearch.value = '';
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];

      applyFilters();
    };

    const selectSubregion = (subregion: string) => {
      selectedSubregion.value = subregion;
      subregionSearch.value = subregion;
      showSubregionDropdown.value = false;

      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];

      applyFilters();
    };

    const selectSubregion2 = (sr2: string) => {
      selectedSubregion2.value = sr2;
      subregion2Search.value = sr2;
      showSubregion2Dropdown.value = false;

      applyFilters();
    };

    // -------------------------
    // WATCHERS
    // -------------------------
    watch(countrySearch, (val) => {
      if (!val.trim()) {
        analyticsStore.selectedCountry = null;
        analyticsStore.countrySuggestions = [];
        applyFilters();
      } else {
        uiStore.persist();
      }
    });

    watch(subregionSearch, (val) => {
      if (!val.trim()) {
        selectedSubregion.value = '';
        analyticsStore.subregion1Suggestions = [];
        applyFilters();
      } else {
        uiStore.persist();
      }
    });

    watch(subregion2Search, (val) => {
      if (!val.trim()) {
        selectedSubregion2.value = '';
        (analyticsStore as any).subregion2Suggestions = [];
        applyFilters();
      } else {
        uiStore.persist();
      }
    });

    watch(searchQuery, () => uiStore.persist());

    watch(hotspots, (newVal) => {
      if (visibleCount.value > newVal.length) {
        visibleCount.value = Math.min(newVal.length, pageSize);
      }
    });

    // -------------------------
    // UI FILTERED HOTSPOTS
    // -------------------------
    const filteredHotspots = computed(() =>
      hotspots.value.slice(0, visibleCount.value)
    );

    // -------------------------
    // ACTIVE FILTER STATE
    // -------------------------
    const hasActiveFilters = computed(() => (
      !!searchQuery.value.trim() ||
      !!analyticsStore.selectedCountry ||
      !!countrySearch.value.trim() ||
      !!selectedSubregion.value ||
      !!subregionSearch.value.trim() ||
      !!selectedSubregion2.value ||
      !!subregion2Search.value.trim()
    ));

    // -------------------------
    // CLEAR FILTERS
    // -------------------------
    const clearSearch = () => {
      searchQuery.value = '';
      applyFilters();
    };

    const clearCountry = () => {
      analyticsStore.selectedCountry = null;
      countrySearch.value = '';
      analyticsStore.countrySuggestions = [];

      selectedSubregion.value = '';
      subregionSearch.value = '';
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];

      applyFilters();
    };

    const clearSubregion = () => {
      selectedSubregion.value = '';
      subregionSearch.value = '';
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];

      applyFilters();
    };

    const clearSubregion2 = () => {
      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];
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

      selectedSubregion2.value = '';
      subregion2Search.value = '';
      (analyticsStore as any).subregion2Suggestions = [];

      applyFilters();
    };

    // -------------------------
    // CLICK OUTSIDE / ESCAPE
    // -------------------------
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (!target.closest('.autocomplete')) {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
        showSubregion2Dropdown.value = false;
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
        showSubregion2Dropdown.value = false;
      }
    };

    // -------------------------
    // INFINITE SCROLL
    // -------------------------
    const setupScrollObserver = () => {
      if (!scrollSentinel.value) return;

      const observer = new IntersectionObserver(entries => {
        if (!entries[0]?.isIntersecting) return;

        if (visibleCount.value < hotspots.value.length) {
          visibleCount.value += pageSize;
        }

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

    // -------------------------
    // HOTSPOT SELECTION (persisted)
    // -------------------------
    const selectHotspotById = (id: HotspotOverview['id']) => {
      analyticsStore.setHotspot(id);
      uiStore.setSelectedHotspotId(String(id));
    };

    const goToSelectedHotspotDetail = () => {
      const selected = analyticsStore.selectedHotspot;
      if (!selected) return;

      uiStore.setSelectedHotspotId(String(selected.id));

      router.push({
        name: "HotspotDetail",
        params: { id: selected.id },
      });
    };

    const redirectToHomeScreen = () => {
      // persist state before leaving
      uiStore.persist();
      router.push({ name: "HomeScreen" });
    };

    // -------------------------
    // LIFECYCLE
    // -------------------------
    onMounted(() => {
      analyticsStore.fetchAllHotspots();

      // re-apply filters when returning to this page
      // (important: ensures results match persisted filters)
      // also restores selected card in analytics store
      if (selectedHotspotId.value) {
        analyticsStore.setHotspot(selectedHotspotId.value as any);
      }
      applyFilters();

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

      // persist on unmount too
      uiStore.persist();
    });

    // -------------------------
    // RETURN TO TEMPLATE
    // -------------------------
    return {
      hotspots,
      analyticsStore,

      // persisted filter state
      searchQuery,
      countrySearch,
      subregionSearch,
      selectedSubregion,
      subregion2Search,
      selectedSubregion2,

      // dropdown state
      showCountryDropdown,
      showSubregionDropdown,
      showSubregion2Dropdown,

      // available values
      availableCountries,
      availableSubregions,
      availableSubregions2,

      // filtered dropdown lists
      filteredCountries,
      filteredSubregions,
      filteredSubregions2,

      // handlers
      onCountryInput,
      onSubregionInput,
      onSubregion2Input,

      // selectors
      selectCountry,
      selectSubregion,
      selectSubregion2,

      // clear controls
      clearSearch,
      clearCountry,
      clearSubregion,
      clearSubregion2,
      clearAllFilters,

      // active state + apply
      hasActiveFilters,
      applyFilters,

      // infinite scroll
      scrollSentinel,
      filteredHotspots,

      // selection
      selectHotspotById,
      goToSelectedHotspotDetail,
      redirectToHomeScreen,

      // right panel species count
      selectedSpeciesCount,
      getSpeciesCountColor,
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
  background: #F2F2F2;     
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
  background: #F2F2F2;
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
  background: #F2F2F2;
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
   background-color: #d2d2d2;
}

.filter-heading {
  display: left;
  align-items: left;
 
 
}

.filter-icon {
  width: 18px;
  height: 18px;
}

.filter-heading-text {
  font-size: 1rem;
}
.row {
  display: flex;
  align-items: center;
  justify-content: flex-start; 
  margin-bottom: 8px;
}

.label {
  display: inline-flex;        
  align-items: center;         
  justify-content: flex-start; 
  gap: 4px;                   
  font-size: 0.95rem;
  font-weight: 700;
  margin: 0;                   
  padding: 0;
}

.icon {
  display: inline-block;
  margin: 5px;                   
  padding: 0;
}

</style>
