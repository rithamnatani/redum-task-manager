export interface Task {
  id: number;
  title: string;
  description?: string;
  due_date?: string;
  priority?: number;
  status?: 'todo' | 'in_progress' | 'done';
  user_id: number;
  created_at?: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date?: string;
  priority?: number;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  due_date?: string;
  priority?: number;
  status?: 'todo' | 'in_progress' | 'done';
}

export interface TaskSuggestion {
  title?: string | null;
  description?: string | null;
  priority?: number | null;
  status?: 'todo' | 'in_progress' | 'done' | null;
}

export interface TaskSuggestionRequest {
  title?: string;
  description?: string;
  priority?: number;
  status?: 'todo' | 'in_progress' | 'done';
}
