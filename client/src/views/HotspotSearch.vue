<template>
  <div class="hotspot-search">

    <!-- Left panel: filters -->
    <div class="filters">
      <h1>Hotspot Browser</h1>

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

      <!-- More filters here later -->

      <div class="filter-summary">
        Showing {{ filteredHotspots.length }} of {{ hotspots.length }} hotspots
      </div>
    </div>

    <!-- Right panel: hotspot cards -->
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
  peakSeason: string;
  colorClass: string; // could map to eBird colors
  speciesCount: number;
  checklistCount: number;
  topBirds: string[];
  isSaved: boolean;
}

export default defineComponent({
  name: 'HotspotSearch',

  components: {
    HotspotCard,
  },

  setup() {
    const router = useRouter();

    // state
    const hotspots = ref<Hotspot[]>([]);
    const searchQuery = ref('');
    const selectedRegion = ref('');

    const availableRegions = computed(() => {
      const set = new Set<string>();
      hotspots.value.forEach(h => set.add(h.region));
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
          topBirds: ['Steller\'s Jay', 'Mountain Chickadee', 'Clark\'s Nutcracker'],
          isSaved: false,
        },
      ];
    };

    // Filtering logic (runs in memory, 1 API call total)
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
    };
  },
});
</script>

<style scoped>
.hotspot-search {
  display: flex;
  height: 100%;
  min-height: 100vh;
  background-color: #121212;
  color: #f5f5f5;
}

/* Left panel – filters */
.hotspot-search {
  display: flex;
  height: 100%;
  min-height: 100vh;
  background-color: #D09B2C; /* white background */
  color: #000000; /* black text */
  font-family: Arial, sans-serif;
}

/* Left panel – filters */
.filters {
  width: 280px;
  padding: 20px;
  border-right: 1px solid #d0d0d0; /* light gray line */
  box-sizing: border-box;
  background-color: #ffffff;
}

.filters h1 {
  margin-top: 0;
  font-size: 1.4rem;
  margin-bottom: 16px;
  color: #D09B2C; /* yello text */
}

.filter-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #D09B2C; /* yellow */
}

.filter-group input,
.filter-group select {
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #bfbfbf;
  background-color: #ffffff;
  color: #000000;
  font-size: 0.9rem;
}

.filter-summary {
  margin-top: 8px;
  font-size: 0.8rem;
  color: #D09B2C;
}

/* Right panel – results */
.results {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  background-color: #ffffff;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  background-color: #ffffff;

}
</style>
