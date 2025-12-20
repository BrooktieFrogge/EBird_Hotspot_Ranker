<template>
  <div class="chart-wrapper">
    <BarChart :chartData="data" :options="options" style="height: 250px" />

    <!-- range slider below chart -->
    <div
      class="range-slider-container"
      :class="{ 'dark-mode-slider': isDarkMode }"
    >
      <div class="range-track" ref="trackRef">
        <!-- filled range -->
        <div class="range-fill" :style="fillStyle"></div>

        <!-- left handle -->
        <div
          class="range-handle left-handle"
          :style="{ left: leftHandlePos + '%' }"
          @mousedown.prevent="startDrag('left', $event)"
          @touchstart.prevent="startDrag('left', $event)"
        >
          <div class="handle-pip"></div>
        </div>

        <!-- right handle -->
        <div
          class="range-handle right-handle"
          :style="{ left: rightHandlePos + '%' }"
          @mousedown.prevent="startDrag('right', $event)"
          @touchstart.prevent="startDrag('right', $event)"
        >
          <div class="handle-pip"></div>
        </div>
      </div>

      <!-- labels -->
      <div class="range-labels">
        <span>{{ startLabel }}</span>
        <span class="range-hint">(Drag handles to adjust)</span>
        <span>{{ endLabel }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, onBeforeUnmount } from "vue";
import { BarChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import { useAnalyticsStore } from "../stores/useAnalyticsStore";
import { useTheme } from "vuetify";

Chart.register(...registerables);

// full set of detailed labels
const detailedLabels = [
  "January 1",
  "January 2",
  "January 3",
  "January 4",
  "February 1",
  "February 2",
  "February 3",
  "February 4",
  "March 1",
  "March 2",
  "March 3",
  "March 4",
  "April 1",
  "April 2",
  "April 3",
  "April 4",
  "May 1",
  "May 2",
  "May 3",
  "May 4",
  "June 1",
  "June 2",
  "June 3",
  "June 4",
  "July 1",
  "July 2",
  "July 3",
  "July 4",
  "August 1",
  "August 2",
  "August 3",
  "August 4",
  "September 1",
  "September 2",
  "September 3",
  "September 4",
  "October 1",
  "October 2",
  "October 3",
  "October 4",
  "November 1",
  "November 2",
  "November 3",
  "November 4",
  "December 1",
  "December 2",
  "December 3",
  "December 4",
];

const monthLabels = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

export default defineComponent({
  name: "DataDistributionGraph",
  components: { BarChart },
  setup() {
    const analyticsStore = useAnalyticsStore();
    const theme = useTheme();

    // refs
    const trackRef = ref<HTMLElement | null>(null);

    // drag state
    const isDragging = ref(false);
    const dragHandle = ref<"left" | "right" | null>(null);
    const tempStartIndex = ref(0);
    const tempEndIndex = ref(47);

    // theme
    const isDarkMode = computed(() => theme.global.current.value?.dark);
    const STANDARD_COLOR = computed(() =>
      isDarkMode.value ? "#7eb8d9" : "#8EB5CC"
    );
    const HIGHLIGHT_COLOR = computed(() =>
      isDarkMode.value ? "#3a5a6d" : "#457999"
    );
    const GRID_COLOR = computed(() =>
      isDarkMode.value ? "rgba(255, 255, 255, 0.05)" : "rgba(0, 0, 0, 0.1)"
    );
    const TEXT_COLOR = computed(() => (isDarkMode.value ? "#e0e0e0" : "#666"));
    const HOVER_COLOR = computed(() =>
      isDarkMode.value ? "#2a4a5d" : "#3a6680"
    );

    // index helpers
    const dateToIndex = (month: number, week: number): number => {
      const safeMonth = Math.max(1, Math.min(12, month));
      const safeWeek = Math.max(1, Math.min(4, week));
      return (safeMonth - 1) * 4 + (safeWeek - 1);
    };

    const indexToDate = (index: number): { month: number; week: number } => {
      const safeIndex = Math.max(0, Math.min(47, index));
      return {
        month: Math.floor(safeIndex / 4) + 1,
        week: (safeIndex % 4) + 1,
      };
    };

    // current indices from store
    const startIndex = computed(() =>
      dateToIndex(analyticsStore.startMonth, analyticsStore.startWeek)
    );
    const endIndex = computed(() =>
      dateToIndex(analyticsStore.endMonth, analyticsStore.endWeek)
    );

    // handle positions (0-100%)
    const leftHandlePos = computed(() => {
      const idx = isDragging.value ? tempStartIndex.value : startIndex.value;
      return (idx / 47) * 100;
    });

    const rightHandlePos = computed(() => {
      const idx = isDragging.value ? tempEndIndex.value : endIndex.value;
      return (idx / 47) * 100;
    });

    // fill style
    const fillStyle = computed(() => ({
      left: leftHandlePos.value + "%",
      width: rightHandlePos.value - leftHandlePos.value + "%",
    }));

    // labels - use 3-letter codes for consistent width
    const startLabel = computed(() => {
      const idx = isDragging.value ? tempStartIndex.value : startIndex.value;
      const date = indexToDate(idx);
      return `${monthLabels[date.month - 1]} Wk${date.week}`;
    });

    const endLabel = computed(() => {
      const idx = isDragging.value ? tempEndIndex.value : endIndex.value;
      const date = indexToDate(idx);
      return `${monthLabels[date.month - 1]} Wk${date.week}`;
    });

    // drag handlers
    const startDrag = (
      handle: "left" | "right",
      _event: MouseEvent | TouchEvent
    ) => {
      isDragging.value = true;
      dragHandle.value = handle;
      tempStartIndex.value = startIndex.value;
      tempEndIndex.value = endIndex.value;

      document.addEventListener("mousemove", onDrag);
      document.addEventListener("mouseup", endDrag);
      document.addEventListener("touchmove", onDrag);
      document.addEventListener("touchend", endDrag);
    };

    const onDrag = (event: MouseEvent | TouchEvent) => {
      if (!isDragging.value || !trackRef.value) return;

      const clientX =
        "touches" in event && event.touches[0]
          ? event.touches[0].clientX
          : (event as MouseEvent).clientX;

      const rect = trackRef.value.getBoundingClientRect();
      const percent = Math.max(
        0,
        Math.min(100, ((clientX - rect.left) / rect.width) * 100)
      );
      const newIndex = Math.round((percent / 100) * 47);

      if (dragHandle.value === "left") {
        tempStartIndex.value = Math.min(newIndex, tempEndIndex.value - 1);
      } else {
        tempEndIndex.value = Math.max(newIndex, tempStartIndex.value + 1);
      }
    };

    const endDrag = () => {
      if (isDragging.value) {
        const startDate = indexToDate(tempStartIndex.value);
        const endDate = indexToDate(tempEndIndex.value);

        analyticsStore.startMonth = startDate.month;
        analyticsStore.startWeek = startDate.week;
        analyticsStore.endMonth = endDate.month;
        analyticsStore.endWeek = endDate.week;

        analyticsStore.fetchHotspotDetail();
      }

      isDragging.value = false;
      dragHandle.value = null;

      document.removeEventListener("mousemove", onDrag);
      document.removeEventListener("mouseup", endDrag);
      document.removeEventListener("touchmove", onDrag);
      document.removeEventListener("touchend", endDrag);
    };

    onBeforeUnmount(() => {
      document.removeEventListener("mousemove", onDrag);
      document.removeEventListener("mouseup", endDrag);
    });

    // chart data - uses temp values during drag for live preview
    const data = computed(() => {
      const rawData =
        analyticsStore.selectedHotspot?.sample_sizes_by_week || {};
      const chartData = Object.values(rawData as Record<string, number>).slice(
        0,
        48
      );

      const start = isDragging.value ? tempStartIndex.value : startIndex.value;
      const end = isDragging.value ? tempEndIndex.value : endIndex.value;

      const backgroundColors: string[] = [];
      for (let i = 0; i < 48; i++) {
        backgroundColors.push(
          i >= start && i <= end ? HIGHLIGHT_COLOR.value : STANDARD_COLOR.value
        );
      }

      return {
        labels: detailedLabels,
        datasets: [
          {
            label: "Data Density by Month",
            data: chartData,
            backgroundColor: backgroundColors,
            borderColor: isDarkMode.value ? "#7eb8d9" : "#457999",
            hoverBackgroundColor: HOVER_COLOR.value,
            pointRadius: 6,
            pointHoverRadius: 10,
          },
        ],
      };
    });

    const options = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: isDragging.value ? 0 : 400 },
      scales: {
        x: {
          ticks: {
            callback: (index: number) =>
              index % 4 === 0 ? monthLabels[Math.floor(index / 4)] : "",
            autoSkip: false,
            maxRotation: 60,
            minRotation: 45,
            font: { size: 9 },
            color: TEXT_COLOR.value,
          },
          grid: { color: GRID_COLOR.value },
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: "Checklists", color: TEXT_COLOR.value },
          ticks: { color: TEXT_COLOR.value },
          grid: { color: GRID_COLOR.value },
        },
      },
      plugins: {
        legend: { display: true, labels: { color: TEXT_COLOR.value } },
      },
    }));

    return {
      data,
      options,
      trackRef,
      leftHandlePos,
      rightHandlePos,
      fillStyle,
      startLabel,
      endLabel,
      startDrag,
      isDarkMode,
    };
  },
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
}

