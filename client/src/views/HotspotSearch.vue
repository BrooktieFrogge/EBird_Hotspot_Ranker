<template>
  <div class="page-layout" @click="handlePageClick">
    <TopNavBar />
    <div class="hotspot-search">
      <div class="mobile-search-bar mobile-only">
        <button
          class="nav-btn filter-toggle-btn"
          @click.stop="showFiltersDrawer = !showFiltersDrawer"
        >
          <span
            style="
              font-size: 1.5rem;
              font-weight: bold;
              color: var(--color-primary);
            "
            >&gt;</span
          >
        </button>

        <div class="search-input-wrapper" style="flex: 1; position: relative">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search hotspots..."
            @input="onHotspotInput"
            @keyup.enter="applyFilters"
            class="mobile-search-input compact"
            style="width: 100%; padding-right: 30px"
          />
          <button
            v-if="searchQuery"
            class="mobile-search-clear"
            @click="clearSearch"
            style="right: 8px"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- backdrop for drawer -->
      <div
        class="drawer-backdrop"
        :class="{ open: showFiltersDrawer }"
        @click="showFiltersDrawer = false"
      ></div>

      <!-- backdrop for summary sheet -->
      <div
        class="sheet-backdrop mobile-only"
        :class="{ open: showSummarySheet }"
        @click="showSummarySheet = false"
      ></div>

      <!-- left panel (becomes slide drawer on mobile) -->
      <div class="filters slide-drawer" :class="{ open: showFiltersDrawer }">
        <!-- close button for mobile drawer -->
        <button
          class="drawer-close-btn mobile-only"
          @click="showFiltersDrawer = false"
        >
          ✕
        </button>

        <!-- buttons container -->
        <div class="buttons-container desktop-only">
          <!-- home button removed -->
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

          <!-- Text search (NOW with autocomplete suggestions) -->
          <div class="filter-group autocomplete">
            <label for="search">Search by name or location</label>
            <input
              id="search"
              type="text"
              v-model="searchQuery"
              placeholder="Type a hotspot name or location..."
              @input="onHotspotInput"
              @keyup.enter="applyFilters"
            />

            <!-- Hotspot suggestions dropdown -->
            <div
              v-if="
                showHotspotDropdown && filteredHotspotSuggestions.length > 0
              "
              class="dropdown"
            >
              <div
                class="dropdown-item"
                v-for="name in filteredHotspotSuggestions"
                :key="name"
                @click="selectHotspotSuggestion(name)"
              >
                {{ name }}
              </div>
            </div>
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
      <div class="results" ref="resultsContainer" @scroll="handleResultsScroll">
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
        </div>

        <!-- infinite scroll sentinel -->
        <div ref="scrollSentinel" style="height: 1px; width: 100%"></div>

        <!-- centered loader for initial load (no cards yet) -->
        <div
          v-if="analyticsStore.isLoading && filteredHotspots.length === 0"
          class="initial-loader"
        >
          <img :src="loadingImage" alt="Loading..." />
        </div>

        <!-- bottom loader for infinite scroll (has cards already) -->
        <div
          v-if="analyticsStore.isLoading && filteredHotspots.length > 0"
          class="bottom-loader"
        >
          <img :src="loadingImage" alt="Loading..." />
        </div>
      </div>

      <!-- right panel (becomes slide sheet on mobile) -->
      <div
        class="summary-panel slide-sheet"
        :class="{ open: showSummarySheet }"
      >
        <!-- close button for mobile sheet -->
        <button
          class="sheet-close-btn mobile-only"
          @click="showSummarySheet = false"
        >
          ✕
        </button>

        <div class="sheet-handle mobile-only"></div>

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
            <span class="summary-label">State/Province:</span>
            <span class="summary-value">
              {{ analyticsStore.selectedHotspot.subregion1 }}
            </span>
          </div>

          <div class="summary-row">
            <span class="summary-label">County/District:</span>
            <span class="summary-value">
              {{ analyticsStore.selectedHotspot.subregion2 || "—" }}
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
                :style="{
                  backgroundColor: getSpeciesCountColor(selectedSpeciesCount),
                }"
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

      <!-- mobile/tablet floating get report button -->
      <button
        class="floating-get-report-btn"
        :class="{ 'btn-disabled': !analyticsStore.selectedHotspot }"
        :disabled="!analyticsStore.selectedHotspot"
        @click="goToSelectedHotspotDetail"
      >
        Get Report
      </button>

      <!-- mobile bottom navigation -->
      <div
        class="carousel-nav-bar mobile-only"
        :class="{ 'dock-lifted': navStore.mobileNavOpen }"
      >
        <button
          class="nav-btn back-btn"
          @click="handleBack"
          aria-label="Go Back"
        >
          <BIconArrowLeft />
        </button>

        <button
          class="nav-btn primary-action"
          :disabled="!analyticsStore.selectedHotspot"
          :class="{ 'btn-disabled': !analyticsStore.selectedHotspot }"
          @click="redirectToReport"
        >
          Get Report
        </button>

        <button
          class="nav-btn"
          @click="navStore.toggleMobileNav()"
          aria-label="Menu"
        >
          <BIconList v-if="!navStore.mobileNavOpen" style="font-size: 1.5rem" />
          <BIconArrowDown v-else style="font-size: 1.5rem" />
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
} from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import HotspotCard from "../components/HotspotCard.vue";
import {
  BIconHouseFill,
  BIconFilter,
  BIconEye,
  BIconArrowLeft,
  BIconList,
  BIconArrowDown,
} from "bootstrap-icons-vue";
import ThemeToggle from "../components/ThemeToggle.vue";
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import { useHotspotSearchUIStore } from "../stores/useHotspotSearchUIStore";
import { useNavigationStore } from "../stores/useNavigationStore";
import TopNavBar from "../components/TopNavBar.vue";
import type { HotspotOverview } from "../types";

