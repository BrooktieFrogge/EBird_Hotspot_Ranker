import { defineStore } from 'pinia'
import type { Bird, HotspotOverview, DetailedHotspot } from '../types'
import axios from 'axios';

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    // --- Hotspot data ---
    allHotspots: [] as HotspotOverview[],
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
    //Maybe we'll need this?? ===============================
    //sortedTopBirds(state) {
    //  return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => b.rank - a.rank)
    //},

    //TEMPORARY ============== !!! -> replace later
    getPlacementTopBirds(state) {
      const birds: Bird[] = [
        { species: "American Robin", rank: 1, wtdrf: 12, rfpc: 8, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303441381/2400" },
        { species: "Mourning Dove", rank: 2, wtdrf: 10, rfpc: 7, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60386921/2400" },
        { species: "House Finch", rank: 3, wtdrf: 9, rfpc: 6, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306327341/2400" },
        { species: "Blue Jay", rank: 4, wtdrf: 8, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/311635911/2400" },
        { species: "Northern Cardinal", rank: 5, wtdrf: 7, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/297087301/2400" },
        { species: "Dark-eyed Junco", rank: 6, wtdrf: 6, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/66115711/2400" },
        { species: "Black-capped Chickadee", rank: 7, wtdrf: 5, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302472691/2400" },
        { species: "European Starling", rank: 8, wtdrf: 5, rfpc: 3, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303928891/2400" },
        { species: "Red-tailed Hawk", rank: 9, wtdrf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60384771/2400" },
        { species: "Canada Goose", rank: 10, wtdrf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59953191/2400" },
        { species: "Great Blue Heron", rank: 11, wtdrf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/304479371/2400" },
        { species: "Bald Eagle", rank: 12, wtdrf: 3, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306062281/2400" },
        { species: "American Goldfinch", rank: 13, wtdrf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306710541/2400" },
        { species: "Downy Woodpecker", rank: 14, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60397941/2400" },
        { species: "White-breasted Nuthatch", rank: 15, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/68039391/2400" },
        { species: "American Crow", rank: 16, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59858041/2400" },
        { species: "Tufted Titmouse", rank: 17, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302627281/2400" },
        { species: "Common Grackle", rank: 18, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/307948931/2400" },
        { species: "Rock Pigeon", rank: 19, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308065631/2400" },
        { species: "Song Sparrow", rank: 20, wtdrf: 1, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308771371/2400" },
      ];
      return birds.sort((a, b) => b.rank - a.rank).slice(0, state.numTopBirds);
    },

    //Replacement? 
    getTopBirds(state) {
        return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => b.rank - a.rank).slice(0, state.numTopBirds);
    },


    getAllPlacementBirds() {
      const birds: Bird[] = [
        { species: "American Robin", rank: 1, wtdrf: 12, rfpc: 8, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303441381/2400" },
        { species: "Mourning Dove", rank: 2, wtdrf: 10, rfpc: 7, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60386921/2400" },
        { species: "House Finch", rank: 3, wtdrf: 9, rfpc: 6, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306327341/2400" },
        { species: "Blue Jay", rank: 4, wtdrf: 8, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/311635911/2400" },
        { species: "Northern Cardinal", rank: 5, wtdrf: 7, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/297087301/2400" },
        { species: "Dark-eyed Junco", rank: 6, wtdrf: 6, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/66115711/2400" },
        { species: "Black-capped Chickadee", rank: 7, wtdrf: 5, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302472691/240  0" },
        { species: "European Starling", rank: 8, wtdrf: 5, rfpc: 3, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303928891/2400" },
        { species: "Red-tailed Hawk", rank: 9, wtdrf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60384771/2400" },
        { species: "Canada Goose", rank: 10, wtdrf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59953191/2400" },
        { species: "Great Blue Heron", rank: 11, wtdrf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/304479371/2400" },
        { species: "Bald Eagle", rank: 12, wtdrf: 3, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306062281/2400" },
        { species: "American Goldfinch", rank: 13, wtdrf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306710541/2400" },
        { species: "Downy Woodpecker", rank: 14, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60397941/2400" },
        { species: "White-breasted Nuthatch", rank: 15, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/68039391/2400" },
        { species: "American Crow", rank: 16, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59858041/2400" },
        { species: "Tufted Titmouse", rank: 17, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302627281/2400" }, 
        { species: "Common Grackle", rank: 18, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/307948931/2400" },
        { species: "Rock Pigeon", rank: 19, wtdrf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308065631/2400" },
        { species: "Song Sparrow", rank: 20, wtdrf: 1, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308771371/2400" },
      ];
      return birds.sort((a, b) => a.rank - b.rank);
    },

    getAllBirds(state) {
      return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => a.rank - b.rank);
    }

  },

  actions: {
    setHotspot(id: string) {
      this.selectedHotspotId = id;
      this.fetchHotspotDetail();
    },

    setDateRange(start: number, end: number) {
      this.yearRange.start = start;
      this.yearRange.end = end;
      this.fetchHotspotDetail(); // TODO: Maybe make a new api call using date ranges
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

    async fetchAllHotspots() {
      this.isLoading = true
      this.error = null

      try {
        // simulate API call
        const response = await axios.get(`'http://localhost:8000/`); //update link

        this.allHotspots = response.data;

      } catch (e: any) {
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

        //have to somehow send both the hotspotId and the date range.
        const response = await axios.get(`'http://localhost:8000/api/${this.selectedHotspotId}`); //update link

        this.selectedHotspot = response.data;

      } catch (e: any) {
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    },

  }
})