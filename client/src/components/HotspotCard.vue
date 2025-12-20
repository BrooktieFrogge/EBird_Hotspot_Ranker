<template>
  <div
    :class="['hotspot-card', { selected: isSelected }]"
    @click="handleClick"
  >
    <!-- title section (top) -->
    <div class="card-name-section">
      <h3>{{ name }}</h3>
    </div>

    <!-- details section (bottom) -->
    <div class="card-bottom-section">
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
  box-shadow: 0 0 0px 1px var(--color-border-light);
  background: var(--color-bg-panel);
  cursor: pointer;
  position: relative;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  box-sizing: border-box;
  flex: 0 0 calc(33.333% - 16px);
  /* flex layout for internal structure */
  display: flex !important;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  contain: layout;
}

.card-name-section {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding-bottom: 8px;
}

.card-bottom-section {
  flex: 0 0 auto;
  margin-top: auto;
  width: 100%;
}

.hotspot-card.selected {
  box-shadow: 0 0 4px 3px rgba(69, 121, 153, 0.6);
  border-color: rgba(69, 121, 153, 0.4);
}

h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;             
  color: var(--color-text-secondary);               
  line-height: 1.25;
  text-align: center; /* Center horizontally */
  width: 100%;
}

/* line under the hotspot name */
.title-line {
  height: 2px;
  border-radius: 999px;
  background: var(--color-border-light);
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
  color: var(--color-text-muted);
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
  color: var(--color-text-primary);
}

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: red; 
  flex-shrink: 0;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.15);
}

/* ===============================
  responsive styles
  =============================== */

@media (max-width: 768px) {
  .hotspot-card {
    padding: 10px 12px;
    border-radius: 10px;
    flex: none;
  }
  
  h3 {
    font-size: 0.9rem;
    margin-bottom: 6px;
  }
  
  .title-line {
    margin-bottom: 6px;
  }
  
  .row {
    font-size: 0.75rem;
    margin-bottom: 2px;
    gap: 4px;
  }
  
  .label {
    min-width: 100px;
  }
  
  .value {
    margin-left: 8px;
    margin-bottom: 4px;
  }
  
  .icon {
    width: 12px;
    height: 12px;
  }
}

/* tablet */
@media (min-width: 769px) and (max-width: 1198px) {
  .hotspot-card {
    padding: 12px 14px;
    flex: none !important;
    width: 100% !important;
    height: 100%;
    min-height: 200px;
    display: flex;
    flex-direction: column;
  }
  
  h3 {
    font-size: 0.95rem;
  }
  
  .row {
    font-size: 0.8rem;
  }
  
  .label {
    min-width: 110px;
  }
}
</style>