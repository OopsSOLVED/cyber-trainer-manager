import type { Topic, Objective } from './curriculum';

export type TaskStatus = 'todo' | 'in_progress' | 'completed' | 'blocked' | 'skipped';

export interface Subtask {
  id: number;
  task_id: number;
  learning_objective_id: number;
  order: number;
  status: TaskStatus;
  notes: string | null;
  learning_objective: Objective;
}

export type TaskPriority = 'low' | 'medium' | 'high' | 'critical';
export type TaskType = 'study' | 'practice' | 'lab' | 'ctf' | 'reading' | 'quiz' | 'review' | 'explain' | 'teach' | 'project' | 'assessment' | 'troubleshooting';

export interface Task {
  id: number;
  user_id: number;
  topic_id: number;
  status: TaskStatus;
  priority?: TaskPriority;
  task_type?: TaskType;
  notes: string | null;
  estimated_hours: number;
  actual_hours: number;
  assigned_date: string | null;
  due_date?: string | null;
  completed_at: string | null;
  confidence_score?: number | null;
  review_date?: string | null;
  topic: Topic;
  subtasks: Subtask[];
  prerequisite_task_ids?: number[];
}


export interface TaskGenerationRequest {
  day_number: number;
}

export interface TodaySummary {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  overdue_tasks: number;
  estimated_hours: number;
  actual_hours: number;
  completion_percentage: number;
  daily_objective: string | null;
}