.range-slider-container {
  margin-top: 8px;
  padding: 0 10px;
}

.range-track {
  position: relative;
  height: 8px;
  background: var(--color-border-light, #444);
  border-radius: 4px;
  cursor: pointer;
}

.range-fill {
  position: absolute;
  top: 0;
  height: 100%;
  background: #457999;
  border-radius: 4px;
}

.range-handle {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  background: #457999;
  border: 2px solid #fff;
  border-radius: 50%;
  cursor: ew-resize;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s, box-shadow 0.2s;
}

.range-handle:hover {
  transform: translate(-50%, -50%) scale(1.1);
  box-shadow: 0 0 8px rgba(69, 121, 153, 0.5);
}

.range-handle:active {
  transform: translate(-50%, -50%) scale(1.15);
}

.handle-pip {
  width: 2px;
  height: 8px;
  background: #fff;
  border-radius: 1px;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 0.75rem;
  color: var(--color-text-secondary, #888);
}

.range-labels > span:first-child,
.range-labels > span:last-child {
  min-width: 70px; /* fixed width to prevent jitter */
}

.range-labels > span:first-child {
  text-align: left;
}

.range-labels > span:last-child {
  text-align: right;
}

.range-hint {
  font-size: 0.7rem;
  opacity: 0.7;
  flex: 1;
  text-align: center;
}

/* dark mode */
.dark-mode-slider .range-fill,
.dark-mode-slider .range-handle {
  background: #7eb8d9;
}

.dark-mode-slider .range-handle {
  border-color: #1a1a2e !important;
}

.dark-mode-slider .handle-pip {
  background: #1a1a2e !important;
}
</style>
