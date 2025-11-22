<template>
  <div class="analytics-container">
    <!-- LEFT SECTION: Table -->
    <div class="bird-table">
      <h2 class="section-title">Top 10 Birds</h2>

      <div class="table-header">
        <div>Species</div>
        <div>Data 1</div>
        <div>Data 2</div>
      </div>

      <div
        class="table-row"
        v-for="(bird, i) in birds"
        :key="i"
      >
        <div class="species-cell">
          <span class="index">{{ i + 1 }}.</span>
          <span>{{ bird.name }}</span>
        </div>

        <div class="cell">{{ bird.data1 }}</div>
        <div class="cell">{{ bird.data2 }}</div>
      </div>
    </div>

    <!-- RIGHT SECTION: Photos -->
    <div class="photo-column" v-show="analyticsStore.showTopBirdPhotos">
      <h2 class="section-title">Top 3 Photos {{ analyticsStore.showTopBirdPhotos }}</h2>

      <div
        class="photo-card"
        v-for="(bird, i) in topThree"
        :key="i"
      >
        <img
          class="photo"
          :src="bird.photo"
          alt=""
        />
        <div class="photo-caption">
          {{ i + 1 }}. {{ bird.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAnalyticsStore } from '../stores/useAnalyticsStore';

interface Bird {
  name: string;
  data1: number;
  data2: number;
}

interface BirdPhoto {
  name: string;
  photo: string;
}

const birds: Bird[] = [
  { name: "American Robin", data1: 12, data2: 8 },
  { name: "Mourning Dove", data1: 10, data2: 7 },
  { name: "House Finch", data1: 9, data2: 6 },
  { name: "Blue Jay", data1: 8, data2: 5 },
  { name: "Northern Cardinal", data1: 7, data2: 5 },
  { name: "Dark-eyed Junco", data1: 6, data2: 4 },
  { name: "Black-capped Chickadee", data1: 5, data2: 4 },
  { name: "European Starling", data1: 5, data2: 3 },
  { name: "Red-tailed Hawk", data1: 4, data2: 2 },
  { name: "Canada Goose", data1: 4, data2: 2 },
];

const topThree: BirdPhoto[] = [
  { name: "American Robin", photo: "https://placehold.co/300x200" },
  { name: "Mourning Dove", photo: "https://placehold.co/300x200" },
  { name: "House Finch", photo: "https://placehold.co/300x200" },
];

const analyticsStore = useAnalyticsStore();


</script>

<style scoped>
.analytics-container {
  display: flex;
  gap: 24px;
  padding: 40px;
  height: 100vh;
  background: white;
  color: #222;
  overflow: scroll;
}

.bird-table {
  flex: 1;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding: 8px 0;
  border-bottom: 1px solid #e4e4e4;
}

.table-header {
  font-weight: 600;
}

.species-cell {
  display: flex;
  gap: 6px;
  align-items: center;
}

.index {
  color: #888;
  width: 20px;
}

.cell {
  text-align: center;
}

.photo-column {
  width: 220px;
  flex-shrink: 0;
}

.photo-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.photo {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.photo-caption {
  padding: 8px;
  font-weight: 500;
  text-align: center;
}
</style>
