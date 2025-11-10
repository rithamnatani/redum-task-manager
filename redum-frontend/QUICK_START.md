# Quick Start Guide - Redum Frontend

## 🚀 Start the Application

### 1. Navigate to the frontend directory
```bash
cd redum-frontend
```

### 2. Install dependencies (if not already done)
```bash
npm install
```

### 3. Start the development server
```bash
npm start
```

The application will open at **http://localhost:4200**

## 🔧 Prerequisites

Make sure your **backend API** is running on **http://localhost:8000**

If your backend is on a different port, update:
```
redum-frontend/src/environments/environment.ts
```

## 📝 First Steps

1. **Open** http://localhost:4200 in your browser
2. **Click** "Sign up" to create an account
3. **Enter** your email and password
4. **Login** with your new credentials
5. **Create tasks** using the + button
6. **Drag & drop** tasks between columns

## 🎯 Available Routes

- `/login` - Login page
- `/register` - Registration page  
- `/tasks` - Task dashboard (requires authentication)

## 🛠️ Development Commands

```bash
# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Watch mode for development
npm run watch
```

## 📦 Build Output

Production builds are created in:
```
redum-frontend/dist/redum-app/
```

## 🎨 Features to Try

1. **Create a task** with the FAB button
2. **Add priority** and due date
3. **Drag tasks** between To Do → In Progress → Done
4. **Edit tasks** using the edit icon
5. **Delete tasks** with confirmation
6. **Logout** from the user menu

## 🐛 Troubleshooting

### Port 4200 already in use
```bash
ng serve --port 4300
```

### Backend connection issues
Check `environment.ts` has correct API URL:
```typescript
apiUrl: 'http://localhost:8000/api/v1'
```

### Build errors
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 📚 Documentation

See `README.md` and `IMPLEMENTATION_SUMMARY.md` for detailed information.

---

**Ready to start!** 🎉
