export interface Bird {
  Rank: number,
  Species: string,
  wtd_rf: number,
  rfpc: number,
  birdCode?: string,
  speciesUrl?: string,
  imageUrl?: string
}


export interface DetailedHotspot {
  id: string;
  name: string;
  region: string;
  location: string;
  birds: Bird[]; // list of bird species with data
  isSaved?: boolean;
}

export interface HotspotOverview {
  id: string;
  name: string;
  country: string;
  subregion1: string;
  subregion2: string;
  speciesCount: number; // Found @ "species list for a region" under "product" 
  checklistCount?: number;  // number of total recorded checklists for a region, not sure if this is possible 
}

