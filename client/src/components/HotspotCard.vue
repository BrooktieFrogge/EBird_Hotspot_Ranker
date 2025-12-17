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
        State/Province:
      </span>
      <span class="value">{{ subregion1 }}</span>
    </div>

    <!-- Subregion 2 -->
    <div class="row">
      <span class="label">
        <BIconGeoFill class="icon" />
        County/District:
      </span>
      <span class="value">
        {{ (!subregion2 || subregion2 === 'None') ? '—' : subregion2 }}
      </span>
    </div>

    <!-- Species Count + Color Dot -->
    <div class="row">
      <span class="label">
       <i class="bi bi-feather"></i>
        Species Count:
      </span>

      <span class="value species-with-dot">
      <span
        class="color-dot"
        :style="{ backgroundColor: getSpeciesCountColor(speciesCount) }"
        aria-hidden="true"
      />
      {{ speciesCount }}
    </span>
    </div>
  </div>
</template>



<script lang="ts">
import {
  BIconGeoAlt,
  BIconGeoFill,
  BIconGlobe,


} from 'bootstrap-icons-vue';
import { defineComponent } from 'vue';
import "bootstrap-icons/font/bootstrap-icons.css";


function getSpeciesCountColor(speciesCount: number): string {
  if (speciesCount >= 600) return '#eb463c';   // 600+
  if (speciesCount >= 500) return '#eb5f50';   // 500–600
  if (speciesCount >= 400) return '#eb8769';   // 400–500
  if (speciesCount >= 300) return '#f0b46e';   // 300–400
  if (speciesCount >= 250) return '#fadc73';   // 250–300
  if (speciesCount >= 200) return '#faf078';   // 200–250
  if (speciesCount >= 150) return '#fafa8c';   // 150–200
  if (speciesCount >= 100) return '#f0f596';   // 100–150
  if (speciesCount >= 50)  return '#e1ebb4';   // 50–100
  if (speciesCount >= 15)  return '#e1ebeb';   // 15–50
  return '#e6f0eb';                            // 0–15
}

export default defineComponent({
  name: 'HotspotCard',

  components: {
    BIconGlobe,
    BIconGeoAlt,
    BIconGeoFill,
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
      // tell the parent which hotspot was clicked
      this.$emit('click', this.id);
    },
    getSpeciesCountColor,
  },
});
</script>

<style scoped>
.hotspot-card {
  border: 2px solid transparent;
  border-radius: 14px;
  padding: 14px 16px;
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
  box-shadow: 0 0 4px 3px rgba(69, 121, 153, 0.6);

}

h3 {
  margin: 0 0 8px 0;
  font-size: 1.05rem;
  font-weight: 600;             
  color: #797979;               
  line-height: 1.25;
}

/* line under the hotspot name */
.title-line {
  height: 2px;
  border-radius: 999px;
  background: #e0e0e0;
  margin-bottom: 10px;
}

/* rows */
.row {
  display: flex;
  align-items: flex-start;      
  gap: 8px;
  font-size: 0.85rem;
  margin-bottom: 4px;     
}

.row:last-child {
  margin-bottom: 0;
}

/* label with icon inline */
.label {
  align-items: left;
  gap: 6px;
  min-width: 140px;
  font-weight: 600;
  color: #797979;
  white-space: no-wrap;
}

/* icon inline  */
.icon {
  width: 14px;
  height: 14px;
  display: inline-block;
  opacity: 0.75;
}

/* aligns perfectly */
.icon :deep(svg) {
  stroke-width: 1.75;
}

/* value */
.value {
  flex: 1;
  margin-left: 20px;
  margin-bottom: 8px;
}

.species-with-dot {
  display: inline-flex;
  align-items: center;
  gap: 6px;                     /* tighter */
  font-weight: 600;
  color: #333;
}

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: red; 
  flex-shrink: 0;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.15);
}
</style>
