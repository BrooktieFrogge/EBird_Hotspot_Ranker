<template>
  <div class="analytics-config-panel">
    
    <div class="buttons-container">
      <!-- Back Button -->
      <div id="back-button" @click="redirectToHotspotSearch">
        <div class="back-button-wrapper">
          <BIconArrowLeft />
        </div>
      </div>

      <!-- Home Button -->
      <div id="home-button" @click="redirectToWelcomeScreen">
        <div class="back-button-wrapper">
          <BIconHouseFill />
        </div>
      </div>
    </div>

    <h3 class="panel-title">Analytics Configuration</h3>

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
          class="ma-0 pa-0"
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
          class="ma-0 pa-0"
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

    <div class="config-section">
      <h4>Bird Selection</h4>
      <div class="ui-block"></div>
    </div>

    <div class="config-section">
      <h4>Display Options</h4>
      <div class="ui-block"></div>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent} from 'vue';
import { useRouter } from 'vue-router';
import {
  BIconHouseFill,
  BIconArrowLeft
} from 'bootstrap-icons-vue';
import { ref } from 'vue';


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
    const yearRange = ref([1900, 2025]);
    
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


    return {
      redirectToWelcomeScreen,
      redirectToHotspotSearch,
      yearRange
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
  border-top: 1px solid #ffffffc9;
  border-bottom: 1px solid #ffffffc9;
  padding-top: 20px;
  padding-inline: 40px;
  padding-bottom: 20px;
  color: #ffffffc9;
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

</style>
