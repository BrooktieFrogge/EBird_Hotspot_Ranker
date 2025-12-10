<template>
  <div class="analytics-config-panel" @scroll="checkScrollPosition" ref="panel">
    
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
          :min="1900"
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
          :max="2025"
        ></v-text-field>
      </div>
      
      <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
        <v-btn
          color="primary"
          @click="confirmYearRange"
          :disabled="!isYearRangeValid"
          size="small"
        >
          Confirm Years
        </v-btn>
      </div>
    </div>

    <div class="config-section">
      <h4>Select Time Frame</h4>
      
      <div style="border: 1px solid #e0e0e0; padding: 10px; border-radius: 6px; margin-bottom: 15px;">
        <h5 style="margin-bottom: 8px;">Start Time</h5>
        
        <v-select
          v-model="startMonth"
          :items="monthOptions"
          label="Month"
          variant="outlined"
          density="compact"
          hide-details
          style="width: 125px; margin-bottom: 10px;"
        ></v-select>

        <div style="margin-top: 10px;">
          <h5 style="margin-bottom: 5px;">Start Week (Data Density)</h5>
          
          <div style="display: flex; gap: 4px; align-items: flex-end; height: 80px; padding: 5px 0;">
            <div
              v-for="week in weeksInMonth"
              :key="'start-week-' + week.value"
              class="week-bar-container"
              :style="{ height: week.height, cursor: 'pointer' }"
              @click="selectStartWeek(week.value)"
            >
              <div
                :class="['week-bar', { 'week-bar-selected': startWeek === week.value }]"
                :style="{ height: '100%' }"
              ></div>
              <div class="week-bar-label">{{ week.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <div style="border: 1px solid #e0e0e0; padding: 10px; border-radius: 6px;">
        <h5 style="margin-bottom: 8px;">End Time</h5>
        
        <v-select
          v-model="endMonth"
          :items="monthOptions"
          label="Month"
          variant="outlined"
          density="compact"
          hide-details
          style="width: 125px; margin-bottom: 10px;"
        ></v-select>

        <div style="margin-top: 10px;">
          <h5 style="margin-bottom: 5px;">End Week (Data Density)</h5>
          
          <div style="display: flex; gap: 4px; align-items: flex-end; height: 80px; padding: 5px 0;">
            <div
              v-for="week in weeksInMonth"
              :key="'end-week-' + week.value"
              class="week-bar-container"
              :style="{ height: week.height, cursor: 'pointer' }"
              @click="selectEndWeek(week.value)"
            >
              <div
                :class="['week-bar', { 'week-bar-selected': endWeek === week.value }]"
                :style="{ height: '100%' }"
              ></div>
              <div class="week-bar-label">{{ week.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
        <v-btn
          color="primary"
          @click="confirmTimeRange"
          size="small"
        >
          Confirm Time
        </v-btn>
      </div>

    </div>
    
    <div class="config-section" style="margin-left: 10px">
      <div style="display: flex; align-items: center; gap: 8px; width: 250px;">
        <span>Show top</span>
        <v-number-input
          control-variant="stacked"
          inset
          v-model="analyticsStore.numTopBirds"
          :min="1"
          :max="allBirds.length || 10"
          style="padding: 5px"
        ></v-number-input>
        <span>birds</span>
      </div>
    </div>

    <div class="config-section">
      <v-switch
        color="primary"
        label="Show Likelihood Curve"
        hide-details
        style="margin-left: 10px"
        @change="handleGraphToggle"
        :model-value="showGraph"
      ></v-switch>
    </div>

    <div class="config-section">
      <v-switch
        color="primary"
        label="Show photos of top 3 birds"
        @change="handlePhotosToggle"
        hide-details
        style="margin-left: 10px"
        :model-value=showTopPhotos
      ></v-switch>
    </div>

    <div class="config-section">

      <v-text-field
        v-model="birdSearch"
        variant="outlined"
        label="Add custom birds..."
        hide-details
        clearable
        density="compact"
        style="height:"
        @input="filterBirds"
      />

      <div
        v-if="filteredBirds.length > 0 && birdSearch.length > 0"
        class="search-results"
      >
        <div
          v-for="bird in filteredBirds"
          :key="bird.Species"
          class="search-result-item"
          @click="selectBird(bird)"
        >
          {{ bird.Species }} &emsp; &#8212;&#8212; &emsp; {{ Math.round((10**3)*bird.wtd_rf)/(10**3) }} &emsp; &#8212;&#8212; &emsp;  {{ Math.round((10**2)*bird.rfpc)/(10**2) }}
        </div>
      </div>
    </div>

    <div class="buttons-container" style="justify-content: left; margin-top: 150px;">
      <div id="upload-button">
        <div class="button-wrapper" style="width: 150px; height: 50px; color: black">
          Export
        </div>
      </div>
    </div>
    
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
    BIconArrowDown
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();
    
    // SCROLL LOGIC STATE
    const panel = ref<HTMLElement | null>(null);
    const showScrollIndicator = ref(false); // Default to false

    // --- YEAR SELECTION LOGIC ---
    const tempStartYear = ref(1900);
    const tempEndYear = ref(2025);
    
    const isYearRangeValid = computed(() => {
        const start = tempStartYear.value;
        const end = tempEndYear.value;
        const minGlobal = 1900;
        const maxGlobal = 2025;
        
        return start <= end && start >= minGlobal && end <= maxGlobal;
    });

    const confirmYearRange = () => {
        if (isYearRangeValid.value) {
            analyticsStore.setYearRange(tempStartYear.value, tempEndYear.value);
            analyticsStore.fetchHotspotDetail();
            console.log(`Confirmed year range: ${tempStartYear.value} to ${tempEndYear.value}`);
            location.reload()
        } else {
            console.error("Invalid year range entered.");
        }
    };

    // --- MONTH/WEEK SELECTION DATA ---
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

    const weekDataDensity = [
        { label: 'Wk 1', value: 1, density: 80 }, 
        { label: 'Wk 2', value: 2, density: 40 }, 
        { label: 'Wk 3', value: 3, density: 65 }, 
        { label: 'Wk 4', value: 4, density: 30 }, 
    ];

    const weeksInMonth = computed(() => {
        return weekDataDensity.map(week => ({
            ...week,
            height: `${week.density * 0.8}px`
        }));
    });

    const selectStartWeek = (weekNumber: number) => {
        startWeek.value = weekNumber;
        console.log(`Start Week selected: ${startMonth.value}/${startWeek.value}`);
    };
    
    const selectEndWeek = (weekNumber: number) => {
        endWeek.value = weekNumber;
        console.log(`End Week selected: ${endMonth.value}/${endWeek.value}`);
    };
    
    const confirmTimeRange = () => {
        analyticsStore.setTimeFrame(startMonth.value, startWeek.value, endMonth.value, endWeek.value);
        analyticsStore.fetchHotspotDetail();
        console.log(`Confirmed Time Range: ${startMonth.value}/${startWeek.value} to ${endMonth.value}/${endWeek.value}`);
        location.reload()
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

    return {
      redirectToHomeScreen,
      redirectToHotspotSearch,
      // Year Logic
      tempStartYear,
      tempEndYear,
      isYearRangeValid,
      confirmYearRange,
      // Month/Week Logic
      monthOptions,
      startMonth,
      endMonth,
      weeksInMonth,
      startWeek,
      endWeek,
      selectStartWeek,
      selectEndWeek,
      confirmTimeRange,
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
      showGraph,
      handleGraphToggle,
      showTopPhotos,
      handlePhotosToggle,
      analyticsStore
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
    max-height: 80px; 
    transition: background-color 0.15s ease;
    border-radius: 4px;
    padding-top: 2px;
}

.week-bar-container:hover {
    background-color: #e0e0e0;
}

.week-bar {
    width: 60%;
    background-color: #64b5f6; 
    border-radius: 3px 3px 0 0;
    transition: background-color 0.15s ease, height 0.3s ease;
}

.week-bar-selected {
    background-color: #1565c0; 
    box-shadow: 0 0 5px rgba(21, 101, 192, 0.5);
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

.search-result-item:hover {
  background: #f1f1f1;
}

</style>