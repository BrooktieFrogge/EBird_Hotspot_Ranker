<template>
  <div :class="['hotspot-detail']">
    <TopNavBar />

    <!-- desktop layout -->
    <div class="content desktop-only">

      <!-- config panel -->
      <div class="config-panel">
        <AnalyticsConfigPanel />
      </div>

      <!-- hotspot analytics report -->
      <div class="analytics-report">
        <HotspotAnalyticsReport />
      </div>

    </div>
    
    <!-- mobile carousel layout -->
    <div class="mobile-carousel mobile-only">
      <div class="carousel-track" ref="carouselTrack" @scroll="handleCarouselScroll">
        
        <!-- slide 1: config panel -->
        <div class="carousel-slide">
          <div class="slide-content">
            <AnalyticsConfigPanel />
          </div>
        </div>
        
        <!-- slide 2: graph + bird list -->
        <div class="carousel-slide" ref="slide2">
          <div class="slide-content">
            <HotspotAnalyticsReport :show-photos="false" />
          </div>
        </div>
        
        <!-- slide 3: photos -->
        <div class="carousel-slide">
          <div class="slide-content photos-slide">
            <HotspotAnalyticsReport :show-graph-and-list="false" />
          </div>
        </div>
        
      </div>
      
      <!-- fixed bottom navigation bar -->
      <nav class="carousel-nav-bar" :class="{ 'dock-lifted': navStore.mobileNavOpen }">
        <button class="nav-btn back-btn" @click="goBack" aria-label="Go back">
          <BIconArrowLeft />
        </button>
        
        <div class="carousel-dots">
          <button 
            v-for="n in 3" 
            :key="n"
            class="carousel-dot" 
            :class="{ active: currentSlide === n }" 
            @click="goToSlide(n)"
            :aria-label="'Go to slide ' + n"
          ></button>
        </div>
        
        <button class="nav-btn" @click="navStore.toggleMobileNav()" aria-label="Menu">
          <BIconList v-if="!navStore.mobileNavOpen" style="font-size: 1.5rem;" />
          <BIconArrowDown v-else style="font-size: 1.5rem;" />
        </button>
      </nav>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAnalyticsStore } from '../stores/useAnalyticsStore';
import { useNavigationStore } from '../stores/useNavigationStore';
import TopNavBar from '../components/TopNavBar.vue';
import HotspotAnalyticsReport from '../components/HotspotAnalyticsReport.vue';
import AnalyticsConfigPanel from '../components/AnalyticsConfigPanel.vue';
import { BIconArrowLeft, BIconList, BIconArrowDown } from 'bootstrap-icons-vue';

export default defineComponent({
  name: 'HotspotDetail',

  components: {
    TopNavBar,
    HotspotAnalyticsReport,
    AnalyticsConfigPanel,
    BIconArrowLeft,
    BIconList,
    BIconArrowDown
  },

  setup() {
    const store = useAnalyticsStore();
    const navStore = useNavigationStore();
    const route = useRoute();
    
    // carousel state - default to middle slide (graph/list)
    const currentSlide = ref(2);
    const carouselTrack = ref<HTMLElement | null>(null);
    const slide2 = ref<HTMLElement | null>(null);
    // mobileNavOpen removed (handled by navStore)

    // trigger fetch on load instead of search page
    onMounted(() => {
      const id = route.params.id as string;

      if (id) {
          store.selectedHotspotId = id
          store.fetchHotspotDetail();
      }
      
      // Scroll to middle slide after mount using scrollIntoView
      setTimeout(() => {
        if (slide2.value) {
          slide2.value.scrollIntoView({ inline: 'center', behavior: 'auto' });
        }
      }, 150);
    });
    

    // shared navigation handler
    // handleNavClick removed (unused)

    // handle scroll to update active dot
    const handleCarouselScroll = () => {
      if (!carouselTrack.value) return;
      
      const scrollLeft = carouselTrack.value.scrollLeft;
      const slideWidth = carouselTrack.value.offsetWidth;
      const newSlide = Math.round(scrollLeft / slideWidth) + 1;
      
      if (newSlide >= 1 && newSlide <= 3 && newSlide !== currentSlide.value) {
        currentSlide.value = newSlide;
      }
    };
    
    // navigate to specific slide
    const goToSlide = (slideNumber: number) => {
      if (!carouselTrack.value) return;
      
      const slideWidth = carouselTrack.value.offsetWidth;
      carouselTrack.value.scrollTo({
        left: (slideNumber - 1) * slideWidth,
        behavior: 'smooth'
      });
      currentSlide.value = slideNumber;
    };
    
    // navigation functions
    const router = useRouter();
    
    const goBack = () => {
      router.push('/hotspot-search');
    };
    

      return { 
      store,
      currentSlide,
      carouselTrack,
      slide2,
      goBack,
      handleCarouselScroll,
      goToSlide,
      navStore
    };
  }

});
</script>

