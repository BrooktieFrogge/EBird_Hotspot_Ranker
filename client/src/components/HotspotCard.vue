<template>
  <div
    :class="['hotspot-card', { 'selected': isSelected }]" @click="handleClick"
  >
    <!-- Title -->
    <h3>{{ name }}</h3>

    <!-- Country / Subregion1  -->
    <div class="row">
      <span class="label">Country:</span>
      <span class="value">{{ country }}</span>
    </div>
    <div class="row">
      <span class="label">subregion 1:</span>
      <span class="value">{{ subregion1 }}</span>
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
  max-width: 290px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 8px 1px #20415a;
  background: #20415a;
  cursor: pointer;
  margin: 8px;
  position: relative;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}


h3 {
  margin: 0 0 6px 0;
  font-size: 1.1em;
  font-weight: 500;
  color: #a2bcd0;
}


.row {
  display: flex;
  font-size: 0.85em;
  margin-bottom: 4px;
  color: #a2bcd0;
}

.label {
  min-width: 300px;
  color: #a2bcd0;
}

.hotspot-card.selected {
  border-color: #b0e28c;
  box-shadow: 0 0 5px 2px #cfe9bd;
  background: #203727;
}

.hotspot-card.selected h3 {
  color: #cfe9bd;
}

.hotspot-card.selected .row {
  color: #cfe9bd;
}

.hotspot-card.selected .label {
  color: #cfe9bd;
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