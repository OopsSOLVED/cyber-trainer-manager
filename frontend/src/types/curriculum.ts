export interface Objective {
  id: number;
  description: string;
  order: number;
  is_measurable: boolean;
}

export interface Topic {
  id: number;
  name: string;
  description: string | null;
  order: number;
  day_number: number | null;
  estimated_hours: number;
  difficulty: string;
  objectives?: Objective[]; // Optional because it's only fetched on TopicDetail
}

export interface Domain {
  id: number;
  name: string;
  description: string | null;
  order: number;
  estimated_days: number;
  topics?: Topic[]; // Optional
}

export interface SkillLayer {
  id: number;
  name: string;
  description: string | null;
  order: number;
  estimated_days: number;
  domains?: Domain[]; // Optional
}

export interface Phase {
  id: number;
  name: string;
  description: string | null;
  order: number;
  skill_layers?: SkillLayer[]; // Optional
}

export interface CurriculumStats {
  total_phases: number;
  total_skill_layers: number;
  total_domains: number;
  total_topics: number;
  total_objectives: number;
  total_days: number;
}
