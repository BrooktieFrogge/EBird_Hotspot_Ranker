<template>
  <div
    class="printable-report"
    v-if="!store.isLoading && store.selectedHotspot"
  >
    <!-- report header -->
    <header class="report-header">
      <h1>FeatherWeight Report</h1>
      <p class="generated-date">Generated: {{ generatedDate }}</p>
    </header>

    <!-- hotspot name -->
    <div class="hotspot-info">
      <h2>{{ store.selectedHotspot?.name ?? "No Hotspot Selected" }}</h2>
      <p class="location">
        {{ store.selectedHotspot?.country ?? "" }},
        {{ store.selectedHotspot?.subregion1 ?? "" }}
      </p>
    </div>

    <!-- observation likelihood graph -->
    <div class="section" v-if="store.showLikelihoodCurve && birds.length > 0">
      <h3 class="section-title">Observation Likelihood</h3>
      <div class="chart-wrapper">
        <LineChart :chartData="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- top birds list - matches original styling -->
    <div class="section bird-table-section">
      <div
        style="
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 4px;
        "
      >
        <h2 class="section-title" style="margin-bottom: 0">
          Top {{ store.numTopBirds }} Birds
        </h2>
        <span style="font-size: 11px; color: #666">
          Based on
          <strong>{{
            store.selectedHotspot?.total_sample_size?.toLocaleString() ?? 0
          }}</strong>
          checklists
        </span>
      </div>

      <div class="table-header">
        <div>Species</div>
        <div>List Likelihood</div>
        <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
      </div>

      <div class="table-row" v-for="(bird, i) in birds" :key="i">
        <div class="species-cell">
          <span class="index">{{ i + 1 }}.</span>
          <a
            v-if="bird.speciesUrl"
            :href="bird.speciesUrl"
            target="_blank"
            class="species-link"
            >{{ bird.Species }}</a
          >
          <span v-else>{{ bird.Species }}</span>
        </div>
        <div class="cell">
          {{ Math.round(10 ** 2 * bird.wtd_rf) / 10 ** 2 }}
        </div>
        <div class="cell">{{ Math.round(10 * bird.rfpc) / 10 }}</div>
      </div>
    </div>

    <!-- top bird photos grid -->
    <div
      class="section photos-section"
      v-if="store.showTopBirdPhotos && topPhotoBirds.length > 0"
    >
      <h3 class="section-title">Top {{ store.numTopPhotos }} Birds</h3>
      <div class="photo-grid">
        <div
          class="photo-card"
          v-for="(bird, i) in topPhotoBirds"
          :key="'top-' + i"
        >
          <img
            v-if="bird.imageUrl"
            :src="bird.imageUrl"
            :alt="bird.Species"
            class="bird-photo"
            referrerpolicy="no-referrer"
          />
          <div class="photo-placeholder" v-else>No Image</div>
          <div class="photo-caption">{{ i + 1 }}. {{ bird.Species }}</div>
        </div>
      </div>
    </div>

    <!-- custom birds section - only if passed via URL -->
    <div class="section bird-table-section" v-if="customBirds.length > 0">
      <h2 class="section-title">Custom Birds</h2>

      <div class="table-header-custom">
        <div style="text-align: right; padding-right: 5px">#</div>
        <!-- Index Header -->
        <div>Species</div>
        <div>Rank</div>
        <div>List Likelihood</div>
        <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
      </div>

      <div
        class="table-row-custom"
        v-for="(bird, i) in customBirds"
        :key="'custom-' + i"
      >
        <div class="index-cell">{{ i + 1 }}.</div>
        <!-- Index Cell -->
        <div class="species-cell">
          <a
            v-if="bird.speciesUrl"
            :href="bird.speciesUrl"
            target="_blank"
            class="species-link"
            >{{ bird.Species }}</a
          >
          <span v-else>{{ bird.Species }}</span>
        </div>
        <div class="cell">{{ bird.Rank }}</div>
        <div class="cell">
          {{ Math.round(10 ** 2 * bird.wtd_rf) / 10 ** 2 }}
        </div>
        <div class="cell">{{ Math.round(10 * bird.rfpc) / 10 }}</div>
      </div>
    </div>

    <!-- custom bird photos grid -->
    <div class="section photos-section" v-if="customBirdPhotos.length > 0">
      <h3 class="section-title">Custom Bird Photos</h3>
      <div class="photo-grid">
        <div
          class="photo-card"
          v-for="(bird, i) in customBirdPhotos"
          :key="'custom-photo-' + i"
        >
          <img
            v-if="bird.imageUrl"
            :src="bird.imageUrl"
            :alt="bird.Species"
            class="bird-photo"
            referrerpolicy="no-referrer"
          />
          <div class="photo-placeholder" v-else>No Image</div>
          <div class="photo-caption">{{ bird.Species }}</div>
        </div>
      </div>
    </div>

    <!-- report footer -->
    <footer class="report-footer">
      <p>Data sourced from eBird.org • Generated by FeatherWeight</p>
    </footer>
  </div>

  <!-- loading state -->
  <div class="loading-container" v-else>
    <p>Loading report data...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed, ref } from "vue";
