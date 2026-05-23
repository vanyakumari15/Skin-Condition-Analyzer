# 🔬 Skin Condition Analyzer

A professional AI-powered web application for analyzing skin conditions using deep learning technology.

## ✨ Features

### 🏠 Multi-Page Website
- **Home Page**: Beautiful landing page with project information and features
- **Authentication System**: Secure user registration and login
- **Analysis Page**: Upload or capture images with camera support
- **Report Page**: Detailed results with downloadable PDF reports

### 🔐 Authentication System
- User registration with email validation
- Secure password hashing
- Session-based authentication
- Protected routes requiring login

### 📸 Image Upload & Capture
- Drag & drop image upload
- Direct camera capture functionality
- Image preview before analysis
- Support for JPG, PNG, JPEG formats

### 🤖 AI Analysis
- Identifies 23 different skin conditions
- Provides top 3 predictions with confidence scores
- Detailed descriptions for each condition
- Advanced deep learning model (EfficientNet)

### 📊 Professional Reports
- Beautiful results display with visual confidence bars
- Downloadable PDF reports with:
  - Analyzed image
  - Diagnosis results table
  - Detailed condition descriptions
  - Timestamp and medical disclaimer

### 🎨 Modern UI/UX
- Responsive design for all devices
- Gradient color scheme
- Smooth animations and transitions
- Flash messages for user feedback
- Mobile-friendly navigation

## 🚀 Installation

1. **Clone the Project**

2. **Install dependencies:**
```bash (Skin_analyzer)
pip install -r requirements.txt
```

3. **Run the application:**
```bash(Skin_analyzer)
python app.py
```
4. **Start Frontend**
```(cd frontend)
npm install
npm run dev
```

5. **Open your browser and navigate to:**
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Register an Account
- Go to the home page
- Click "Sign Up" or "Get Started Free"
- Fill in username, email, and password
- Click "Create Account"

### 2. Login
- Click "Login" in the navigation
- Enter your username and password
- You'll be redirected to the analysis page

### 3. Analyze Skin Condition
- **Option A - Upload Image:**
  - Click the upload area or drag & drop an image
  - Preview the image
  - Click "Analyze Image"

- **Option B - Capture Photo:**
  - Click "Capture Photo" button
  - Allow camera access
  - Position the camera and click "Capture"
  - Click "Analyze Image"

### 4. View Results
- Automatically redirected to report page
- View top 3 predictions with confidence scores
- Read detailed descriptions
- Download PDF report for your records

### 5. Download Report
- Click "Download PDF Report" button
- PDF includes image, results, and descriptions
- Save for future reference or medical consultation

## 🏥 Supported Conditions (23 Total)

- Acne
- Athlete Foot
- Atopic Dermatitis
- Bullous Disease
- Cellulitis
- Chicken Pox
- Eczema
- Exanthems
- Herpes
- Measles
- Melanocytic Nevi
- Melanoma
- Monkey Pox
- Nail Fungus
- Poison Ivy
- Psoriasis
- Ringworm
- Rosacea
- Shingles
- Urticaria
- Vascular Lesion
- Vasculitis
- Warts

## 📁 Project Structure

```
skin_disease/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── users.db                        # SQLite database (auto-created)
├── final_specific_disease_model.keras  # AI model
├── templates/
│   ├── base.html                  # Base template with navigation
│   ├── home.html                  # Landing page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── analyze.html               # Image upload/capture page
│   └── report.html                # Results display page
└── README.md                      # This file
```

## 🔧 Technical Details

- **Backend**: Flask (Python)
- **AI Model**: Keras/TensorFlow (EfficientNet)
- **Database**: SQLite
- **Authentication**: Werkzeug password hashing
- **PDF Generation**: ReportLab
- **Image Processing**: PIL/Pillow

## 📝 Tips for Best Results

- Ensure good lighting when taking photos
- Keep the camera steady and focused
- Capture the affected area clearly
- Avoid blurry or dark images
- Include some surrounding healthy skin for context

## ⚠️ Important Disclaimer

**This application is for educational and informational purposes only.**

- NOT a substitute for professional medical advice
- NOT for making medical diagnoses
- Results should not be used as sole basis for medical decisions
- Always consult a qualified dermatologist or healthcare provider
- Seek immediate medical attention for concerning skin changes

## 🔒 Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session-based authentication
- Protected routes require login
- Change the `app.secret_key` in production!

## 🌐 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Camera capture requires HTTPS in production

## 📧 Support

For issues or questions about this educational project, please refer to the code comments and documentation.

---

**Built with ❤️ for educational purposes**
