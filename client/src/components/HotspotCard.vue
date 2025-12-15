<template>
  <div
    :class="['hotspot-card', { selected: isSelected }]"
    @click="handleClick"
  >
    <!-- Title -->
    <h3>{{ name }}</h3>
    <div class="title-line"></div>

    <!-- Country -->
    <div class="row">
      <span class="label">
        <BIconGlobe class="icon" />
        Country:
      </span>
      <span class="value">{{ country }}</span>
    </div>

    <!-- Subregion 1 -->
    <div class="row">
      <span class="label">
        <BIconGeoAlt class="icon" />
        Subregion 1:
      </span>
      <span class="value">{{ subregion1 }}</span>
    </div>

    <!-- Subregion 2 -->
    <div class="row">
      <span class="label">
        <BIconGeoFill class="icon" />
        Subregion 2:
      </span>
      <span class="value">
        {{ (!subregion2 || subregion2 === 'None') ? ' —' : subregion2 }}
      </span>
    </div>

    <!-- Species Count -->
    <div class="row">
      <span class="label">
        <BIconPin class="icon" />
        Species Count:
      </span>
      <span class="value">{{ speciesCount }}</span>
    </div>
  </div>
</template>


<script lang="ts">
import {
  BIconGeoAlt,
  BIconGeoFill,
  BIconGlobe,
  BIconPin,

} from 'bootstrap-icons-vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HotspotCard',

  components: {
    BIconGlobe,
    BIconGeoAlt,
    BIconGeoFill,
    BIconPin
  },

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
    subregion2: {
      type: String,
      required: false,
      default: '',
    },
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

.hotspot-card.selected {
  box-shadow: 0 0 5px 4px #457999;
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

/* rows */
.row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85em;
  margin-bottom: 4px;
  color: #797979;
}

/* label with icon inline */
.label {
  display: left;
  align-items: left;
  gap: 6px;
  min-width: 130px;
  font-weight: 700;
  color: #797979;
}

/* icon inline fix */
.icon {
  width: 14px;
  height: 14px;
  display: inline-block;
  
}

/* ensures svg aligns perfectly */
.icon :deep(svg) {
  display: block;
}

/* value */
.value {
  flex: 1;
}
</style>
