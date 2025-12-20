<template>
  <div
    class="analytics-container"
    v-if="birds.length > 1 && analyticsStore.isLoading == false"
  >
    <!-- graph and bird lists section -->
    <div class="bird-lists-container" v-if="showGraphAndList">
      <!--------------------------->
      <!--- HOTSPOT NAME/HEADER --->
      <!--------------------------->
      <div class="hotspot-header mobile-title-container">
        <span style="padding-bottom: 8px"
          ><BIconGeoAltFill style="margin-right: 15px"
        /></span>
        <h4>
          {{ analyticsStore.selectedHotspot?.name ?? "No Hotspot Selected" }}:
          {{ analyticsStore.selectedHotspot?.country ?? "" }},
          {{ analyticsStore.selectedHotspot?.subregion1 ?? "" }}
        </h4>
      </div>

      <hr />

      <!-- sample size indicator + export button -->
      <div class="report-header-row">
        <span class="checklist-count">
          Based on
          <strong>{{
            analyticsStore.selectedHotspot?.total_sample_size?.toLocaleString() ??
            0
          }}</strong>
          checklists
        </span>
        <v-btn
          color="#296239"
          size="small"
          @click="exportReport"
          :disabled="isExporting"
          class="export-btn"
        >
          <span v-if="!isExporting"
            ><i class="bi bi-upload" style="margin-right: 8px"></i>Export
            PDF</span
          >
          <span v-else>Generating...</span>
        </v-btn>
      </div>

      <!--------------------------->
      <!----- LIKELIHOOD GRAPH ---->
      <!--------------------------->
      <h5>Observation Likelihood</h5>
      <div
        id="linechart"
        style="width: 95%; height: 350px; padding: 10px"
        v-show="
          analyticsStore.showLikelihoodCurve &&
          analyticsStore.selectedHotspot != null &&
          'birds' in analyticsStore.selectedHotspot &&
          analyticsStore.selectedHotspot.birds.length > 0
        "
      >
        <LineChart style="height: 100%" :chartData="chartData" />
      </div>

      <!--------------------------->
      <!-------- TOP BIRDS -------->
      <!--------------------------->
      <div class="bird-table">
        <h2 class="section-title">
          Top {{ analyticsStore.numTopBirds }} Birds
        </h2>

        <div class="table-header">
          <div class="header-index">#</div>
          <div class="header-species">Species</div>
          <div>List Likelihood</div>
          <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
        </div>

        <div class="table-row" v-for="(bird, i) in birds" :key="i">
          <div class="index-cell">{{ i + 1 }}.</div>
          <div class="species-cell">
            <a :href="bird.speciesUrl" target="_blank">{{ bird.Species }}</a>
          </div>

          <div class="cell">
            {{ Math.round(10 ** 2 * bird.wtd_rf) / 10 ** 2 }}
          </div>
          <div class="cell">{{ Math.round(10 * bird.rfpc) / 10 }}</div>
        </div>
      </div>

      <!--------------------------->
      <!-- CUSTOM SELECTED BIRDS -->
      <!--------------------------->
      <div
        id="custom-birds"
        class="bird-table"
        v-show="analyticsStore.selectedBirds.length > 0"
      >
        <h2 class="section-title">Custom Birds</h2>

        <div class="table-header-custom">
          <div style="text-align: right; padding-right: 5px">#</div>
          <!-- New Index Header -->
          <div>Species</div>
          <div>Rank</div>
          <div>List Likelihood</div>
          <div>List Likelihood (normalized to {{ birds[0]?.Species }})</div>
        </div>

        <div
          class="table-row-custom"
          v-for="(bird, i) in analyticsStore.selectedBirds.sort(
            (a, b) => a.Rank - b.Rank
          )"
          :key="i"
        >
          <div class="index-cell">{{ i + 1 }}.</div>
          <!-- New Index Cell -->
          <div class="species-cell">
            <span>
              <a :href="bird.speciesUrl" target="_blank">{{ bird.Species }}</a>
            </span>
          </div>
          <div class="cell">{{ bird.Rank }}</div>
          <div class="cell">
            {{ Math.round(10 ** 2 * bird.wtd_rf) / 10 ** 2 }}
          </div>
          <div class="cell">{{ Math.round(10 * bird.rfpc) / 10 }}</div>
          <div class="cell">
            <div class="icon-btn" @click="analyticsStore.deselectBird(bird)">
              <BIconXCircle />
            </div>
          </div>
          <div class="cell">
            <div
              class="icon-btn"
              @click="analyticsStore.displayBirdPhoto(bird)"
            >
              <BIconCamera />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--------------------------->
    <!-- RIGHT SECTION: Photos -->
    <!--------------------------->

    <!-- Top Three Birds -->
    <div class="photo-column" v-if="showPhotos">
      <div v-show="analyticsStore.showTopBirdPhotos">
        <h5 style="padding-top: 10px">
          Top {{ analyticsStore.numTopPhotos }} Birds
        </h5>
        <div
          class="photo-card"
          v-for="(bird, i) in birds.slice(0, analyticsStore.numTopPhotos)"
          :key="i"
        >
          <img class="photo" :src="bird.imageUrl" alt="" />
          <div class="photo-caption">{{ i + 1 }}. {{ bird.Species }}</div>
        </div>
      </div>

      <!-- Custom Selected Birds -->
      <div
        v-if="analyticsStore.selectedBirdPhotos.length > 0"
        class="custom-birds-section"
      >
        <hr />
        <h5 style="padding-top: 10px">Custom Birds</h5>
        <div class="custom-birds-gallery">
          <div
            class="photo-card"
            v-for="(bird, i) in analyticsStore.selectedBirdPhotos"
            :key="i"
          >
            <img class="photo" :src="bird.imageUrl" alt="" />
            <div class="photo-caption">
              {{ bird.Species }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!---------------------------->
  <!-- DEFAULT: Loading Image -->
  <!---------------------------->
  <div class="loading-screen" v-else>
    <img class="loading-photo" :src="loadingImage" alt="" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, watch, ref } from "vue";
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import {
  BIconXCircle,
  BIconCamera,
  BIconGeoAltFill,
} from "bootstrap-icons-vue";
import { LineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default defineComponent({
  name: "HotspotAnalyticsReport",

  components: {
    BIconXCircle,
    BIconCamera,
    BIconGeoAltFill,
    LineChart,
  },

  props: {
    showGraphAndList: {
      type: Boolean,
      default: true,
    },
    showPhotos: {
      type: Boolean,
      default: true,
    },
  },

  setup(props) {
    const analyticsStore = useAnalyticsStore();
    const birds = computed(() => analyticsStore.getTopBirds);

    const loadingImage =
      "https://cdn.pixabay.com/animation/2024/07/04/20/46/20-46-07-872_512.gif";

    // Theme-aware colors
    const isDarkMode = computed(() =>
      document.body.classList.contains("theme--dark")
    );

    // Data for the Likelihood Graph
    const chartData = computed(() => {
      const wtdrfData = birds.value.map((b: any) => b.wtd_rf);
      const rfpcData = birds.value.map((b: any) => b.rfpc / 100);

      // Theme-aware chart colors (matching UI color system)
      const primaryColor = isDarkMode.value ? "#7eb8d9" : "#457999"; // Blue: matches --color-primary
      const secondaryColor = isDarkMode.value ? "#5db667" : "#296239"; // Green: matches --color-secondary

      return {
        labels: birds.value.map((b: any) => b.Species),
        datasets: [
          {
            label: "List Likelihood",
            data: wtdrfData,
            backgroundColor: isDarkMode.value ? "#7eb8d940" : "#45799940",
            borderColor: primaryColor,
            pointRadius: 6,
            pointHoverRadius: 10,
          },
          {
            label: "List Likelihood (normalized to top bird)",
            data: rfpcData,
            backgroundColor: isDarkMode.value ? "#5db66740" : "#29623940",
            borderColor: secondaryColor,
            pointRadius: 6,
            pointHoverRadius: 10,
          },
        ],
      };
    });

    // export state
    const isExporting = ref(false);

    // export to PDF using the endpoint
    const exportReport = async () => {
      if (!analyticsStore.selectedHotspotId || isExporting.value) return;

      isExporting.value = true;

      try {
        // build URL for PDF endpoint with current config
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

        // pass custom bird ranks only
        if (analyticsStore.selectedBirds.length > 0) {
          const ranks = analyticsStore.selectedBirds.map((b: any) => b.Rank);
          params.append("custom_ranks", ranks.join(","));
        }
        if (analyticsStore.selectedBirdPhotos.length > 0) {
          const photoRanks = analyticsStore.selectedBirdPhotos.map(
            (b: any) => b.Rank
          );
          params.append("photo_ranks", photoRanks.join(","));
        }

        // pass the current date from client
        const today = new Date().toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
        params.append("gen_date", today);

        const pdfUrl = `/api/hotspots/report/${
          analyticsStore.selectedHotspotId
        }/pdf?${params.toString()}`;

        // open PDF in new tab
        window.open(pdfUrl, "_blank");
      } catch (error) {
        console.error("Export failed:", error);
        alert("Failed to generate PDF. Please try again.");
      } finally {
        isExporting.value = false;
      }
    };

    watch(analyticsStore.selectedBirds, () => {
      const element = document.getElementById("custom-birds");
      console.log("CALLED");
      setTimeout(() => {
        element?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 0);
    });

    return {
      analyticsStore,
      birds,
      loadingImage,
      chartData,
      isExporting,
      exportReport,
      showGraphAndList: props.showGraphAndList,
      showPhotos: props.showPhotos,
    };
  },
});
</script>

<style scoped>
.analytics-container {
  display: flex;
  gap: 24px;
  padding: 40px;
  height: 100%; /* fix desktop clipping: match parent height, don't force viewport height */
  background: transparent; /* use parent background for seamless look */
  color: var(--color-text-primary);
  overflow-anchor: none; /* suppress browser scroll anchoring warnings (Chart.js/Resize) */
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

.bird-lists-container {
  display: block;
  gap: 24px;
  width: 100vh;
  color: var(--color-text-primary);
  opacity: 100%;
}

.hotspot-header {
  display: flex;
  align-items: center;
  margin-top: 5px;
  font-size: 0.9em;
  padding-left: 20px;
}

/* report header row - contains checklist count and export button */
.report-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 8px 0;
}

.checklist-count {
  font-size: 12px;
  color: var(--color-text-muted);
}

.export-btn {
  margin-left: auto;
  color: white !important;
  background-color: #296239 !important;
  border: 1px solid #296239 !important;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background-color: white !important;
  color: #296239 !important;
  border-color: #296239 !important;
}

.export-btn:hover :deep(.v-btn__content),
.export-btn:hover :deep(.v-btn__overlay) {
  color: #296239 !important;
}

.export-btn :deep(.v-btn__overlay) {
  opacity: 0 !important;
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
  grid-template-columns: 40px 1.2fr 1fr 1fr;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border-light);
}

.table-header-custom,
.table-row-custom {
  display: grid;
  grid-template-columns: 35px 1fr 0.5fr 0.8fr 0.8fr 0.2fr 0.2fr; /* Added index column */
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border-light);
}

