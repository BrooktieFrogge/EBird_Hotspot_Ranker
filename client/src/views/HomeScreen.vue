<template>
  <div class="homescreen-container">
    <TopNavBar />

    <div class="page-shell">
      <div
        class="carousel-nav-bar mobile-only"
        :class="{ 'dock-lifted': navStore.mobileNavOpen }"
      >
        <div style="width: 44px"></div>

        <button
          class="nav-btn nav-search-dock-text"
          @click="goToHotspotSearch"
          aria-label="Search"
        >
          <span>Search Hotspots</span>
        </button>

        <button
          class="nav-btn"
          @click="navStore.toggleMobileNav()"
          aria-label="Toggle navigation"
        >
          <BIconList v-if="!navStore.mobileNavOpen" style="font-size: 1.5rem" />
          <BIconArrowDown v-else style="font-size: 1.5rem" />
        </button>
      </div>

      <div class="cover-banner">
        <img
          class="cover-photo"
          :src="coverPhoto"
          alt="FeatherWeight Cover Photo, colorful bird"
        />
        <div class="cover-content">
          <h1 class="cover-heading">Welcome to FeatherWeight!</h1>

          <h2 class="cover-subheading">the eBird Hotspot Likelihood Ranker</h2>

          <div class="cover-buttons">
            <button class="cover-item" @click="scrollToSection('how-to')">
              How to Use
            </button>
            <button
              class="cover-item cover-item-dark"
              @click="scrollToSection('learn')"
            >
              Learn More
            </button>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT -->
      <main class="main-layout">
        <section class="content">
          <!-- Intro Section -->
          <div class="intro-section">
            <div class="intro-section-imgs">
              <div class="intro-item">
                <p class="standout">
                  <b>Question:</b> At the Copalinga Lodge (Ecuador), what is the
                  likelihood of seeing the rare, reclusive Gray Tinamou?!
                </p>
                <figure>
                  <img
                    :src="birdImage2"
                    alt="Bird illustration"
                    class="rect-image"
                  />
                  <figcaption class="captions">© Brandon Nidiffer</figcaption>
                </figure>
              </div>

              <div class="intro-item">
                <p class="standout">
                  <b>Question:</b> Is it a “sure-bet”, or not, to see the
                  stunning Green-and-gold Tanager?
                </p>
                <figure>
                  <img
                    :src="birdImage"
                    alt="Bird illustration"
                    class="rect-image"
                  />
                  <figcaption class="captions">
                    © Luis Alberto Salagaje Muela
                  </figcaption>
                </figure>
              </div>

              <div class="intro-item">
                <p class="standout">
                  <b>Question:</b> For any eBird Hotspot, what are the top 40-50
                  most likely bird species that you might spot at the time you
                  will be there??
                </p>

                <figure>
                  <img
                    :src="eBirdStill"
                    alt="Bird illustration"
                    class="rect-image"
                  />

                  <figcaption class="captions">
                    <a href="https://ebird.org/hotspots">
                      eBird Explore Hotspots</a
                    >
                  </figcaption>
                </figure>
              </div>
            </div>
            <div class="gs-info">
              <p class="med-text">
                The eBird hotspot ranker lets you estimate the likelihood of
                seeing bird species with hotspot data during the same interval
                of weeks compiled over multiple years. Using real-time reports
                from the eBird hotspot data at the Cornell Ornithology
                Laboratory, you can:
              </p>

              <ul class="feature-list">
                <li>
                  determine the most likely birds you will encounter at a
                  hotspot in a specific week,
                </li>
                <li>
                  assess the relative likelihood of seeing a target species at a
                  given hotspot around specific weeks relative to reports of
                  other species,
                </li>
                <li>
                  evaluate how often an uncommon or rare bird that you spotted
                  is reported, or
                </li>
                <li>
                  use the ranked list to practice songs and calls of resident
                  species before visiting the hotspot
                </li>
              </ul>

              <p class="med-text">
                Please continue to the
                <b>eBird Hotspot List Likelihood Page</b>, and learn
                <b>How To Use</b>, or see webpage Documentation.
              </p>
            </div>
          </div>

          <div class="about-section" id="about">
            <div class="about-section-content">
              <h2 class="section-heading">About FeatherWeight</h2>
              <figure class="right-image-panel">
                <img
                  :src="birdImage4"
                  alt="Bird illustration"
                  class="rect-image"
                />
                <figcaption class="captions">©John Clough</figcaption>
              </figure>

              <p class="about-subsection">
                Among exciting birding experiences is venturing to a new
                locality to explore new ecosystems and birds. Such travels,
                domestic or international, might include seeking “target”
                species for a lifelist or year list, or experiencing a wholly
                new avian slate in a completely novel setting. Reviewing eBird
                hotspots lists and bar charts is an excellent approach to
                study-up prior to a trip to see what one might expect to see, or
                to gauge the possibility of spotting new or target species. It's
                a good place to start.
              </p>

              <p class="about-subsection">
                At the same time, for a venture that includes a number of
                hotspots with a high species diversity, scrolling through
                multiple sets of eBird hotspot lists can be a dizzying affair.
                This is particularly true for hotspots such as in neotropical
                regions that may have upward of 400-500 species, many or all of
                which might be new for a birder.
              </p>

              <figure class="left-image-panel">
                <img
                  :src="birdImage3"
                  alt="Bird illustration"
                  class="rect-image"
                />
                <figcaption class="captions">©Andrés Posada</figcaption>
              </figure>

              <p class="about-subsection">
                How might one focus on some of the common birds at an eBird
                hotspot to know what one might see? Or, what is the relative
                likelihood of seeing rare or “target” species at the hotspot you
                are visiting? That's where the eBird hotspot likelihood ranker
                can help.
              </p>

              <p class="about-subsection">
                Using select hotspots for an upcoming birding outing, this site
                lets birders pool, rank, or filter data from eBird hotspot lists
                to help a birder identify the top, expected 40-50 (or however
                many) most common species for a hotspot, as well as estimate the
                likelihood of rarer or “target” species. Likelihoods are
                determined from eBird data reported from that hotspot for an
                interval of weeks over a duration of years. Likelihood
                “rankings” are also normalized as percentages to the most
                frequently reported species at each hotspot for the selected
                time interval.
              </p>
            </div>
          </div>
          <div class="how-section" id="how-to">
            <div class="how-section-content">
              <div class="cards-grid">
                <div class="card-column">
                  <h2 class="section-heading">How to Use</h2>
                  <div class="how-card blue-card">
                    <ol class="how-ol">
                      <li>
                        Enter the name of your eBird hotspot. Click on
                        identifying card for your hotspot.
                      </li>
                      <li>
                        Enter the start year and end year for your sample. Many
                        birders select 10-15 year intervals to get a good sample
                        of lists. Click “CONFIRM YEARS”
                      </li>
                      <li>
                        Select the interval of weeks to include in your sample
                        of lists. For example, if you were visiting a hotspot
                        the 1st week or July, you might bracket this week with 5
                        weeks prior, and 5 weeks after (i.e., bracket week 4 in
                        May to week 2 August, for an 11-week interval).
                      </li>
                      <li>
                        Inspect the distribution of lists in that interval of
                        weeks to see if you have a representative distribution
                        of lists in that interval of weeks over several years.
                        You can adjust weeks of the interval or years to
                        increase or decrease the number of lists in your sample.
                        Note that simply adding more years may not increase list
                        sample if lists don't exist for the added years (i.e.,
                        extending years to 1900).
                      </li>
                      <li>Enter the number of species to display.</li>
                      <li>
                        Decide whether to show the List Likelihood curve for the
                        hotspot, the List Likelihood curve as percent (i.e.,
                        normalized to top-ranked species for week interval), or
                        both.
                      </li>
                      <li>
                        For species you are curious about that may have a low
                        ranking, enter names in “custom species…” You have
                        choice to display photo of custom species.
                      </li>
                      <li>
                        Export: To obtain a file with your ranked likelihoods,
                        select export file format (e.g., .docx, .pdf, .csv) and
                        browse to location to download the file.
                      </li>
                    </ol>
                  </div>
                </div>

                <div class="card-column">
                  <h2 class="section-heading-2">Items to Keep in Mind</h2>
                  <div class="how-card white-card">
                    <p class="how-subsection">
                      A number of factors might increase or decrease the
                      relative ranks of species at a hotspot for the interval of
                      weeks and duration of years selected. For example,
                    </p>
                    <ul class="how-ul">
                      <li>
                        Hotspots that are new or on private property may have a
                        relatively limited set of lists as part of the sample.
                        One can assess total number of lists in sample after
                        entering years and weeks.
                      </li>
                      <li>
                        Data in the lists is reported by birders with varying
                        levels of experience, yet also reviewed for accuracy by
                        local eBird moderators.
                      </li>
                      <li>
                        Rankings may be biased in favor of target species,
                        particularly when birders and guides go to specific
                        hotspots for hard-to-get species. But then again, that's
                        what the rankings are intended to show -likelihood of
                        spotting hard-to-get species when birders are trying to
                        see them.
                      </li>
                      <li>
                        Similarly, lists may not include all common residents
                        when birders are focused on target species.
                      </li>
                      <li>
                        During migration, species passing through may have
                        relatively narrow windows where they are relatively more
                        likely.
                      </li>
                      <li>
                        Birders might have included in their hotspot list
                        species spotted in specialized habitats near the
                        hotspot, but not exactly at the hotspot.
                      </li>
                      <li>
                        Likelihood rankings do not take into account number of
                        individuals of a species on a list. It only accounts for
                        whether or not the species was observed and included in
                        a list.
                      </li>
                      <li>
                        Likelihoods may change for a hotspot depending on the
                        years selected, or as new checklists are added to the
                        database in the future.
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="doc-section" id="learn">
            <div class="doc-section-content">
              <h2 class="section-heading">Documentation</h2>

              <h2 class="section-heading-2">Validity Tests</h2>

              <p class="doc-subsection">
                Several approaches were used to test the validity of the hotspot
                likelihood ranks. First, to test webpage for rank accuracy,
                results for an interval of 10 weeks over a duration of 12 years
                were compared between the code output and ranks computed “by
                hand” in an Excel file. The results were identical. Second, to
                test the approach in the field, eBird data from 4 hotspots in
                southern Ecuador with high species diversity were processed late
                spring, 2024, prior to a birding trip to those hotspots in
                mid-July, 2024. Species lists at the hopspots in February, 2025,
                were Copalinga Lodge=550, Jorupe Lodge=230, Reserva Utuana=330,
                and Cabañas Yankuam=511. The sample consisted of sightings for
                the week of the visit, bracketted by data from 6 weeks prior to
                and 6 weeks after the week of the visit, all pooled in the same
                interval over 5 consecutive years.
              </p>

              <p class="doc-subsection">
                In all cases, nearly all of the ranked, top 40 most common
                species were spotted at each of the 4 hotspots. Moreover, the
                approach was able to place in context, compared with other eBird
                lists at the hotspot, much rarer species that were observed at
                the hotspot (see figure) While some of the latter species are
                very infrequently encounted, data indicate that hard work at the
                4 hotspots did yield some of the “really tough” or very
                infrequently observed species.
              </p>

              <figure class="centered-image-panel">
                <img
                  :src="graph"
                  alt="Relative likelihood graph"
                  class="rect-image graph"
                />
              </figure>

              <p class="doc-subsection">
                <b>FIGURE:</b> Graph of relative likelihood (as Report Factor %)
                by species at 4 hotspots, and whether (YES) or not (NO) a
                species was observed in July 2024 trip to the hotspot. In almost
                all cases, species with a relative rank greater than about 60
                were observed. A number of relatively uncommon species in the
                20-40% range were observed, along with a several species in the
                &lt 10% bracket for each site. In several cases, high ranking
                species in the “NO” distribution that weren't observed at the
                hotspot were observed within several kilometers of the hotspot.
                Note that data tend to cluster in horizontal bars (Utauna,
                Yankuam) when the total number of lists in the sample starts to
                become limited.
              </p>
            </div>
          </div>
          <div class="footer-section">
            <div class="footer-section-content">
              <h2 class="footer-heading">Image Credits</h2>

              <p class="footer">
                <a href="https://media.ebird.org/" class="footer-link">
                  Sources: "https://media.ebird.org/"</a
                >
              </p>
              <p class="footer">Cover Photo: © Fernando Saravia</p>

              <h2 class="footer-heading">Project Acknowledgements</h2>

              <p class="footer">
                Collaborators from Colorado College developing this version of
                Hotspot Featherweight are Dr. Steve Getty and Computer Science
                students Brooktie Frogge, Erin Liedeker, Jevon Lipsey, Zahara
                Love. The team acknowledges the work by Cornell Lab of
                Ornithology to develop eBird and enable users access to eBird
                hotspot raw data.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { BIconList, BIconArrowDown } from "bootstrap-icons-vue";
