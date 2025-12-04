<template>
  <div style="border:2px solid red; padding:20px; width:800px;">
    <apexchart
      width="800"
      height="350"
      type="line"
      :series="[{ name: 'Test', data: [1, 2, 3, 4, 5] }]"
      :options="{
        chart: { type: 'line' },
        xaxis: { categories: [1, 2, 3, 4, 5] }
      }"
    />
  </div>
</template>

<script setup lang="ts">
import VueApexCharts from "vue3-apexcharts";
</script>
