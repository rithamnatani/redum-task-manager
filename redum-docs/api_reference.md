# API Reference

This document provides a reference for the available API endpoints.

## Authentication

### `POST /auth/register`

Registers a new user.

**Request Body:**

- `email` (string, required)
- `password` (string, required)

**Response Body:**

- `id` (integer)
- `email` (string)

### `POST /auth/token`

Logs in a user and returns an access token.

**Request Body:**

- `email` (string, required)
- `password` (string, required)

**Response Body:**

- `access_token` (string)
- `token_type` (string)

## Tasks

### `POST /tasks/`

Creates a new task.

**Request Body:**

- `title` (string, required)
- `description` (string, optional)
- `due_date` (datetime, optional)
- `priority` (integer, optional)
- `status` (string, optional) - One of: `"todo"`, `"in_progress"`, `"done"`. Defaults to `"todo"`

**Response Body:**

- `id` (integer)
- `title` (string)
- `description` (string, optional)
- `due_date` (datetime, optional)
- `priority` (integer, optional)
- `status` (string) - One of: `"todo"`, `"in_progress"`, `"done"`
- `user_id` (integer)
- `created_at` (datetime, optional)

### `GET /tasks/`

Lists all tasks for the authenticated user.

**Response Body:**

A list of task objects, each with the following fields:

- `id` (integer)
- `title` (string)
- `description` (string, optional)
- `due_date` (datetime, optional)
- `priority` (integer, optional)
- `status` (string) - One of: `"todo"`, `"in_progress"`, `"done"`
- `user_id` (integer)
- `created_at` (datetime, optional)

### `PUT /tasks/{task_id}`

Updates an existing task.

**Path Parameters:**

- `task_id` (integer, required) - The ID of the task to update

**Request Body:**

- `title` (string, optional)
- `description` (string, optional)
- `due_date` (datetime, optional)
- `priority` (integer, optional)
- `status` (string, optional) - One of: `"todo"`, `"in_progress"`, `"done"`

**Response Body:**

- `id` (integer)
- `title` (string)
- `description` (string, optional)
- `due_date` (datetime, optional)
- `priority` (integer, optional)
- `status` (string) - One of: `"todo"`, `"in_progress"`, `"done"`
- `user_id` (integer)
- `created_at` (datetime, optional)

**Error Responses:**

- `404` - Task not found
- `403` - Not authorized to update this task

### `DELETE /tasks/{task_id}`

Deletes an existing task.

**Path Parameters:**

- `task_id` (integer, required) - The ID of the task to delete

**Response:**

- Status: `204 No Content`

**Error Responses:**

- `404` - Task not found
- `403` - Not authorized to delete this task