import { useRoute } from "vue-router";
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import { LineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import type { Bird } from "../types";

Chart.register(...registerables);

export default defineComponent({
  name: "PrintableReport",

  components: {
    LineChart,
  },

  setup() {
    const store = useAnalyticsStore();
    const route = useRoute();

    // custom bird ranks parsed from URL
    const customRanks = ref<number[]>([]);
    const photoRanks = ref<number[]>([]);

    // date passed from client (handles timezone correctly)
    const generatedDate = ref(
      new Date().toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    );

    const birds = computed(() => store.getTopBirds);
    const allBirds = computed(() => store.getAllBirds);
    const topPhotoBirds = computed(() =>
      birds.value.slice(0, store.numTopPhotos)
    );

    // look up custom birds by rank from the full bird list
    const customBirds = computed(() => {
      if (customRanks.value.length === 0 || allBirds.value.length === 0)
        return [];
      return customRanks.value
        .map((rank) => allBirds.value.find((b) => b.Rank === rank))
        .filter((b) => b !== undefined) as Bird[];
    });

    const customBirdPhotos = computed(() => {
      if (photoRanks.value.length === 0 || allBirds.value.length === 0)
        return [];
      return photoRanks.value
        .map((rank) => allBirds.value.find((b) => b.Rank === rank))
        .filter((b) => b !== undefined) as Bird[];
    });

    // chart configuration
    const chartData = computed(() => {
      const birdsData = birds.value;
      const wtdrfData = birdsData.map((b: any) => b.wtd_rf);
      const rfpcData = birdsData.map((b: any) => b.rfpc / 100);

      return {
        labels: birdsData.map((b: any) => b.Species),
        datasets: [
          {
            label: "List Likelihood",
            data: wtdrfData,
            backgroundColor: "#45799980",
            borderColor: "#457999",
            pointRadius: 5,
            pointHoverRadius: 7,
            borderWidth: 2.5,
            tension: 0.1,
          },
          {
            label: "List Likelihood (normalized to top bird)",
            data: rfpcData,
            backgroundColor: "#29623980",
            borderColor: "#296239",
            pointRadius: 5,
            pointHoverRadius: 7,
            borderWidth: 2.5,
            tension: 0.1,
          },
        ],
      };
    });

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 2.5,
      animation: false,
      plugins: {
        legend: {
          position: "top" as const,
          labels: {
            font: { size: 11 },
            padding: 15,
          },
        },
      },
      scales: {
        x: {
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            font: { size: 9 },
            autoSkip: true,
            maxTicksLimit: 30,
          },
          grid: {
            display: false,
          },
        },
        y: {
          beginAtZero: true,
          ticks: { font: { size: 10 } },
          grid: {
            color: "#e0e0e0",
          },
        },
      },
    };

    onMounted(() => {
      const id = route.params.id as string;
      const query = route.query;

      // parse configuration
      if (query.numTopBirds)
        store.numTopBirds = parseInt(query.numTopBirds as string) || 10;
      if (query.numTopPhotos)
        store.numTopPhotos = parseInt(query.numTopPhotos as string) || 3;
      if (query.showGraph !== undefined)
        store.showLikelihoodCurve = query.showGraph === "true";
      if (query.showPhotos !== undefined)
        store.showTopBirdPhotos = query.showPhotos === "true";
      if (query.startYear)
        store.startYear = parseInt(query.startYear as string);
      if (query.endYear) store.endYear = parseInt(query.endYear as string);
      if (query.startMonth)
        store.startMonth = parseInt(query.startMonth as string);
      if (query.startWeek)
        store.startWeek = parseInt(query.startWeek as string);
      if (query.endMonth) store.endMonth = parseInt(query.endMonth as string);
      if (query.endWeek) store.endWeek = parseInt(query.endWeek as string);

      // parse custom bird ranks from url (comma-separated)
      if (query.customRanks) {
        customRanks.value = (query.customRanks as string)
          .split(",")
          .map((r) => parseInt(r))
          .filter((r) => !isNaN(r));
      }
      if (query.photoRanks) {
        photoRanks.value = (query.photoRanks as string)
          .split(",")
          .map((r) => parseInt(r))
          .filter((r) => !isNaN(r));
      }

      // use date from client
      if (query.genDate) {
        generatedDate.value = query.genDate as string;
      }

      if (id) {
        store.selectedHotspotId = id;
        store.fetchHotspotDetail();
      }
    });

    return {
      store,
      birds,
      topPhotoBirds,
      customBirds,
      customBirdPhotos,
      chartData,
      chartOptions,
      generatedDate,
    };
  },
});
</script>

