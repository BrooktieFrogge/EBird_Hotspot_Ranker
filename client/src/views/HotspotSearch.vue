<template>
  <div class="hotspot-search">
    <!-- LEFT PANEL -->
    <div class="filters">
      <!-- Buttons container  -->
      <div class="buttons-container">
        <div id="home-button" @click="redirectToHomeScreen">
          <div class="back-button-wrapper">
            <BIconHouseFill />
          </div>
        </div>
      </div>

      <h1 class="panel-title">Hotspot Browser</h1>

      <!-- Text search -->
      <div class="filter-group">
        <label for="search">Search by name or location</label>
        <input
          id="search"
          type="text"
          v-model="searchQuery"
          placeholder="Type a hotspot name or location..."
        />
      </div>

      <!-- Country filter -->
      <div class="filter-group">
        <label for="country">Country</label>
        <select id="country" v-model="analyticsStore.selectedCountry">
          <option value="">All countries</option>
          <option
            v-for="country in availableCountries"
            :key="country"
            :value="country"
          >
            {{ country }}
          </option>
        </select>
      </div>

      <div class="filter-summary">
        Showing {{ filteredHotspots.length }} of {{ hotspots.length }} hotspots
      </div>
    </div>

    <!-- MIDDLE PANEL: Hotspot Cards (scrollable) -->
    <div class="results">
      <div class="cards-container">
        <HotspotCard
          v-for="hotspot in filteredHotspots"
          :key="hotspot.id"
          :id="hotspot.id"
          :name="hotspot.name"
          :region="hotspot.region"
          :location="hotspot.location"
          :peak-season="hotspot.peakSeason"
          :color-class="hotspot.colorClass"
          :species-count="hotspot.speciesCount"
          :checklist-count="hotspot.checklistCount"
          :top-birds="hotspot.topBirds"
          :is-saved="hotspot.isSaved"
          @click="goToHotspotDetail"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import HotspotCard from "../components/HotspotCard.vue";


interface Hotspot {
  id: number | string;
  name: string;
  region: string;
  location: string;
  colorClass: string;
  speciesCount: number;
  checklistCount: number;
  isSaved: boolean;
} **/

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
    BIconHouseFill,
  },

  setup() {
    const router = useRouter();

    // state
    const hotspots = ref<Hotspot[]>([]);
    const searchQuery = ref('');
    const selectedRegion = ref('');

    // HARDCODED
    //const hotspots = ref<Hotspot[]>([]);
    //const selectedRegion = ref('');
    //const selectedHotspot = ref<Hotspot | null>(null);

    // REAL DATA USING STORE
    console.log("running setup");
    const analyticsStore = useAnalyticsStore();

    console.log("about to fetch hotspots...");
    analyticsStore.fetchAllHotspots();
    console.log("fetched hotspots...");

    const hotspots = analyticsStore.allHotspots;
      //when you want to access these, use:
      //hotspots = analyticsStore.allHotspots
      //selectedRegion = analyticsStore.selectedCountry
      //selectedHotspot = analyticsStore.selectedHotspot (this is of type DetailedHotspot)



    const availableCountries = computed(() => {
      const set = new Set<string>();
      console.log(hostpots[0]);
      console.log(hostpots);
      hotspots.forEach(h => set.add(h.country));
      //analyticsStore.allHotspots.value.forEach(h => set.add(h.region));
      return Array.from(set).sort();
    });

    // Load all hotspots once (replace this with a real API call)
    const loadHotspots = async () => {


      hotspots.value = [
        {
          id: 1,
          name: 'City Park Lake',
          region: 'Colorado Front Range',
          location: 'Denver, CO',
          colorClass: '#4caf50',
          speciesCount: 185,
          checklistCount: 1320,
          isSaved: true,
        },
        {
          id: 2,
          name: 'Metropolitan Wastewater Ponds',
          region: 'Colorado Front Range',
          location: 'Brighton, CO',
          colorClass: '#ff9800',
          speciesCount: 210,
          checklistCount: 980,
          isSaved: false,
        },
        {
          id: 3,
          name: 'Mountain Trailhead',
          region: 'Rocky Mountains',
          location: 'Estes Park, CO',
          colorClass: '#2196f3',
          speciesCount: 162,
          checklistCount: 430,
          isSaved: false,
        },
        {
          id: 4,
          name: 'Highline Canal Preserve',
          region: 'Colorado Front Range',
          location: 'Littleton, CO',
          colorClass: '#8bc34a',
          speciesCount: 145,
          checklistCount: 720,
          isSaved: true,
        },
        {
          id: 5,
          name: 'Cherry Creek Reservoir',
          region: 'Colorado Front Range',
          location: 'Aurora, CO',
          colorClass: '#f44336',
          speciesCount: 230,
          checklistCount: 1500,
          isSaved: false,
        },
        {
          id: 6,
          name: 'Prairie Grasslands WMA',
          region: 'Eastern Plains',
          location: 'Limon, CO',
          colorClass: '#ffeb3b',
          speciesCount: 120,
          checklistCount: 260,
          isSaved: false,
        },
        {
          id: 7,
          name: 'Foothills Ridge Overlook',
          region: 'Foothills',
          location: 'Golden, CO',
          colorClass: '#03a9f4',
          speciesCount: 134,
          checklistCount: 510,
          isSaved: true,
        },
        {
          id: 8,
          name: 'Wetland Education Boardwalk',
          region: 'Colorado Front Range',
          location: 'Fort Collins, CO',
          colorClass: '#9c27b0',
          speciesCount: 168,
          checklistCount: 640,
          isSaved: false,
        },
        {
          id: 9,
          name: 'Lakeside Migrant Stopover',
          region: 'Western Slope',
          location: 'Grand Junction, CO',
          colorClass: '#ff7043',
          speciesCount: 142,
          checklistCount: 380,
          isSaved: false,
        },
        {
          id: 10,
          name: 'Alpine Tundra Pullout',
          region: 'Rocky Mountains',
          location: 'Trail Ridge Road, CO',
          colorClass: '#607d8b',
          speciesCount: 95,
          checklistCount: 190,
          isSaved: false,
        },
        {
          id: 11,
          name: 'Urban Creek Greenway',
          region: 'Colorado Front Range',
          location: 'Boulder, CO',
          colorClass: '#4caf50',
          speciesCount: 157,
          checklistCount: 820,
          isSaved: true,
        },
        {
          id: 12,
          name: 'Reservoir Overlook Parking Lot',
          region: 'Western Slope',
          location: 'Durango, CO',
          colorClass: '#ffb300',
          speciesCount: 132,
          checklistCount: 340,
          isSaved: false,
        },
        {
          id: 13,
          name: 'Riverbottom Cottonwood Grove',
          region: 'Western Slope',
          location: 'Montrose, CO',
          colorClass: '#8bc34a',
          speciesCount: 158,
          checklistCount: 410,
          isSaved: false,
        },
        {
          id: 14,
          name: 'County Landfill Scrub',
          region: 'Eastern Plains',
          location: 'Burlington, CO',
          colorClass: '#ff5722',
          speciesCount: 110,
          checklistCount: 220,
          isSaved: false,
        },
        {
          id: 15,
          name: 'Riverside Campground Loop',
          region: 'Rocky Mountains',
          location: 'Salida, CO',
          colorClass: '#03a9f4',
          speciesCount: 140,
          checklistCount: 360,
          isSaved: true,
        },
      ];
    };

    // Filtering logic (runs in memory, 1 API call total)
    const filteredHotspots = computed(() => {
      const q = searchQuery.value.trim().toLowerCase();
      //const region = selectedRegion.value;
      const country = analyticsStore.selectedCountry;

      return hotspots.filter(h => {
        const matchesSearch =
          !q ||
          h.name.toLowerCase().includes(q) ||
          h.subregion1.toLowerCase().includes(q);

        const matchesCountry =
          !country || h.country === country;

        return matchesSearch && matchesCountry;
      });
    });

    const goToHotspotDetail = (id: number | string) => {
      router.push({ name: 'HotspotDetail', params: { id } });
    };

    onMounted(() => {
      //loadHotspots();
      console.log("about to fetch hotspots")
      analyticsStore.fetchAllHotspots();
      console.log("fetched hotspots");
    });

    return {
      hotspots,
      analyticsStore,
      searchQuery,
      //selectedRegion,
      availableCountries,
      filteredHotspots,
      goToHotspotDetail,
    };
  },
});
</script>

