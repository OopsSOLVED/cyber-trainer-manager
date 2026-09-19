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

export interface Task {
  id: number;
  user_id: number;
  topic_id: number;
  status: TaskStatus;
  notes: string | null;
  estimated_hours: number;
  actual_hours: number;
  assigned_date: string | null;
  completed_at: string | null;
  topic: Topic;
  subtasks: Subtask[];
}

export interface TaskGenerationRequest {
  day_number: number;
}
