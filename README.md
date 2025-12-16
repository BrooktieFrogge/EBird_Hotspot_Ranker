# FeatherWeight: eBird Hotspot Ranker

## Overview

The eBird Hotspot Ranker lets you estimate the likelihood of seeing bird species with hotspot data during the same interval of weeks compiled over multiple years. Using real-time reports from the eBird hotspot dataset (The Cornell Lab of Ornithology), you can:

- determine the most likely birds you will encounter at a hotspot in a specific week,
- assess the relative likelihood of seeing a target species at a given hotspot around specific weeks relative to reports of other species,
- evaluate how often an uncommon or rare bird that you spotted is reported, or
- use the ranked list to practice songs and calls of resident species before visiting the hotspot.

## About FeatherWeight

Among exciting birding experiences is venturing to a new locality to explore new ecosystems and birds. Such travels, domestic or international, might include seeking "target" species for a region or country, or experiencing a totally new avian show in a completely novel setting. Reviewing eBird Hotspot lists and bar charts is an excellent approach for cleaning up prior to a trip to see what one might expect to see, or to gauge the likelihood of spotting new or forest species. It's a good place to start.

At the same time, for a venture that includes a number of hotspots with a high species diversity, sorting through multiple lists of bird species can be a daunting affair. This is particularly true for hotspots such as in neotropical regions that may have a spawn of 400-500 species, more or all of which might be new for a birder.

How might one focus on some of the common birds of an active hotspot to ensure what one might see? Or, what is the relative likelihood of seeing rare or "target" species at the hotspot you are visiting? That's where the eBird Hotspot Likelihood ranker can help.

Using strict filters for an upcoming birding outing, the site lets birders rank, filter, or filter-down eBird Hotspot lists to help a birder identify the species (top 20, 50, or however many) most common species for a hotspot, as well as estimate the likelihood of rare or "target" species. "Likelihoods" are determined from eBird data reported from that hotspot for an interval of weeks over a duration of years. Used "total frankings" are also normalized as percentages to the most frequently reported species at each hotspot for the selected time interval.

## How To Use

1. **Enter the name** of an eBird hotspot (or use country/region info) for your target.
2. **Enter the start year and end year** for your census. Many birders select a 10-15 year interval to get a good sample size (e.g., 2010-2024 or 2015-2024).
3. **Select the interval of weeks** that includes your sample of dates. For example, if you are scheduling a trip to the Canopy Tower, Panama, and will be there the first two weeks of August, select "August" as the Month, and "Week 1" and "Week 2".
4. **Inspect the distribution** of checklists (sample sizes) for each of the weeks in your interval. If you have a minimal amount of checklists (less than 10 per week for recent years), you can widen the interval of weeks to increase the sample size (e.g., enable Weeks 1-4 of August) or expand the years (e.g., 2005-2024).
5. **Enter the number of species** to display (defaults to 50).
6. **Review the ranked list** and relative likelihood curves for the hotspot. The rank is defined relative to the top reported species (ranked #1, 100%).
7. **For custom purposes**, you can filter out species that may have already been seen or common species. This leaves charts displaying relative rarity reports.
8. **Export the ranked table** for your own use (Excel, CSV, or Text) to create practice lists for songs/calls.

## Documentation

### Validity Tests

Several approaches were used to test the validity of the hotspot likelihood ranks. First, to test webpage-to-rank accuracy, results for an interval of 10 weeks over a duration of 10 years were compared between the code output and ranks compiled "by hand" in an Excel file. The results were identical.

Second, to test the approach "in the field," eBird data from 4 hotspots in the Southern Rainforest with high species diversity were processed into Rankings. (e.g., reports in February 2024, were Copalinga Lodge=450, Savegre Lodge=230, Reserva Urumaco=330, and Carara/Tarcoles Mangrove=410...). The sample contained all sightings for the week of the visit, bracketed by data from 5 weeks prior to and 5 weeks after the week of the visit, all pooled in the same interval over 5 common recent years.

In all cases, nearly all of the ranked top 40 most common species were spotted at each of the viewpoints. Moreover, the approach was able to place in context, compared with other allied lists at the hotspot, many more species that were observed at the hotspot (see Figure). While some of the latter species are very infrequently encountered, data indicate that hard work at the right bottom can yield some of the "rarely sought" or "very infrequently observed" species.

### Image Credits
- Images used in this project are for educational/demonstration purposes.

### Project Acknowledgements
Data comes from Cornell University's eBird project.
Steve Getty, our Client and Expert Birder
Blake Jackson, our Thesis Mentor

---

## Installation & Development

### Running with Docker

This project is fully dockerized. To run the application:

```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
