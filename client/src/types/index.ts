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
  region: number;
  location: string;
  birds: Bird[]; // list of bird species with data
}

export interface HotspotOverview {
  id: number;
  name: string;
  region: number;
  location: string;
  speciesCount: number; // Found @ "species list for a region" under "product" 
  checklistCount?: number;  // number of total recorded checklists for a region, not sure if this is possible 
}

