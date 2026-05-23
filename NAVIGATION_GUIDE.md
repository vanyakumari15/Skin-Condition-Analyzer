# 🗺️ Website Navigation Guide

## 📍 Page Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        HOME PAGE (/)                         │
│  • Hero section with project description                    │
│  • Features showcase (6 cards)                              │
│  • About section with statistics                            │
│  • Call-to-action buttons                                   │
└─────────────────────────────────────────────────────────────┘
                    │                    │
        ┌───────────┘                    └───────────┐
        │                                            │
        ▼                                            ▼
┌──────────────────┐                      ┌──────────────────┐
│  REGISTER (/register)                   │  LOGIN (/login)  │
│  • Username field                       │  • Username      │
│  • Email field                          │  • Password      │
│  • Password field                       │  • Submit        │
│  • Submit button                        │                  │
└──────────────────┘                      └──────────────────┘
        │                                            │
        │ (Success)                                  │
        └────────────────┬───────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  ANALYZE (/analyze)  │ 🔒 Protected
              │  • Upload image      │
              │  • Capture photo     │
              │  • Preview image     │
              │  • Analyze button    │
              └──────────────────────┘
                         │
                         │ (After Analysis)
                         ▼
              ┌──────────────────────┐
              │  REPORT (/report)    │ 🔒 Protected
              │  • Results display   │
              │  • Confidence bars   │
              │  • Download PDF      │
              │  • New analysis btn  │
              └──────────────────────┘
                         │
                         │ (New Analysis)
                         ▼
              ┌──────────────────────┐
              │  Back to ANALYZE     │
              └──────────────────────┘
