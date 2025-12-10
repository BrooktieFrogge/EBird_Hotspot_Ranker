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

    // search/filter text that UI can bind to
    searchHotspotName: '' as string,      
    searchCountry: '' as string,          
    searchSubregion1: '' as string,       
    searchSubregion2: '' as string,       

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
      this.startYear = 1900;
      this.endYear = 2025; //TODO: make this update to this year
      this.startMonth = 1;
      this.startWeek = 1;
      this.endMonth = 4;
      this.endWeek = 4;
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
          `/api/hotspots/browse-hotspots`
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

    // use the /hotspots/search endpoint and update allHotspots
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
          '/api/hotspots/search',
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
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          console.warn('No hotspots matched search, clearing list.');
          this.allHotspots = [];
          this.error = null; // no "error" message for the user, just empty results
        } else {
          console.error('Error searching hotspots:', e)
          this.error = e.message ?? 'Unknown error'
        }
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
      const url = `/api/hotspots/report/${this.selectedHotspotId}`;
      
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
