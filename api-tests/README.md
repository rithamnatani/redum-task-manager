# Redum Task Manager API Tests

This directory contains Bruno API tests for the Redum Task Manager backend.

## Prerequisites

1. Install [Bruno](https://www.usebruno.com/) API client
2. Ensure the backend server is running on `http://localhost:8000`

## Test Files

### Authentication Tests
- `auth-register.bru` - Register a new user
- `auth-login.bru` - Login and get access token

### Task CRUD Tests
- `tasks-create.bru` - Create a new task (stores `test_task_id`)
- `tasks-list.bru` - List all tasks for the authenticated user
- `tasks-update.bru` - Update an existing task
- `tasks-delete.bru` - Delete a task

### Error Handling Tests
- `tasks-update-not-found.bru` - Test 404 error when updating non-existent task
- `tasks-delete-not-found.bru` - Test 404 error when deleting non-existent task

## Running the Tests

### Option 1: Run All Tests in Sequence

1. Open Bruno and load this collection
2. Select the "Local Development" environment
3. Run tests in this order:
   - `auth-register.bru` (first time only)
   - `auth-login.bru` (get access token)
   - `tasks-create.bru` (creates task and stores ID)
   - `tasks-list.bru`
   - `tasks-update.bru` (uses stored task ID)
   - `tasks-list.bru` (verify update)
   - `tasks-delete.bru` (uses stored task ID)
   - `tasks-list.bru` (verify deletion)

### Option 2: Run Individual Tests

You can run tests individually, but note:
- **Authentication Required**: Most endpoints require authentication. Run `auth-login.bru` first to get an access token.
- **Task ID Required**: Update and delete tests require a valid `test_task_id`. Run `tasks-create.bru` first to create and store a task ID.

### Option 3: Run Error Tests

Error tests can be run independently after authentication:
- `auth-login.bru`
- `tasks-update-not-found.bru`
- `tasks-delete-not-found.bru`

## Environment Variables

The following variables are used (defined in `environments/Local Development.bru`):

- `BASE_URL` - Backend server URL (default: `http://localhost:8000`)
- `API_VERSION` - API version prefix (default: `api/v1`)
- `access_token` - JWT token (set by `auth-login.bru`)
- `test_task_id` - Task ID for testing (set by `tasks-create.bru`)
- `test_user_id` - User ID (set by `auth-register.bru`)
- `test_user_email` - User email (set by `auth-register.bru`)

## Expected Results

### Success Cases
- **Create Task**: Returns 200 with task object including `id`, `title`, `description`, etc.
- **List Tasks**: Returns 200 with array of task objects
- **Update Task**: Returns 200 with updated task object
- **Delete Task**: Returns 204 with no content

### Error Cases
- **Update Non-existent Task**: Returns 404 with `"Task not found"` message
- **Delete Non-existent Task**: Returns 404 with `"Task not found"` message
- **Unauthorized Access**: Returns 403 with `"Not authorized"` message (if task belongs to another user)

## Notes

- The backend currently uses a hardcoded `user_id = 1` for testing purposes
- In production, the user ID would be extracted from the JWT token
- Task ownership is verified on update and delete operations