.table-header {
  font-weight: 600;
  text-align: center;
  align-items: center;
}

.table-header > div {
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-header-custom {
  font-weight: 600;
  text-align: center;
  align-items: center;
}

.table-header-custom > div {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* index column */
.index-cell,
.header-index {
  text-align: right;
  padding-right: 8px;
  color: #888;
}

/* species column */
.species-cell,
.header-species {
  text-align: center;
}

.species-cell a {
  color: #457999;
  text-decoration: none;
}

.species-cell a:hover {
  text-decoration: underline;
  color: #296239;
}

.cell {
  text-align: center;
}

.icon-btn {
  color: var(--color-secondary);
  cursor: pointer;
  transition: color 0.2s ease;
}

.icon-btn:hover {
  color: var(--color-primary);
}

.photo-column {
  width: 220px;
  flex-shrink: 0;
}

.photo-card {
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
  background: var(--color-bg-panel);
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

.loading-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
  padding: 0;
  margin: 0;
  min-height: 100%;
  height: 100%;
  width: 100%;
  background: transparent; /* Use parent container background */
  color: var(--color-text-primary);
  box-sizing: border-box;
}

.loading-photo {
  width: 200px;
  height: 200px;
  object-fit: contain;
}

/* ===============================
    responsive styles
   =============================== */

@media (max-width: 768px) {
  .analytics-container {
    flex-direction: column;
    padding: 16px;
    height: auto;
    gap: 16px;
  }

  .bird-lists-container {
    width: 100%;
  }

  .hotspot-header {
    padding-left: 0;
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .hotspot-header span {
    display: flex;
    justify-content: center;
  }

  .hotspot-header h4 {
    font-size: 0.85em;
    padding-left: 0;
    text-align: center;
  }

  .bird-table {
    padding: 16px 0;
  }

  .section-title {
    font-size: 16px;
  }

  /* table */
  .table-header,
  .table-row {
    grid-template-columns: 30px 1fr 0.6fr 0.8fr;
    font-size: 0.8rem;
  }

  .table-header-custom,
  .table-row-custom {
    grid-template-columns: 35px 1.2fr 0.4fr 0.6fr 0.8fr 0.2fr 0.2fr;
    font-size: 0.75rem;
    align-items: center;
  }

  .species-cell {
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .index-cell {
    font-size: 0.75rem;
  }

  /* graph responsive */
  #linechart {
    width: 100% !important;
    height: 250px !important;
    padding: 5px !important;
  }

  /* photo column */
  .photo-column {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* top 3 birds grid */
  .photo-column > div:first-child {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }

  /* custom birds grid */
  .custom-birds-gallery {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }

  .custom-birds-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* photo card */
  .photo-card {
    width: calc(50% - 10px);
    max-width: 200px;
    height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-bottom: 0;
  }

  .photo {
    height: 140px;
    width: 100%;
    object-fit: cover;
    flex-shrink: 0;
  }

  .photo-caption {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    font-size: 0.85rem;
    text-align: center;
    line-height: 1.2;
  }

  /* section headers */
  .photo-column h5 {
    width: 100%;
    text-align: center;
    margin-bottom: 12px;
  }

  /* loading screen */
  .loading-screen {
    padding: 100px 20px;
  }

  .loading-screen {
    padding: 0;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    display: flex;
  }

  .loading-photo {
    width: 85vw;
    max-width: 400px;
    height: auto;
  }
}

/* ===============================
  tablet T-Layout (769px - 1330px)
  =============================== */

@media (min-width: 769px) and (max-width: 1330px) {
  .analytics-container {
    flex-direction: column;
    padding: 16px;
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .bird-lists-container {
    width: 100%;
    order: 1;
    overflow: visible;
  }

  /* photo column */
  .photo-column {
    width: 100%;
    order: 2;
    padding: 24px 0 40px;
    margin-top: 24px;
  }

  /* photo column header */
  .photo-column h5 {
    font-size: 1.1rem;
    color: var(--color-primary);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(69, 121, 153, 0.2);
    text-align: left;
    width: 100%;
  }

  /* top 3 birds section */
  .photo-column > div:first-child {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    align-items: flex-start;
    margin-bottom: 24px;
  }

  /* custom birds section */
  .photo-column > div:nth-child(2) {
    display: block;
    width: 100%;
  }

  .custom-birds-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    align-items: flex-start;
  }

  .photo-card {
    flex: 0 0 auto;
    width: 180px;
    max-width: 200px;
    height: auto;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background: var(--color-bg-panel);
    border-radius: 10px;
    box-shadow: var(--shadow-card);
    overflow: hidden;
    margin-bottom: 8px;
  }

  .photo-caption {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
  }

  .photo {
    width: 100%;
    height: 140px;
    object-fit: cover;
  }

  .photo-caption {
    padding: 8px 10px;
    font-size: 0.85rem;
  }

  #linechart {
    width: 100% !important;
    height: 280px !important;
    padding: 5px !important;
  }

  .table-header,
  .table-row,
  .table-header-custom,
  .table-row-custom {
    font-size: 0.85rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 40px 1.2fr 0.8fr 1fr;
  }

  .species-cell {
    text-align: center;
  }

  .species-cell a {
    text-align: center;
  }

  .bird-table {
    padding: 12px 0;
  }

  .section-title {
    font-size: 16px;
  }

  .hotspot-header h4 {
    font-size: 0.9em;
  }

  .custom-birds-section {
    width: 100%;
  }

  .custom-birds-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: flex-start;
    align-items: flex-start;
    margin-top: 12px;
  }

  .photo-column > div:first-child {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    gap: 16px;
    justify-content: flex-start;
    align-items: flex-start;
    margin-bottom: 24px;
  }

  .photo-column > div:nth-child(2) {
    display: block;
    width: 100%;
  }

  .photo-column {
    padding: 24px;
    text-align: center;
  }

  .custom-birds-gallery {
    justify-content: center !important;
  }
  .photo-column > div:first-child {
    justify-content: center !important;
  }
}

.analytics-container {
  padding-bottom: 120px;
}

@media (max-width: 768px) {
  .analytics-container {
    min-height: 100vh;
    padding: 16px;
    padding-top: 24px;
    padding-bottom: 95px;
    box-sizing: border-box;
  }

  .mobile-title-container {
    background-color: var(--color-bg-muted);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
}
</style>
