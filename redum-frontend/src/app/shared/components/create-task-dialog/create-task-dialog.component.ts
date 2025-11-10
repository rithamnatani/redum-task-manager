import { Component, inject, Inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../../../core/models/task.model';

export interface TaskDialogData {
  task?: Task;
  mode: 'create' | 'edit';
}

@Component({
  selector: 'app-create-task-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatTooltipModule
  ],
  templateUrl: './create-task-dialog.component.html',
  styleUrls: ['./create-task-dialog.component.scss']
})
export class CreateTaskDialogComponent {
  private readonly fb = inject(FormBuilder);
  readonly dialogRef = inject(MatDialogRef<CreateTaskDialogComponent>);

  readonly taskForm: FormGroup;
  readonly isEditMode: boolean;
  readonly aiGenerateDisabled = signal(true); // Future AI feature
  readonly statusOptions: Array<{ value: 'todo' | 'in_progress' | 'done'; label: string }> = [
    { value: 'todo', label: 'To Do' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'done', label: 'Done' }
  ];

  constructor(@Inject(MAT_DIALOG_DATA) public data: TaskDialogData) {
    this.isEditMode = data.mode === 'edit';

    this.taskForm = this.fb.group({
      title: [data.task?.title || '', [Validators.required]],
      description: [data.task?.description || ''],
      due_date: [data.task?.due_date ? new Date(data.task.due_date) : null],
      priority: [data.task?.priority || null],
      status: [data.task?.status || 'todo', this.isEditMode ? Validators.required : null]
    });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.taskForm.invalid) {
      return;
    }

    const formValue = this.taskForm.getRawValue();
    const normalizedDueDate = formValue.due_date ? formValue.due_date.toISOString() : undefined;
    const normalizedPriority = formValue.priority ?? undefined;

    if (this.isEditMode) {
      const taskData: UpdateTaskRequest = {
        title: formValue.title,
        description: formValue.description || undefined,
        due_date: normalizedDueDate,
        priority: normalizedPriority,
        status: formValue.status ?? undefined
      };

      this.dialogRef.close(taskData);
      return;
    }

    const { status: _status, ...createFormValue } = formValue;
    const taskData: CreateTaskRequest = {
      title: createFormValue.title,
      description: createFormValue.description || undefined,
      due_date: normalizedDueDate,
      priority: normalizedPriority
    };

    this.dialogRef.close(taskData);
  }

  onAiGenerate(): void {
    // Placeholder for future AI integration
    // This will be implemented when backend AI features are ready
  }
}