import TopNavBar from "../components/TopNavBar.vue";
import { useNavigationStore } from "../stores/useNavigationStore";
import birdImage from "../assets/bird.png";
import birdImage2 from "../assets/bird2.png";
import birdImage3 from "../assets/bird3.png";
import birdImage4 from "../assets/bird4.png";
import graph from "../assets/graph.png";
import coverPhoto from "../assets/coverPhoto.png";
import eBirdStill from "../assets/ebird.png";
const router = useRouter();
const navStore = useNavigationStore();
const isDarkMode = ref(false);

// watch for theme changes
const checkDarkMode = () => {
  isDarkMode.value = document.body.classList.contains("theme--dark");
};

onMounted(() => {
  checkDarkMode();
  const observer = new MutationObserver(checkDarkMode);
  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["class"],
  });
});

function goToHotspotSearch() {
  router.push("/hotspot-search");
}

const scrollToSection = (id: string) => {
  navStore.closeMobileNav();
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  } else if (id === "home") {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  font-family: CloSans, CloSans override, Noto Sans, Noto Sans Hebrew,
    -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen-Sans, Ubuntu,
    Cantarell, Helvetica Neue, sans-serif;
}
.homescreen-container {
  height: 100vh;
  background: var(--color-bg-page);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-shell {
  width: 100%;
  flex: 1;
  background: var(--color-bg-page);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scrollbar-width: none;
}

.page-shell::-webkit-scrollbar {
  display: none;
}

/* Title bar */
.title-bar {
  background-color: var(--color-bg-panel);
  padding: 25px 40px 29x;
  text-align: center;
  border-bottom: 1px solid var(--color-border-light);
}

@media (min-width: 769px) {
  .title-bar {
    display: none;
  }
}

.title-bar h1 {
  font-size: 32px;
  letter-spacing: 0.03em;
}

.title-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.header-logo {
  margin-top: 1%;
  width: 740px;
  height: 130px;
  aspect-ratio: 343/47;
  border-radius: 5px;
}
/* Top blue strip */

.nav-search-dock {
  background: var(--color-danger) !important;
  color: white !important;
  border-radius: 6px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
}

.nav-search-dock-text {
  background: var(--color-danger) !important;
  color: white !important;
  border-radius: 6px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border: none !important;
  font-size: 16px;
  font-weight: 500;
  width: auto;
  flex: none;
}
.cover-banner {
  width: 100%;
  position: relative;
  text-align: center;
  min-height: 500px;
}
.cover-photo {
  width: 100%;
  height: 100%;
  min-height: 500px;
  object-fit: cover;
  opacity: 90%;
}

.cover-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
  padding: 40px 20px;
}