export default defineComponent({
  name: "HotspotSearch",

  components: {
    HotspotCard,
    BIconHouseFill,
    BIconFilter,
    BIconEye,
    BIconArrowLeft,
    BIconList,
    BIconArrowDown,
    ThemeToggle,
    TopNavBar,
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();
    const navStore = useNavigationStore();

    // cleanup timers
    onBeforeUnmount(() => {
      clearTimeout(hotspotDebounceTimer);
      clearTimeout(countryDebounceTimer);
    });

    // UI state store (persists across route changes)
    const uiStore = useHotspotSearchUIStore();

    // shared loading image
    const loadingImage =
      "https://cdn.pixabay.com/animation/2024/07/04/20/46/20-46-07-872_512.gif";

    const {
      searchQuery,
      countrySearch,
      subregionSearch,
      selectedSubregion,
      subregion2Search,
      selectedSubregion2,
      selectedHotspotId,
    } = storeToRefs(uiStore);

    // mobile ui state
    const showFiltersDrawer = ref(false);
    const showSummarySheet = ref(false);
    // mobileNavOpen removed (handled by navStore)

    // toggle filter drawer (for hamburger button)
    const toggleFiltersDrawer = () => {
      showFiltersDrawer.value = !showFiltersDrawer.value;
    };

    // handle page click to close sheets when clicking outside
    const handlePageClick = (e: Event) => {
      // don't close if clicking inside summary panel or filters
      const target = e.target as HTMLElement;
      if (
        target.closest(".summary-panel") ||
        target.closest(".filters") ||
        target.closest(".mobile-header") ||
        target.closest(".mobile-search-bar")
      ) {
        return;
      }
      // close summary sheet if open
      if (showSummarySheet.value) {
        showSummarySheet.value = false;
      }
    };

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
    const showHotspotDropdown = ref(false);

    // -------------------------
    // SCROLL OBSERVER
    // -------------------------
    const scrollSentinel = ref<HTMLElement | null>(null);
    const scrollObserver = ref<IntersectionObserver | null>(null);

    // -------------------------
    // SPECIES COUNT COLOR LOGIC
    // -------------------------
    function getSpeciesCountColor(speciesCount: number): string {
      if (speciesCount >= 600) return "#eb463c";
      if (speciesCount >= 500) return "#eb5f50";
      if (speciesCount >= 400) return "#eb8769";
      if (speciesCount >= 300) return "#f0b46e";
      if (speciesCount >= 250) return "#fadc73";
      if (speciesCount >= 200) return "#faf078";
      if (speciesCount >= 150) return "#fafa8c";
      if (speciesCount >= 100) return "#f0f596";
      if (speciesCount >= 50) return "#e1ebb4";
      if (speciesCount >= 15) return "#e1ebeb";
      return "#e6f0eb";
    }

    // -------------------------
    // RIGHT PANEL SAFE SPECIES COUNT
    // -------------------------
    const selectedSpeciesCount = computed<number | null>(() => {
      const selected: any = analyticsStore.selectedHotspot;

      if (typeof selected?.speciesCount === "number") {
        return selected.speciesCount;
      }

      const id = analyticsStore.selectedHotspotId;
      if (!id) return null;

      const overview = analyticsStore.allHotspots.find((h) => h.id === id);
      return typeof overview?.speciesCount === "number"
        ? overview.speciesCount
        : null;
    });

    // -------------------------
    // APPLY FILTERS (BACKEND)
    // -------------------------

    function canonicalize(input: string, options: string[]): string {
      const raw = (input ?? "").trim();
      if (!raw) return "";
      const lower = raw.toLowerCase();

      const match = options.find(
        (opt) => (opt ?? "").trim().toLowerCase() === lower
      );
      return match ?? raw; // if we can't find a canonical option, fall back to what they typed
    }

    const applyFilters = () => {
      const hotspotFilter = searchQuery.value.trim();
      const countryFilter = analyticsStore.selectedCountry ?? "";

      const subregion1Raw = (
        selectedSubregion.value || subregionSearch.value
      ).trim();
      const subregion2Raw = (
        selectedSubregion2.value || subregion2Search.value
      ).trim();

      // Convert typed input into the correct-cased value if it exists
      const subregion1Filter = canonicalize(
        subregion1Raw,
        availableSubregions.value
      );

      const sr2Options = (() => {
        const set = new Set<string>();
        hotspots.value.forEach((h) => {
          if (
            subregion1Filter &&
            h.subregion1?.toLowerCase() !== subregion1Filter.toLowerCase()
          )
            return;
          const sr2 = (h.subregion2 ?? "").toString().trim();
          if (
            sr2 &&
            sr2.toLowerCase() !== "none" &&
            sr2.toLowerCase() !== "null"
          )
            set.add(sr2);
        });
        return Array.from(set);
      })();

      const subregion2Filter = canonicalize(subregion2Raw, sr2Options);

      const hasAnyFilter =
        !!hotspotFilter ||
        !!countryFilter ||
        !!subregion1Filter ||
        !!subregion2Filter;

      analyticsStore.searchHotspotName = hotspotFilter;
      analyticsStore.searchCountry = countryFilter;
      analyticsStore.searchSubregion1 = subregion1Filter;
      analyticsStore.searchSubregion2 = subregion2Filter;

      visibleCount.value = pageSize;
      uiStore.persist();

      if (!hasAnyFilter) {
        analyticsStore.countrySuggestions = [];
        analyticsStore.subregion1Suggestions = [];
        analyticsStore.subregion2Suggestions = [];
        analyticsStore.hotspotSuggestions = [];
        analyticsStore.fetchAllHotspots();
        return;
      }

      analyticsStore.searchHotspots({
        hotspot: hotspotFilter,
        country: countryFilter,
        subregion1: subregion1Filter,
        subregion2: subregion2Filter,
        mode: "hotspot",
      });
    };

    // -------------------------
    // AVAILABLE FILTER VALUES (fallback from current hotspots)
    // -------------------------
    const availableCountries = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach((h) => set.add(h.country));
      return Array.from(set).sort();
    });

    const availableSubregions = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach((h) => {
        if (
          !analyticsStore.selectedCountry ||
          h.country === analyticsStore.selectedCountry
        ) {
          if (h.subregion1) set.add(h.subregion1);
        }
      });
      return Array.from(set).sort();
    });

    const availableSubregions2 = computed(() => {
      const set = new Set<string>();
      const sr1Filter = (
        selectedSubregion.value || subregionSearch.value
      ).trim();

      hotspots.value.forEach((h) => {
        if (
          sr1Filter &&
          h.subregion1?.toLowerCase() !== sr1Filter.toLowerCase()
        )
          return;

        const sr2 = (h.subregion2 ?? "").toString().trim();
        if (
          sr2 &&
          sr2.toLowerCase() !== "none" &&
          sr2.toLowerCase() !== "null"
        ) {
          set.add(sr2);
        }
      });

      return Array.from(set).sort();
    });

    // -------------------------
    // AUTOCOMPLETE FILTERING
    // -------------------------

    const filteredHotspotSuggestions = computed(() => {
      // prefer backend suggestions
      if (analyticsStore.hotspotSuggestions?.length > 0) {
        return analyticsStore.hotspotSuggestions;
      }

      // fallback: local filtering on currently loaded hotspots
      const q = searchQuery.value.trim().toLowerCase();
      if (!q) return [];

      const names = hotspots.value.map((h) => h.name).filter(Boolean);
      const matches = names.filter((n) => n.toLowerCase().includes(q));
      return Array.from(new Set(matches)).slice(0, 10);
    });

    const filteredCountries = computed(() => {
      if (analyticsStore.countrySuggestions?.length > 0) {
        return analyticsStore.countrySuggestions;
      }
      if (!countrySearch.value.trim()) return availableCountries.value;
      return availableCountries.value.filter((c) =>
        c.toLowerCase().includes(countrySearch.value.toLowerCase())
      );
    });

    const filteredSubregions = computed(() => {
      if (analyticsStore.subregion1Suggestions?.length > 0) {
        return analyticsStore.subregion1Suggestions;
      }
      if (!subregionSearch.value.trim()) return availableSubregions.value;
      return availableSubregions.value.filter((sr) =>
        sr.toLowerCase().includes(subregionSearch.value.toLowerCase())
      );
    });

    const filteredSubregions2 = computed(() => {
      if (analyticsStore.subregion2Suggestions.length > 0) {
        return analyticsStore.subregion2Suggestions;
      }

      if (!subregion2Search.value.trim()) return availableSubregions2.value;

      return availableSubregions2.value.filter((sr2) =>
        sr2.toLowerCase().includes(subregion2Search.value.toLowerCase())
      );
    });

    // -------------------------
    // INPUT HANDLERS
    // -------------------------
    let hotspotDebounceTimer: ReturnType<typeof setTimeout>;
    const onHotspotInput = () => {
      showHotspotDropdown.value = true;
      const q = searchQuery.value.trim();

      if (!q) {
        analyticsStore.hotspotSuggestions = [];
        applyFilters();
        return;
      }

      clearTimeout(hotspotDebounceTimer);
      hotspotDebounceTimer = setTimeout(() => {
        // pass current filters so suggestions respect location filters
        const countryFilter = analyticsStore.selectedCountry ?? "";
        const subregion1Filter = (
          selectedSubregion.value || subregionSearch.value
        ).trim();
        const subregion2Filter = (
          selectedSubregion2.value || subregion2Search.value
        ).trim();

        // fetch suggestions
        analyticsStore.fetchHotspotSuggestions(q, {
          country: countryFilter,
          subregion1: subregion1Filter,
          subregion2: subregion2Filter,
          limit: 10,
        });

        // trigger auto-search with debounces
        applyFilters();
      }, 500);
    };

    let countryDebounceTimer: ReturnType<typeof setTimeout>;
    const onCountryInput = () => {
      showCountryDropdown.value = true;
      const q = countrySearch.value.trim();

      clearTimeout(countryDebounceTimer);
      countryDebounceTimer = setTimeout(() => {
        if (q) {
          analyticsStore.searchCountries(q);
        } else {
          analyticsStore.countrySuggestions = [];
          analyticsStore.selectedCountry = null;
          applyFilters();
        }
      }, 300);
    };

    let subregionDebounceTimer: ReturnType<typeof setTimeout>;
    const onSubregionInput = () => {
      showSubregionDropdown.value = true;
      const q = subregionSearch.value.trim();

      clearTimeout(subregionDebounceTimer);
      subregionDebounceTimer = setTimeout(() => {
        if (q) {
          analyticsStore.fetchSubregion1Suggestions(
            analyticsStore.selectedCountry ?? "",
            q
          );
        } else {
          analyticsStore.subregion1Suggestions = [];
          selectedSubregion.value = "";
          applyFilters();
        }
      }, 300);
    };

    let subregion2DebounceTimer: ReturnType<typeof setTimeout>;
    const onSubregion2Input = () => {
      showSubregion2Dropdown.value = true;
      const q = subregion2Search.value.trim();

      clearTimeout(subregion2DebounceTimer);
      subregion2DebounceTimer = setTimeout(() => {
        if (q) {
          analyticsStore.fetchSubregion2Suggestions(
            selectedSubregion.value ?? "",
            q
          );
        } else {
          analyticsStore.subregion2Suggestions = [];
          selectedSubregion2.value = "";
          applyFilters();
        }
      }, 300);
    };

    const selectHotspotSuggestion = (name: string) => {
      searchQuery.value = name;
      showHotspotDropdown.value = false;
      analyticsStore.hotspotSuggestions = [];
      applyFilters();
    };

    // -------------------------
    // SELECT FILTER VALUES
    // -------------------------
    const selectCountry = (country: string) => {
      analyticsStore.selectedCountry = country;
      countrySearch.value = country;
      showCountryDropdown.value = false;

      selectedSubregion.value = "";
      subregionSearch.value = "";
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];

      applyFilters();
    };

    const selectSubregion = (subregion: string) => {
      selectedSubregion.value = subregion;
      subregionSearch.value = subregion;
      showSubregionDropdown.value = false;

      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];

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
        selectedSubregion.value = "";
        analyticsStore.subregion1Suggestions = [];
        applyFilters();
      } else {
        uiStore.persist();
      }
    });

    watch(subregion2Search, (val) => {
      if (!val.trim()) {
        selectedSubregion2.value = "";
        analyticsStore.subregion2Suggestions = [];
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
    const hasActiveFilters = computed(
      () =>
        !!searchQuery.value.trim() ||
        !!analyticsStore.selectedCountry ||
        !!countrySearch.value.trim() ||
        !!selectedSubregion.value ||
        !!subregionSearch.value.trim() ||
        !!selectedSubregion2.value ||
        !!subregion2Search.value.trim()
    );

    // -------------------------
    // CLEAR FILTERS
    // -------------------------
    const clearSearch = () => {
      searchQuery.value = "";
      applyFilters();
      analyticsStore.hotspotSuggestions = [];
      showHotspotDropdown.value = false;
    };

    const clearCountry = () => {
      analyticsStore.selectedCountry = null;
      countrySearch.value = "";
      analyticsStore.countrySuggestions = [];

      selectedSubregion.value = "";
      subregionSearch.value = "";
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];

      applyFilters();
    };

    const clearSubregion = () => {
      selectedSubregion.value = "";
      subregionSearch.value = "";
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];

      applyFilters();
    };

    const clearSubregion2 = () => {
      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];
      applyFilters();
    };

    const clearAllFilters = () => {
      searchQuery.value = "";

      analyticsStore.selectedCountry = null;
      countrySearch.value = "";
      analyticsStore.countrySuggestions = [];

      selectedSubregion.value = "";
      subregionSearch.value = "";
      analyticsStore.subregion1Suggestions = [];

      selectedSubregion2.value = "";
      subregion2Search.value = "";
      analyticsStore.subregion2Suggestions = [];

      applyFilters();
    };

    // -------------------------
    // CLICK OUTSIDE / ESCAPE
    // -------------------------
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (!target.closest(".autocomplete")) {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
        showSubregion2Dropdown.value = false;
        showHotspotDropdown.value = false;
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        showCountryDropdown.value = false;
        showSubregionDropdown.value = false;
        showSubregion2Dropdown.value = false;
        showHotspotDropdown.value = false;
      }
    };

    // -------------------------
    // INFINITE SCROLL
    // -------------------------
    const setupScrollObserver = () => {
      if (!scrollSentinel.value) return;

      const observer = new IntersectionObserver(
        (entries) => {
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
        },
        {
          rootMargin: "0px 0px 600px 0px", // trigger 600px before reaching bottom
          threshold: 0, // trigger as soon as sentinel is partially visible
        }
      );

      observer.observe(scrollSentinel.value);
      scrollObserver.value = observer;
    };

    // Backup scroll handler for when IntersectionObserver doesn't re-fire
    const resultsContainer = ref<HTMLElement | null>(null);

    const handleResultsScroll = () => {
      if (!resultsContainer.value) return;

      const container = resultsContainer.value;
      const scrollTop = container.scrollTop;
      const scrollHeight = container.scrollHeight;
      const clientHeight = container.clientHeight;
      const scrollPercent = scrollTop / (scrollHeight - clientHeight);

      // Trigger when scrolled past 40% OR within 800px of bottom
      // This ensures early loading on first scroll
      const nearBottom = scrollHeight - scrollTop - clientHeight < 800;
      const past40Percent = scrollPercent > 0.4;

      if (nearBottom || past40Percent) {
        if (visibleCount.value < hotspots.value.length) {
          visibleCount.value += pageSize;
        }

        if (
          !hasActiveFilters.value &&
          visibleCount.value >= hotspots.value.length &&
          analyticsStore.hotspotsHasMore &&
          !analyticsStore.isLoading
        ) {
          analyticsStore.loadMoreHotspots();
        }
      }
    };

    // -------------------------
    // HOTSPOT SELECTION (persisted)
    // -------------------------
    const selectHotspotById = (id: HotspotOverview["id"]) => {
      analyticsStore.setHotspot(id);
      uiStore.setSelectedHotspotId(String(id));
      // auto-open summary sheet on mobile when card is selected
      if (window.innerWidth <= 768) {
        showSummarySheet.value = true;
      }
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

    const handleBack = () => {
      // If summary sheet is open, close it first?
      // User requested "Back button" to mimic detail page.
      if (showSummarySheet.value) {
        showSummarySheet.value = false;
        return;
      }
      // If drawer is open
      if (showFiltersDrawer.value) {
        showFiltersDrawer.value = false;
        return;
      }
      // always go to Home
      router.push("/");
    };

    // -------------------------
    // LIFECYCLE
    // -------------------------
    onMounted(async () => {
      // fetch hotspots and wait for them to load
      await analyticsStore.fetchAllHotspots();

      // restore selection from cached UI state
      // This ensures button and card highlight stay in sync after refresh
      if (selectedHotspotId.value) {
        analyticsStore.setHotspot(selectedHotspotId.value as any);
      }
      applyFilters();

      document.addEventListener("click", handleClickOutside);
      document.addEventListener("keydown", handleEscape);
      setupScrollObserver();
    });

    onBeforeUnmount(() => {
      if (scrollObserver.value && scrollSentinel.value) {
        scrollObserver.value.unobserve(scrollSentinel.value);
        scrollObserver.value.disconnect();
      }
      document.removeEventListener("click", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);

      // persist on unmount too
      uiStore.persist();
    });

    // -------------------------
    // RETURN TO TEMPLATE
    // -------------------------
    return {
      hotspots,
      analyticsStore,
      uiStore, // Expose uiStore so we can use selectedHotspotId from it if needed, or refs
      // But we have refs below.

      // Navigation / Actions
      handleBack,
      goToSelectedHotspotDetail, // original name
      redirectToReport: goToSelectedHotspotDetail, // Alias for template usage
      // persisted filter state
      searchQuery,
      countrySearch,
      subregionSearch,
      selectedSubregion,
      subregion2Search,
      selectedSubregion2,
      selectedHotspotId,

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
      canonicalize,

      // infinite scroll
      scrollSentinel,
      filteredHotspots,
      resultsContainer,
      handleResultsScroll,

      // selection
      selectHotspotById,

      // right panel species count
      selectedSpeciesCount,
      getSpeciesCountColor,

      // hotspot autocomplete
      showHotspotDropdown,
      filteredHotspotSuggestions,
      onHotspotInput,
      selectHotspotSuggestion,

      // mobile UI
      showFiltersDrawer,
      showSummarySheet,
      toggleFiltersDrawer,
      handlePageClick,
      // handlePageClick duplicate removed
      navStore,
      loadingImage,
    };
  },
});
</script>

