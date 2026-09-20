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

export interface TopicRoadmapItem {
  id: number;
  name: string;
  description: string | null;
  order: number;
  day_number: number | null;
  estimated_hours: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced' | 'expert' | string;
  objectives_count: number;
  objectives: Objective[];
  task_id: number | null;
  status: 'todo' | 'in_progress' | 'completed' | 'blocked' | null;
}

export interface DomainRoadmapItem {
  id: number;
  name: string;
  description: string | null;
  order: number;
  estimated_days: number;
  topic_count: number;
  day_start: number | null;
  day_end: number | null;
  total_hours: number;
  completed_topics: number;
  progress_percent: number;
}

export interface SkillLayerRoadmapItem {
  id: number;
  name: string;
  description: string | null;
  order: number;
  estimated_days: number;
  domain_count: number;
  total_topics: number;
  completed_topics: number;
  progress_percent: number;
  domains: DomainRoadmapItem[];
}

export interface PhaseRoadmapItem {
  id: number;
  name: string;
  description: string | null;
  order: number;
  estimated_weeks: number | null;
  total_topics: number;
  completed_topics: number;
  progress_percent: number;
  skill_layers: SkillLayerRoadmapItem[];
}

export interface RoadmapResponse {
  total_phases: number;
  total_skill_layers: number;
  total_domains: number;
  total_topics: number;
  total_days: number;
  completed_topics: number;
  progress_percent: number;
  phases: PhaseRoadmapItem[];
}

export interface DomainTopicsResponse {
  domain_id: number;
  domain_name: string;
  domain_description: string | null;
  day_start: number | null;
  day_end: number | null;
  total_topics: number;
  completed_topics: number;
  progress_percent: number;
  topics: TopicRoadmapItem[];
}