.cover-heading {
  color: var(--color-white);
  font-size: clamp(1.8rem, 7vw, 6rem);
  text-align: center;
  margin-bottom: 2vh;
  text-shadow: 0 0 0.8rem var(--shadow-text-strong);
  letter-spacing: -0.03rem;
  font-weight: 800;
  line-height: 1.1;
  max-width: 90%;
}

.cover-subheading {
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 2.5rem);
  text-align: center;
  margin-bottom: 4vh;
  text-shadow: 0 0 0.8rem var(--shadow-text-strong);
  font-weight: 400;
  max-width: 90%;
}

.cover-item {
  background: var(--color-white);
  color: var(--color-black);
  width: 160px;
  font-weight: 400;
  font-size: 20px;
  font-style: normal;
  border-radius: 6px;
  padding: 8px 16px;
  border: none;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35);
  cursor: pointer;
}

.cover-item-dark {
  background: var(--color-primary-variation);
  color: var(--color-white);
}

.cover-item:hover {
  background: var(--color-bg-hover);
}

.cover-item-dark:hover {
  background: var(--color-primary-dark);
}

.cover-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.main-layout {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
}

.content {
  color: var(--color-text-primary);
}

.section-heading {
  font-weight: 300;
  font-size: 4rem;
  line-height: 1.111;
  letter-spacing: -0.02rem;
  margin: 0 0 2rem 0;
  color: var(--color-text-primary);
}

