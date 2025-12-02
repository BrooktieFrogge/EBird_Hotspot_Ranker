<template>
  <div class="hotspot-search">

    <!-- LEFT PANEL -->
    <div class="filters">

      <!-- Buttons container  -->
      <div class="buttons-container">
        <div id="home-button" @click="redirectToWelcomeScreen">
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

      <!-- Region filter -->
      <div class="filter-group">
        <label for="region">Region</label>
        <select id="region" v-model="selectedRegion">
          <option value="">All regions</option>
          <option
            v-for="region in availableRegions"
            :key="region"
            :value="region"
          >
            {{ region }}
          </option>
        </select>
      </div>

      <div class="filter-summary">
        Showing {{ filteredHotspots.length }} of {{ hotspots.length }} hotspots
      </div>
    </div>

    <!-- RIGHT PANEL: Hotspot Cards -->
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
import { BIconHouseFill } from 'bootstrap-icons-vue';

interface Hotspot {
  id: number | string;
  name: string;
  region: string;
  location: string;
  peakSeason: string;
  colorClass: string;
  speciesCount: number;
  checklistCount: number;
  topBirds: string[];
  isSaved: boolean;
}

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
    BIconHouseFill,
  },

  setup() {
    const router = useRouter();

    const hotspots = ref<Hotspot[]>([]);
    const searchQuery = ref('');
    const selectedRegion = ref('');

    const availableRegions = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach(h => set.add(h.region));
      return Array.from(set).sort();
    });

    // Load hotspot data (replace with API later)
    const loadHotspots = async () => {
      hotspots.value = [
        {
          id: 1,
          name: 'City Park Lake',
          region: 'Colorado Front Range',
          location: 'Denver, CO',
          peakSeason: 'April–May',
          colorClass: '#4caf50',
          speciesCount: 180,
          checklistCount: 1200,
          topBirds: ['American Robin', 'Mallard', 'House Finch'],
          isSaved: true,
        },
        {
          id: 2,
          name: 'Wetlands Reserve',
          region: 'Colorado Front Range',
          location: 'Brighton, CO',
          peakSeason: 'May–June',
          colorClass: '#ff9800',
          speciesCount: 210,
          checklistCount: 900,
          topBirds: ['Red-winged Blackbird', 'American Avocet', 'Killdeer'],
          isSaved: false,
        },
        {
          id: 3,
          name: 'Mountain Trailhead',
          region: 'Rocky Mountains',
          location: 'Estes Park, CO',
          peakSeason: 'June–July',
          colorClass: '#2196f3',
          speciesCount: 160,
          checklistCount: 400,
          topBirds: ["Steller's Jay", 'Mountain Chickadee', "Clark's Nutcracker"],
          isSaved: false,
        },
      ];
    };

    const filteredHotspots = computed(() => {
      const q = searchQuery.value.trim().toLowerCase();
      const region = selectedRegion.value;

      return hotspots.value.filter(h => {
        const matchesSearch =
          !q ||
          h.name.toLowerCase().includes(q) ||
          h.location.toLowerCase().includes(q);

        const matchesRegion =
          !region || h.region === region;

        return matchesSearch && matchesRegion;
      });
    });

    const goToHotspotDetail = (id: number | string) => {
      router.push({ name: 'HotspotDetail', params: { id } });
    };

    const redirectToWelcomeScreen = () => {
      router.push({ name: 'HomeScreen' });
    };

    onMounted(() => {
      loadHotspots();
    });

    return {
      hotspots,
      searchQuery,
      selectedRegion,
      availableRegions,
      filteredHotspots,
      goToHotspotDetail,
      redirectToWelcomeScreen,
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
}

/* LEFT PANEL */
.filters {
  width: 280px;
  padding: 16px;
  border-right: 1px solid #ddd;
  box-sizing: border-box;
  background: #fafafa;
}

/* Buttons container  */
.buttons-container {
  display: flex;
  justify-content: center; /* center home button */
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

/* RIGHT PANEL */
.results {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  background: white;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
</style>
