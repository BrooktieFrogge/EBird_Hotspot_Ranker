<template>
  <div :class="['hotspot-card', { selected: isSelected }]" @click="handleClick">
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

    <!-- eBird color / stats -->
    <div class="row">
      <span class="label">Species Observed :</span>
      <span class="value">
        <span class="color-dot" :style="{ backgroundColor: colorClass }"></span>
        {{ speciesCount }} species
      </span>
    </div>
    -->

    <!--<div class="row">
      <span class="label">Checklists:</span>
      <span class="value">{{ checklistCount }}</span>
    </div>

    <!-- Saved indicator -->
    <div class="saved-indicator" v-if="isSaved">★ Saved</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "HotspotCard",

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
      default: "#4caf50",
    },
    speciesCount: {
      type: Number,
      required: false,
      default: 0,
    },
    checklistCount: {
      type: Number,
      required: false,
      default: 0,
    },
    topBirds: {
      type: Array as PropType<string[]>,
      required: false,
      default: () => [],
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

  emits: ["click"],

  methods: {
    handleClick() {
      // bubble up the click so the parent can route to HotspotDetail
      this.$emit("click", this.isSelected);
    },
  },
});
</script>

<style scoped>
.hotspot-card {
  border: 1px solid #296239;
  border-radius: 12px;
  padding: 10px;
  max-width: 290px;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 8px 1px #949494;
  cursor: pointer;
  margin: 8px;
  position: relative;
}

.hotspot-card.selected {
  border: 1px solid #71e7ff;
  padding: 10px;
  box-shadow: 0 0 10px 1px rgba(113, 231, 255, 0.7); /* Glow effect */
  transition: box-shadow 0.3s ease; /* Smooth transition */
}

h3 {
  margin: 0 0 6px 0;
  font-size: 1.1em;
  font-weight: 500;
  color: #000000;
}

.row {
  display: flex;
  font-size: 0.85em;
  margin-bottom: 4px;
}

.label {
  min-width: 300px;
  color: #aaa;
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

.top-birds {
  margin-top: 6px;
  border-top: 0.5px solid gray;
  padding-top: 4px;
}

.saved-indicator {
  position: absolute;
  top: 8px;
  right: 10px;
  font-size: 0.8em;
  color: #ffd700;
}
</style>
