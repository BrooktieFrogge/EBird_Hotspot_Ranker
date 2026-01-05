<template>
  <div class="analytics-config-panel" @scroll="checkScrollPosition" ref="panel">
    <!--------------------------->
    <!----- YEAR SELECTION ------>
    <!--------------------------->
    <div class="config-section year-section">
      <h4 class="unified-config-header">Select Year Range</h4>

      <div class="unified-time-container unified-inputs-container">
        <div class="year-inputs-row">
          <v-text-field
            v-model.number="tempStartYear"
            density="compact"
            style="width: 100px"
            type="number"
            variant="outlined"
            hide-details
            single-line
            :min="minYear"
            :max="tempEndYear"
          ></v-text-field>

          <span class="to-text">to</span>

          <v-text-field
            v-model.number="tempEndYear"
            density="compact"
            style="width: 100px"
            type="number"
            variant="outlined"
            hide-details
            single-line
            :min="tempStartYear"
            :max="currentYear"
          ></v-text-field>
        </div>

        <!--- Confirmation --->
        <div class="confirm-btn-wrapper">
          <v-btn
            color="#296239"
            @click="confirmYearRange"
            :disabled="!isYearRangeValid"
            size="small"
            class="confirm-btn"
            elevation="2"
          >
            Confirm Years
          </v-btn>
        </div>
      </div>
    </div>

    <!--------------------------->
    <!----- TIME SELECTION ------>
    <!--------------------------->
    <div class="config-section">
      <h4 class="unified-config-header">Select Time Frame</h4>

      <!-- unified time container -->
      <div class="unified-time-container">
        <!-- seasonal presets selector -->
        <div class="preset-selector-row">
          <v-select
            v-model="selectedPreset"
            :items="presetOptions"
            variant="outlined"
            density="compact"
            hide-details
            class="preset-dropdown"
            @update:model-value="applyPreset"
          ></v-select>
        </div>

        <!-- single header for both blocks -->
        <div class="container-header">
          <span class="header-main">Checklists per Week</span>
          <span class="header-sub">(Click bars to select)</span>
        </div>

        <!-- start time block -->
        <div class="time-block-minimal">
          <div class="block-label">Start Time</div>
          <v-select
            v-model="startMonth"
            :items="monthOptions"
            label="Month"
            variant="outlined"
            density="compact"
            hide-details
            class="dropdown-minimal"
            @update:model-value="onMonthChange"
          ></v-select>
          <div class="weeks-row-max">
            <div
              v-for="week in weeksInStartMonth"
              :key="'start-week-' + week.value"
              class="week-bar-wrapper-max"
              @click="selectStartWeek(week.value)"
            >
              <div class="week-bar-density">{{ week.density }}</div>
              <div
                :class="[
                  'week-bar-max',
                  { 'week-bar-selected': startWeek === week.value },
                ]"
                :style="{ height: week.height }"
              ></div>
              <div class="week-bar-text">{{ week.label }}</div>
            </div>
          </div>
          <span class="click-subtext-mobile">(Click bar to select)</span>
        </div>

        <!-- divider -->
        <div class="time-divider"></div>

        <!-- end time block -->
        <div class="time-block-minimal">
          <div class="block-label">End Time</div>
          <v-select
            v-model="endMonth"
            :items="monthOptions"
            label="Month"
            variant="outlined"
            density="compact"
            hide-details
            class="dropdown-minimal"
            @update:model-value="onMonthChange"
          ></v-select>
          <div class="weeks-row-max">
            <div
              v-for="week in weeksInEndMonth"
              :key="'end-week-' + week.value"
              class="week-bar-wrapper-max"
              @click="selectEndWeek(week.value)"
            >
              <div class="week-bar-density">{{ week.density }}</div>
              <div
                :class="[
                  'week-bar-max',
                  { 'week-bar-selected': endWeek === week.value },
                ]"
                :style="{ height: week.height }"
              ></div>
              <div class="week-bar-text">{{ week.label }}</div>
            </div>
          </div>
          <span class="click-subtext-mobile">(Click bar to select)</span>
        </div>
      </div>

      <!-- data distribution graph -->
      <h4 class="unified-config-header">Data Density</h4>

      <!-- graph inside unified container -->
      <div class="unified-time-container graph-container">
        <h5 v-if="!analyticsStore.selectedHotspot" class="empty-graph-label">
          Select Hotspot to View Data
        </h5>
        <!-- graph itself -->
        <DataDistributionGraph />
      </div>
    </div>

    <!--------------------------->
    <!--- PICK # OF TOP BIRDS --->
    <!----------------------------->
    <!--------------------------->
    <!--- PICK # OF TOP BIRDS --->
    <!----------------------------->
    <div class="config-section">
      <h4 class="unified-config-header">Display Counts</h4>
      <div class="unified-time-container top-counts-container">
        <!-- show top birds row -->
        <div class="top-count-row">
          <span class="config-text">Show top</span>
          <v-text-field
            v-model.number="analyticsStore.numTopBirds"
            density="compact"
            class="top-count-input"
            type="number"
            variant="outlined"
            hide-details
            single-line
            :min="1"
            :max="allBirds.length || 10"
          ></v-text-field>
          <span class="config-text">birds</span>
        </div>

        <!-- show top photos row -->
        <div class="top-count-row">
          <span class="config-text">Show top</span>
          <v-text-field
            v-model.number="analyticsStore.numTopPhotos"
            density="compact"
            class="top-count-input"
            type="number"
            variant="outlined"
            hide-details
            single-line
            :min="1"
            :max="analyticsStore.numTopBirds"
          ></v-text-field>
          <span class="config-text">photos</span>
        </div>
      </div>
    </div>

    <!--------------------------->
    <!------ CUSTOM BIRDS ------->
    <!--------------------------->
    <div class="config-section">
      <h4 class="unified-config-header">Add Custom Birds</h4>
      <div class="unified-time-container" style="padding: 12px 16px">
        <div class="search-container">
          <v-text-field
            v-model="birdSearch"
            variant="outlined"
            placeholder="Search birds..."
            label=""
            hide-details
            clearable
            density="compact"
            @input="filterBirds"
            @blur="handleSearchBlur"
            @click:clear="clearSearch"
          />

          <div
            v-if="filteredBirds.length > 0 && birdSearch.length > 0"
            class="search-results"
          >
            <div
              v-for="bird in filteredBirds"
              :key="bird.Species"
              class="search-result-item"
              @mousedown.prevent="selectBird(bird)"
            >
              <div style="font-weight: 500">{{ bird.Species }}</div>
              <div class="search-result-subtext">
                #{{ bird.Rank }} · Likelihood
                {{ Math.round(bird.wtd_rf * 100) / 100 }} · Normalized
                {{ Math.round(bird.rfpc * 10) / 10 }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--------------------------->
    <!------ TOGGLES ------->
    <!--------------------------->
    <div class="config-section">
      <h4 class="unified-config-header">Display Options</h4>
      <div class="unified-time-container" style="padding: 8px 16px">
        <div class="toggle-container">
          <v-switch
            color="#296239"
            base-color="grey-lighten-1"
            label="Show Likelihood Curve"
            hide-details
            @change="handleGraphToggle"
            :model-value="showGraph"
          ></v-switch>
          <v-switch
            color="#296239"
            base-color="grey-lighten-1"
            label="Show photos of top 3 birds"
            @change="handlePhotosToggle"
            hide-details
            :model-value="showTopPhotos"
            style="margin-top: -8px"
          ></v-switch>
        </div>
      </div>
    </div>
    <!---- scroll indicator ----->
    <div v-if="showScrollIndicator" class="scroll-indicator">
      <BIconArrowDown />
    </div>
  </div>
</template>

<style scoped>
/* centered header style */
.centered-header {
  text-align: center;
  width: 100%;
  margin-bottom: 16px;
  position: relative;
}

.empty-graph-label,
.graph-label {
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.85rem;
  margin-bottom: 8px;
  font-weight: 500;
}

/* custom input styling for dark mode */
:deep(.v-field__outline) {
  --v-field-border-opacity: 0.15;
}

/* on hover, slightly more visible */
:deep(.v-field:hover .v-field__outline) {
  --v-field-border-opacity: 0.3;
}

/* focused state - use primary color but keep it clean */
:deep(.v-field--focused .v-field__outline) {
  --v-field-border-opacity: 0.5;
}

:deep(.v-field) {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.time-section-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 24px;
}

.time-section-box h5 {
  width: 100%;
  text-align: center;
}
:deep(.v-switch .v-selection-control__input input:checked + .v-switch__track) {
  background-color: #2196f3 !important; /* Active Blue */
  opacity: 1 !important;
}

:deep(.v-switch .v-selection-control__input input:checked ~ .v-switch__thumb) {
  color: #2196f3 !important;
}

:deep(
    .v-switch .v-selection-control__input input:not(:checked) + .v-switch__track
  ) {
  background-color: #90ee90 !important;
  opacity: 1 !important;
}

:deep(
    .v-switch .v-selection-control__input input:not(:checked) ~ .v-switch__thumb
  ) {
  color: #fff !important;
}
</style>

<script lang="ts">
import { computed, defineComponent, ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import {
  BIconHouseFill,
  BIconArrowLeft,
  BIconArrowDown,
} from "bootstrap-icons-vue";
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import type { Bird } from "../types";
import DataDistributionGraph from "../components/DataDistributionGraph.vue";
import "bootstrap-icons/font/bootstrap-icons.css";

/**
 * A panel for configurating the analytics report.
 * It includes functionality for date range, etc. (has yet to be completed).
 * The panel allows users to ...
 */
export default defineComponent({
  name: "AnalyticsConfigPanel",

  components: {
    BIconHouseFill,
    BIconArrowLeft,
    BIconArrowDown,
    DataDistributionGraph,
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();

    // SCROLL LOGIC STATE
    const panel = ref<HTMLElement | null>(null);
    const showScrollIndicator = ref(false); // Default to false

    // --- YEAR SELECTION LOGIC ---
    const currentYear = new Date().getFullYear();
    const minYear = 1900; // eBird's historical minimum

    const tempStartYear = ref(analyticsStore.startYear);
    const tempEndYear = ref(analyticsStore.endYear);

    const isYearRangeValid = computed(() => {
      const start = tempStartYear.value;
      const end = tempEndYear.value;

      return start <= end && start >= minYear && end <= currentYear;
    });

    const confirmYearRange = () => {
      if (isYearRangeValid.value) {
        analyticsStore.setYearRange(tempStartYear.value, tempEndYear.value);
        analyticsStore.fetchHotspotDetail();
        console.log(
          `Confirmed year range: ${tempStartYear.value} to ${tempEndYear.value}`
        );
      } else {
        console.error("Invalid year range entered.");
      }
    };

    // --- MONTH/WEEK SELECTION DATA ---

    const monthOptions = [
      { title: "January", value: 1 },
      { title: "February", value: 2 },
      { title: "March", value: 3 },
      { title: "April", value: 4 },
      { title: "May", value: 5 },
      { title: "June", value: 6 },
      { title: "July", value: 7 },
      { title: "August", value: 8 },
      { title: "September", value: 9 },
      { title: "October", value: 10 },
      { title: "November", value: 11 },
      { title: "December", value: 12 },
    ];

    const startMonth = ref(1);
    const endMonth = ref(12);

    const startWeek = ref(1);
    const endWeek = ref(4);

    // watch for external changes to store values (e.g., from slider)
    // and sync local refs to match
    watch(
      () => analyticsStore.startMonth,
      (newVal) => {
        if (newVal && newVal !== startMonth.value) startMonth.value = newVal;
      }
    );
    watch(
      () => analyticsStore.startWeek,
      (newVal) => {
        if (newVal && newVal !== startWeek.value) startWeek.value = newVal;
      }
    );
    watch(
      () => analyticsStore.endMonth,
      (newVal) => {
        if (newVal && newVal !== endMonth.value) endMonth.value = newVal;
      }
    );
    watch(
      () => analyticsStore.endWeek,
      (newVal) => {
        if (newVal && newVal !== endWeek.value) endWeek.value = newVal;
      }
    );

    // --- SEASONAL PRESETS ---
    const SEASONAL_PRESETS = {
      year: {
        label: "Entire Year (Jan-Dec)",
        startMonth: 1,
        startWeek: 1,
        endMonth: 12,
        endWeek: 4,
      },
      spring: {
        label: "Spring Migration (Mar-May)",
        startMonth: 3,
        startWeek: 1,
        endMonth: 5,
        endWeek: 4,
      },
      breeding: {
        label: "Breeding Season (Jun-Jul)",
        startMonth: 6,
        startWeek: 1,
        endMonth: 7,
        endWeek: 4,
      },
      fall: {
        label: "Fall Migration (Aug-Nov)",
        startMonth: 8,
        startWeek: 1,
        endMonth: 11,
        endWeek: 4,
      },
      winter: {
        label: "Winter (Dec-Feb)",
        startMonth: 12,
        startWeek: 1,
        endMonth: 2,
        endWeek: 4,
      },
      custom: {
        label: "Custom",
        startMonth: null,
        startWeek: null,
        endMonth: null,
        endWeek: null,
      },
    };

    const presetOptions = Object.entries(SEASONAL_PRESETS).map(
      ([key, val]) => ({
        title: val.label,
        value: key,
      })
    );

    const selectedPreset = ref("year");

    const applyPreset = (presetKey: string) => {
      selectedPreset.value = presetKey;
      const preset =
        SEASONAL_PRESETS[presetKey as keyof typeof SEASONAL_PRESETS];
      if (preset && preset.startMonth !== null) {
        let sM = preset.startMonth;
        let sW = preset.startWeek!;
        let eM = preset.endMonth!;
        let eW = preset.endWeek!;

        // check if start > end (ex. winter: dec -> feb)
        // swap to avoid slider break (feb -> dec)
        if (sM > eM) {
          const tempM = sM;
          const tempW = sW;
          sM = eM;
          sW = eW;
          eM = tempM;
          eW = tempW;
        }

        startMonth.value = sM;
        startWeek.value = sW;
        endMonth.value = eM;
        endWeek.value = eW;
        // sync with store
        analyticsStore.startMonth = sM;
        analyticsStore.startWeek = sW;
        analyticsStore.endMonth = eM;
        analyticsStore.endWeek = eW;
        debouncedFetchHotspot();
      }
    };

    const startWeekDataDensity = computed(() => {
      // find selected month title
      const selectedMonthOption = monthOptions.find(
        (m) => m.value === startMonth.value
      );
      if (
        !selectedMonthOption ||
        !analyticsStore.selectedHotspot?.sample_sizes_by_week
      ) {
        return [];
      }

      // Set month
      analyticsStore.startMonth = startMonth.value;

      // Get three-letter abbreviation
      const monthAbbrev = selectedMonthOption.title.substring(0, 3);
      const densityData = analyticsStore.selectedHotspot.sample_sizes_by_week;

      // populate list + loop through weeks in month
      const result: { label: string; value: number; density: number }[] = [];
      for (let i = 1; i <= 4; i++) {
        const wkIndex = `${monthAbbrev}_w${i}`;
        const density = densityData[wkIndex] ?? 0;
        result.push({
          label: `Wk ${i}`,
          value: i,
          density: density,
        });
      }
      return result;
    });

    //For formatting, keeps the bars below a max height and computed relative to max data
    const maxDensity = computed(() => {
      const densityData = analyticsStore.selectedHotspot?.sample_sizes_by_week;

      if (!densityData || Object.keys(densityData).length === 0) {
        return 1;
      }
      const values = Object.values(densityData) as number[];

      return Math.max(...values, 1);
    });

    const endWeekDataDensity = computed(() => {
      // find selected month title
      const selectedMonthOption = monthOptions.find(
        (m) => m.value === endMonth.value
      );
      if (
        !selectedMonthOption ||
        !analyticsStore.selectedHotspot?.sample_sizes_by_week
      ) {
        return [];
      }

      // Set month
      analyticsStore.endMonth = endMonth.value;

      // Get three-letter abbreviation
      const monthAbbrev = selectedMonthOption.title.substring(0, 3);
      const densityData = analyticsStore.selectedHotspot.sample_sizes_by_week;

      // populate list + loop through weeks in month
      const result: { label: string; value: number; density: number }[] = [];
      for (let i = 1; i <= 4; i++) {
        const wkIndex = `${monthAbbrev}_w${i}`;
        const density = densityData[wkIndex] ?? 0;
        result.push({
          label: `Wk ${i}`,
          value: i,
          density: density,
        });
      }
      return result;
    });

    const weeksInStartMonth = computed(() => {
      const maxD = maxDensity.value;
      return startWeekDataDensity.value.map((week) => {
        // calculate percentage (min 10% to show bar even if empty/low)
        const percent = maxD > 0 ? (week.density / maxD) * 100 : 0;
        const safePercent = Math.max(10, percent);

        return {
          ...week,
          height: `${safePercent}%`,
        };
      });
    });

    const weeksInEndMonth = computed(() => {
      const maxD = maxDensity.value;
      return endWeekDataDensity.value.map((week) => {
        const percent = maxD > 0 ? (week.density / maxD) * 100 : 0;
        const safePercent = Math.max(10, percent);

        return {
          ...week,
          height: `${safePercent}%`,
        };
      });
    });

    // debounce timer for auto-fetch
    let fetchDebounceTimer: ReturnType<typeof setTimeout> | null = null;

    const debouncedFetchHotspot = () => {
      // clear existing timer
      if (fetchDebounceTimer) {
        clearTimeout(fetchDebounceTimer);
      }
      // set new timer - fetch after 300ms
      fetchDebounceTimer = setTimeout(() => {
        console.log(
          `[auto-fetch] Time changed: ${startMonth.value}/${startWeek.value} to ${endMonth.value}/${endWeek.value}`
        );
        analyticsStore.fetchHotspotDetail();
      }, 300);
    };

    const selectStartWeek = (weekNumber: number) => {
      startWeek.value = weekNumber;
      analyticsStore.startWeek = startWeek.value;
      selectedPreset.value = "custom"; // Switch to custom on manual change
      debouncedFetchHotspot(); // Auto-fetch with debounce
    };

    const selectEndWeek = (weekNumber: number) => {
      endWeek.value = weekNumber;
      analyticsStore.endWeek = endWeek.value;
      selectedPreset.value = "custom"; // Switch to custom on manual change
      debouncedFetchHotspot(); // auto-fetch with debounce
    };

    // keep manual trigger if we need it later
    const confirmTimeRange = () => {
      if (fetchDebounceTimer) clearTimeout(fetchDebounceTimer);
      analyticsStore.fetchHotspotDetail();
      console.log(
        `Manual confirm: ${startMonth.value}/${startWeek.value} to ${endMonth.value}/${endWeek.value}`
      );
    };

    // handler for month dropdown changes - triggers debounced fetch
    const onMonthChange = () => {
      selectedPreset.value = "custom"; // Switch to custom on manual change
      debouncedFetchHotspot();
    };

    // --- SCROLL LOGIC FUNCTIONS ---
    const checkScrollPosition = () => {
      if (!panel.value) return;

      const { scrollTop, clientHeight, scrollHeight } = panel.value;

      // Check if content overflows/not near bottom
      const hasOverflow = scrollHeight > clientHeight;
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 5;

      showScrollIndicator.value = hasOverflow && !isNearBottom;
    };

    onMounted(() => {
      setTimeout(checkScrollPosition, 100); // for checking the scroll position
    });

    // --- OTHER LOGIC (UNCHANGED) ---
    const birdSearch = ref("");
    const allBirds = computed(() => analyticsStore.getAllBirds);
    const filteredBirds = ref<Bird[]>([]);

    const filterBirds = () => {
      const q = birdSearch.value.toLowerCase();
      filteredBirds.value = allBirds.value.filter((bird) =>
        bird.Species.toLowerCase().includes(q)
      );
    };

    const selectBird = (bird: Bird) => {
      analyticsStore.selectBird(bird);
      birdSearch.value = ""; // clear search to allow quick addition of more birds
      filteredBirds.value = [];
    };

    const handleSearchBlur = () => {
      // Delay to allow click on search result to register
      setTimeout(() => {
        filteredBirds.value = [];
      }, 150);
    };

    const clearSearch = () => {
      birdSearch.value = "";
      filteredBirds.value = [];
    };

    const redirectToHomeScreen = () => {
      analyticsStore.resetAnalyticsConfiguration();
      analyticsStore.resetSelectedHotspot();
      router.push({ name: "HomeScreen" });
    };

    const redirectToHotspotSearch = () => {
      analyticsStore.resetAnalyticsConfiguration();
      router.push({ name: "HotspotSearch" });
    };

    const showGraph = analyticsStore.showLikelihoodCurve;

    const handleGraphToggle = () => {
      analyticsStore.toggleLikelihoodCurve();
    };

    const showTopPhotos = analyticsStore.showTopBirdPhotos;

    const handlePhotosToggle = () => {
      analyticsStore.toggleTopPhotos();
    };

    // Export Report as PDF
    const isExporting = ref(false);

    const exportReport = async () => {
      if (!analyticsStore.selectedHotspotId || isExporting.value) return;

      isExporting.value = true;

      try {
        // Build URL for PDF endpoint with current config
        const params = new URLSearchParams({
          num_top_birds: analyticsStore.numTopBirds.toString(),
          num_top_photos: analyticsStore.numTopPhotos.toString(),
          show_graph: analyticsStore.showLikelihoodCurve.toString(),
          show_photos: analyticsStore.showTopBirdPhotos.toString(),
        });

        if (analyticsStore.startYear)
          params.append("start_yr", analyticsStore.startYear.toString());
        if (analyticsStore.endYear)
          params.append("end_yr", analyticsStore.endYear.toString());
        if (analyticsStore.startMonth)
          params.append("start_month", analyticsStore.startMonth.toString());
        if (analyticsStore.startWeek)
          params.append("start_week", analyticsStore.startWeek.toString());
        if (analyticsStore.endMonth)
          params.append("end_month", analyticsStore.endMonth.toString());
        if (analyticsStore.endWeek)
          params.append("end_week", analyticsStore.endWeek.toString());

        // Pass custom bird ranks only (much shorter than full objects)
        if (analyticsStore.selectedBirds.length > 0) {
          const ranks = analyticsStore.selectedBirds.map((b) => b.Rank);
          params.append("custom_ranks", ranks.join(","));
        }
        if (analyticsStore.selectedBirdPhotos.length > 0) {
          const photoRanks = analyticsStore.selectedBirdPhotos.map(
            (b) => b.Rank
          );
          params.append("photo_ranks", photoRanks.join(","));
        }

        // Pass the current date from client (correct timezone)
        const today = new Date().toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
        params.append("gen_date", today);

        const pdfUrl = `/api/hotspots/report/${
          analyticsStore.selectedHotspotId
        }/pdf?${params.toString()}`;

        // Open PDF in new tab - browser will show print dialog or PDF viewer
        window.open(pdfUrl, "_blank");
      } catch (error) {
        console.error("Export failed:", error);
        alert("Failed to generate PDF. Please try again.");
      } finally {
        isExporting.value = false;
      }
    };

    return {
      redirectToHomeScreen,
      redirectToHotspotSearch,
      // Year Logic
      tempStartYear,
      tempEndYear,
      isYearRangeValid,
      confirmYearRange,
      currentYear,
      minYear,
      // Month/Week Logic
      monthOptions,
      startMonth,
      endMonth,
      weeksInStartMonth,
      weeksInEndMonth,
      startWeek,
      endWeek,
      selectStartWeek,
      selectEndWeek,
      confirmTimeRange,
      onMonthChange,
      // Presets
      selectedPreset,
      presetOptions,
      applyPreset,
      // Scroll Logic
      panel,
      showScrollIndicator,
      checkScrollPosition,
      // Other Logic
      birdSearch,
      allBirds,
      filteredBirds,
      filterBirds,
      selectBird,
      handleSearchBlur,
      clearSearch,
      showGraph,
      handleGraphToggle,
      showTopPhotos,
      handlePhotosToggle,
      analyticsStore,
      exportReport,
      isExporting,
    };
  },
});
</script>

<style scoped>
.analytics-config-panel {
  padding: clamp(12px, 2vw, 20px) clamp(12px, 2vw, 20px) 80px
    clamp(12px, 2vw, 20px);
  background: var(--color-bg-seamless);
  border-right: 1px solid var(--color-border-light);

  height: 100vh;
  overflow-y: auto;
  position: relative;

  box-sizing: border-box;
}

:deep(.v-field__outline__notch) {
  display: none !important;
}
:deep(.v-field__outline__start) {
  border-radius: 8px 0 0 8px !important;
}
:deep(.v-field__outline__end) {
  border-radius: 0 8px 8px 0 !important;
}
:deep(.v-label.v-field-label--floating) {
  display: none !important;
}

.scroll-indicator {
  position: sticky;
  bottom: 0px;
  left: 0;
  right: 0;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 1.2em;
  pointer-events: none;
  opacity: 0.6;
}

/* --- YEAR SECTION STYLES --- */
.year-section {
  padding-top: clamp(4px, 1vw, 10px);
  padding-bottom: clamp(12px, 2vw, 24px);
}

.config-section.year-section h4 {
  margin-bottom: 14px;
}

.year-inputs-row {
  display: flex;
  gap: clamp(12px, 2vw, 16px);
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  width: 100%;
}

.confirm-btn-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 0;
  padding-bottom: clamp(8px, 1.5vw, 16px);
}

.confirm-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  color: white !important;
  background-color: #296239 !important;
  border: 1px solid #296239 !important;
  transition: all 0.3s ease;
}

