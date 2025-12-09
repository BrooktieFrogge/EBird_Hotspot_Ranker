import { defineStore } from 'pinia'
import type { Bird, HotspotOverview, DetailedHotspot } from '../types'
import axios from 'axios';

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    // --- Hotspot data ---
    allHotspots: [] as Array<HotspotOverview>,
    selectedHotspotName: null as string | null,
    selectedHotspotId: null as string | null,
    selectedHotspot: null as DetailedHotspot | null,

    // --- Filters / parameters ---
    selectedSpeciesCount: null as number | null,
    selectedCountry: null as string | null,

    // NEW: search/filter text that UI can bind to
    searchHotspotName: '' as string,      // NEW
    searchCountry: '' as string,          // NEW
    searchSubregion1: '' as string,       // NEW
    searchSubregion2: '' as string,       // NEW

    // --- Analytics Panels / Toggles ---
    yearRange: {
      start: null as number | null,
      end: null as number | null,
    },

    numTopBirds: 10,
    showLikelihoodCurve: true,
    showTopBirdPhotos: true,
    selectedBirds: [] as Bird[],

    // --- UI-only state ---
    isLoading: false,
    error: null as string | null,
  }),

  getters: {
    getTopBirds(state) {
      return [...(state.selectedHotspot?.birds ?? [])]
        .sort((a, b) => a.Rank - b.Rank)
        .slice(0, state.numTopBirds);
    },

    getAllBirds(state) {
      return [...(state.selectedHotspot?.birds ?? [])]
        .sort((a, b) => a.Rank - b.Rank);
    }
  },

  actions: {
    setHotspot(id: string) {
      this.selectedHotspotId = id;
      const overview = this.allHotspots.find(h => h.id === id);
      if (overview) {
        this.selectedHotspot = { ...overview, birds: [] } as any; 
      }
    },

    setDateRange(start: number, end: number) {
      this.yearRange.start = start;
      this.yearRange.end = end;
      this.fetchHotspotDetail();
    },

    toggleLikelihoodCurve() {
      this.showLikelihoodCurve = !this.showLikelihoodCurve;
    },

    toggleTopPhotos() {
      this.showTopBirdPhotos = !this.showTopBirdPhotos;
    },

    selectBird(bird: Bird) {
      if (!this.selectedBirds.some(b => b === bird)) {
        this.selectedBirds.push(bird);
      }
    },

    deselectBird(bird: Bird) {
      console.log("deselected bird");
      this.selectedBirds = this.selectedBirds.filter(b => b !== bird);
      console.log(this.selectedBirds);
    },

    resetAnalyticsConfiguration() {
      this.selectedBirds = [];
      this.numTopBirds = 10;
      this.showLikelihoodCurve = true;
      this.showTopBirdPhotos = true;
      this.yearRange = { start: null, end: null };
    },

    resetSelectedHotspot() {
      this.selectedHotspotId = null;
      this.selectedHotspot = null;
    },

    async fetchAllHotspots() {
      this.isLoading = true
      this.error = null

      try {
        const response = await axios.get(
          `http://localhost:8000/hotspots/browse-hotspots`
        );
        this.allHotspots = response.data;
      } catch (e: any) {
        console.log("there was an error");
        console.log(e);
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    },

    // NEW: use the /hotspots/search endpoint and update allHotspots
    async searchHotspots(options?: {
      hotspot?: string
      country?: string
      subregion1?: string
      subregion2?: string
      mode?: 'hotspot' | 'country' | 'subregion1' | 'subregion2' | null
    }) {
      this.isLoading = true
      this.error = null

      try {
        const {
          hotspot = this.searchHotspotName || '',
          country = this.searchCountry || '',
          subregion1 = this.searchSubregion1 || '',
          subregion2 = this.searchSubregion2 || '',
          mode = 'hotspot',
        } = options || {}

        const response = await axios.get(
          'http://localhost:8000/hotspots/search',
          {
            params: {
              hotspot,
              country,
              subregion1,
              subregion2,
              mode,
            },
          }
        )

        this.allHotspots = response.data.results
      } catch (e: any) {
        console.error('Error searching hotspots:', e)
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    },

    async fetchHotspotDetail() {
      if (!this.selectedHotspotId) return

      this.isLoading = true
      this.error = null

      try {
        console.log("Fetching hotspot detail for hotspot ID:", this.selectedHotspotId);

        // if you later want year filters, add params here
        const response = await axios.get(
          `http://localhost:8000/hotspots/report/${this.selectedHotspotId}`
        );

        this.selectedHotspot = response.data;
        console.log("Fetched hotspot detail:", response.data);

      } catch (e: any) {
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    },
  }
})
