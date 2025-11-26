<template>
  <div class="analytics-container">
    <div class="bird-lists-container">
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
            <span>{{ bird.species }}</span>
          </div>

          <div class="cell">{{ bird.data1 }}</div>
          <div class="cell">{{ bird.data2 }}</div>
        </div>
      </div>

      <!-- CUSTOM SELECTED BIRDS -->
      <div class="bird-table" v-show="(analyticsStore.selectedBirds.length > 0)">
        <h2 class="section-title">Custom Birds</h2>

        <div class="table-header">
          <div>Species</div>
          <div>Data 1</div>
          <div>Data 2</div>
        </div>

        <div
          class="table-row"
          v-for="(bird, i) in analyticsStore.selectedBirds"
          :key="i"
        >
          <div class="species-cell">
            <span class="index">{{ i + 1 }}.</span>
            <span>{{ bird.species }}</span>
          </div>

          <div class="cell">{{ bird.data1 }}</div>
          <div class="cell">{{ bird.data2 }}</div>
        </div>
      </div>

    </div>

    <!-- RIGHT SECTION: Photos -->
    <div class="photo-column" v-show="analyticsStore.showTopBirdPhotos">
    <h2 class="section-title">Top 3 </h2>

      <div
        class="photo-card"
        v-for="(bird, i) in birds.slice(0, 3)"
        :key="i"
      >
        <img
          class="photo"
          :src="bird.photo"
          alt=""
        />
        <div class="photo-caption">
          {{ i + 1 }}. {{ bird.species }}
        </div>
      </div>
    </div>


    <!-- RIGHT SECTION: Graph -->

  </div>
</template>

<script setup lang="ts">
import { BIconXCircle } from 'bootstrap-icons-vue';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';

const analyticsStore = useAnalyticsStore();
const birds = analyticsStore.getPlacementTopBirds;


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

.bird-lists-container {
  display: block;
  gap: 24px;
  height: 100vh;
  width: 100vh;
  background: white;
  color: #222;
  overflow: scroll;
}

.bird-table {
  flex: 1;
  padding: 40px;
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
