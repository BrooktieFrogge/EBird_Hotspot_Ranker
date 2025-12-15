<template>
  <BarChart :chartData="data" :options="options" style="height: 250px"/>  
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";
import { useAnalyticsStore } from '../stores/useAnalyticsStore';

Chart.register(...registerables);

// Define the full set of detailed labels
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

// Define the simplified month labels for the X-axis display
const monthLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];


export default defineComponent({
  name: 'DataDistributionGraph',
  components: { BarChart },
  setup() {
    const analyticsStore = useAnalyticsStore();

    const data = computed(() => {
      console.log(analyticsStore.selectedHotspot?.sample_sizes_by_week);

      const rawData = analyticsStore.selectedHotspot?.sample_sizes_by_week || {};
      
      const chartData = Object.values(rawData as Record<string, number>).slice(0, 48);

      return {
        labels: detailedLabels,
        datasets: [
          {
            label: 'Data Density by Month',
            data: chartData,
            backgroundColor: ['#72A2C0', '#72A2C0', '#72A2C0', '#72A2C0', '#457999', '#457999', '#457999', '#457999'],
            borderColor: '#457999',
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
                        callback: function(val: number, index: number) {
                            // Display month label only on the first week (index 0, 4, 8, etc.)
                            if (index % 4 === 0) {
                                const monthIndex = Math.floor(index / 4);
                                return monthLabels[monthIndex];
                            }
                            return '';
                        },
                        autoSkip: false,
                        maxRotation: 0, 
                        minRotation: 0,
                    },
                },
                y: {
                    beginAtZero: true,
                }
            },
            plugins: {
                legend: {
                    display: true,
                }
            }
        };
    });


    return { data, options };
  },
});
</script>