<style scoped>
.hotspot-search {
  display: flex;
  height: 100vh;
  background: #fafafa;
  color: #222;
  font-family: Arial, sans-serif;
  overflow: hidden;
}

/* LEFT PANEL */
.filters {
  width: 280px;
  padding: 16px;
  border-right: 1px solid #ddd;
  box-sizing: border-box;
  background: #fafafa;
  overflow-y: auto;
}

/* Buttons container  */
.buttons-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 60px;
  border-top: 1px solid #ffffffc9;
  border-bottom: 1px solid #ffffffc9;
  padding-top: 20px;
  padding-inline: 40px;
  padding-bottom: 20px;
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

.back-button-wrapper:hover {
  background-color: #d2d2d2;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  margin-top: 20px;
  margin-bottom: 20px;
}

.filter-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #333;
}

.filter-group input,
.filter-group select {
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #bfbfbf;
  background-color: #ffffff;
  color: #000000;
}

.filter-summary {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #555;
}

/* MIDDLE PANEL: cards */
.results {
  flex: 1.5;
  padding: 20px;
  box-sizing: border-box;
  background: white;
  overflow-y: auto;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-content: flex-start;
}

/* RIGHT PANEL: summary */
.summary-panel {
  width: 320px;
  border-left: 1px solid #ddd;
  box-sizing: border-box;
  padding: 16px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
}

.summary-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.summary-body {
  font-size: 0.95rem;
  color: #333;
  margin: 0 0 0px 0;
}

.summary-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.summary-row {
  display: flex;
  margin-bottom: 6px;
}

.summary-label {
  width: 110px;
  font-weight: 500;
  color: #666;
}

.summary-value {
  flex: 1;
}

.summary-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.detail-button {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #000;
  background: #fff;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
}

.detail-button:disabled {
  border-color: #ccc;
  color: #999;
  cursor: not-allowed;
  background: #f5f5f5;
}

.detail-button:not(:disabled):hover {
  background: #000;
  color: #fff;
}
</style>
