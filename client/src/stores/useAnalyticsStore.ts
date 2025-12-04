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
    //Maybe we'll need this?? ===============================
    //sortedTopBirds(state) {
    //  return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => b.Rank - a.Rank)
    //},

    //TEMPORARY ============== !!! -> replace later
    getPlacementTopBirds(state) {
      const birds: Bird[] = [
        { Species: "American Robin", Rank: 1, wtd_rf: 12, rfpc: 8, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303441381/2400" },
        { Species: "Mourning Dove", Rank: 2, wtd_rf: 10, rfpc: 7, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60386921/2400" },
        { Species: "House Finch", Rank: 3, wtd_rf: 9, rfpc: 6, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306327341/2400" },
        { Species: "Blue Jay", Rank: 4, wtd_rf: 8, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/311635911/2400" },
        { Species: "Northern Cardinal", Rank: 5, wtd_rf: 7, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/297087301/2400" },
        { Species: "Dark-eyed Junco", Rank: 6, wtd_rf: 6, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/66115711/2400" },
        { Species: "Black-capped Chickadee", Rank: 7, wtd_rf: 5, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302472691/2400" },
        { Species: "European Starling", Rank: 8, wtd_rf: 5, rfpc: 3, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303928891/2400" },
        { Species: "Red-tailed Hawk", Rank: 9, wtd_rf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60384771/2400" },
        { Species: "Canada Goose", Rank: 10, wtd_rf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59953191/2400" },
        { Species: "Great Blue Heron", Rank: 11, wtd_rf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/304479371/2400" },
        { Species: "Bald Eagle", Rank: 12, wtd_rf: 3, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306062281/2400" },
        { Species: "American Goldfinch", Rank: 13, wtd_rf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306710541/2400" },
        { Species: "Downy Woodpecker", Rank: 14, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60397941/2400" },
        { Species: "White-breasted Nuthatch", Rank: 15, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/68039391/2400" },
        { Species: "American Crow", Rank: 16, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59858041/2400" },
        { Species: "Tufted Titmouse", Rank: 17, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302627281/2400" },
        { Species: "Common Grackle", Rank: 18, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/307948931/2400" },
        { Species: "Rock Pigeon", Rank: 19, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308065631/2400" },
        { Species: "Song Sparrow", Rank: 20, wtd_rf: 1, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308771371/2400" },
      ];
      return birds.sort((a, b) => b.Rank - a.Rank).slice(0, state.numTopBirds);
    },

    //Replacement? 
    getTopBirds(state) {
        return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => a.Rank - b.Rank).slice(0, state.numTopBirds);
    },


    getAllPlacementBirds() {
      const birds: Bird[] = [
        { Species: "American Robin", Rank: 1, wtd_rf: 12, rfpc: 8, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303441381/2400" },
        { Species: "Mourning Dove", Rank: 2, wtd_rf: 10, rfpc: 7, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60386921/2400" },
        { Species: "House Finch", Rank: 3, wtd_rf: 9, rfpc: 6, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306327341/2400" },
        { Species: "Blue Jay", Rank: 4, wtd_rf: 8, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/311635911/2400" },
        { Species: "Northern Cardinal", Rank: 5, wtd_rf: 7, rfpc: 5, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/297087301/2400" },
        { Species: "Dark-eyed Junco", Rank: 6, wtd_rf: 6, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/66115711/2400" },
        { Species: "Black-capped Chickadee", Rank: 7, wtd_rf: 5, rfpc: 4, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302472691/240  0" },
        { Species: "European Starling", Rank: 8, wtd_rf: 5, rfpc: 3, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303928891/2400" },
        { Species: "Red-tailed Hawk", Rank: 9, wtd_rf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60384771/2400" },
        { Species: "Canada Goose", Rank: 10, wtd_rf: 4, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59953191/2400" },
        { Species: "Great Blue Heron", Rank: 11, wtd_rf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/304479371/2400" },
        { Species: "Bald Eagle", Rank: 12, wtd_rf: 3, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306062281/2400" },
        { Species: "American Goldfinch", Rank: 13, wtd_rf: 3, rfpc: 2, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/306710541/2400" },
        { Species: "Downy Woodpecker", Rank: 14, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/60397941/2400" },
        { Species: "White-breasted Nuthatch", Rank: 15, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/68039391/2400" },
        { Species: "American Crow", Rank: 16, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/59858041/2400" },
        { Species: "Tufted Titmouse", Rank: 17, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302627281/2400" }, 
        { Species: "Common Grackle", Rank: 18, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/307948931/2400" },
        { Species: "Rock Pigeon", Rank: 19, wtd_rf: 2, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308065631/2400" },
        { Species: "Song Sparrow", Rank: 20, wtd_rf: 1, rfpc: 1, photo: "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/308771371/2400" },
      ];
      return birds.sort((a, b) => a.Rank - b.Rank);
    },

    getAllBirds(state) {
      return [...(state.selectedHotspot?.birds ?? [])].sort((a, b) => a.Rank - b.Rank);
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
      console.log("fetchHotspotDetail called");
      //this.selectedHotspotId = "L901084"; //TEMPORARY
      if (!this.selectedHotspotId) return

      this.isLoading = true
      this.error = null

      try {
        console.log("Fetching hotspot detail for hotspot ID:", this.selectedHotspotId);

        //have to somehow send both the hotspotId and the date range.
        const response = await axios.get(`http://localhost:8000/hotspots/report/${this.selectedHotspotId}`); //update link

        this.selectedHotspot = response.data;

      } catch (e: any) {
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    },

  }
})