<style scoped>
.page-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.hotspot-search {
  display: flex;
  flex: 1;
  height: 100%;
  background: var(--color-bg-page);
  color: var(--color-text-primary);
  font-family: Arial, sans-serif;
  overflow: hidden;
}

/* LEFT PANEL */
.filters {
  width: 300px;
  padding: 20px 18px;
  box-sizing: border-box;
  background: var(--color-bg-page);
  overflow-y: auto;
  margin-left: 20px;
}

/* floating card for filters */
.filters-card {
  margin-top: 16px;
  padding: 16px;
  background: var(--color-bg-panel);
  border-radius: 20px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border-light);
}

/* Dropdown wrapper */
.autocomplete {
  position: relative;
}

/* MIDDLE PANEL: cards */
.results {
  flex: 1.5;
  padding: 24px 20px;
  box-sizing: border-box;
  background: var(--color-bg-page);
  overflow-y: auto;
  position: relative; /* for absolute positioning of initial loader */
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
  background: var(--color-bg-panel);
  border: 1px solid var(--color-primary);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
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
  border: 1px solid #457999;
  background: rgba(69, 121, 153, 0.12);
  color: #457999;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
}

.chip-x {
  font-weight: 600;
  line-height: 1;
}

.chip:hover {
  background: rgba(69, 121, 153, 0.2);
}

