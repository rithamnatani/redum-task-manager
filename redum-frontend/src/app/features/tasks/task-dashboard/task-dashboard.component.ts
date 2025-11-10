import { Component, inject, OnInit, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, DragDropModule, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { TaskService } from '../../../core/services/task.service';
import { Task } from '../../../core/models/task.model';
import { TaskCardComponent } from '../../../shared/components/task-card/task-card.component';
import { CreateTaskDialogComponent, TaskDialogData } from '../../../shared/components/create-task-dialog/create-task-dialog.component';

@Component({
  selector: 'app-task-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    DragDropModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    TaskCardComponent
  ],
  templateUrl: './task-dashboard.component.html',
  styleUrls: ['./task-dashboard.component.scss']
})
export class TaskDashboardComponent implements OnInit {
  private readonly taskService = inject(TaskService);
  private readonly dialog = inject(MatDialog);
  private readonly snackBar = inject(MatSnackBar);

  // Computed signals for filtered tasks by status
  readonly todoTasks = computed(() => 
    this.taskService.tasks().filter(task => !task.status || task.status === 'todo')
  );

  readonly inProgressTasks = computed(() => 
    this.taskService.tasks().filter(task => task.status === 'in_progress')
  );

  readonly doneTasks = computed(() => 
    this.taskService.tasks().filter(task => task.status === 'done')
  );

  readonly isLoading = this.taskService.isLoading;

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(): void {
    this.taskService.getTasks().subscribe({
      error: (error) => {
        this.snackBar.open('Failed to load tasks', 'Close', { duration: 3000 });
      }
    });
  }

  onDrop(event: CdkDragDrop<Task[]>, newStatus: 'todo' | 'in_progress' | 'done'): void {
    if (event.previousContainer === event.container) {
      // Same list - just reorder (no backend update needed)
      return;
    } else {
      // Different list - update task status
      const task = event.previousContainer.data[event.previousIndex];
      
      this.taskService.updateTaskStatus(task.id, newStatus).subscribe({
        error: (error) => {
          this.snackBar.open('Failed to update task status', 'Close', { duration: 3000 });
          // Reload tasks to reset state
          this.loadTasks();
        }
      });
    }
  }

  openCreateTaskDialog(): void {
    const dialogRef = this.dialog.open<CreateTaskDialogComponent, TaskDialogData>(
      CreateTaskDialogComponent,
      {
        width: '600px',
        data: { mode: 'create' }
      }
    );

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.taskService.createTask(result).subscribe({
          next: () => {
            this.snackBar.open('Task created successfully', 'Close', { duration: 2000 });
          },
          error: (error) => {
            this.snackBar.open('Failed to create task', 'Close', { duration: 3000 });
          }
        });
      }
    });
  }

  onEditTask(task: Task): void {
    const dialogRef = this.dialog.open<CreateTaskDialogComponent, TaskDialogData>(
      CreateTaskDialogComponent,
      {
        width: '600px',
        data: { mode: 'edit', task }
      }
    );

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.taskService.updateTask(task.id, result).subscribe({
          next: () => {
            this.snackBar.open('Task updated successfully', 'Close', { duration: 2000 });
          },
          error: (error) => {
            this.snackBar.open('Failed to update task', 'Close', { duration: 3000 });
          }
        });
      }
    });
  }

  onDeleteTask(taskId: number): void {
    if (confirm('Are you sure you want to delete this task?')) {
      this.taskService.deleteTask(taskId).subscribe({
        next: () => {
          this.snackBar.open('Task deleted successfully', 'Close', { duration: 2000 });
        },
        error: (error) => {
          this.snackBar.open('Failed to delete task', 'Close', { duration: 3000 });
        }
      });
    }
  }
}
