import { defineStore } from "pinia";
import type { Bird, HotspotOverview, DetailedHotspot } from "../types";
import axios from "axios";

export const useAnalyticsStore = defineStore("analytics", {
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
    searchHotspotName: "" as string,
    searchCountry: "" as string,
    searchSubregion1: "" as string,
    searchSubregion2: "" as string,

    // suggestions from backend search
    countrySuggestions: [] as string[],
    subregion1Suggestions: [] as string[],
    subregion2Suggestions: [] as string[],
    hotspotSuggestions: [] as string[],

    // pagination for browse-hotspots (for infinite scroll)
    hotspotsOffset: 0,
    hotspotsLimit: 20,
    hotspotsHasMore: true,

    // prefetch cache for faster scroll (warms up DB connection)
    _prefetchedData: null as HotspotOverview[] | null,
    _prefetchedOffset: null as number | null,

    // --- Analytics Panels / Toggles ---
    // dynamic year defaults: current year and 20 years prior
    startYear: new Date().getFullYear() - 20,
    endYear: new Date().getFullYear(),
    startMonth: 1,
    startWeek: 1,
    endMonth: 12,
    endWeek: 4,

    numTopBirds: 10,
    numTopPhotos: 3,
    showLikelihoodCurve: true,
    showTopBirdPhotos: true,
    selectedBirds: [] as Bird[],
    selectedBirdPhotos: [] as Bird[],

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
      return [...(state.selectedHotspot?.birds ?? [])].sort(
        (a, b) => a.Rank - b.Rank
      );
    },
  },

  actions: {
    setHotspot(id: string) {
      this.selectedHotspotId = id;
      const overview = this.allHotspots.find((h) => h.id === id);
      if (overview) {
        this.selectedHotspot = { ...overview, birds: [] } as any;
      }
    },

    setYearRange(start: number, end: number) {
      this.startYear = start;
      this.endYear = end;
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
      if (!this.selectedBirds.some((b) => b === bird)) {
        this.selectedBirds.push(bird);
      }
    },

    deselectBird(bird: Bird) {
      console.log("deselected bird");
      this.selectedBirds = this.selectedBirds.filter((b) => b !== bird);
      this.selectedBirdPhotos = this.selectedBirdPhotos.filter(
        (b) => b !== bird
      );
    },

    displayBirdPhoto(bird: Bird) {
      console.log("pushed:", bird.Species);
      const alreadySelected = this.selectedBirdPhotos.some(
        (p: Bird) => p.Species === bird.Species
      );

      if (!alreadySelected) {
        console.log("Adding photo for:", bird.Species);
        this.selectedBirdPhotos.push(bird);
      } else {
        console.warn("Photo for", bird.Species, "is already displayed.");
      }
    },

    resetAnalyticsConfiguration() {
      this.selectedBirds = [];
      this.selectedBirdPhotos = [];
      this.numTopBirds = 10;
      this.numTopPhotos = 3;
      this.showLikelihoodCurve = true;
      this.showTopBirdPhotos = true;
      this.startYear = new Date().getFullYear() - 20;
      this.endYear = new Date().getFullYear();
      this.startMonth = 1;
      this.startWeek = 1;
      this.endMonth = 12;
      this.endWeek = 4;
    },

    resetSelectedHotspot() {
      this.selectedHotspotId = null;
      this.selectedHotspot = null;
    },

    /**
     * Initial browse: first page of hotspots, sorted by speciesCount
     */
    async fetchAllHotspots() {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get(`/api/hotspots/browse-hotspots`, {
          params: {
            limit: this.hotspotsLimit,
            offset: 0,
          },
        });
        const data = response.data as HotspotOverview[];
        this.allHotspots = data;

        // reset pagination state
        this.hotspotsOffset = data.length;
        this.hotspotsHasMore = data.length === this.hotspotsLimit;

        // prefetch next batch in background to warm up DB connection
        if (this.hotspotsHasMore) {
          this.prefetchNextBatch();
        }
      } catch (e: any) {
        console.log("there was an error");
        console.log(e);
        this.error = e.message ?? "Unknown error";
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * prefetch next batch - warms up DB, doesn't update loading state
     */
    async prefetchNextBatch() {
      try {
        const response = await axios.get(`/api/hotspots/browse-hotspots`, {
          params: {
            limit: this.hotspotsLimit,
            offset: this.hotspotsOffset,
          },
        });

        // store prefetched data for later use
        const newItems = response.data as HotspotOverview[];
        this._prefetchedData = newItems;
        this._prefetchedOffset = this.hotspotsOffset;
      } catch (e) {
        // silent fail
      }
    },

    /**
     * Load next page for infinite scroll (browse mode)
     */
    async loadMoreHotspots() {
      if (this.isLoading || !this.hotspotsHasMore) return;

      // check if we have prefetched data for this offset
      if (
        this._prefetchedData &&
        this._prefetchedOffset === this.hotspotsOffset
      ) {
        const newItems = this._prefetchedData;
        this._prefetchedData = null;
        this._prefetchedOffset = null;

        this.allHotspots = [...this.allHotspots, ...newItems];
        this.hotspotsOffset += newItems.length;
        this.hotspotsHasMore = newItems.length === this.hotspotsLimit;

        // prefetch next batch
        if (this.hotspotsHasMore) {
          this.prefetchNextBatch();
        }
        return;
      }

      // otherwise fetch normally with loading state
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get(`/api/hotspots/browse-hotspots`, {
          params: {
            limit: this.hotspotsLimit,
            offset: this.hotspotsOffset,
          },
        });
        const newItems = response.data as HotspotOverview[];

        this.allHotspots = [...this.allHotspots, ...newItems];
        this.hotspotsOffset += newItems.length;
        this.hotspotsHasMore = newItems.length === this.hotspotsLimit;

        // prefetch next batch for fast scrolling
        if (this.hotspotsHasMore) {
          this.prefetchNextBatch();
        }
      } catch (e: any) {
        console.error("Error loading more hotspots:", e);
        this.error = e.message ?? "Unknown error";
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * use the /hotspots/search endpoint and update allHotspots
     * mode='hotspot' returns hotspot overviews filtered by hotspot / country / subregion
     */
    async searchHotspots(options?: {
      hotspot?: string;
      country?: string;
      subregion1?: string;
      subregion2?: string;
      mode?: "hotspot" | "country" | "subregion1" | "subregion2" | null;
    }) {
      this.isLoading = true;
      this.error = null;

      try {
        const {
          hotspot = this.searchHotspotName || "",
          country = this.searchCountry || "",
          subregion1 = this.searchSubregion1 || "",
          subregion2 = this.searchSubregion2 || "",
          mode = "hotspot",
        } = options || {};

        const response = await axios.get("/api/hotspots/search", {
          params: {
            hotspot,
            country,
            subregion1,
            subregion2,
            mode,
          },
        });

        this.allHotspots = response.data.results;

        // when using search endpoint, we currently treat it as a single page
        this.hotspotsOffset = this.allHotspots.length;
        this.hotspotsHasMore = false; // no pagination wired for search yet
      } catch (e: any) {
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          console.warn("No hotspots matched search, clearing list.");
          this.allHotspots = [];
          this.hotspotsOffset = 0;
          this.hotspotsHasMore = false;
          this.error = null; // no "error" message for the user, just empty results
        } else {
          console.error("Error searching hotspots:", e);
          this.error = e.message ?? "Unknown error";
        }
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Backend-powered autocomplete for hotspot names (mode='hotspot')
     * Returns list of hotspot name strings.
     */
    async fetchHotspotSuggestions(
      query: string,
      opts?: {
        country?: string;
        subregion1?: string;
        subregion2?: string;
        limit?: number;
      }
    ) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get("/api/hotspots/search", {
          params: {
            hotspot: query,
            country: opts?.country ?? "",
            subregion1: opts?.subregion1 ?? "",
            subregion2: opts?.subregion2 ?? "",
            mode: "hotspot",
            limit: opts?.limit ?? 10,
          },
        });

        const raw = response.data.results ?? [];

        // mode='hotspot' returns hotspot overviews, so map to .name
        const names = raw
          .map((item: any) => item?.name ?? item?.hotspot ?? "")
          .filter((s: string) => !!s);

        // unique + keep order
        this.hotspotSuggestions = Array.from(new Set(names));
      } catch (e: any) {
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          this.hotspotSuggestions = [];
          this.error = null;
        } else {
          console.error("Error searching hotspot suggestions:", e);
          this.error = e.message ?? "Unknown error";
        }
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Backend-powered autocomplete for countries (mode='country')
     * Normalizes results into plain country name strings.
     */
    async searchCountries(query: string) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get("/api/hotspots/search", {
          params: {
            hotspot: "",
            country: query,
            subregion1: "",
            subregion2: "",
            mode: "country",
          },
        });

        const raw = response.data.results ?? [];

        this.countrySuggestions = raw
          .map((item: any) => {
            if (typeof item === "string") return item;
            if (item.name) return item.name;
            if (item.country_name) return item.country_name;
            if (item.COUNTRY_NAME) return item.COUNTRY_NAME;
            return "";
          })
          .filter((name: string) => !!name);
      } catch (e: any) {
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          this.countrySuggestions = [];
          this.error = null;
        } else {
          console.error("Error searching countries:", e);
          this.error = e.message ?? "Unknown error";
        }
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Backend-powered autocomplete for subregion1 (mode='subregion1')
     * Requires an exact country filter.
     */
    async fetchSubregion1Suggestions(country: string, query: string) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get("/api/hotspots/search", {
          params: {
            hotspot: "",
            country: country ?? "", // <-- allow empty
            subregion1: query,
            subregion2: "",
            mode: "subregion1",
          },
        });

        const raw = response.data.results ?? [];

        this.subregion1Suggestions = raw
          .map((item: any) => {
            if (typeof item === "string") return item;
            if (item.name) return item.name;
            if (item.subregion1) return item.subregion1;
            if (item.SUBREGION1_NAME) return item.SUBREGION1_NAME;
            return "";
          })
          .filter((name: string) => !!name);
      } catch (e: any) {
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          this.subregion1Suggestions = [];
          this.error = null;
        } else {
          console.error("Error searching subregion1:", e);
          this.error = e.message ?? "Unknown error";
        }
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Backend-powered autocomplete for subregion2 (mode='subregion2')
     * Requires an exact subregion1 filter (backend uses it as a filter).
     */
    async fetchSubregion2Suggestions(subregion1: string, query: string) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get("/api/hotspots/search", {
          params: {
            hotspot: "",
            country: "",
            subregion1: subregion1 ?? "",
            subregion2: query,
            mode: "subregion2",
          },
        });

        const raw = response.data.results ?? [];

        this.subregion2Suggestions = raw
          .map((item: any) => {
            if (typeof item === "string") return item;
            if (item.name) return item.name;
            if (item.subregion2) return item.subregion2;
            if (item.SUBREGION2_NAME) return item.SUBREGION2_NAME;
            return "";
          })
          .filter((name: string) => !!name);
      } catch (e: any) {
        if (axios.isAxiosError(e) && e.response?.status === 404) {
          this.subregion2Suggestions = [];
          this.error = null;
        } else {
          console.error("Error searching subregion2:", e);
          this.error = e.message ?? "Unknown error";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async fetchHotspotDetail() {
      if (!this.selectedHotspotId) return;

      this.isLoading = true;
      this.error = null;

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
        console.log(
          "Fetching hotspot detail for hotspot ID:",
          this.selectedHotspotId
        );

        // enqueue job
        const response = await axios.get(url, { params });

        if (response.status === 202) {
          const jobId = response.data.jobId;
          console.log(`Job enqueued: ${jobId}. Polling...`);

          // poll for result
          while (true) {
            await new Promise((resolve) => setTimeout(resolve, 2000)); // 2s delay
            const pollResponse = await axios.get(`/api/jobs/${jobId}`);
            const job = pollResponse.data;

            if (job.status === "completed") {
              this.selectedHotspot = job.result;
              console.log("Fetched hotspot detail (async):", job.result);
              break;
            } else if (job.status === "failed") {
              throw new Error(job.error || "Job failed");
            }
            // continue polling if queued or processing
          }
        } else {
          // fallback if backend returns immediate result\
          this.selectedHotspot = response.data;
          console.log("Fetched hotspot detail (immediate):", response.data);
        }
      } catch (e: any) {
        this.error = e.message ?? "Unknown error";
        console.log("ERROR:", e.message);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
