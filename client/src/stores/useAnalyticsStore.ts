import { defineStore } from 'pinia'

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    // --- Hotspot selection ---
    selectedHotspotName: null as string | null,
    selectedHotspotId: null as string | null,
    
    // --- Filters / parameters ---
    hotspotFrequency: Number,
    region: String,

    // --- Analytics Panels / Toggles ---
    yearRange: {
      start: null as number | null,
      end: null as number | null,
    },

    showLikelihoodCurve: false,  
    showTopBirdPhotos: true,

    // --- Data ---
    topBirds: [] as Array<{ species: string; likelihood: number }>,


    // --- UI-only state ---
    isLoading: false,
    error: null as string | null,
  }),

  getters: {
    sortedTopBirds(state) {
      return [...state.topBirds].sort((a, b) => b.likelihood - a.likelihood)
    }
  },

  actions: {
    setHotspot(id: string) {
      this.selectedHotspotId = id
      this.fetchAnalytics()
    },

    setDateRange(start: number, end: number) {
      this.yearRange.start = start
      this.yearRange.end = end
      this.fetchAnalytics()
    },

    toggleLikelihoodCurve() {
      this.showLikelihoodCurve = !this.showLikelihoodCurve
    },

    toggleTopPhotos() {
      this.showTopBirdPhotos = !this.showTopBirdPhotos
    },

    async fetchAnalytics() {
      if (!this.selectedHotspotId) return

      this.isLoading = true
      this.error = null

      try {
        // simulate API call
        await new Promise(r => setTimeout(r, 400))


        this.topBirds = [
          { species: 'Mallard', likelihood: 0.92 },
          { species: 'Red-tailed Hawk', likelihood: 0.55 },
          { species: 'Black Phoebe', likelihood: 0.44 },
        ]
      } catch (e: any) {
        this.error = e.message ?? 'Unknown error'
      } finally {
        this.isLoading = false
      }
    }
  }
})
