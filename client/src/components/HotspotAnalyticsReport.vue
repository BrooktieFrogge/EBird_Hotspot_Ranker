<template>
  <div class="analytics-container" v-if="birds.length > 1 && analyticsStore.isLoading == false">
    <div class="bird-lists-container">


      <!--------------------------->
      <!--- HOTSPOT NAME/HEADER --->
      <!--------------------------->
      <div class="hotspot-header">
        <span style="padding-bottom: 8px"><BIconPinMapFill style="margin-right: 15px;"/></span> 
        <h4>{{ analyticsStore.selectedHotspot?.name ?? 'No Hotspot Selected' }}: {{ analyticsStore.selectedHotspot?.country ?? ''}}, {{ analyticsStore.selectedHotspot?.subregion1 ?? ''}}</h4>
      </div>

      <hr />

      <!--------------------------->
      <!----- LIKELIHOOD GRAPH ---->
      <!--------------------------->
      <h5>Observation Likelihood</h5>
      <div id="linechart" style="width:95%; height:60%; padding:10px" v-show="(analyticsStore.showLikelihoodCurve && (analyticsStore.selectedHotspot != null) && ('birds' in analyticsStore.selectedHotspot) && (analyticsStore.selectedHotspot.birds.length > 0))">
        <LineChart 
          style="height: 100%;"
          :chartData="chartData" 
        />
      </div>
      

      <!--------------------------->
      <!-------- TOP BIRDS -------->
      <!--------------------------->
      <div class="bird-table">
        <h2 class="section-title">Top {{ analyticsStore.numTopBirds }} Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>List Likelihood</div>
          <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
        </div>

        <div
          class="table-row"
          v-for="(bird, i) in birds"
          :key="i"
        >
          <div class="species-cell">
            <span class="index">{{ i + 1 }}.</span>
             <span> <a :href="bird.speciesUrl" target="_blank">{{ bird.Species }}</a> </span>
          </div>

          <div class="cell">{{ Math.round((10**2)*bird.wtd_rf)/(10**2)}}</div>
          <div class="cell">{{ Math.round((10)*bird.rfpc)/(10) }}</div>
        </div>
      </div>


      <!--------------------------->
      <!-- CUSTOM SELECTED BIRDS -->
      <!--------------------------->
      <div id="custom-birds" class="bird-table" v-show="(analyticsStore.selectedBirds.length > 0)">
        <h2 class="section-title">Custom Birds</h2>

        <div class="table-header-custom">
          <div>Species</div>
          <div>Rank</div>
          <div>List Likelihood</div>
          <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
        </div>

        <div
          class="table-row-custom"
          v-for="(bird, i) in analyticsStore.selectedBirds.sort((a, b) => a.Rank - b.Rank)"
          :key="i"
        >
          <div class="species-cell">
            <span class="index">{{ i + 1 }}.</span>
            <span> <a :href="bird.speciesUrl" target="_blank">{{ bird.Species }}</a> </span>
          </div>
          <div class="cell">{{ bird.Rank }}</div>
          <div class="cell">{{ Math.round((10**2)*bird.wtd_rf)/(10**2) }}</div>
          <div class="cell">{{ Math.round((10)*bird.rfpc)/(10)}}</div>
          <div class="cell">
            <div id="remove-bird-button" style="color: blue" @click="analyticsStore.deselectBird(bird)">
              <BIconXCircle/>
            </div>
          </div>
          <div class="cell">
            <div id="add-photo-button" style="color: blue" @click="analyticsStore.displayBirdPhoto(bird)" >
              <BIconCamera/>
            </div>
          </div>
        </div>
      </div>

    </div>


    <!--------------------------->
    <!-- RIGHT SECTION: Photos -->
    <!--------------------------->

    <!-- Top Three Birds -->
    <div class="photo-column">
      <div v-show="analyticsStore.showTopBirdPhotos">
        <h5 style="padding-top: 10px">Top 3 Birds</h5>
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

      <!-- Custom Selected Birds -->
      <div v-if="analyticsStore.selectedBirdPhotos.length > 0">
        <hr />
        <h5 style="padding-top: 10px">Custom Birds</h5>
      </div>

      <div
        class="photo-card"
        v-for="(bird, i) in analyticsStore.selectedBirdPhotos"
        :key="i"
      >
        <img
          class="photo"
          :src="bird.imageUrl"
          alt=""
        />
        <div class="photo-caption">
          {{ bird.Species }}
        </div>
      </div>

    </div>

  </div>


  <!---------------------------->
  <!-- DEFAULT: Loading Image -->
  <!---------------------------->
  <div class="loading-screen" v-else>
    <img
        class="loading-photo"
        :src="loadingImage"
        alt=""
      />
  </div>  
  
</template>



<script lang="ts">
import { computed, defineComponent, watch } from 'vue';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import { BIconXCircle, BIconCamera, BIconPinMapFill } from 'bootstrap-icons-vue';
import { LineChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default defineComponent({
  name: 'HotspotAnalyticsReport',

  components: {
    BIconXCircle,
    BIconCamera,
    BIconPinMapFill,
    LineChart
  },

  setup() {
    const analyticsStore = useAnalyticsStore();
    const birds = computed(() => analyticsStore.getTopBirds);

    const loadingImage = "https://cdn.pixabay.com/animation/2024/07/04/20/46/20-46-07-872_512.gif"; 

    // Data for the Likelihood Graph
    const chartData = computed(() => {
      const wtdrfData = birds.value.map((b: any) => b.wtd_rf);
      const rfpcData = birds.value.map((b: any) => b.rfpc / 100);

      return {
        labels: birds.value.map((b: any) => b.Species),
        datasets: [
          {
            label: 'List Likelihood',
            data: wtdrfData,
            backgroundColor: '#45799980',
            borderColor: '#457999',
            pointRadius: 6,
            pointHoverRadius: 10,
          },
          {
            label: 'List Likelihood (normalized to top bird)',
            data: rfpcData,
            backgroundColor: '#29623980',
            borderColor: '#296239',
            pointRadius: 6,
            pointHoverRadius: 10,
          },
        ],
      };
    });

    watch(analyticsStore.selectedBirds, () => {
      const element = document.getElementById("custom-birds");
      console.log("CALLED")
      setTimeout(() => {
        element?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 0);
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
  grid-template-columns: 1.1fr 1fr 1fr;
  padding: 8px 0;
  border-bottom: 1px solid #e4e4e4;
}

.table-header-custom,
.table-row-custom {
  display: grid;
  grid-template-columns: 1fr .5fr .8fr .8fr 0.2fr 0.2fr;
  padding: 8px 0;
  border-bottom: 1px solid #e4e4e4;
}


.table-header {
  font-weight: 600;
}

.table-header-custom {
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
  margin-right: 10px;
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