.clear-filters {
  border: none;
  background: transparent;
  color: var(--color-danger, #b31b1b);
  cursor: pointer;
  padding: 0 4px;
  font-size: 0.9rem;
  white-space: nowrap;
}

.clear-filters:hover {
  text-decoration: underline;
}

/* Dropdown for autocomplete */
.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 180px;
  overflow-y: auto;
  background: var(--color-bg-panel);
  border-radius: 10px;
  border: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-dropdown);
  z-index: 20;
}

.dropdown-item {
  padding: 8px 10px;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: rgba(69, 121, 153, 0.1);
}

/* Buttons container  */
.buttons-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: auto;
  padding: 12px 0 8px;
}

.back-button-wrapper {
  display: flex;
  width: fit-content;
  padding: 15px;
  border-radius: 10px;
  border: none;
  background: #457999;
  color: white;
  box-shadow: 0 4px 10px rgba(69, 121, 153, 0.3);
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button-wrapper:hover {
  background: #296239;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 12px;
  margin-bottom: 8px;
  text-align: center;
}

.filter-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #457999;
  font-weight: 600;
}

.filter-group input {
  border: 1px solid rgba(69, 121, 153, 0.4);
  transition: border 0.2s, box-shadow 0.2s;
}
.filter-group input:focus {
  outline: none;
  border-color: #457999;
  box-shadow: 0 0 0 2px rgba(69, 121, 153, 0.2);
}