.section-heading-2 {
  font-weight: 300;
  font-size: 4rem;
  line-height: 1.111;
  letter-spacing: -0.02rem;
  margin: 1rem 2rem;
  color: var(--color-accent-blue);
}

.footer-heading {
  font-weight: 300;
  font-size: 2rem;
  line-height: 1.111;
  letter-spacing: -0.02rem;
  margin: 1rem 2rem;
  color: var(--color-accent-blue);
}

.about-section {
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset,
    0 4px 4px 0 rgba(0, 0, 0, 0.25);
}

.about-section-content {
  align-items: start;
  max-width: 1480px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  padding: 100px 10px 100px 80px;
}

.about-subsection {
  font-weight: 400;
  font-size: 1.5rem;
  color: var(--color-text-primary);
}

.how-section {
  position: relative;
  z-index: 2;
  background: var(--color-bg-muted);
  padding: 100px 10px 100px 80px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset,
    0 4px 4px 0 rgba(0, 0, 0, 0.25);
}
.cards-grid {
  display: flex;
  flex-direction: column;
  gap: 60px;
  padding-top: 20px;
  position: relative;
}

.card-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}
.card-column .section-heading,
.card-column .section-heading-2 {
  margin: 0 0 1.5rem 0;
  text-align: center;
  width: 100%;
}

