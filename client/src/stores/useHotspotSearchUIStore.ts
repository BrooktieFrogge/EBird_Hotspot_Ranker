import { defineStore } from "pinia";

// states we want to track
export type HotspotSearchUIState = {
  // text search
  searchQuery: string;

  // country
  countrySearch: string;

  // subregion 1
  subregionSearch: string;
  selectedSubregion: string;

  // subregion 2
  subregion2Search: string;
  selectedSubregion2: string;

  // selected card
  selectedHotspotId: string | null;
};

const STORAGE_KEY = "hotspotSearchUIState_v1"; // key used to save info in local storage 

export const useHotspotSearchUIStore = defineStore("hotspotSearchUI", {
  state: (): HotspotSearchUIState => {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
      try {
        return JSON.parse(saved) as HotspotSearchUIState;
      } catch {
        // corrupted storage → fall back to defaults
      }
    }

    return {
      searchQuery: "",
      countrySearch: "",
      subregionSearch: "",
      selectedSubregion: "",
      subregion2Search: "",
      selectedSubregion2: "",
      selectedHotspotId: null,
    };
  },

  // helper methonds that update the state
  actions: {
    /** Persist current UI state to localStorage */
    persist() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(this.$state)
      );
    },

    /** Clear all filters but keep selected hotspot */
    clearFilters() {
      this.searchQuery = "";
      this.countrySearch = "";
      this.subregionSearch = "";
      this.selectedSubregion = "";
      this.subregion2Search = "";
      this.selectedSubregion2 = "";

      this.persist();
    },

    /** Set & persist selected hotspot id */
    setSelectedHotspotId(id: string | null) {
      this.selectedHotspotId = id;
      this.persist();
    },

    /** Full reset (filters + selection) */
    resetAll() {
      this.searchQuery = "";
      this.countrySearch = "";
      this.subregionSearch = "";
      this.selectedSubregion = "";
      this.subregion2Search = "";
      this.selectedSubregion2 = "";
      this.selectedHotspotId = null;

      localStorage.removeItem(STORAGE_KEY);
    },
  },
});
