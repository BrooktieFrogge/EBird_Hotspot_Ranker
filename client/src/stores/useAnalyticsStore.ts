import { defineStore } from 'pinia'
import type { Bird, Hotspot } from '../types'
import axios from 'axios';

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    // --- Hotspot selection ---
    selectedHotspotName: null as string | null,
    selectedHotspotId: null as string | null,
    selectedHotspot: null as Hotspot | null,
    
    // --- Filters / parameters ---
    selectedHotspotFrequency: Number,
    selectedRegion: String,

    // --- Data ---
    hotspotData:  null as Hotspot | null,
    topBirds: [] as Bird[],

    // --- Analytics Panels / Toggles ---
    yearRange: {
      start: null as number | null,
      end: null as number | null,
    },

    showLikelihoodCurve: false,  
    showTopBirdPhotos: true,
    selectedBirds: [] as Bird[],


    // --- UI-only state ---
    isLoading: false,
    error: null as string | null,
  }),

  getters: {
    sortedTopBirds(state) {
      return [...state.topBirds].sort((a, b) => b.data1 - a.data1)
    },

    //TEMPORARY ============== !!! -> replace later
    getPlacementTopBirds() {
       const birds: Bird[] = [
        { species: "American Robin", data1: 12, data2: 8, photo: "https://placehold.co/300x200" },
        { species: "Mourning Dove", data1: 10, data2: 7, photo: "https://placehold.co/300x200" },
        { species: "House Finch", data1: 9, data2: 6, photo: "https://placehold.co/300x200" },
        { species: "Blue Jay", data1: 8, data2: 5, photo: "https://placehold.co/300x200" },
        { species: "Northern Cardinal", data1: 7, data2: 5, photo: "https://placehold.co/300x200" },
        { species: "Dark-eyed Junco", data1: 6, data2: 4, photo: "https://placehold.co/300x200" },
        { species: "Black-capped Chickadee", data1: 5, data2: 4, photo: "https://placehold.co/300x200" },
        { species: "European Starling", data1: 5, data2: 3, photo: "https://placehold.co/300x200" },
        { species: "Red-tailed Hawk", data1: 4, data2: 2, photo: "https://placehold.co/300x200" },
        { species: "Canada Goose", data1: 4, data2: 2, photo: "https://placehold.co/300x200" },
      ];
      return birds;
    }

  },

  actions: {
    setHotspot(id: string) {
      this.selectedHotspotId = id;
      this.fetchAnalytics();
    },

    setDateRange(start: number, end: number) {
      this.yearRange.start = start;
      this.yearRange.end = end;
      this.fetchAnalytics();
    },

    toggleLikelihoodCurve() {
      this.showLikelihoodCurve = !this.showLikelihoodCurve;
    },

    toggleTopPhotos() {
      this.showTopBirdPhotos = !this.showTopBirdPhotos;
    },

    selectBird(bird: Bird) {
      this.selectedBirds.push(bird);
    },

    async fetchAnalytics() {
      if (!this.selectedHotspotId) return

      this.isLoading = true
      this.error = null

      try {
        // simulate API call

        //have to somehow send both the hotspotId and the date range.
        const response = await axios.get(`/api/hotspots/${this.selectedHotspotId}`); //update link
        
        this.selectedHotspot = response.data;

      } catch (e: any) {
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    }
  }
})