.filter-group select {
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #bfbfbf;
  background-color: #ffffff;
  color: #000000;
}

.filter-group::placeholder {
  color: #7b7b7b;
}

.filter-group:last-of-type {
  margin-bottom: 12px;
}

.filter-summary {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #555;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-content: flex-start;
}

/* RIGHT PANEL: summary */
.summary-panel {
  width: 320px;
  box-sizing: border-box;
  padding: 20px;
  background: var(--color-bg-panel);
  border-left: 1px solid var(--color-border-light);
  box-shadow: -6px 0 16px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.summary-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--color-text-primary);
  letter-spacing: 0.2px;
}

.summary-body {
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  margin: 0 0 0px 0;
}

.summary-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.summary-name::after {
  content: "";
  display: block;
  width: 40px;
  height: 3px;
  background: var(--color-accent);
  margin-top: 6px;
  border-radius: 2px;
}

.summary-row {
  display: flex;
  margin-bottom: 8px;
}

.summary-label {
  width: 110px;
  font-weight: 500;
  color: var(--color-primary);
}

.summary-value {
  flex: 1;
}

.summary-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--color-border-light);
  display: flex;
  justify-content: center;
}

.detail-button {
  padding: 14px 28px;
  border-radius: 12px;
  border: none;
  background: #457999;
  color: white;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 4px 16px rgba(69, 121, 153, 0.4);
  transition: background 0.2s, box-shadow 0.2s;
  text-transform: capitalize;
}