.confirm-btn:hover {
  background-color: white !important;
  color: #296239 !important;
  border-color: #296239 !important;
}

.confirm-btn:hover :deep(.v-btn__content),
.confirm-btn:hover :deep(.v-btn__overlay) {
  color: #296239 !important;
}

.confirm-btn :deep(.v-btn__overlay) {
  opacity: 0 !important;
}

.unified-config-header {
  font-size: clamp(12px, 1.5vw, 15px);
  font-weight: 600;
  margin-bottom: 8px; /* strict separation from container */
  margin-top: 24px; /* strict separation from previous section */
  color: var(--color-text-primary) !important;
  text-align: center;
  position: relative;
}

/* first header shouldn't have top margin */
.year-section .unified-config-header {
  margin-top: 0;
}

.unified-inputs-container {
  padding: 20px 16px !important;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* keep previous rule for safety/specificity but renamed targets */
.config-section h5 {
  font-size: clamp(12px, 1.5vw, 15px);
  font-weight: 600;
  margin-bottom: clamp(6px, 1vw, 12px);
  color: var(--color-text-primary) !important;
}

.to-text {
  font-weight: 600;
  font-size: 0.9rem;
  margin: 0 4px;
  color: var(--color-text-primary) !important;
}

.config-text {
  font-weight: 500;
  font-size: 0.9rem;
  color: var(--color-text-primary) !important;
}

/* --- TOP COUNTS CONTAINER (Birds + Photos) --- */
.top-counts-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 20px;
}

