<template>
  <BarChart :chartData="data" :options="options" style="height: 250px"/>  
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import { useTheme } from 'vuetify';

Chart.register(...registerables);

// full set of detailed labels
const detailedLabels = [
    "January 1", "January 2", "January 3", "January 4", 
    "February 1", "February 2", "February 3", "February 4", 
    "March 1", "March 2", "March 3", "March 4",
    "April 1", "April 2", "April 3", "April 4", 
    "May 1", "May 2", "May 3", "May 4", 
    "June 1", "June 2", "June 3", "June 4",
    "July 1", "July 2", "July 3", "July 4", 
    "August 1", "August 2", "August 3", "August 4", 
    "September 1", "September 2", "September 3", "September 4", 
    "October 1", "October 2", "October 3", "October 4", 
    "November 1", "November 2", "November 3", "November 4", 
    "December 1", "December 2", "December 3", "December 4"
];

// month labels for x-axis
const monthLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];


export default defineComponent({
  name: 'DataDistributionGraph',
  components: { BarChart },
  setup() {
    const analyticsStore = useAnalyticsStore();
    const theme = useTheme();
    
    // access to dark mode state to prevent crash
    const isDarkMode = computed(() => theme.global.current.value?.dark);
    
    // theme-aware colors
    const STANDARD_COLOR = computed(() => isDarkMode.value ? '#7eb8d9' : '#8EB5CC');
    const HIGHLIGHT_COLOR = computed(() => isDarkMode.value ? '#3a5a6d' : '#457999');
    const GRID_COLOR = computed(() => isDarkMode.value ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.1)');
    const TEXT_COLOR = computed(() => isDarkMode.value ? '#e0e0e0' : '#666');
    const HOVER_COLOR = computed(() => isDarkMode.value ? '#2a4a5d' : '#3a6680');

    // Helper function to convert (month, week) to index (0-47) of the bars
    const dateToIndex = (month: number, week: number): number => {
        const safeMonth = Math.max(1, Math.min(12, month));
        const safeWeek = Math.max(1, Math.min(4, week));
        
        return (safeMonth - 1) * 4 + (safeWeek - 1);
    };

    const data = computed(() => {
      const rawData = analyticsStore.selectedHotspot?.sample_sizes_by_week || {};
      const chartData = Object.values(rawData as Record<string, number>).slice(0, 48);

      let startIndex = -1;
      let endIndex = -1;

      if (analyticsStore.startMonth && analyticsStore.startWeek && analyticsStore.endMonth && analyticsStore.endWeek) {
        startIndex = dateToIndex(analyticsStore.startMonth, analyticsStore.startWeek);
        endIndex = dateToIndex(analyticsStore.endMonth, analyticsStore.endWeek);
      }

      const isWrapping = startIndex > endIndex;

      // populate background colors based on if index range
      const backgroundColors: string[] = [];
      for (let i = 0; i < 48; i++) {
        let color = STANDARD_COLOR.value;

        if (isWrapping) {
          if (i <= endIndex || i >= startIndex) {
            color = HIGHLIGHT_COLOR.value;
          }
        }
        
        else {
          if (i >= startIndex && i <= endIndex) {
            color = HIGHLIGHT_COLOR.value
          }
        }

        backgroundColors.push(color);
      }

      return {
        labels: detailedLabels,
        datasets: [
          {
            label: 'Data Density by Month',
            data: chartData,
            backgroundColor: backgroundColors,
            borderColor: isDarkMode.value ? '#7eb8d9' : '#457999',
            hoverBackgroundColor: HOVER_COLOR.value,
            pointRadius: 6,
            pointHoverRadius: 10,
          }
        ],
      };
    });
    
    const options = computed(() => {
        return {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        callback: function(index: number) {
                            // Display month label only on the first week (index 0, 4, 8, etc.)
                            if (index % 4 === 0) {
                                const monthIndex = Math.floor(index / 4);
                                return monthLabels[monthIndex];
                            }
                            return '';
                        },
                        autoSkip: false,
                        maxRotation: 60, 
                        minRotation: 45,
                        font: {
                            size: 9
                        },
                        color: TEXT_COLOR.value
                    },
                    grid: {
                        color: GRID_COLOR.value
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: "Checklists",
                      color: TEXT_COLOR.value
                    },
                    ticks: {
                        color: TEXT_COLOR.value
                    },
                    grid: {
                        color: GRID_COLOR.value
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: TEXT_COLOR.value
                    }
                }
            }
        };
    });


    return { data, options };
  },
});
</script>