<template>
  <div class="homescreen-container">
    <div class="page-shell">
      <!-- PAGE TITLE BAR -->
      <header class="title-bar" id="home">
        <div class="title-content">
          <img class="header-logo" :src="logo" alt="FeatherWeight Logo" />
        </div>
      </header>

      <!-- TOP NAV / MENU -->
      <nav class="top-nav">
        <div class="nav-left">
          <button class="nav-item nav-item-active"><a href="#home"> Home</a>
          </button>
          <button class="nav-item"><a href="#about"> About</a>
          </button>
        </div>

        <div class="nav-right">
          <button class="nav-search" @click="goToHotspotSearch">Search Hotspots</button>
        </div>
      </nav>

      <div class="cover-banner">

        <img class="cover-photo" :src="coverPhoto" alt="FeatherWeight Cover Photo, colorful bird"/>
        <h1 class="cover-heading">Welcome to Hotspot FeatherWeight!</h1>

          <h2 class="cover-subheading">the eBird Hotspot Likelihood Ranker</h2>

          <div class="cover-left">
          <button class="cover-item"><a href="#how-to"> How to Use</a>
          </button>
          </div>

          <div class="cover-right">
            <button class="cover-item cover-item-dark" ><a href="#learn"> Learn More</a>
            </button>
          </div>

      </div>

      <!-- MAIN CONTENT -->
      <main class="main-layout">
        <section class="content">
           <!-- Intro Section -->
           <div class="intro-section">
              <div class="intro-section-imgs">
                <div class="intro-item">
                  <figure>
                    <img
                      :src="birdImage2"
                      alt="Bird illustration"
                      class="rect-image
                    "
                    />
                    <figcaption class="captions">© Brandon Nidiffer</figcaption>
                  </figure>
              
                  <p class="standout">
                    <b>Question:</b> At the Copalinga Lodge (Ecuador), what is the likelihood of seeing the rare, reclusive Gray Tinamou?!</p>
                </div>

                <div class="intro-item">
                  <figure>
                    <img
                      :src="birdImage"
                      alt="Bird illustration"
                      class="rect-image
                    "
                    />
                    <figcaption  class="captions">© Luis Alberto Salagaje Muela</figcaption>
                  </figure>

                  <p class="standout">
                    <b>Question:</b> Is it a “sure-bet”, or not, to see the stunning Green-and-gold Tanager? </p>
                </div>
              
                <div class="intro-item">
                  <figure>
                    <img
                      :src="eBirdStill"
                      alt="Bird illustration"
                      class="rect-image
                    "
                    />

                    <figcaption  class="captions">
                    <a href="https://ebird.org/hotspots" style="color:black"> eBird Explore Hotspots</a></figcaption>

                  </figure>
                  <p class="standout">
                      <b>Question:</b> For any eBird Hotspot, what are the top 40-50 most likely bird species that you might spot at the time you will be there??
                    </p>
                </div>

              </div>
            </div>

            <div class="gradient-section">
              <div class ="gs-info">
                  <p class="med-text"> The eBird hotspot ranker lets you estimate the likelihood of seeing bird species with hotspot data during the same interval of weeks compiled over multiple years. Using real-time reports from the eBird hotspot data at the Cornell Ornithology Laboratory, you can:</p>

                  <ul class="feature-list">
                    <li>determine the most likely birds you will encounter at a hotspot in a specific week,</li>
                    <li>assess the relative likelihood of seeing a target species at a given hotspot around specific weeks relative to reports of other species,</li>
                    <li>evaluate how often an uncommon or rare bird that you spotted is reported, or</li>
                    <li>use the ranked list to practice songs and calls of resident species before visiting the hotspot</li>
                  
                  </ul> 

                  <p class="med-text">Please continue to the <b>eBird Hotspot List Likelihood Page</b>, and learn <b>How To Use</b>, or see webpage Documentation.</p>
              </div>

            </div>

            <div class="about-section" id="about">
              <div class="about-section-content">
                <h2 class="section-heading">About FeatherWeight</h2>
                <figure class="right-image-panel">
                    <img
                      :src="birdImage4"
                      alt="Bird illustration"
                      class="rect-image
                    "
                    />
                    <figcaption  class="captions">
                      © insert official caption here</figcaption>

                  </figure>

                <p class="about-subsection">
                    Among exciting birding experiences is venturing to a new locality to explore new ecosystems and birds. Such travels, domestic or international, might include seeking “target” species for a lifelist or year list, or experiencing a wholly new avian slate in a completely novel setting. Reviewing eBird hotspots lists and bar charts is an excellent approach to study-up prior to a trip to see what one might expect to see, or to gauge
                    the possibility of spotting new or target species. It's a good place to start.</p>

                  <p class="about-subsection">At the same time, for a venture that includes a number of hotspots with a high species diversity, scrolling through multiple sets of eBird hotspot lists can be a dizzying affair. This is particularly true for hotspots such as in neotropical regions that may have upward of 400-500 species, many or all of which might be new for a birder.</p>

                  <figure class="left-image-panel">
                    <img
                      :src="birdImage3"
                      alt="Bird illustration"
                      class="rect-image
                    "
                    />
                    <figcaption  class="captions">
                      © insert official caption here</figcaption>

                  </figure>

                  <p class="about-subsection">
                    How might one focus on some of the common birds at an eBird hotspot to know what one might see? Or, what is the relative likelihood of seeing rare or “target” species at the hotspot you are visiting? That's where the eBird hotspot likelihood ranker can help.</p>

                    <p class="about-subsection">Using select hotspots for an upcoming birding outing, this site lets birders pool, rank, or filter data from eBird hotspot lists to help a birder identify the top, expected 40-50  (or however many) most common species for a hotspot, as well as estimate the likelihood of rarer or “target” species. Likelihoods are determined from eBird data reported from that hotspot for an interval of weeks over a duration of years. Likelihood “rankings” are also normalized as percentages to the most frequently reported species at each hotspot for the selected time interval.
                    </p>
              </div>
            </div>
            <div class="how-section" id="how-to">
              <div class="how-section-content">
                <h2 class="section-heading">How to Use</h2>
                <div class="cards">
                  <div class="how-card blue-card">
            
                    <ol class="how-ol">
                      <li>Enter the name of your eBird hotspot. Click on identifying card for your hotspot. </li>
                    <li> Enter the start year and end year for your sample. Many birders select 10-15 year intervals to get a good sample of lists. Click “CONFIRM YEARS”</li>
                    <li>Select the interval of weeks to include in your sample of lists. For example, if you were visiting a hotspot the 1st week or July, you might bracket this week with 5 weeks prior, and 5 weeks after (i.e., bracket week 4 in May to week 2 August, for an 11-week interval). Click “CONFIRM WEEKS”</li>
                    <li>Inspect the distribution of lists in that interval of weeks to see if you have a representative distribution of lists in that interval of weeks over several years. You can adjust weeks of the interval or years to increase or decrease the number of lists in your sample. Note that simply adding more years may not increase list sample if lists don't exist for the added years (i.e., extending years to 1900).</li>
                    <li>Enter the number of species to display (and export?).</li>
                    <li>Decide whether to show the List Likelihood curve for the hotspot, the List Likelihood curve as percent (i.e., normalized to top-ranked species for week interval), or both.</li>
                    <li>For species you are curious about that may have a low ranking, enter names in “custom species…” You have choice to display photo of custom species.</li> 
                    <li>Export: To obtain a file with your ranked likelihoods, select export file format (e.g., .docx, .pdf, .csv) and browse to location to download the file. </li>
                      
                    </ol>
                
                  </div>

                      <div class="how-card white-card">
                        <h2 class="section-heading-2">Items to Keep in Mind</h2>
                        <p class="how-subsection">
                      A number of factors might increase or decrease the relative ranks of species at a hotspot for the interval of weeks and duration of years selected. For example,</p> 

                        <ul class="how-ul">
                          <li>
                            hotspots that are new or on private property may have a relatively limited set of lists as part of the sample. One can assess total number of lists in sample after entering years and weeks.
                          </li>
                          <li>
                            data in the lists is reported by birders with varying levels of experience, yet also reviewed for accuracy by local eBird moderators.
                          </li>
                          <li>
                            rankings may be biased in favor of target species, particularly when birders and guides go to specific hotspots for hard-to-get species. But then again, that's what the rankings are intended to show -likelihood of spotting hard-to-get species when birders are trying to see them.
                          </li>
                          <li>
                            similarly, lists may not include all common residents when birders are focused on target species.
                          </li>
                          <li>
                            during migration, species passing through may have relatively narrow windows where they are relatively more likely. 
                          </li>
                          <li>
                            birders might have included in their hotspot list species spotted in specialized habitats near the hotspot, but not exactly at the hotspot.
                          </li>
                          <li>
                            likelihood rankings do not take into account number of individuals of a species on a list. It only accounts for whether or not the species was observed and included in a list.
                          </li>
                          <li>
                            likelihoods may change for a hotspot depending on the years selected, or as new checklists are added to the database in the future.
                          </li>
                    
                        </ul>
                      </div>
                  </div>
              </div>
            </div>

            <div class="doc-section" id="learn">
              <div class="doc-section-content">
                <h2 class="section-heading">Documentation</h2>

                <h2 class="section-heading-2">Validity Tests</h2>

                <p class="doc-subsection">
                  Several approaches were used to test the validity of the hotspot likelihood ranks. First, to test webpage for rank accuracy, results for an interval of 10 weeks over a duration of 12 years were compared between the code output and ranks computed “by hand” in an Excel file. The results were identical.
                  Second, to test the approach in the field, eBird data from 4 hotspots in southern Ecuador with high species diversity were processed late spring, 2024, prior to a birding trip to those hotspots in mid-July, 2024. Species lists at the hopspots in February, 2025, were Copalinga Lodge=550, Jorupe Lodge=230, Reserva Utuana=330, and Cabañas Yankuam=511. The sample consisted of sightings for the week of the visit, bracketted by data from 6 weeks prior to and 6 weeks after the week of the visit, all pooled in the same interval over 5 consecutive years.</p>

                  <p class="doc-subsection">In all cases, nearly all of the ranked, top 40 most common species were spotted at each of the 4 hotspots. Moreover, the approach was able to place in context, compared with other eBird lists at the hotspot, much rarer species that were observed at the hotspot (see figure) While some of the latter species are very infrequently encounted, data indicate that hard work at the 4 hotspots did yield some of the “really tough” or very infrequently observed species.</p>

                  <figure class="centered-image-panel">
                    <img
                      :src="graph"
                      alt="Relative likelihood graph"
                      class="rect-image"/>

                  </figure>

                  <p class="doc-subsection">
                    <b>FIGURE:</b> Graph of relative likelihood (as Report Factor %) by species at 4 hotspots, and whether (YES) or not (NO) a species was observed in July 2024 trip to the hotspot. In almost all cases, species with a relative rank greater than about 60 were observed. A number of relatively uncommon species in the 20-40% range were observed, along with a several species in the &lt 10% bracket for each site. In several cases, high ranking species in the “NO” distribution that weren't observed at the hotspot were observed within several kilometers of the hotspot. Note that data tend to cluster in horizontal bars (Utauna, Yankuam) when the total number of lists in the sample starts to become limited.</p>

              </div>
            </div>
            <div class="footer-section">
              <div class="footer-section-content">
                <h2 class="section-heading-2">Image Credits</h2>
                <h2 class="section-heading-2">Project Acknowledgements</h2>

                <p class="footer">
                  Collaborators from Colorado College developing this version of Hotspot Featherweight are Dr. Steve Getty and Computer Science students Brooktie Frogge, Erin Liedeker, Jevon Lipsey, Zahara Love. The team acknowledges the work by Cornell Lab of Ornithology to develop eBird and enable users access to eBird hotspot raw data.
                </p>
              </div>

            </div>

        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import birdImage from "../assets/bird.png";
