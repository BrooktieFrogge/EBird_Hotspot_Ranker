<template>
  <div class="analytics-config-panel" @scroll="checkScrollPosition" ref="panel">
    
    <!--------------------------->
    <!---- HOME/BACK BUTTONS ---->
    <!--------------------------->
    <div class="buttons-container">
      <div id="back-button" @click="redirectToHotspotSearch">
        <div class="button-wrapper">
          <BIconArrowLeft />
        </div>
      </div>

      <div id="home-button" @click="redirectToHomeScreen">
        <div class="button-wrapper">
          <BIconHouseFill />
        </div>
      </div>
    </div>


    <!--------------------------->
    <!----- YEAR SELECTION ------>
    <!--------------------------->
    <div class="config-section">
      <h4>Select Year Range</h4>

      <div style="display: flex; gap: 10px; align-items: center;">
        <v-text-field
          v-model.number="tempStartYear"
          density="compact"
          style="width: 100px;"
          type="number"
          variant="outlined"
          label="Start"
          hide-details
          single-line
          :min="minYear"
          :max="tempEndYear"
        ></v-text-field>

        <span style="font-weight: bold;">to</span>

        <v-text-field
          v-model.number="tempEndYear"
          density="compact"
          style="width: 100px"
          type="number"
          variant="outlined"
          label="End"
          hide-details
          single-line
          :min="tempStartYear"
          :max="currentYear"
        ></v-text-field>
      </div>
      
      <!--- Confirmation --->
      <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
        <v-btn
          color="#296239"
          @click="confirmYearRange"
          :disabled="!isYearRangeValid"
          size="small"
        >
          Confirm Years
        </v-btn>
      </div>
    </div>


    <!--------------------------->
    <!----- TIME SELECTION ------>
    <!--------------------------->
    <div class="config-section">
      <h4>Select Time Frame</h4>
      
      <!-- FIRST MONTH/WEEK -->
      <div style="background: #f5f5f5; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
        <h5 style="margin-bottom: 8px;">Start Time</h5>
        
        <v-select
          v-model="startMonth"
          :items="monthOptions"
          label="Month"
          variant="outlined"
          density="compact"
          hide-details
          style="width: 125px; margin-bottom: 10px;"
          @update:model-value="onMonthChange"
        ></v-select>

        <div style="margin-top: 10px;">
          <h5 style="margin-bottom: 5px;">Checklists per Week</h5>
          <p style="font-size: 11px; color: #777; margin: 0 0 8px 0;">Click a bar to select start week</p>
          
          <div style="display: flex; gap: 4px; align-items: flex-end; height: 100%; padding: 5px 0;">
            <div
              v-for="week in weeksInStartMonth"
              :key="'start-week-' + week.value"
              class="week-bar-container"
              :style="{ height: week.height, cursor: 'pointer' }"
              @click="selectStartWeek(week.value)"
            >
              <div class="week-bar-label">{{ week.density }}</div>
              <div
                :class="['week-bar', { 'week-bar-selected': startWeek === week.value }]"
                :style="{ height: '100%' }"
              ></div>
              <div class="week-bar-label">{{ week.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- ENDING MONTH/WEEK -->
      <div style="background: #f5f5f5; padding: 12px; border-radius: 8px;">
        <h5 style="margin-bottom: 8px;">End Time</h5>
        
        <v-select
          v-model="endMonth"
          :items="monthOptions"
          label="Month"
          variant="outlined"
          density="compact"
          hide-details
          style="width: 125px; margin-bottom: 10px;"
          @update:model-value="onMonthChange"
        ></v-select>

        <div style="margin-top: 10px;">
          <h5 style="margin-bottom: 5px;">Checklists per Week</h5>
          <p style="font-size: 11px; color: #777; margin: 0 0 8px 0;">Click a bar to select end week</p>
          
          <div style="display: flex; gap: 4px; align-items: flex-end; height: 100%; padding: 5px 0;">
            <div
              v-for="week in weeksInEndMonth"
              :key="'end-week-' + week.value"
              class="week-bar-container"
              :style="{ height: week.height, cursor: 'pointer' }"
              @click="selectEndWeek(week.value)"
            >
              <div class="week-bar-label">{{ week.density }}</div>
              <div
                :class="['week-bar', { 'week-bar-selected': endWeek === week.value }]"
                :style="{ height: '100%' }"
              ></div>
              <div class="week-bar-label">{{ week.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!--- Confirmation --->
      <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
        <v-btn
          color="#296239"
          @click="confirmTimeRange"
          :disabled="(!isYearRangeSelected)"
          size="small"
        >
          Confirm Time
        </v-btn>
      </div>
      <!-- Data Distribution Graph -->
      <div style="margin-top: 15px; padding: 12px; background: #f5f5f5; border-radius: 8px;">
        <DataDistributionGraph/>
      </div>

    </div>
    
    <!--------------------------->
    <!--- PICK # OF TOP BIRDS --->
    <!----------------------------->
    <div class="config-section">
      <div style="display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; border-radius: 8px;">
        <span style="font-weight: 500;">Show top</span>
        <v-text-field
          v-model.number="analyticsStore.numTopBirds"
          density="compact"
          style="width: 80px; flex: none;"
          type="number"
          variant="outlined"
          hide-details
          single-line
          :min="1"
          :max="allBirds.length || 10"
        ></v-text-field>
        <span style="font-weight: 500;">birds</span>
      </div>
    </div>


    <!--------------------------->
    <!------ TOGGLES ------->
    <!--------------------------->
    <div class="config-section">
      <div style="padding: 12px; background: #f5f5f5; border-radius: 8px;">
        <v-switch
          color="primary"
          label="Show Likelihood Curve"
          hide-details
          @change="handleGraphToggle"
          :model-value="showGraph"
        ></v-switch>
        <v-switch
          color="primary"
          label="Show photos of top 3 birds"
          @change="handlePhotosToggle"
          hide-details
          :model-value="showTopPhotos"
          style="margin-top: -8px;"
        ></v-switch>
      </div>
    </div>


    <!--------------------------->
    <!------ CUSTOM BIRDS ------->
    <!--------------------------->
    <div class="config-section">
      <div style="padding: 12px; border-radius: 8px;">
        <v-text-field
          v-model="birdSearch"
          variant="outlined"
          label="Add custom birds..."
          hide-details
          clearable
          density="compact"
          bg-color="white"
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
            <div style="font-weight: 500;">{{ bird.Species }}</div>
            <div style="font-size: 11px; color: #666;">
              #{{ bird.Rank }} · Likelihood {{ Math.round(bird.wtd_rf * 100) / 100 }} · Normalized {{ Math.round(bird.rfpc * 10) / 10 }}
            </div>
          </div>
        </div>
      </div>
    </div>


    <!--------------------------->
    <!------ UPLOAD AS ... ------>
    <!--------------------------->
    <div class="buttons-container" style="justify-content: center; margin-top: 150px;">
      <div id="upload-button" @click="exportReport">
        <div class="button-wrapper" style="width: 150px; height: 50px; color: black; cursor: pointer;">
          <span v-if="!isExporting">Export PDF</span>
          <span v-else>Generating...</span>
        </div>
      </div>
    </div>
    

    <!---- Scroll Indicator ----->
    <div v-if="showScrollIndicator" class="scroll-indicator">
      <BIconArrowDown />
    </div>

  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import {
  BIconHouseFill,
  BIconArrowLeft,
  BIconArrowDown
} from 'bootstrap-icons-vue';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import type { Bird } from '../types';
import DataDistributionGraph from '../components/DataDistributionGraph.vue'


/**
 * A panel for configurating the analytics report. 
 * It includes functionality for date range, etc. (has yet to be completed). 
 * The panel allows users to ...
 */
export default defineComponent({
  name: 'AnalyticsConfigPanel',

  components: {
    BIconHouseFill,
    BIconArrowLeft,
    BIconArrowDown,
    DataDistributionGraph
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();
    
    // SCROLL LOGIC STATE
    const panel = ref<HTMLElement | null>(null);
    const showScrollIndicator = ref(false); // Default to false

    // --- YEAR SELECTION LOGIC ---
    const currentYear = new Date().getFullYear();
    const minYear = 1900;  // eBird's historical minimum
    
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
            console.log(`Confirmed year range: ${tempStartYear.value} to ${tempEndYear.value}`);
        } else {
            console.error("Invalid year range entered.");
        }
    };

    // --- MONTH/WEEK SELECTION DATA ---
    const isYearRangeSelected = computed(() => {
        return (tempStartYear.value == analyticsStore.startYear && tempEndYear.value == analyticsStore.endYear)
    });

    const monthOptions = [
      { title: 'January', value: 1 }, { title: 'February', value: 2 }, 
      { title: 'March', value: 3 }, { title: 'April', value: 4 }, 
      { title: 'May', value: 5 }, { title: 'June', value: 6 }, 
      { title: 'July', value: 7 }, { title: 'August', value: 8 }, 
      { title: 'September', value: 9 }, { title: 'October', value: 10 }, 
      { title: 'November', value: 11 }, { title: 'December', value: 12 }
    ];

    const startMonth = ref(1);
    const endMonth = ref(12);
    
    const startWeek = ref(1);
    const endWeek = ref(4); 

    const startWeekDataDensity = computed(() => {
      // find selected month title
      const selectedMonthOption = monthOptions.find(m => m.value === startMonth.value);
      if (!selectedMonthOption || !analyticsStore.selectedHotspot?.sample_sizes_by_week) {
          return [];
      }

      // Set month
      analyticsStore.startMonth = startMonth.value;

      // Get three-letter abbreviation
      const monthAbbrev = selectedMonthOption.title.substring(0, 3);
      const densityData = analyticsStore.selectedHotspot.sample_sizes_by_week;

      // populate list + loop through weeks in month
      const result: { label: string, value: number, density: number }[] = [];
      for (let i = 1; i <= 4; i++) {
          const wkIndex = `${monthAbbrev}_w${i}`;
          const density = densityData[wkIndex] ?? 0;
          result.push({
              label: `Wk ${i}`,
              value: i,
              density: density
          });
      }
      return result;
    });

    const MAX_BAR_HEIGHT_PX = 100;

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
      const selectedMonthOption = monthOptions.find(m => m.value === endMonth.value);
      if (!selectedMonthOption || !analyticsStore.selectedHotspot?.sample_sizes_by_week) {
          return [];
      }

      // Set month
      analyticsStore.endMonth = endMonth.value;

      // Get three-letter abbreviation
      const monthAbbrev = selectedMonthOption.title.substring(0, 3);
      const densityData = analyticsStore.selectedHotspot.sample_sizes_by_week;

      // populate list + loop through weeks in month
      const result: { label: string, value: number, density: number }[] = [];
      for (let i = 1; i <= 4; i++) {
          const wkIndex = `${monthAbbrev}_w${i}`;
          const density = densityData[wkIndex] ?? 0;
          result.push({
              label: `Wk ${i}`,
              value: i,
              density: density
          });
      }
      return result;
    });


    const weeksInStartMonth = computed(() => {
      const maxD = maxDensity.value;
      return startWeekDataDensity.value.map(week => {
        const scaledHeight = (week.density / maxD) * MAX_BAR_HEIGHT_PX;
            
        return {
          ...week,
          height: `${Math.max(5, scaledHeight) + 43}px`
        };
      });
    });

    const weeksInEndMonth = computed(() => {
      const maxD = maxDensity.value;
      return endWeekDataDensity.value.map(week => {
        const scaledHeight = (week.density / maxD) * MAX_BAR_HEIGHT_PX;
            
        return {
          ...week,
          height: `${Math.max(5, scaledHeight) + 43}px` 
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
            console.log(`[auto-fetch] Time changed: ${startMonth.value}/${startWeek.value} to ${endMonth.value}/${endWeek.value}`);
            analyticsStore.fetchHotspotDetail();
        }, 300);
    };

    const selectStartWeek = (weekNumber: number) => {
        startWeek.value = weekNumber;
        analyticsStore.startWeek = startWeek.value;
        debouncedFetchHotspot();  // Auto-fetch with debounce
    };

    const selectEndWeek = (weekNumber: number) => {
        endWeek.value = weekNumber;
        analyticsStore.endWeek = endWeek.value;
        debouncedFetchHotspot();  // auto-fetch with debounce
    };
    
    // keep manual trigger if we need it later
    const confirmTimeRange = () => {
        if (fetchDebounceTimer) clearTimeout(fetchDebounceTimer);
        analyticsStore.fetchHotspotDetail();
        console.log(`Manual confirm: ${startMonth.value}/${startWeek.value} to ${endMonth.value}/${endWeek.value}`);
    };

    // handler for month dropdown changes - triggers debounced fetch
    const onMonthChange = () => {
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
        setTimeout(checkScrollPosition, 100);  // for checking the scroll position
    });


    // --- OTHER LOGIC (UNCHANGED) ---
    const birdSearch = ref("");
    const allBirds = computed(() => analyticsStore.getAllBirds);
    const filteredBirds = ref<Bird[]>([]);

    const filterBirds = () => {
      const q = birdSearch.value.toLowerCase();
      filteredBirds.value = allBirds.value.filter(bird =>
        bird.Species.toLowerCase().includes(q)
      );
    };

    const selectBird = (bird: Bird) => {
      birdSearch.value = bird.Species;
      filteredBirds.value = [];
      analyticsStore.selectBird(bird);
    };

    const handleSearchBlur = () => {
      // Delay to allow click on search result to register
      setTimeout(() => {
        filteredBirds.value = [];
      }, 150);
    };

    const clearSearch = () => {
      birdSearch.value = '';
      filteredBirds.value = [];
    };

    const redirectToHomeScreen = () => {
      analyticsStore.resetAnalyticsConfiguration();
      analyticsStore.resetSelectedHotspot();
      router.push({ name: 'HomeScreen' });
    };

    const redirectToHotspotSearch = () => {
      analyticsStore.resetAnalyticsConfiguration();
      router.push({ name: 'HotspotSearch' });
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
          show_graph: analyticsStore.showLikelihoodCurve.toString(),
          show_photos: analyticsStore.showTopBirdPhotos.toString(),
        });
        
        if (analyticsStore.startYear) params.append('start_yr', analyticsStore.startYear.toString());
        if (analyticsStore.endYear) params.append('end_yr', analyticsStore.endYear.toString());
        if (analyticsStore.startMonth) params.append('start_month', analyticsStore.startMonth.toString());
        if (analyticsStore.startWeek) params.append('start_week', analyticsStore.startWeek.toString());
        if (analyticsStore.endMonth) params.append('end_month', analyticsStore.endMonth.toString());
        if (analyticsStore.endWeek) params.append('end_week', analyticsStore.endWeek.toString());
        
        // Pass custom bird ranks only (much shorter than full objects)
        if (analyticsStore.selectedBirds.length > 0) {
          const ranks = analyticsStore.selectedBirds.map(b => b.Rank);
          params.append('custom_ranks', ranks.join(','));
        }
        if (analyticsStore.selectedBirdPhotos.length > 0) {
          const photoRanks = analyticsStore.selectedBirdPhotos.map(b => b.Rank);
          params.append('photo_ranks', photoRanks.join(','));
        }
        
        // Pass the current date from client (correct timezone)
        const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        params.append('gen_date', today);
        
        const pdfUrl = `/api/hotspots/report/${analyticsStore.selectedHotspotId}/pdf?${params.toString()}`;
        
        // Open PDF in new tab - browser will show print dialog or PDF viewer
        window.open(pdfUrl, '_blank');
      } catch (error) {
        console.error('Export failed:', error);
        alert('Failed to generate PDF. Please try again.');
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
      isYearRangeSelected,
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
      isExporting
    };
  },
});