.top-count-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.top-count-input {
  width: 80px;
  flex: none;
}

/* Responsive adjustments for smaller screens */
@media (max-width: 480px) {
  .top-counts-container {
    gap: 12px;
    padding: 12px 16px;
  }

  .top-count-row {
    gap: 8px;
  }

  .top-count-input {
    width: 70px;
  }
}

:global(body.theme--dark) .top-counts-container {
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

/* --- PRESET SELECTOR --- */
.preset-selector-row {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border-light);
}

.preset-dropdown {
  width: 100%;
  max-width: 280px;
}

.preset-dropdown :deep(.v-field__input) {
  justify-content: center;
  text-align: center;
  font-size: 0.85rem;
  padding-top: 6px;
  padding-bottom: 6px;
}

.preset-dropdown :deep(.v-select__selection) {
  justify-content: center;
  width: 100%;
}

.preset-dropdown :deep(.v-field) {
  border-radius: 8px;
}

/* responsive adjustments */
@media (max-width: 480px) {
  .preset-dropdown {
    max-width: 100%;
  }

  .preset-selector-row {
    margin-bottom: 8px;
    padding-bottom: 8px;
  }
}

/* --- UNIFIED TIME CONTAINER --- */
.unified-time-container {
  background: var(--color-bg-muted);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

:global(body.theme--dark) .unified-time-container {
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

/* container header - shows once */
.container-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  width: 100%;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border-light);
}

