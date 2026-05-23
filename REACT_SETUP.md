# 🚀 React Frontend Setup Guide

## Overview

The application now has a **React frontend** (modern SPA) that communicates with the **Flask backend** via REST API.

## Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Port 5173)      │
│  - Modern UI with React Router          │
│  - Component-based architecture         │
│  - Axios for API calls                  │
└─────────────────────────────────────────┘
                    ↕ HTTP/REST API
┌─────────────────────────────────────────┐
│         Flask Backend (Port 5000)       │
│  - API endpoints (/api/*)               │
│  - AI Model processing                  │
│  - PDF generation                       │
│  - User authentication                  │
└─────────────────────────────────────────┘
```

## Quick Start

### 1. Start Backend (Flask)
```bash
# In the main project directory
python app.py
```
Backend will run on: **http://localhost:5000**

### 2. Start Frontend (React)
```bash
# In a new terminal
cd frontend
npm run dev
```
Frontend will run on: **http://localhost:5173**

### 3. Access the Application
Open your browser and go to: **http://localhost:5173**

## Project Structure

```
skin_disease/
├── app.py                      # Flask backend with API endpoints
├── requirements.txt            # Python dependencies
├── users.db                    # SQLite database
├── final_specific_disease_model.keras  # AI model
│
└── frontend/                   # React application
    ├── package.json            # Node dependencies
    ├── vite.config.js          # Vite configuration
    ├── index.html              # HTML entry point
    │
    └── src/
        ├── main.jsx            # React entry point
        ├── App.jsx             # Main app component
        ├── App.css             # Global styles
        ├── index.css           # Base styles
        │
        ├── components/
        │   ├── Navbar.jsx      # Navigation component
        │   └── Navbar.css
        │
        └── pages/
            ├── Home.jsx        # Landing page
            ├── Home.css
            ├── Login.jsx       # Login page
            ├── Register.jsx    # Registration page
            ├── Auth.css        # Auth pages styles
            ├── Analyze.jsx     # Image upload/capture
            ├── Analyze.css
            ├── Report.jsx      # Results display
            └── Report.css
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/check-auth` - Check authentication status

### Analysis
- `POST /api/predict` - Analyze skin condition image
- `POST /download-report` - Generate and download PDF report

## Features

### Frontend (React)
✅ Modern single-page application
✅ React Router for navigation
✅ Component-based architecture
✅ Axios for API communication
✅ Session storage for results
✅ Camera capture support
✅ Drag & drop file upload
✅ Responsive design
✅ Loading states
✅ Error handling

### Backend (Flask)
✅ RESTful API endpoints
✅ CORS enabled for React
✅ Session-based authentication
✅ AI model integration
✅ PDF report generation
✅ SQLite database
✅ Secure password hashing

## Development

### Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Run Development Servers

**Backend (Terminal 1):**
```bash
python app.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

## Building for Production

### Build React App
```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`

### Serve with Flask
You can configure Flask to serve the built React app:
1. Build the React app
2. Update Flask to serve static files from `frontend/dist`
3. Run only Flask server

## Technologies Used

### Frontend
- **React 19** - UI library
- **React Router DOM 7** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **CSS3** - Styling

### Backend
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin support
- **TensorFlow/Keras** - AI model
- **ReportLab** - PDF generation
- **SQLite** - Database
- **Werkzeug** - Security

## Key Differences from HTML Version

### Before (HTML Templates)
- Server-side rendering
- Page reloads on navigation
- Form submissions reload page
- Tightly coupled frontend/backend

### After (React SPA)
- Client-side rendering
- No page reloads
- AJAX API calls
- Separated frontend/backend
- Better user experience
- Easier to maintain
- Modern development workflow

## Advantages of React Version

1. **Better Performance** - No full page reloads
2. **Modern UX** - Smooth transitions and interactions
3. **Easier Maintenance** - Component-based code
4. **Scalability** - Easy to add new features
5. **Developer Experience** - Hot reload, better tooling
6. **Separation of Concerns** - Frontend and backend independent
7. **Reusable Components** - DRY principle
8. **State Management** - React hooks for state

## Troubleshooting

### CORS Errors
- Make sure Flask-CORS is installed
- Check CORS configuration in `app.py`
- Verify frontend is running on port 5173

### API Connection Issues
- Ensure backend is running on port 5000
- Check Vite proxy configuration
- Verify axios baseURL

### Camera Not Working
- Use HTTPS in production
- Check browser permissions
- Try different browser

### Build Errors
- Delete `node_modules` and reinstall
- Clear npm cache: `npm cache clean --force`
- Update Node.js to latest LTS version

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Modern mobile browsers

## Next Steps

1. ✅ Backend API ready
2. ✅ React frontend complete
3. ✅ Authentication working
4. ✅ Image analysis working
5. ✅ PDF reports working

**Optional Enhancements:**
- Add Redux for state management
- Implement React Query for API caching
- Add TypeScript for type safety
- Add unit tests (Jest, React Testing Library)
- Add E2E tests (Cypress, Playwright)
- Implement PWA features
- Add dark mode
- Add internationalization (i18n)

## Commands Cheat Sheet

```bash
# Backend
python app.py                    # Start Flask server

# Frontend
cd frontend
npm install                      # Install dependencies
npm run dev                      # Start dev server
npm run build                    # Build for production
npm run preview                  # Preview production build

# Both (use 2 terminals)
# Terminal 1: python app.py
# Terminal 2: cd frontend && npm run dev
```

---

**Your modern React + Flask application is ready! 🎉**

Access it at: **http://localhost:5173**
