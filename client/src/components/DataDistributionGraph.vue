<template>
  <BarChart :chartData="data"/>  
  Hello
</template>



<script lang="ts">
import { computed, defineComponent } from 'vue';
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";
import { useAnalyticsStore } from '../stores/useAnalyticsStore';

Chart.register(...registerables);

export default defineComponent({
  name: 'DataDistributionGraph',
  components: { BarChart },
  setup() {
    const analyticsStore = useAnalyticsStore();
    // const data = {
    //   labels: ["January 1", "January 2", "January 3", "January 4", "February 1", "February 2", "February 3", "February 4", "March 1", "March 2", "March 3", "March 4",
    //   "April 1", "April 2", "April 3", "April 4", "May 1", "May 2", "May 3", "May 4", "June 1", "June 2", "June 3", "June 4",
    //   "July 1", "July 2", "July 3", "July 4", "August 1", "August 2", "August 3", "August 4", "September 1", "September 2", "September 3", "September 4", 
    //   "October 1", "October 2", "October 3", "October 4", "November 1", "November 2", "November 3", "November 4", "December 1", "December 2", "December 3", "December 4"],
    //   datasets: [
    //     {
    //       data: Object.values(analyticsStore.selectedHotspot?.sample_sizes_by_week as Record<string, number>).slice(0, 48),
    //       backgroundColor: ['#D09B2C'],
    //     },
    //   ],
    // };

    const data = computed(() => {
      console.log(analyticsStore.selectedHotspot?.sample_sizes_by_week)

      return {
        labels: ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
        datasets: [
          {
            label: 'List Likelihood',
            data: Object.values(analyticsStore.selectedHotspot?.sample_sizes_by_week as Record<string, number>).slice(0, 48),
            backgroundColor: '#D09B2C',
            borderColor: '#457999',
            pointRadius: 6,
            pointHoverRadius: 10,
          }
        ],
      };
    });


    // const config = {
		// 	type: 'bar',
		// 	data: data,
		// 	options: {
		// 		responsive: true,
		// 		plugins: {
		// 			legend: {
		// 					position: 'top',
		// 			},
		// 			title: {
		// 				display: true,
		// 				text: 'Chart.js Bar Chart'
		// 			}
		// 		}
		// 	},
    // };

		// const chart = new Chart(
		// 	document.getElementById('myChart'),
		// 	config
		// )


    return { data };
  },
});
</script>