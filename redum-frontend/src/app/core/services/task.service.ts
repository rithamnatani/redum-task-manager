import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Task, CreateTaskRequest, UpdateTaskRequest, TaskSuggestion, TaskSuggestionRequest } from '../models/task.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private readonly http = inject(HttpClient);
  private readonly API_URL = environment.apiUrl;

  // Signal-based state for tasks
  readonly tasks = signal<Task[]>([]);
  readonly isLoading = signal<boolean>(false);

  getTasks(): Observable<Task[]> {
    this.isLoading.set(true);
    return this.http.get<Task[]>(`${this.API_URL}/tasks/`).pipe(
      tap(tasks => {
        this.tasks.set(tasks);
        this.isLoading.set(false);
      })
    );
  }

  createTask(data: CreateTaskRequest): Observable<Task> {
    return this.http.post<Task>(`${this.API_URL}/tasks/`, data).pipe(
      tap(task => {
        this.tasks.update(tasks => [...tasks, { ...task, status: 'todo' }]);
      })
    );
  }

  updateTask(id: number, data: UpdateTaskRequest): Observable<Task> {
    return this.http.put<Task>(`${this.API_URL}/tasks/${id}`, data).pipe(
      tap(updatedTask => {
        this.tasks.update(tasks => 
          tasks.map(task => task.id === id ? { ...updatedTask, status: updatedTask.status || 'todo' } : task)
        );
      })
    );
  }

  deleteTask(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/tasks/${id}`).pipe(
      tap(() => {
        this.tasks.update(tasks => tasks.filter(task => task.id !== id));
      })
    );
  }

  updateTaskStatus(id: number, status: 'todo' | 'in_progress' | 'done'): Observable<Task> {
    return this.updateTask(id, { status });
  }

  suggestTaskMetadata(data: TaskSuggestionRequest): Observable<TaskSuggestion> {
    return this.http.post<TaskSuggestion>(`${this.API_URL}/tasks/suggest`, data);
  }
}
