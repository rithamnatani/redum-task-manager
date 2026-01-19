# API Reference

This document provides a reference for the available API endpoints.

All endpoints are prefixed with `/api/v1`.

## Authentication

### `POST /api/v1/auth/register`

Registers a new user.

**Request Body:**

- `email` (string, required)
- `password` (string, required)

**Response Body:**

- `id` (integer)
- `email` (string)
- `created_at` (datetime, optional)

### `POST /api/v1/auth/token`

Logs in a user and returns an access token.

**Request Body:**

- `email` (string, required)
- `password` (string, required)

**Response Body:**

- `access_token` (string)
- `token_type` (string) - Defaults to `"bearer"`

## Tasks

### `POST /api/v1/tasks/`

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

### `GET /api/v1/tasks/`

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

### `PUT /api/v1/tasks/{task_id}`

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

### `DELETE /api/v1/tasks/{task_id}`

Deletes an existing task.

**Path Parameters:**

- `task_id` (integer, required) - The ID of the task to delete

**Response:**

- Status: `204 No Content`

**Error Responses:**

- `404` - Task not found
- `403` - Not authorized to delete this task

### `POST /api/v1/tasks/suggest`

Returns AI-powered suggestions for task metadata based on provided title or description.

**Request Body:**

- `title` (string, optional)
- `description` (string, optional)
- `priority` (integer, optional)
- `status` (string, optional) - One of: `"todo"`, `"in_progress"`, `"done"`

> At least one of `title` or `description` must be provided.

**Response Body:**

- `title` (string, optional)
- `description` (string, optional)
- `priority` (integer, optional)
- `status` (string, optional) - One of: `"todo"`, `"in_progress"`, `"done"`

## Chat

### `POST /api/v1/chat/`

Conversational AI endpoint that uses task context to provide helpful responses.

**Request Body:**

- `message` (string, required) - The user's chat message
- `history` (array, optional) - Previous conversation messages, each with:
  - `role` (string) - Either `"user"` or `"assistant"`
  - `content` (string) - The message content

**Response Body:**

- `response` (string) - The AI assistant's response
- `history` (array) - Updated conversation history including the new exchange

**Error Responses:**

- `503` - AI chat service is not configured (missing `GEMINI_API_KEY`)
- `500` - Chat service error