.how-card {
  position: relative;
  padding: 40px;
  width: 100%;
  border-radius: 12px;
  box-sizing: border-box;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.blue-card,
.white-card {
  background: var(--color-bg-panel);
  z-index: 2;
  border: none;
}

:deep(body.theme--dark) .white-card {
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border-light);
}

/* ===============================
  Desktop Layout (>1024px)
  =============================== */
@media (min-width: 1024px) {
  .cards-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: stretch;
  }

  .how-card {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

ol li,
ul li {
  margin-bottom: 25px;
}
.feature-list {
  margin: 0 0 16px;
  line-height: 1.6;
  font-size: 23px;
  font-weight: 400;
  align-items: center;
  text-align: left;
  flex-direction: column;
  color: var(--color-text-primary);
  max-width: 1350px;
  margin-left: auto;
  margin-right: auto;
}

/* Right-side image panel */
.right-image-panel {
  justify-content: right;
  align-items: flex-start;
  float: right;
  margin: 0 0 20px 40px;
}

/* Left-side image panel */
.left-image-panel {
  float: left;
  margin: 40px 40px 0 0;
  justify-content: left;
  align-items: flex-start;
}

.centered-image-panel {
  max-width: 1200px;
  margin: 40px 100px 20px 100px;
  justify-content: center;
  align-items: flex-start;
}

.doc-section {
  position: relative;
  z-index: 2;
  max-width: 100%;
  padding: 10px 10px 100px 80px;
  max-height: 1800px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset,
    0 4px 4px 0 rgba(0, 0, 0, 0.25);
}

.doc-section-content {
  height: 100%;
  position: relative;
  color: var(--color-text-primary);
  max-width: 1480px;
  margin-left: auto;
  margin-right: auto;
  margin: 50px auto 50px auto;
}

.doc-subsection {
  margin-top: 10px;
  font-weight: 400;
  font-size: 24px;
  color: var(--color-text-primary);
}

.intro-section {
  max-height: auto;
  max-width: 1480px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 40px;
  padding: 10px 5%;
  position: relative;
  z-index: 2;
}

.intro-section-imgs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  align-items: stretch;
}
.intro-item {
  display: grid;
  grid-template-rows: 1fr 300px;
  flex-direction: column;
  height: 100%;
  align-items: center;
}