.detail-button:disabled {
  background: #457999 !important;
  opacity: 0.5;
  color: white !important;
  cursor: not-allowed;
  box-shadow: none;
}

.detail-button:not(:disabled):hover {
  background: #3a6680;
  box-shadow: 0 6px 20px rgba(69, 121, 153, 0.5);
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
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0;
  padding: 0;
}

.icon {
  display: inline-block;
  margin: 5px;
  padding: 0;
}

/* ===============================
  responsive styles
  =============================== */

/* mobile header bar */
.mobile-header {
  display: none;
}

@media (max-width: 768px) {
  /* adjust main layout */
  .hotspot-search {
    flex-direction: column;
    padding-top: 0;
  }

  /* mobile header */
  .mobile-header {
    display: flex !important;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: var(--color-bg-page);
    border-bottom: 1px solid var(--color-border-light);
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .mobile-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    color: var(--color-text-primary);
  }

  #home-button-mobile {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #457999;
    border-radius: 8px;
    color: white;
    cursor: pointer;
  }

  /* hide desktop filters, show as drawer */
  .filters {
    padding-top: 60px;
    margin-left: 0;
  }

  .results {
    width: 100%;
    padding: 16px;
    padding-bottom: 80px;
  }

  /* cards single column */
  .cards-container {
    flex-direction: column;
  }

  .cards-container > * {
    width: 100%;
  }

  /* summary panel as slide-up sheet */
  .summary-panel {
    width: 100%;
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    max-height: 70vh;
    z-index: 999;
    transform: translateY(100%);
    transition: transform 0.3s ease;
    border-radius: 20px 20px 0 0;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
    border-left: none;
  }

  .summary-panel.open {
    transform: translateY(0);
  }

  /* sheet handle */
  .summary-panel::before {
    display: none;
  }

  /* sheet handle (drag indicator) */
  .sheet-handle {
    width: 40px;
    height: 4px;
    background: #ddd;
    border-radius: 2px;
    margin: 8px auto 4px;
  }

  /* sheet close button */
  .sheet-close-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 32px;
    height: 32px;
    border: none;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1001;
  }

  /* sheet backdrop */
  .sheet-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 998;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
  }

  .sheet-backdrop.open {
    opacity: 1;
    visibility: visible;
  }

  /* drawer close button */
  .drawer-close-btn {
    position: absolute;
    top: 70px;
    right: 16px;
    width: 36px;
    height: 36px;
    border: 1px solid var(--color-border-light);
    background: var(--color-bg-muted);
    color: var(--color-text-primary);
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }

  /* hide panel title on mobile (shown in header) */
  .panel-title {
    display: none;
  }

  /* filters card adjustments */
  .filters-card {
    margin-top: 60px;
  }

  /* mobile search bar */
  .mobile-search-bar {
    position: relative;
    padding: 12px 16px;
    background: var(--color-bg-page);
    border-bottom: 1px solid var(--color-border-light);
    z-index: 99;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .mobile-search-input {
    flex: 1;
    width: 100%;
    max-width: 100%;
    padding: 10px 14px;
    border: 1px solid var(--color-border-light);
    border-radius: 10px;
    font-size: 16px;
    background: var(--color-bg-panel);
    color: var(--color-text-primary);
  }

  .mobile-search-input::placeholder {
    color: var(--color-text-muted);
  }

  .mobile-search-input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 2px rgba(69, 121, 153, 0.2);
  }

  .mobile-search-clear {
    width: 32px;
    height: 32px;
    border: none;
    background: var(--color-bg-muted);
    color: var(--color-text-primary);
    border-radius: 50%;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    line-height: 1;
  }

  /* ensure active filters have breathing room from search bar */
  .bottom-loader {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0;
  }

  .bottom-loader img {
    width: 40px;
    height: auto;
  }

  /* centered loader for initial empty state */
  .initial-loader {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    width: 100%;
  }

  .initial-loader img {
    width: 80px;
    height: auto;
  }
}

