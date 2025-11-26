export interface Bird {
  species: string,
  data1: number,
  data2: number,
  photo?: string
}

export interface Hotspot {
  id: number;
  name: string;
  frequency: number;
  region: string;
  birds: Bird[];
}