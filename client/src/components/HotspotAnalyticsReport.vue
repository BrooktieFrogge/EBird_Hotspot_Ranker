<template>
  <div class="analytics-container">
    <div class="bird-lists-container">
      <h3 style="text-align: left; padding-left:40px"> {{ analyticsStore.selectedHotspot?.name ?? 'No Hotspot Selected' }}: Analytics Report </h3>
      <hr />

      <!-- LEFT SECTION: Table -->
      <div class="bird-table">
        <h2 class="section-title">Top {{ analyticsStore.numTopBirds }} Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>Weighted Rank Factor</div>
          <div>RFPC</div>
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

          <div class="cell">{{ bird.wtd_rf }}</div>
          <div class="cell">{{ bird.rfpc }}</div>
        </div>
      </div>


      <!-- RIGHT SECTION: Graph -->
      <div id="apexchart" style="width:100%; height:350px; border: 1px solid black;">
        <apexchart 
          ref="chart"
          type="line"
          :options = "chartOptions"
          :series = "series"
          >
        </apexchart>
      </div>


      <!-- CUSTOM SELECTED BIRDS -->
      <div class="bird-table" v-show="(analyticsStore.selectedBirds.length > 0)">
        <h2 class="section-title">Custom Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>Weighted Rank Factor</div>
          <div>RFPC</div>
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

          <div class="cell">{{ bird.wtd_rf }}</div>
          <div class="cell">{{ bird.rfpc }}</div>
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
          :src="bird.photo"
          alt=""
        />
        <div class="photo-caption">
          {{ i + 1 }}. {{ bird.Species }}
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { computed, defineComponent, nextTick, ref, watch } from 'vue';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import VueApexCharts from 'vue3-apexcharts';
import { BIconXCircle } from 'bootstrap-icons-vue';
import type { ApexOptions } from 'apexcharts';
import { addSyntheticTrailingComment } from 'typescript';

export default defineComponent({
  name: 'HotspotAnalyticsReport',

  components: {
    apexchart: VueApexCharts,
    BIconXCircle
  },

  setup() {
    const analyticsStore = useAnalyticsStore();
    const birds = computed(() => analyticsStore.getTopBirds);

    const placeholdPic = "https://cdn1.byjus.com/wp-content/uploads/2021/03/line-graph.png";

    //not sure if necessary for the chart to update when toggling visibility
    const chart = ref<InstanceType<typeof VueApexCharts> | null>(null);

    //same as above
    watch(() => analyticsStore.showLikelihoodCurve, async (visible) => {
      if (visible) {
        await nextTick();
        chart.value?.updateOptions({});
      }
    });

    const series = computed(() => [{
      name: "Ranking",
      data: birds.value.map((bird: any) => bird.wtd_rf)
      //data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
    }]);

    const chartOptions = computed<ApexOptions>(() => ({
      chart: {
        id: "apexchart",
        height: 350,
        type: 'line',
        zoom: {
          enabled: true
        },
      },
      stroke: {
        curve: "straight"
      },
      title: {
        text: 'Bird Frequency Ranking',
        align: 'left'
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'],
          opacity: 0.5
        },
      },
      xaxis: {
        categories: birds.value.map((bird: any) => bird.rank),
        //categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
      }
    }));

    return {
      analyticsStore,
      birds,
      placeholdPic,
      series,
      chartOptions
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
}

.bird-lists-container {
  display: block;
  gap: 24px;
  width: 100vh;
  color: #222;
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
</style>