<style>
html,
body {
  height: auto !important;
  overflow: visible !important;
}

@page {
  size: letter;
  margin: 0.5in;
}

@media print {
  body {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    background: white !important;
  }
  html {
    background: white !important;
    height: auto !important;
  }
}
</style>

<style scoped>
.printable-report {
  width: 100%;
  max-width: 7.5in;
  margin: 0 auto;
  background: white;
  color: #222;
  padding: 20px;
  box-sizing: border-box;
}

/* report header */
.report-header {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #296239;
}

.report-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #296239;
  margin: 0 0 5px 0;
}

.generated-date {
  font-size: 11px;
  color: #666;
  margin: 0;
}

/* hotspot info */
.hotspot-info {
  text-align: center;
  margin-bottom: 25px;
}

.hotspot-info h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.hotspot-info .location {
  font-size: 13px;
  color: #666;
  margin: 0;
}

/* sections */
.section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #457999;
  break-after: avoid;
  page-break-after: avoid;
}

/* chart */
.chart-wrapper {
  width: 100%;
  min-height: 220px;
  max-height: 280px;
  break-inside: avoid;
  page-break-inside: avoid;
}

/* bird table */
.bird-table-section {
  padding: 20px 0;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1fr;
  padding: 6px 0;
  border-bottom: 1px solid #e4e4e4;
  font-size: 11px;
  break-inside: avoid;
  page-break-inside: avoid;
}

.table-header-custom,
.table-row-custom {
  display: grid;
  grid-template-columns: 35px 1fr 0.5fr 0.8fr 0.8fr;
  padding: 6px 0;
  border-bottom: 1px solid #e4e4e4;
  font-size: 11px;
  align-items: center;
  break-inside: avoid;
  page-break-inside: avoid;
}

.table-header,
.table-header-custom {
  font-weight: 600;
  background: #f8f8f8;
}

.species-cell {
  display: flex;
  gap: 6px;
  align-items: center;
}

.index {
  color: #888;
  width: 25px;
}

.species-link {
  color: #457999;
  text-decoration: none;
}

.species-link:hover {
  text-decoration: underline;
  color: #296239;
}

.cell {
  text-align: center;
}

.index-cell {
  color: #888;
  width: 25px;
}

/* photo grid */
.photos-section {
  margin-top: 25px;
}

.photo-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.photo-card {
  width: 140px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  break-inside: avoid;
  page-break-inside: avoid;
}

.bird-photo {
  width: 100%;
  height: 110px;
  object-fit: cover;
  display: block;
}

.photo-placeholder {
  width: 100%;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  color: #999;
  font-size: 10px;
}

.photo-caption {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  font-size: 10px;
  font-weight: 500;
  text-align: center;
  background: #f9f9f9;
  border-top: 1px solid #eee;
}

/* report footer */
.report-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
  font-size: 9px;
  color: #888;
}

/* loading */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background: white;
}

.loading-container p {
  font-size: 14px;
  color: #666;
}
</style>
