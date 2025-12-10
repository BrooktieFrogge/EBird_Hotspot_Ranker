<template>
  <div class="analytics-container" v-if="birds.length > 1">
    <div class="bird-lists-container">
      <h3 style="text-align: left; padding-left: 20px;"> {{ analyticsStore.selectedHotspot?.name ?? 'No Hotspot Selected' }}</h3>
      <div class="hotspot-header">
        <span><BIconPinMapFill style="margin-right: 15px;"/></span> 
        <h4>{{ analyticsStore.selectedHotspot?.country ?? ''}}, {{ analyticsStore.selectedHotspot?.subregion1 ?? ''}}</h4>
      </div>

      <hr />

      <!-- LEFT SECTION: Table -->
      <div class="bird-table">
        <h2 class="section-title">Top {{ analyticsStore.numTopBirds }} Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>Weighted Rank Factor</div>
          <div>Ranked Factor Percentage</div>
        </div>

        <div
          class="table-row"
          v-for="(bird, i) in birds"
          :key="i"
        >
          <div class="species-cell">
            <span class="index">{{ i + 1 }}.</span>
            <span>{{ bird.Species }}</span>
          </div>

          <div class="cell">{{ Math.round((10**5)*bird.wtd_rf)/(10**5)}}</div>
          <div class="cell">{{ Math.round((10**4)*bird.rfpc)/(10**4) }}</div>
        </div>
      </div>


      <!-- LIKELIHOOD GRAPH-->
      <div id="linechart" style="width:95%; height:60%; padding:10px" v-show="(analyticsStore.showLikelihoodCurve && (analyticsStore.selectedHotspot != null) && ('birds' in analyticsStore.selectedHotspot) && (analyticsStore.selectedHotspot.birds.length > 0))">
        <LineChart 
          style="height: 100%;"
          :chartData="chartData" 
        />
      </div>


      <!-- CUSTOM SELECTED BIRDS -->
      <div class="bird-table" v-show="(analyticsStore.selectedBirds.length > 0)">
        <h2 class="section-title">Custom Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>Weighted Rank Factor</div>
          <div>Ranked Factor Percentage</div>
        </div>

        <div
          class="table-row"
          v-for="(bird, i) in analyticsStore.selectedBirds"
          :key="i"
        >
          <div class="species-cell">
            <span class="index">{{ i + 1 }}.</span>
            <span>{{ bird.Species }}</span>
          </div>

          <div class="cell">{{ Math.round((10**5)*bird.wtd_rf)/(10**5) }}</div>
          <div class="cell">{{ Math.round((10**4)*bird.rfpc)/(10**4)}}</div>
          <div class="cell">
            <div id="remove-bird-button" @click="analyticsStore.deselectBird(bird)">
              <BIconXCircle/>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- RIGHT SECTION: Photos -->
    <div class="photo-column" v-show="analyticsStore.showTopBirdPhotos">
      <div
        class="photo-card"
        v-for="(bird, i) in birds.slice(0, 3)"
        :key="i"
      >
        <img
          class="photo"
          :src="bird.imageUrl"
          alt=""
        />
        <div class="photo-caption">
          {{ i + 1 }}. {{ bird.Species }}
        </div>
      </div>
    </div>

  </div>
  <div class="loading-screen" v-else>
    <img
        class="loading-photo"
        :src="loadingImage"
        alt=""
      />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import { BIconXCircle, BIconPinMapFill } from 'bootstrap-icons-vue';
import { LineChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default defineComponent({
  name: 'HotspotAnalyticsReport',

  components: {
    BIconXCircle,
    BIconPinMapFill,
    LineChart
  },

  setup() {
    const analyticsStore = useAnalyticsStore();
    const birds = computed(() => analyticsStore.getTopBirds);

    /*const loadingImage = "https://i.pinimg.com/originals/c0/c4/1b/c0c41b77b01b48d9a62b4ae3b79cb654.gif";*/
    const loadingImage = "https://cdn.pixabay.com/animation/2024/07/04/20/46/20-46-07-872_512.gif";

    const chartData = computed(() => {
    const wtdrfData = birds.value.map((b: any) => b.wtd_rf);
    const rfpcData = birds.value.map((b: any) => b.rfpc / 100);

    return {
      labels: birds.value.map((b: any) => b.Species),
      datasets: [
        {
          label: 'Weighted Rank Factor',
          data: wtdrfData,
          backgroundColor: '#45799980',
          borderColor: '#457999',
          pointRadius: 6,
          pointHoverRadius: 10,
        },
        {
          label: 'Ranked Factor Percentage',
          data: rfpcData,
          backgroundColor: '#29623980',
          borderColor: '#296239',
          pointRadius: 6,
          pointHoverRadius: 10,
        },
      ],
    };
  });


    return {
      analyticsStore,
      birds,
      loadingImage,
      chartData
    };
  },

});
</script>

<style scoped>
.analytics-container {
  display: flex;
  gap: 24px;
  padding: 40px;
  height: 100vh;
  background: white;
  color: #222;
  overflow: scroll;
  opacity: 100%;
}

.bird-lists-container {
  display: block;
  gap: 24px;
  width: 100vh;
  color: #222;
  opacity: 100%;
}

.hotspot-header {
  display: flex;
  align-items: center;
  margin-top: 5px;
  font-size: 0.9em;
  padding-left: 20px
}

.bird-table {
  flex: 1;
  padding: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1fr 0.1fr;
  padding: 8px 0;
  border-bottom: 1px solid #e4e4e4;
}


.table-header {
  font-weight: 600;
}

.species-cell {
  display: flex;
  gap: 6px;
  align-items: center;
}

.index {
  color: #888;
  width: 20px;
}

.cell {
  text-align: center;
}

.photo-column {
  width: 220px;
  flex-shrink: 0;
}

.photo-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.photo {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.photo-caption {
  padding: 8px;
  font-weight: 500;
  text-align: center;
}

.loading-screen{
  align-items: center;
  vertical-align: middle;
  gap: 24px;
  padding: 300px;
  height: 100vh;
  /*background: #18233e;*/
  background: white;
  color: #222;
  opacity: 100%;
}


.loading-photo {
  width: 300px;
  height: 300px;
  object-fit: cover;
}

</style>
