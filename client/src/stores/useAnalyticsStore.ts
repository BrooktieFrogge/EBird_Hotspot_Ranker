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
    startYear: null as number | null,
    endYear: null as number | null,
    startMonth: null as number | null,
    startWeek: null as number | null,
    endMonth: null as number | null,
    endWeek: null as number | null,

    numTopBirds: 10,
    showLikelihoodCurve: true,
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

    setYearRange(start: number, end: number) {
      this.startYear = start;
      this.endYear = end;
      this.fetchHotspotDetail(); // TODO: Maybe make a new api call using date ranges
    },

    setTimeFrame(startMonth: number, startWeek: number, endMonth: number, endWeek: number) {
      this.startMonth = startMonth;
      this.startWeek = startWeek;
      this.endMonth = endMonth;
      this.endWeek = endWeek;
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
      this.showLikelihoodCurve = true;
      this.showTopBirdPhotos = true;
      this.startYear = 1900;
      this.endYear = 2025; //TODO: make this update to this year
      this.startMonth = 1;
      this.startWeek = 1;
      this.endMonth = 4;
      this.endWeek = 4;
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
         // const num = 100
        const response = await axios.get(`http://localhost:8000/hotspots/browse-hotspots`); //update link -now a query param

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

    // 1. Prepare the query parameters object
    const params = {
        start_yr: this.startYear,
        end_yr: this.endYear,
        start_month: this.startMonth,
        start_week: this.startWeek,
        end_month: this.endMonth,
        end_week: this.endWeek,
    };

    // 2. Construct the base URL using the path parameter
    const url = `http://localhost:8000/hotspots/report/${this.selectedHotspotId}`;
    
    try {
        console.log("Fetching hotspot detail for hotspot ID:", this.selectedHotspotId);

        const response = await axios.get(url, { params }); 

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