/* centered loader for initial empty state - outside media query for global application */
.initial-loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.initial-loader img {
  width: 100px;
  height: auto;
}

@media (max-width: 768px) {
  .results-filters {
    margin-top: 32px;
    margin-bottom: 20px;
    padding: 0 4px;
    width: 100%;
    position: relative;
    z-index: 5;
  }

  /* compact cards on mobile */
  .cards-container > * {
    width: 100%;
  }

  /* mobile floating get report button */
  .mobile-get-report-fab {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    background: #457999;
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(69, 121, 153, 0.4);
    cursor: pointer;
    z-index: 95;
    animation: fab-pulse 2s infinite;
  }

  @keyframes fab-pulse {
    0%,
    100% {
      box-shadow: 0 4px 12px rgba(69, 121, 153, 0.4);
    }
    50% {
      box-shadow: 0 4px 20px rgba(69, 121, 153, 0.7);
    }
  }

  .mobile-get-report-fab:hover {
    background: #3a6680;
  }
}

/* ===============================
  Tablet/Medium screens (769px - 1198px)
  hide summary panel, show floating button, use grid layout
  =============================== */

@media (min-width: 769px) and (max-width: 1198px) {
  /* hide the summary panel */
  .summary-panel {
    display: none !important;
  }

  /* filters panel - consistent width */
  .filters {
    width: 240px;
    padding: 12px 10px;
  }

  .results {
    flex: 1;
    padding: 12px;
  }

  /* card grid - consistent 3 columns for all tablet sizes */
  .cards-container {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 10px;
    align-items: stretch;
  }

  .cards-container > * {
    width: 100% !important;
    height: 100%;
    min-height: 200px;
    box-sizing: border-box;
    flex: none !important; /* override any flex from default */
  }

  /* show floating get report button */
  .floating-get-report-btn {
    display: flex !important;
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 14px 28px;
    background: #457999;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(69, 121, 153, 0.4);
    cursor: pointer;
    z-index: 100;
    align-items: center;
    gap: 8px;
    text-transform: capitalize;
  }

  .floating-get-report-btn:hover {
    background: #3a6680;
    box-shadow: 0 6px 20px rgba(69, 121, 153, 0.5);
  }
}