.header-main {
  font-size: clamp(0.8rem, 1.3vw, 0.95rem);
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-sub {
  font-size: clamp(0.6rem, 1vw, 0.75rem);
  font-weight: 400;
  color: var(--color-text-muted);
}

/* mobile-only subtext (hidden by default) */
.click-subtext-mobile {
  display: none;
  font-size: 0.6rem;
  color: var(--color-text-muted);
  text-align: center;
  margin-top: 4px;
}

/* time block - minimal */
.time-block-minimal {
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto 1fr;
  gap: 8px 16px;
  width: 100%;
  align-items: start;
}

.block-label {
  grid-column: 1;
  grid-row: 1;
  font-size: clamp(0.75rem, 1.2vw, 0.9rem);
  font-weight: 600;
  color: var(--color-text-primary);
  align-self: center;
}

.dropdown-minimal {
  grid-column: 1;
  grid-row: 2;
  width: clamp(100px, 100%, 140px);
  align-self: start;
}

/* center text in dropdowns */
.dropdown-minimal :deep(.v-field__input) {
  justify-content: center;
  text-align: center;
}

.dropdown-minimal :deep(.v-select__selection) {
  justify-content: center;
  width: 100%;
}

/* bars - take maximum remaining space */
.weeks-row-max {
  grid-column: 2;
  grid-row: 1 / 3; /* span both rows */
  display: flex;
  justify-content: center;
  gap: clamp(6px, 1.5vw, 12px);
  height: clamp(100px, 20vh, 160px);
  align-items: flex-end;
  width: 100%;
}

.week-bar-wrapper-max {
  flex: 1;
  max-width: 55px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.15s ease;
  border-radius: 5px;
  padding: 3px 2px;
}

.week-bar-wrapper-max:hover {
  background-color: rgba(69, 121, 153, 0.15);
}

.week-bar-density {
  font-size: clamp(9px, 1vw, 11px);
  color: var(--color-text-muted);
  margin-bottom: 2px;
  font-weight: 500;
}

.week-bar-max {
  width: 70%;
  min-height: 4px;
  background-color: #4a7d99;
  border-radius: 5px;
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

body.theme--dark .week-bar-max {
  background-color: #8eb5cc;
}

.week-bar-selected {
  background-color: #2f5b7a !important;
  box-shadow: 0 0 12px rgba(47, 91, 122, 0.7), 0 0 4px rgba(255, 255, 255, 0.3);
  transform: scaleY(1.08);
}

/* Dark mode selected bar - brighter for visibility */
:global(body.theme--dark) .week-bar-selected {
  background-color: #5a9bc0 !important;
  box-shadow: 0 0 14px rgba(90, 155, 192, 0.8), 0 0 4px rgba(255, 255, 255, 0.4);
}

.week-bar-text {
  font-size: clamp(9px, 1vw, 11px);
  margin-top: 3px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.time-divider {
  height: 1px;
  background: var(--color-border-light);
  margin: 12px 0;
  width: 100%;
}

/* --- SEARCH DROPDOWN STYLES --- */
.search-container {
  position: relative;
  width: 100%;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 220px;
  overflow-y: auto;
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border-light);
  border-radius: 0 0 8px 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
  margin-top: 4px;
}

.search-result-item {
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid var(--color-border-light);
  transition: background-color 0.15s ease;
  text-align: left; /* Left align results */
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.search-result-item div:first-child {
  color: #457999; /* light mode blue */
  font-weight: 600;
}

body.theme--dark .search-result-item div:first-child {
  color: #7eb8d9; /* Dark mode blue */
}

.search-result-subtext {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 2px;
}

body.theme--dark .search-results {
  background: #252525;
  border-color: #444;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

body.theme--dark .search-result-item:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

/* --- DESKTOP (>1330px) --- */
@media (min-width: 1331px) {
  .container-header {
    flex-direction: column;
    align-items: center;
    gap: 4px;
    margin-bottom: 14px;
  }

  .header-sub {
    display: none;
  }

  .click-subtext-mobile {
    display: block;
  }

  .time-block-minimal {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .block-label {
    font-size: 1rem;
    text-align: center;
  }

  .dropdown-minimal {
    width: clamp(140px, 60%, 200px);
    align-self: center;
  }

  .weeks-row-max {
    height: clamp(120px, 22vh, 180px);
    gap: 16px;
  }

  .week-bar-wrapper-max {
    flex: 1;
    max-width: clamp(55px, 12vw, 80px);
  }

  .week-bar-max {
    width: 75%;
  }
}

/* --- RESPONSIVE (minimal layout) --- */

/* large tablet (768-1024px) */
@media (min-width: 768px) and (max-width: 1024px) {
  .container-header {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    margin-bottom: 10px;
  }

  .header-sub {
    display: none;
  }

  .click-subtext-mobile {
    display: block;
  }

  .time-block-minimal {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .block-label {
    text-align: center;
  }

  .dropdown-minimal {
    width: clamp(100px, 40%, 160px);
    align-self: center;
  }

  .weeks-row-max {
    height: clamp(80px, 15vh, 120px);
    gap: 10px;
  }

  .week-bar-wrapper-max {
    flex: 1;
    max-width: clamp(35px, 8vw, 50px);
  }
}

/* small desktop (1025-1330px) */
@media (min-width: 1025px) and (max-width: 1330px) {
  .container-header {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    margin-bottom: 12px;
  }

  .header-sub {
    display: none;
  }

  .click-subtext-mobile {
    display: block;
  }

  .time-block-minimal {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .block-label {
    text-align: center;
  }

  .dropdown-minimal {
    width: clamp(120px, 50%, 180px);
    align-self: center;
  }

  .weeks-row-max {
    height: clamp(100px, 18vh, 150px);
    gap: 12px;
  }

  .week-bar-wrapper-max {
    flex: 1;
    max-width: clamp(45px, 10vw, 60px);
  }
}

/* phablet (600-768px) */
@media (min-width: 600px) and (max-width: 767px) {
  .container-header {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    margin-bottom: 10px;
  }

  .header-sub {
    display: none;
  }

  .click-subtext-mobile {
    display: block;
  }

  .time-block-minimal {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .block-label {
    text-align: center;
  }

  .dropdown-minimal {
    width: 50%;
    max-width: 180px;
    align-self: center;
  }

  .weeks-row-max {
    height: clamp(100px, 22vh, 160px);
    gap: 12px;
  }

  .week-bar-wrapper-max {
    flex: 1;
    max-width: clamp(50px, 12vw, 70px);
  }
}

/* mobile */
@media (max-width: 599px) {
  .unified-time-container {
    padding: 12px 10px;
  }

  .container-header {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    margin-bottom: 10px;
  }

  .header-main {
    font-size: 0.85rem;
  }

  .header-sub {
    font-size: 0.6rem;
  }

  .time-block-minimal {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .block-label {
    font-size: 0.8rem;
    text-align: center;
  }

  .header-sub {
    display: none;
  }

  .click-subtext-mobile {
    display: block;
  }

  .dropdown-minimal {
    width: 60%;
    max-width: 160px;
    align-self: center;
  }

  .weeks-row-max {
    height: clamp(120px, 35vh, 200px);
    width: 100%;
    gap: 12px;
  }

  .week-bar-wrapper-max {
    flex: 1;
    max-width: clamp(50px, 12vw, 70px);
    padding: 4px 2px;
  }

  .week-bar-max {
    width: 75%;
    border-radius: 6px;
  }

  .week-bar-density {
    font-size: 10px;
  }

  .week-bar-text {
    font-size: 9px;
  }

  .time-divider {
    margin: 10px 0;
  }
}
</style>