```

## 🎯 User Journeys

### Journey 1: New User
```
1. Land on HOME
2. Click "Get Started Free"
3. Fill REGISTER form
4. Redirected to LOGIN
5. Enter credentials
6. Redirected to ANALYZE
7. Upload/capture image
8. Click "Analyze Image"
9. Redirected to REPORT
10. View results
11. Download PDF
12. Click "New Analysis" → back to step 6
```

### Journey 2: Returning User
```
1. Land on HOME
2. Click "Login"
3. Enter credentials
4. Redirected to ANALYZE
5. Upload/capture image
6. Click "Analyze Image"
7. Redirected to REPORT
8. View results
9. Download PDF
```

### Journey 3: Browsing User
```
1. Land on HOME
2. Scroll through features
3. Read about section
4. View statistics
5. Decide to register
6. Click "Sign Up"
7. Continue to Journey 1
```

## 🔐 Access Control

### Public Pages (No Login Required)
- ✅ Home (`/`)
- ✅ Register (`/register`)
- ✅ Login (`/login`)

### Protected Pages (Login Required)
- 🔒 Analyze (`/analyze`)
- 🔒 Report (`/report`)

### Special Routes
- 🚪 Logout (`/logout`) - Clears session, redirects to home
- 🤖 Predict (`/predict`) - API endpoint for analysis
- 📄 Download Report (`/download-report`) - API endpoint for PDF

## 🧭 Navigation Bar

### When NOT Logged In
```
┌────────────────────────────────────────────────────┐
│ 🔬 SkinAnalyzer  |  Home  |  Login  |  Sign Up    │
└────────────────────────────────────────────────────┘
```

### When Logged In
```
┌────────────────────────────────────────────────────┐
│ 🔬 SkinAnalyzer  |  Home  |  Analyze  |  Hi, User! |  Logout │
└────────────────────────────────────────────────────┘
```

## 📱 Mobile Navigation

### Collapsed Menu
```
┌────────────────────────────────┐
│ 🔬 SkinAnalyzer          ☰     │
└────────────────────────────────┘
```

### Expanded Menu (Click ☰)
```
┌────────────────────────────────┐
│ 🔬 SkinAnalyzer          ☰     │
├────────────────────────────────┤
│ Home                           │
│ Analyze                        │
│ Hi, User!                      │
│ Logout                         │
└────────────────────────────────┘
```

## 🎨 Page Sections

### HOME PAGE
```
┌─────────────────────────────────┐
│         NAVIGATION BAR          │
├─────────────────────────────────┤
│         HERO SECTION            │
│  • Title                        │
│  • Description                  │
│  • CTA Buttons                  │
├─────────────────────────────────┤
│       FEATURES SECTION          │
│  • 6 Feature Cards              │
├─────────────────────────────────┤
│        ABOUT SECTION            │
│  • Description                  │
│  • Statistics                   │
├─────────────────────────────────┤
│    CALL-TO-ACTION SECTION       │
│  • Final CTA                    │
├─────────────────────────────────┤
│           FOOTER                │
└─────────────────────────────────┘
```

### ANALYZE PAGE
```
┌─────────────────────────────────┐
│         NAVIGATION BAR          │
├─────────────────────────────────┤
│         PAGE HEADER             │
│  • Title                        │
│  • Description                  │
├─────────────────────────────────┤
│       UPLOAD SECTION            │
│  • Upload area                  │
│  • Image preview                │
├─────────────────────────────────┤
│       BUTTON GROUP              │
│  • Capture Photo                │
│  • Analyze Image                │
├─────────────────────────────────┤
│       INSTRUCTIONS              │
│  • Tips for best results        │
├─────────────────────────────────┤
│           FOOTER                │
└─────────────────────────────────┘
```

### REPORT PAGE
```
┌─────────────────────────────────┐
│         NAVIGATION BAR          │
├─────────────────────────────────┤
│       REPORT HEADER             │
│  • Title                        │
│  • Timestamp                    │
├─────────────────────────────────┤
│       IMAGE SECTION             │
│  • Analyzed image               │
├─────────────────────────────────┤
│      RESULTS SECTION            │
│  • Result Card 1 (Primary)      │
│  • Result Card 2                │
│  • Result Card 3                │
├─────────────────────────────────┤
│      ACTION BUTTONS             │
│  • Download PDF                 │
│  • New Analysis                 │
├─────────────────────────────────┤
│        DISCLAIMER               │
│  • Medical warning              │
├─────────────────────────────────┤
│           FOOTER                │
└─────────────────────────────────┘
```

## 🔄 State Management

### Session Data
- `user_id` - User's database ID
- `username` - User's username

### SessionStorage (Browser)
- `analysisResults` - JSON array of predictions
- `analysisImage` - Base64 encoded image

## 💡 Quick Actions

### From Any Page
- Click logo → Go to HOME
- Click "Home" → Go to HOME
- Click "Logout" → Clear session, go to HOME

### From HOME
- Click "Get Started" → Go to REGISTER
- Click "Login" → Go to LOGIN
- Click "Sign Up" → Go to REGISTER

### From ANALYZE
- Upload image → Enable analyze button
- Capture photo → Enable analyze button
- Click "Analyze" → Process and go to REPORT

### From REPORT
- Click "Download PDF" → Generate and download PDF
- Click "New Analysis" → Go to ANALYZE

## 🎯 URL Structure

```
http://localhost:5000/              → Home page
http://localhost:5000/register      → Registration
http://localhost:5000/login         → Login
http://localhost:5000/analyze       → Analysis (protected)
http://localhost:5000/report        → Report (protected)
http://localhost:5000/logout        → Logout action
```

## 📊 Data Flow

### Registration Flow
```
User Input → Form Submit → Validate → Hash Password → 
Save to DB → Flash Success → Redirect to Login
```

### Login Flow
```
User Input → Form Submit → Check DB → Verify Password → 
Create Session → Flash Success → Redirect to Analyze
```

### Analysis Flow
```
Upload/Capture → Preview → Submit → Send to Server → 
AI Processing → Return Results → Store in SessionStorage → 
Redirect to Report
```

### Report Flow
```
Load from SessionStorage → Display Results → 
User clicks Download → Send to Server → Generate PDF → 
Return File → Browser Downloads
```

## 🎨 Visual Hierarchy

### Color Coding
- 🟣 Purple - Primary actions (Analyze, Sign Up)
- 🟢 Green - Success states (Primary diagnosis, Download)
- 🔴 Red - Warnings (Disclaimer, Errors)
- ⚪ White - Content areas
- ⚫ Gray - Secondary text

### Button Hierarchy
1. **Primary** - Purple gradient (main actions)
2. **Success** - Green (positive actions)
3. **Secondary** - White with border (alternative actions)

---

**Use this guide to understand the complete navigation structure!**