/* larger screens (1199px+) - hide floating button, show summary panel */
@media (min-width: 1199px) {
  .floating-get-report-btn {
    display: none !important;
  }
}

/* mobile (below 769px) - floating button centered at bottom */
@media (max-width: 768px) {
  .floating-get-report-btn {
    display: none !important; /* hidden on mobile, handled by dock */
  }
}

/* default: hide floating button on desktop */
.floating-get-report-btn {
  display: none;
}

/* mobile drawer styles (scoped) */
.nav-left {
  display: none;
}

@media (max-width: 768px) {
  .nav-left.mobile-open {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: auto;
    bottom: 72px;
    left: 0;
    right: 0;
    background: var(--color-bg-panel);
    padding: 16px;
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.15);
    z-index: 99;
    border-top: 1px solid var(--color-border-light);
    border-radius: 16px 16px 0 0;
    max-height: 50vh;
  }

  .nav-item {
    padding: 12px;
    font-size: 1.2rem;
    border: none;
    background: transparent;
    text-align: left;
    color: var(--color-text-primary);
    cursor: pointer;
  }

  .nav-item:hover {
    background: var(--color-bg-muted);
    border-radius: 8px;
  }
}

/* filter toggle button (new) */
@media (max-width: 768px) {
  .filter-toggle-btn {
    width: 44px;
    height: 44px;
    background: var(--color-bg-panel);
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--color-border-light);
    display: flex !important; /* Only on mobile */
    align-items: center;
    justify-content: center;
    padding: 0;
    margin-right: 8px;
  }

  .mobile-search-bar {
    display: flex !important;
    align-items: center;
  }

  .mobile-search-input.compact {
    padding-left: 16px;
    padding-right: 30px;
  }
}

.btn-disabled {
  background-color: #457999 !important;
  opacity: 0.5;
  color: white !important;
  cursor: not-allowed;
  pointer-events: none;
}

/* mobile bottom navigation styles */
@media (max-width: 768px) {
  .carousel-nav-bar.mobile-only {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 72px;
    background: var(--color-bg-panel);
    border-top: 1px solid var(--color-border-light);
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    z-index: 1000;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  }

  /* get report button specific tweaks */
  .nav-btn.primary-action {
    background-color: #457999;
    color: white;
    border-radius: 6px;
    padding: 0 16px;
    height: 44px;
    font-size: 16px;
    font-weight: 500;
    text-transform: capitalize;
    flex: none;
    width: auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .nav-btn.primary-action.btn-disabled {
    background-color: #457999;
    opacity: 0.5;
    color: white;
    cursor: not-allowed;
    box-shadow: none;
  }
}

/* utility to hide mobile nav on desktop */
@media (min-width: 769px) {
  .mobile-only {
    display: none !important;
  }
}
</style>
