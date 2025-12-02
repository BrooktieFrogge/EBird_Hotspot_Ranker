<template>
  <div class="analytics-config-panel">
    
    <div class="buttons-container">
      <!-- Back Button -->
      <div id="back-button" @click="redirectToHotspotSearch">
        <div class="button-wrapper">
          <BIconArrowLeft />
        </div>
      </div>

      <!-- Home Button -->
      <div id="home-button" @click="redirectToWelcomeScreen">
        <div class="button-wrapper">
          <BIconHouseFill />
        </div>
      </div>
    </div>

    <!-- Year Selection -->
    <div class="config-section">
      <h4>Select Year</h4>
      <v-range-slider
        v-model="yearRange"
        strict
        :max="2025"
        :min="1900"
        :step="1"
      >
        <template v-slot:prepend>
        <v-text-field
          v-model="yearRange[0]"
          density="compact"
          style="width: 95px;"
          type="number"
          variant="outlined"
          hide-details
          single-line
        ></v-text-field>
        </template>
        <template v-slot:append>
          <v-text-field
            v-model="yearRange[1]"
            density="compact"
            style="width: 95px"
            type="number"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
        </template>
      </v-range-slider>
    </div>

    <!-- Week Selection -->
    <div class="config-section">
      <h4>Select Weeks</h4>
      <v-range-slider
        v-model="weekRange"
        strict
        :max="48"
        :min="0"
        :step="1"
        :ticks="[4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44]"
        :show-ticks="true"
      >
        <template v-slot:prepend>
        <v-text-field
          v-model="weekRange[0]"
          density="compact"
          style="width: 75px;"
          type="number"
          variant="outlined"
          hide-details
          single-line
        ></v-text-field>
        </template>
        <template v-slot:append>
          <v-text-field
            v-model="weekRange[1]"
            density="compact"
            style="width: 75px"
            type="number"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
        </template>
      </v-range-slider>
    </div>

    <!-- Top Number of Birds Chooser -->
    <div class="config-section" style="margin-left: 10px">
      <div style="display: flex; align-items: center; gap: 8px; width: 250px;">
        <span>Show top</span>
        <v-number-input
          control-variant="stacked"
          inset
          v-model="analyticsStore.numTopBirds"
          :min="1"
          :max="allBirds.length"
          style="padding: 5px"
        ></v-number-input>
        <span>birds</span>
      </div>
    </div>

    <!-- Graph Toggle -->
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

    <!-- Photos Toggle -->
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
      <h4>Bird Selection</h4>

      <!-- Bird Search Bar -->
      <v-text-field
        v-model="birdSearch"
        variant="outlined"
        label="Search birds..."
        hide-details
        clearable
        density="compact"
        style="height:"
        @input="filterBirds"
      />

      <!-- Search Results Dropdown -->
      <div
        v-if="filteredBirds.length > 0 && birdSearch.length > 0"
        class="search-results"
      >
        <div
          v-for="bird in filteredBirds"
          :key="bird.species"
          class="search-result-item"
          @click="selectBird(bird)"
        >
          {{ bird.species }} &emsp; &#8212;&#8212; &emsp; {{ bird.rfpc }} &emsp; &#8212;&#8212; &emsp;  {{ bird.wtdrf }}
        </div>
      </div>
    </div>

    <!-- Upload Button -->
    <div class="buttons-container" style="justify-content: left; margin-top: 150px;">
      <div id="upload-button">
        <div class="button-wrapper" style="width: 150px; height: 50px; color: black">
          Export
          <BIconCloudDownload />
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import {
  BIconHouseFill,
  BIconArrowLeft,
  BIconCloudDownload
} from 'bootstrap-icons-vue';
import { ref } from 'vue';
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
    BIconArrowLeft
  },

  setup() {
    const router = useRouter();
    const analyticsStore = useAnalyticsStore();


    const yearRange = ref([1900, 2025]);
    const weekRange = ref([0, 48]);
    const ex11 = ['red', 'indigo', 'orange', 'primary', 'secondary', 'success', 'info', 
    'warning', 'error', 'red-darken-3', 'indigo-darken-3', 'orange-darken-3'];

    const birdSearch = ref("");
    const allBirds = analyticsStore.getAllPlacementBirds;
    

    const filteredBirds = ref<Bird[]>([]);

    const filterBirds = () => {
      const q = birdSearch.value.toLowerCase();
      filteredBirds.value = allBirds.filter(bird =>
        bird.species.toLowerCase().includes(q)
      );
    };

    const selectBird = (bird: Bird) => {
      birdSearch.value = bird.species;
      filteredBirds.value = [];
      console.log("Selected bird:", bird.species);
      analyticsStore.selectBird(bird);
      // optionally emit event or store selected state
    };

    
    /**
     * Redirects the router to the welcome screen.
     */
    const redirectToWelcomeScreen = () => {
      router.push({ name: 'WelcomeScreen' });
    };

     /**
     * Redirects the router to the hotspot search.
     */
    const redirectToHotspotSearch = () => {
      router.push({ name: 'HotspotSearch' });
    };

    
    const showGraph = analyticsStore.showLikelihoodCurve;

     /**
     * Toggles the addition of a likelihood graph on the layout.
     * 
     */
    const handleGraphToggle = () => {
        analyticsStore.toggleLikelihoodCurve();
    };

    const showTopPhotos = analyticsStore.showTopBirdPhotos;

    /**
     * Toggles the addition of top 3 photos on the layout.
     * 
     */
    const handlePhotosToggle = () => {
        analyticsStore.toggleTopPhotos();
    };

    return {
      redirectToWelcomeScreen,
      redirectToHotspotSearch,
      yearRange,
      weekRange,
      ex11, 
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
  height: 100%;
  box-sizing: border-box;
}

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
  margin-top: 24px;
  margin-bottom: 24px;
}

.config-section h4 {
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
  transition: background 0.15s;
}

.search-result-item:hover {
  background: #f1f1f1;
}

</style>