<style scoped>
.hotspot-detail {
  padding: 0;
  text-align: center;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg-seamless);
}

/* desktop layout */
.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.config-panel {
  flex: 1;
  max-width: 30%;
  background-color: var(--color-bg-seamless);
  padding: 0;
  box-sizing: border-box;
}

.analytics-report {
  flex: 2;
  min-width: 40%;
  background: var(--color-bg-seamless);
  padding: 0;
  box-sizing: border-box;
}

/* mobile carousel */
.mobile-carousel {
  display: none;
}

/* desktop/mobile visibility */
.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }
  
  .mobile-only {
    display: block !important;
  }
  
  .mobile-carousel {
    display: block;
    position: relative;
    width: 100%;
    flex: 1;
    height: 100%;
    overflow: hidden;
  }
  
  .carousel-track {
    display: flex;
    width: 100%;
    height: 100%;
    padding-bottom: 0;
    overflow-x: auto;
    overflow-y: hidden;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  
  .carousel-track::-webkit-scrollbar {
    display: none;
  }
  
  .carousel-slide {
    flex: 0 0 100%;
    min-width: 100%;
    scroll-snap-align: start;
    scroll-snap-stop: always;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    background: var(--color-bg-page);
    scrollbar-width: none;
  }
  
  .carousel-slide::-webkit-scrollbar {
    display: none;
  }
  
  .slide-content {
    min-height: 100%;
    padding-bottom: 0px;
  }
  

  
  /* fixed bottom navigation bar */
  .carousel-nav-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 72px;
    background: var(--color-bg-panel);
    border-top: 1px solid var(--color-border-light);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    z-index: 100;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  }
  
  .carousel-dots {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
  }
  
  .carousel-dot {
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background: var(--color-text-muted, #888);
    opacity: 0.4;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
  }
  
  .carousel-dot.active {
    width: 24px; /* Wider when active */
    background: var(--color-primary);
    opacity: 1;
  }
  
  /* .nav-btn styles removed to use global responsive.css version */

}

/* ===============================
  Tablet Styles (769px - 1330px)
  wider config panel for data distribution graph
  =============================== */

@media (min-width: 769px) and (max-width: 1330px) {
  .hotspot-detail {
    display: flex;
    flex-direction: column;
  }
  
  .content {
    display: flex;
  }
  
  .config-panel {
    max-width: 280px;
    min-width: 260px;
    height: 100vh;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    flex-shrink: 0;
  }
  
  .analytics-report {
    flex: 1;
    height: 100vh;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
}

/* mobile drawer styles */
.nav-left {
  display: none; /* hidden on desktop / default */
}

@media (max-width: 768px) {
  .nav-left.mobile-open {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: auto;
    bottom: 72px;
    left: 0;
    right: 0;
    background: var(--color-bg-panel);
    padding: 16px;
    box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
    z-index: 99;
    border-top: 1px solid var(--color-border-light);
    border-radius: 16px 16px 0 0;
    max-height: 50vh;
  }

  .nav-item {
    padding: 12px;
    font-size: 1.2rem;
    border: none;
    background: transparent;
    text-align: left;
    color: var(--color-text-primary);
    cursor: pointer;
  }
  
  .nav-item:hover {
    background: var(--color-bg-muted);
    border-radius: 8px;
  }
  
  .mobile-nav-item {
    margin-top: 10px;
    display: flex;
    justify-content: center;
  }
}
</style>