.intro-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.captions {
  text-align: left;
  color: var(--color-text-secondary);
}
.standout {
  font-weight: 700;
  font-size: 21px;
  font-style: normal;
  color: var(--color-accent-blue);
  text-align: center;
  margin-bottom: 1rem;
}

/* Rect image */
.rect-image {
  width: 40em;
  height: 25em;
  background: transparent;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  margin-bottom: 10px;
}

.graph {
  width: 100%;
  height: 100%;
  background: transparent;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  margin-bottom: 10px;
}

.gs-info {
  max-width: 1480px;
  height: 100%;
  position: relative;
  bottom: 50%;
  justify-content: center;
  padding: 50px 5% 20px 5%;
  text-align: center;
}

.med-text {
  color: var(--color-text-primary);
  font-size: 28px;
  font-style: normal;
  font-weight: 400;
  margin-left: auto;
  margin-right: auto;
  text-align: left;
}

.footer-section {
  position: relative;
  z-index: 2;
  max-width: 100%;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset,
    0 4px 4px 0 rgba(0, 0, 0, 0.25);
  background: var(--color-bg-panel);
}

.footer-section-content {
  max-width: 100%;
  margin-left: auto;
  margin-right: auto;
  height: auto;
  padding: 40px;
}

a {
  text-decoration: none;
  color: inherit;
}

.footer {
  font-size: 18px;
  color: var(--color-text-secondary);
  margin-top: 16px;
  margin-left: 50px;
}

/* ===============================
  Responsive Styles
  =============================== */

/* Large Tablet (1024-1430px) */
@media (min-width: 1024px) and (max-width: 1430px) {
  .cover-banner,
  .cover-photo {
    min-height: 480px;
  }
}

/* Medium screens (900-1250px) - shift photo to show bird */
@media (min-width: 900px) and (max-width: 1250px) {
  .cover-photo {
    object-position: 65% center;
  }
}

/* Tablet */
@media (max-width: 1024px) {
  .header-logo {
    width: auto;
    max-width: 450px;
    height: auto !important;
    aspect-ratio: auto;
    object-fit: contain;
  }

  .cover-banner,
  .cover-photo {
    min-height: 400px;
  }

  .intro-section-imgs {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    padding: 0 20px;
  }

  .rect-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .about-section-content,
  .how-section,
  .doc-section {
    padding: 60px 30px;
    height: auto !important;
    min-height: auto;
  }

  .intro-section {
    margin-top: 50px;
  }
}

/* Small Tablet (769-900px) */
@media (min-width: 769px) and (max-width: 900px) {
  .cover-banner,
  .cover-photo {
    min-height: 360px;
  }

  .cover-photo {
    object-position: 70% center; /* shift right to show the bird */
  }

  .intro-section {
    margin-top: 50px;
  }

  .cover-item {
    min-width: 90px;
    font-size: 14px;
    padding: 6px 12px;
  }
}

