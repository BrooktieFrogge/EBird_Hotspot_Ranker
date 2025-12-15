<template>
  <div
    :class="['hotspot-card', { 'selected': isSelected }]"
    @click="handleClick"
  >
    <!-- Title -->
    <h3>{{ name }}</h3>
    <div class="title-line"></div>

    <!-- Country / Subregions -->
    <div class="row">
      <span class="label">Country:</span>
      <span class="value">{{ country }}</span>
    </div>

    <div class="row">
      <span class="label">Subregion 1:</span>
      <span class="value">{{ subregion1 }}</span>
    </div>

    <div class="row">
  <span class="label">Subregion 2:</span>
  <span class="value">{{ subregion2 || '—' }}</span>
</div>

    <div class="row">
      <span class="label">Species Count:</span>
      <span class="value">{{ speciesCount }}</span>
    </div>

    <!-- Saved indicator -->
    <div class="saved-indicator" v-if="isSaved">
      ★ Saved
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HotspotCard',

  props: {
    id: {
      type: [String, Number],
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    country: {
      type: String,
      required: true,
    },
    subregion1: {
      type: String,
      required: true,
    },
    // subregion2 
    subregion2: {
      type: String,
      required: false,
      default: '',
    },
    // species count
    speciesCount: {
      type: Number,
      required: true,
    },

    colorClass: {
      type: String,
      required: false,
      default: '#4caf50',
    },
    isSaved: {
      type: Boolean,
      required: false,
      default: false,
    },
    isSelected: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  emits: ['click'],

  methods: {
    handleClick() {
      // tell the parent which hotspot was clicked
      this.$emit('click', this.id);
    },
  },
});
</script>

<style scoped>
.hotspot-card {
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 10px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 0px 1px #eeeeee;
  background: #ffffff;
  cursor: pointer;
  position: relative;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  box-sizing: border-box;
  flex: 0 0 calc(33.333% - 16px);
}

h3 {
  margin: 0 0 6px 0;
  font-size: 1.1em;
  font-weight: 500;
  color: #797979;
}

/* line under the hotspot name */
.title-line {
  height: 2px;
  border-radius: 999px;
  background: #e0e0e0;
  margin-bottom: 6px;
}

.row {
  display: flex;
  font-size: 0.85em;
  margin-bottom: 4px;
  color: #797979;
}

.label {
  min-width: 110px;
  color: #797979;
  font-weight: 700; /* bold labels */
}

.hotspot-card.selected {
  box-shadow: 0 0 5px 4px #457999;
}

.value {
  flex: 1;
}

.color-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 6px;
}

.saved-indicator {
  position: absolute;
  top: 8px;
  right: 10px;
  font-size: 0.8em;
  color: #ffd700;
}
</style>
