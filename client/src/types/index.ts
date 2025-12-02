export interface Bird {
  species: string,
  rank: number,
  rfpc: number,
  wtdrf: number,
  photo?: string
}

export interface DetailedHotspot {
  id: number;
  name: string;
  region: string;
  location: string;
  birds: Bird[]; // list of bird species with data
  isSaved?: boolean;
}

export interface HotspotOverview {
  id: number;
  name: string;
  country: string;
  subregion1: string;
  subregion2: string;
  speciesCount: number; // Found @ "species list for a region" under "product" 
  checklistCount?: number;  // number of total recorded checklists for a region, not sure if this is possible 
}

