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


    // --- Analytics Panels / Toggles ---
    yearRange: {
      start: null as number | null,
      end: null as number | null,
    },

    numTopBirds: 10,
    showLikelihoodCurve: false,
    showTopBirdPhotos: true,
    selectedBirds: [] as Bird[],


    // --- UI-only state ---
    isLoading: false,
    error: null as string | null,
  }),

  getters: {

    /**
     * Sorts and returns the top N birds for the selected hotspot
     * @param state 
     * @returns Top N birds sorted by Rank
     */
    getTopBirds(state) {
        return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => a.Rank - b.Rank).slice(0, state.numTopBirds);
    },

    /**
     * Returns all birds for the selected hotspot, sorted by Rank
     * @param state 
     * @returns All birds sorted by Rank
     */
    getAllBirds(state) {
      return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => a.Rank - b.Rank);
    }

  },

  actions: {

    setHotspot(id: string) {
      this.selectedHotspotId = id;
      const overview = this.allHotspots.find(h => h.id === id);
      if (overview) {
        // cast to DetailedHotspot temporarily (birds will be empty)
        this.selectedHotspot = { ...overview, birds: [] } as any; 
      }
    },

    setDateRange(start: number, end: number) {
      this.yearRange.start = start;
      this.yearRange.end = end;
      this.fetchHotspotDetail(); // TODO: Maybe make a new api call using date ranges
    },

    /**
     * Toggles the visibility of the likelihood curve in the analytics report
     */
    toggleLikelihoodCurve() {
      this.showLikelihoodCurve = !this.showLikelihoodCurve;
    },

    /**
     * Toggles the visibility of top bird photos in the analytics report
     */
    toggleTopPhotos() {
      this.showTopBirdPhotos = !this.showTopBirdPhotos;
    },

    /**
     * Selects a bird to be highlighted in the analytics report
     * @param bird 
     */
    selectBird(bird: Bird) {
      if (!this.selectedBirds.some(b => b === bird)) {
        this.selectedBirds.push(bird);
      }
    },

    /**
     * Deselects a bird from the analytics report
     * @param bird 
     */
    deselectBird(bird: Bird) {
      console.log("deselected bird");
      this.selectedBirds = this.selectedBirds.filter(b => b !== bird);
      console.log(this.selectedBirds);
    },

    /**
     * Resets the analytics configuration to default values
     */
    resetAnalyticsConfiguration() {
      this.selectedBirds = [];
      this.numTopBirds = 10;
      this.showLikelihoodCurve = false;
      this.showTopBirdPhotos = true;
      this.yearRange = { start: null, end: null };
    },

    /**
     * Resets the selected hotspot
     */
    resetSelectedHotspot() {
      this.selectedHotspotId = null;
      this.selectedHotspot = null;
    },

    async fetchAllHotspots() {
      this.isLoading = true
      this.error = null

      try {
        // simulate API call
        console.log("making a call");
        const num = 100
        const response = await axios.get(`http://localhost:8000/hotspots/browse-hotspots/${num}`); //update link

        console.log("length", response.data);
        this.allHotspots = response.data;

      } catch (e: any) {
        console.log("there was an error");
        console.log(e);
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

        //have to somehow send both the hotspotId and the date range.
        const response = await axios.get(`http://localhost:8000/hotspots/report/${this.selectedHotspotId}`); //update link

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