/* Mobile */
@media (max-width: 768px) {
  /* header & logo */
  .title-bar {
    padding: 10px 15px;
    border-bottom: none;
  }

  .header-logo {
    width: 200px;
    height: auto !important;
    aspect-ratio: auto;
    object-fit: contain;
  }

  /* navigation */
  .top-nav {
    padding: 0;
    height: 0;
    overflow: visible;
    background: transparent;
    box-shadow: none;
    pointer-events: none;
  }

  .top-nav > * {
    pointer-events: auto;
  }

  .nav-left {
    display: none;
  }

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
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.15);
    border-top: 1px solid var(--color-border-light);
    border-bottom: none;
    border-radius: 16px 16px 0 0;
    align-items: flex-start;
  }

  .nav-left.mobile-open .nav-item {
    text-align: left;
    padding-left: 0;
  }

  .nav-search {
    font-size: 16px;
    padding: 6px 12px;
  }

  /* cover banner - mobile tweaks */
  .cover-banner {
    min-height: 380px;
  }

  .cover-photo {
    height: 400px;
    object-position: 75% center; /* shift right to show the bird */
  }

  .cover-heading {
    white-space: normal;
    padding: 0 10px;
  }

  .cover-subheading {
    padding: 0 10px;
  }

  .cover-buttons {
    gap: 12px;
  }

  .cover-item {
    width: auto;
    min-width: 100px;
    font-size: 14px;
    padding: 8px 14px;
  }

  /* intro section - single column */
  .intro-section {
    margin-top: 60px;
    padding: 0 16px;
  }

  .intro-section-imgs {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .intro-item {
    grid-template-rows: auto auto;
  }

  .standout {
    font-size: 18px;
  }

  .gs-info {
    padding: 30px 10px;
  }

  .med-text {
    font-size: 18px;
  }

  .feature-list {
    font-size: 16px;
    padding-left: 20px;
  }

  /* section headings */
  .section-heading {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .section-heading-2 {
    font-weight: 300;
    font-size: 4rem;
    line-height: 1.111;
    letter-spacing: -0.02rem;
    margin: 1rem 2rem;
    color: var(--color-accent-blue);
  }

  /* about section */
  .about-section-content {
    padding: 40px 20px;
  }

  .about-subsection {
    font-size: 1rem;
  }

  .right-image-panel,
  .left-image-panel {
    float: none;
    margin: 20px auto;
    width: 100%;
  }

  .right-image-panel .rect-image,
  .left-image-panel .rect-image {
    width: 100%;
    height: auto;
    max-height: 300px;
    object-fit: cover;
  }

  /* how section */
  .how-section {
    padding: 40px 20px;
    max-height: none;
  }

  .how-section-content {
    height: auto;
  }

  .cards {
    position: static;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .how-card {
    position: static;
    width: 100%;
    transform: none;
    filter: none;
  }

  .blue-card,
  .white-card {
    transform: none;
    margin-bottom: 20px;
  }

  .how-ol,
  .how-ul {
    font-size: 16px;
    padding: 15px 10px 20px 25px;
    margin: 0;
  }

  .how-subsection {
    font-size: 18px;
    margin: 15px;
  }

  /* documentation section */
  .doc-section {
    padding: 40px 20px;
    max-height: none;
  }

  .doc-subsection {
    font-size: 16px;
  }

  .centered-image-panel {
    margin: 20px 0;
  }

  .centered-image-panel .rect-image {
    width: 100%;
    height: auto;
  }

  /* footer */
  .footer-section {
    max-height: none;
  }

  .footer-section-content {
    padding: 20px;
  }

  .footer {
    font-size: 14px;
    margin-left: 0;
  }

  .footer-heading {
    font-size: 1.5rem;
  }
}
</style>
