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