</script>

<style scoped>
.analytics-config-panel {
  padding: 16px;
  background: #fafafa;
  border-right: 1px solid #ddd;
  
  height: 100vh; 
  overflow-y: auto; 
  position: relative;
    
  box-sizing: border-box;
}

/* SCROLL INDICATOR STYLES */

.scroll-indicator {
    position: sticky; 
    bottom: 0px; 
    left: 0;
    right: 0;
    height: 30px; 
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(to top, #fafafa 50%, rgba(0, 0, 0, 0) 100%);
    color: #333;
    font-size: 1.2em;
    pointer-events: none; 
    opacity: 0.8;
}

/* --- WEEK BAR STYLES --- */
.week-bar-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    width: 25%;
    /*max-height: 120px; */
    transition: background-color 0.15s ease;
    border-radius: 4px;
    padding-top: 2px;
}

.week-bar-container:hover {
    background-color: #e0e0e0;
}

.week-bar {
    width: 60%;
    background-color: #8EB5CC; 
    border-radius: 3px 3px 0 0;
    transition: background-color 0.15s ease, height 0.3s ease;
}

.week-bar-selected {
    background-color: #457999; 
    box-shadow: 0 0 5px rgba(38, 67, 84, 0.5);
}

.week-bar-label {
    font-size: 11px;
    margin-top: 4px;
    color: #555;
    font-weight: 500;
}

/* --- OTHER STYLES --- */

.buttons-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 60px;
  padding-top: 20px;
  padding-inline: 40px;
  padding-bottom: 20px;
  color: #ffffffc9;
}

.button-wrapper {
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

.home-button-wrapper:hover {
  background-color: #d2d2d2;
  color: rgb(3, 3, 42);
}


.panel-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  margin-top: 20px;
}

.config-section {
  margin-top: 15px;
}

.config-section h4, .config-section h5 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.ui-block {
  width: 100%;
  height: 36px;
  background: #e3e3e3;
  border-radius: 4px;
}

.search-results {
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 6px;
  max-height: 220px;
  overflow-y: auto;
  box-shadow: 0px 2px 8px rgba(0,0,0,0.12);
  text-align: left;
}

.search-result-item {
  padding: 10px 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #f1f1f1;
}

</style>