import birdImage2 from "../assets/bird2.png";
import birdImage3 from "../assets/bird3.png";
import birdImage4 from "../assets/bird4.png";
import graph from "../assets/graph.png";
import coverPhoto from "../assets/coverPhoto.png";
import eBirdStill from "../assets/ebird.png";
import logo from "../assets/logo.jpg";

const router = useRouter();

function goToHotspotSearch() {
  router.push("/hotspot-search");
}

</script>

<style>
/* ---- App Colors ---- */
:root {
  --color-charcoal: #1a1a1a;
  --color-offwhite: #f9fafb;
  --color-lightgray: #e5e7eb;

  --color-accent-red: #d64545;
  --color-accent-green: #57a773;
  --color-accent-teal: #3cafaf;

  --color-border: #d1d5db;
  --color-muted: #6b7280;
}
</style>

<style scoped>
/* Outer blue margins similar to the ECM page */
.homescreen-container {
  min-height: 100vh;
  background: white;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* White central panel */
.page-shell {
  width: 100%;
  height: 100vh;
  background: white;
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
  background-color: white;
  padding: 25px 40px 29x;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
}

.title-bar h1 {
  margin: 0;
  font-family: "Monospace", monaco;
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
  width: 740px;
  height: 120px;
  aspect-ratio: 343/47;
  border-radius: 5px;
}

/* Top blue strip */
.top-nav {
  max-height: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 10px 40px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset, 0 4px 4px 0 rgba(0, 0, 0, 0.25);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left,
.nav-right {
  display: flex;
  width: auto;
  gap: 12px;
}

.nav-search{
  width: auto;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  background: #2C2C2C;
  border: black;
  justify-content:center;
  align-items: center;
  padding: 7px;
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  font-family: "Sans", inter;
  line-height: 100%;
  transition: background 0.15s ease, color 0.15s ease;
}


.nav-search:hover {
  background: #335c74;
}

.nav-item {
  border: none;
  background: transparent;
  color: black;
  padding: 7px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 6px;
  font-style: normal;
  font-weight: 400;
  font-family: "Sans", inter;
  line-height: 100%;
  transition: background 0.15s ease, color 0.15s ease;
  
}

.nav-item:hover {
  background: #F5F5F5;
}

.nav-item-active {
  background: #F5F5F5;
  border-bottom: 3px solid #F5F5F5;
  border-radius: 6;
}

.cover-banner{
  width:100%;
  height: 288px;
  aspect-ratio: 437/72;
  position: relative;
  text-align: center; 
}
.cover-photo{
  width:100%;
  height: 100%;
}

.cover-heading{
  color: black;
  font-family: "Serif", Noto;
  font-size: 50px;
  font-style: normal;
  font-weight: 400;
  justify-content: center;
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: transparent;
}

.cover-subheading{
  color: black;
  font-family: "Roboto", sans-serif;
  font-size: 32px;
  font-style: normal;
  font-weight: 300;
  justify-content: center;
  position: absolute;
  top: 62%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: transparent;
}

.cover-item{

  background: white;
  color: #000000;
  width: 160px;
  font-weight: 400;
  font-size:20px;
  font-family: "Sans", inter;
  font-style: normal;
  border-radius: 6px;
  padding: 2px;
  border: none;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35);
}

.cover-item-dark{
  background: #2C2C2C;
  color: white;
}

.cover-item:hover{
  background: #d0cfcf;
}
.cover-item-dark:hover{
  background: #335c74;
}

.cover-left{
  position: absolute;
  top: 85%;
  left: 50%;
  transform: translate(-120%, -50%);
}

.cover-right{
  position: absolute;
  top: 85%;
  left: 50%;
  transform: translate(5%,-50%);
 
}
.main-layout {
  display: grid;
}

.content {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
  color: black;
}

.about-section{
  position: relative;
  z-index: 2;
  top: -750px;
  max-width: 100%;
  max-height: 1800px;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset, 0 4px 4px 0 rgba(0, 0, 0, 0.25);
}

.section-heading {
  font-family: "Serif", Noto;
  font-weight: 400;
  font-size: 48px;
  margin: 0 0 16px;
  color: #950000;
  text-decoration: underline;
}

.section-heading-2 {
  font-family: "Serif", Noto;
  font-weight: 400;
  font-size: 36px;
  margin: 15px 30px;
  color: #203746;
  text-decoration: underline;
}

.about-section-content {
  max-width: 1480px;
  margin-left: 150px ;
  padding: 100px 10px 100px 80px ;
}

.about-subsection{
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-size: 24px;
  color: black;
}

.how-section {
  position: relative;
  z-index: 2;
  top: -750px;
  max-width: 100%;
  max-height: 5900px;
  padding: 100px 10px 100px 80px ;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset, 0 4px 4px 0 rgba(0, 0, 0, 0.25);
}

.cards{
  position: relative;
  top: 80px;
  max-width: 1450px;
}

.how-section-content {
  height: 1600px;
  position: relative;
  margin-left: 150px ;
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-size: 24px;
  color: black;
}

.how-ol{
color: white;
padding: 20px 10px 40px 60px;
font-family: "Roboto", sans-serif;
font-weight: 400;
font-size: 20px;
margin: 0 50px;

}
.how-ul{
color: #203746;
padding: 0px 10px 40px 60px;
font-family: "Roboto", sans-serif;
font-weight: 400;
font-size: 20px;
margin: 0 50px;
}

.how-subsection{
  margin: 20px 30px 0 30px ;
  max-width: 100%;
  font-size: 26px;
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  color: #203746;;

}
.how-card{
  position: absolute;
  padding: 20px 10px 20px 0 ;
  fill: #203746;;
  width: 1000;
  margin-bottom: 0px;
  border-radius: 12px;

}

.blue-card{
  background: #203746;
  box-shadow: 0 4px 4px 0 rgb(0,0,0,0.25) inset;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset;
  transform: translate(-50px,-50px);
  filter: drop-shadow(10px 10px 4px rgba(0,0,0,0.25));

}
.white-card{
  background: white ;
  position: relative;
  top: 560px;
  z-index: 3;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset;
  filter: drop-shadow(10px 10px 4px rgba(0,0,0,0.25));
  transform: translate(24px,24px);;;
}

ol li,
ul li{
  margin-bottom: 25px;
}
.feature-list {
  margin: 0 0 16px;
  line-height: 1.6;
  font-family: "Roboto", sans-serif;
  font-size: 23px;
  font-weight: 400;;
  align-items: center;
  text-align: left;
  flex-direction: column;
  color: black;
  max-width: 1450px;
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
  margin: 40px 40px 0 0 ;
  justify-content: left;
  align-items: flex-start;
}

.centered-image-panel{
  max-width: 1200px;
  margin: 40px 100px 20px  100px  ;
  justify-content: left;
  align-items: flex-start;
}

.doc-section{
  position: relative;
  z-index: 2;
  top: -750px;
  max-width: 100%;
  padding: 10px 10px 100px 80px ;
  max-height: 100%;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset, 0 4px 4px 0 rgba(0, 0, 0, 0.25);
}

.doc-section-content{
  height: 100%;
  position: relative;
  max-width: 1480px;
  color: black;
  margin: 160px ;
}

.doc-subsection{
  font-family: "Roboto", sans-serif;
  margin-top: 10px;
  font-weight: 400;
  font-size: 24px;
  color: black;
}

.intro-section{
  max-width: 1480px;
  max-height: 1382px;
  margin-bottom: 0%;
  margin-top: 5%;
  margin-left: 178px;
  position: relative;
  z-index: 2;
}

.intro-section-imgs{
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 1.5rem;
  align-items:start;

}
.intro-item{
  display: flex;
  flex-direction: column;
}

.intro-item img{
  width: 100%;
  height: 350px;
  object-fit: cover;
}

.intro-item p{
  margin-top: 0.75rem;;
}
.captions{
  text-align: left;
}
.standout {
  font-family: "Sans", Inter;
  font-weight: 700;
  font-size: 19px;
  font-style: normal;
  color: #950000;
}

/* Rect image */
.rect-image {
  width: 100%;
  height: 100%;
  background: lightgray;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
  margin-bottom: 10px;
}

.gradient-section{
  width: 100%;
  top: -250px;
  z-index: 1;
  position: relative;
  height: 1382px;
  background: linear-gradient(180deg, #FFF 6.67%, rgba(129,170,197,0.90) 37.88%, #FFF 66.21%);
}

.gs-info{
 max-width: 1480px;
 margin-left: 130px;
 position: absolute;
 top: 0%;
 bottom: 50%;
 transform: translate(5%, 29%);
 justify-content:center;
 padding: 100px 20px 20px 20px ;
 text-align:center;
}

.med-text{
  color: #1e1e1e;
  font-family: "Serif", Noto;
  font-size: 28px;
  font-style: normal;
  font-weight: 400;
  margin-left: auto;
  margin-right: auto;
  text-align: left;
}

.footer-section{
  position: relative;
  z-index: 2;
  top: -750px;
  max-width: 100%;
  max-height: 100%;
  box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.35) inset, 0 4px 4px 0 rgba(0, 0, 0, 0.25);

}

.footer-section-content{
  max-width: 1480px;
  padding: 100px 10px 100px 80px ;

}

a{
  text-decoration: none;
  color:inherit;
}

.footer{
  font-size: 18px;
  color: rgb(62, 62, 62);
  margin-top: 16px;
}

/* Responsive tweaks */
@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
  }

  .image-panel {
    justify-content: center;
  }
}
</style>
