# Redum Task Manager - Frontend

A modern Angular 20 frontend application for task management with a beautiful Kanban board interface.

Built with Angular 20, Angular Material 3, standalone components, and zoneless architecture.

## Features

- **Modern Angular 20**: Zoneless change detection, standalone components, signals
- **Kanban Board**: Drag-and-drop task management with three columns (To Do, In Progress, Done)
- **Authentication**: JWT-based login and registration
- **Material Design 3**: Beautiful UI with Material You theming
- **Responsive**: Works on desktop and mobile devices
- **Type-Safe**: Full TypeScript implementation with strict typing
- **Future-Ready**: Prepared for AI features with placeholder UI hooks

## Architecture

### Project Structure

```
src/app/
├── core/                    # Core application logic
│   ├── guards/              # Route guards (functional)
│   ├── interceptors/        # HTTP interceptors (functional)
│   ├── models/              # TypeScript interfaces
│   └── services/            # Singleton services
│       ├── auth.service.ts
│       ├── task.service.ts
│       └── token-storage.service.ts
├── features/                # Feature modules
│   ├── auth/
│   │   ├── login/
│   │   └── register/
│   └── tasks/
│       └── task-dashboard/
├── shared/                  # Shared components
│   ├── components/
│   │   ├── task-card/
│   │   └── create-task-dialog/
│   └── layout/
│       └── main-layout/
└── environments/            # Environment configurations
```

### Key Architectural Principles

1. **Standalone Components**: All components are standalone with explicit imports
2. **Functional Guards/Interceptors**: Modern functional approach using `inject()`
3. **Signals for State**: Using Angular Signals for reactive state management
4. **Smart vs Dumb Components**: Clear separation of concerns
5. **Lazy Loading**: Route-based code splitting for optimal performance

## Prerequisites

- Node.js 20.x or higher
- npm or yarn
- Backend API running on `http://localhost:8000`

## Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Configure API endpoint** (if different from default):
   Edit `src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api/v1'
   };
   ```

3. **Start development server**:
```bash
npm start
# or
ng serve
```

4. **Navigate to** `http://localhost:4200/`

## Usage

### First Time Setup

1. Navigate to `http://localhost:4200/`
2. Click "Sign up" to create a new account
3. Enter your email and password
4. After registration, you'll be redirected to login
5. Sign in with your credentials
6. You'll be taken to the Task Board

### Creating Tasks

1. Click the **+** FAB (Floating Action Button) in the top right
2. Fill in the task details:
   - **Title** (required)
   - **Description** (optional)
   - **Priority** (Low/Medium/High)
   - **Due Date** (optional)
3. Click "Create"

### Managing Tasks

- **Move Tasks**: Drag and drop tasks between columns (To Do → In Progress → Done)
- **Edit Task**: Click the edit icon on any task card
- **Delete Task**: Click the delete icon on any task card

### AI Feature (Coming Soon)

- The sparkle icon (✨) next to the title field is prepared for future AI-powered task generation
- This will be enabled when backend AI features are implemented

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project for production:

```bash
ng build --configuration production
```

This will:
- Compile your project with production optimizations
- Store build artifacts in the `dist/` directory
- Use ESBuild for faster builds (3x faster than Webpack)
- Enable AOT compilation and tree-shaking
- Minify all assets

## Technologies Used

### Core
- **Angular 20**: Latest version with zoneless change detection
- **TypeScript 5.5+**: Strong typing and latest language features
- **RxJS**: Reactive programming for async operations
- **Angular Signals**: Fine-grained reactivity

### UI/UX
- **Angular Material 20**: Material Design 3 components
- **Angular CDK**: Drag-and-drop functionality
- **SCSS**: Modular, maintainable styling

### Build Tools
- **ESBuild**: Ultra-fast JavaScript bundler
- **Angular CLI**: Project scaffolding and build system

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api/v1`.

### Endpoints Used

- `POST /auth/register` - User registration
- `POST /auth/token` - User login (returns JWT)
- `GET /tasks/` - Get all tasks for authenticated user
- `POST /tasks/` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Authentication

- JWT token is stored in localStorage
- Token is automatically attached to all API requests via HTTP interceptor
- Auth guard protects routes requiring authentication

## Additional Resources

- [Angular Documentation](https://angular.dev)
- [Angular Material](https://material.angular.dev)
- [Angular CLI Reference](https://angular.dev/tools/cli)
- [Angular Signals](https://angular.dev/guide/signals)

## License

MIT
