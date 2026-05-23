import os
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for, session, flash
from flask_cors import CORS
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.units import inch
import base64
from functools import wraps
from database_hybrid import db
import config

# --- KERAS 3 SETUP ---
os.environ["KERAS_BACKEND"] = "tensorflow"

import keras
from keras.layers import InputLayer, Rescaling
from keras.applications.efficientnet import preprocess_input

# --- AUTO-DOWNLOAD MODEL IF NOT PRESENT ---
def download_model_if_needed():
    model_path = config.Config.MODEL_PATH
    if not os.path.exists(model_path):
        gdrive_id = os.getenv('MODEL_GDRIVE_ID', '')
        if gdrive_id:
            print(f"Model not found. Downloading from Google Drive...")
            try:
                import gdown
                url = f"https://drive.google.com/uc?id={gdrive_id}"
                gdown.download(url, model_path, quiet=False)
                print("Model downloaded successfully!")
            except Exception as e:
                print(f"Failed to download model: {e}")
        else:
            print(f"ERROR: Model file '{model_path}' not found and no MODEL_GDRIVE_ID set.")

download_model_if_needed()

app = Flask(__name__)
app.secret_key = config.Config.SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])

# Configuration
MODEL_PATH = config.Config.MODEL_PATH
IMG_SIZE = config.Config.IMG_SIZE

CLASS_NAMES = sorted([
    "Acne", "Athlete foot", "Atopic Dermatitis", "Bullous Disease",
    "Cellulitis", "Chicken Pox", "Eczema", "Exanthems",
    "Herpes", "Measles", "Melanocytic Nevi", "Melanoma",
    "Monkey Pox", "Nail Fungus", "Poison Ive", "Psoriasis",
    "Ringworm", "Rosacea", "Shingles", "Urticaria",
    "Vascular Lesion", "Vasculitis", "Warts"
])

# Disease information
DISEASE_INFO = {
    "Acne": "Common skin condition causing pimples, blackheads, and cysts. Usually affects face, chest, and back.",
    "Athlete foot": "Fungal infection affecting the feet, causing itching, scaling, and redness between toes.",
    "Atopic Dermatitis": "Chronic inflammatory skin condition causing dry, itchy, and inflamed skin.",
    "Bullous Disease": "Group of conditions causing fluid-filled blisters on the skin.",
    "Cellulitis": "Bacterial skin infection causing redness, swelling, and warmth in affected area.",
    "Chicken Pox": "Viral infection causing itchy rash with fluid-filled blisters.",
    "Eczema": "Inflammatory skin condition causing dry, itchy, and red patches.",
    "Exanthems": "Widespread rash usually caused by viral infections.",
    "Herpes": "Viral infection causing painful blisters or sores on skin or mucous membranes.",
    "Measles": "Highly contagious viral infection causing fever and red rash.",
    "Melanocytic Nevi": "Common moles or birthmarks on the skin, usually benign.",
    "Melanoma": "Serious form of skin cancer developing in melanocytes. Requires immediate medical attention.",
    "Monkey Pox": "Viral disease causing rash and flu-like symptoms.",
    "Nail Fungus": "Fungal infection affecting fingernails or toenails.",
    "Poison Ive": "Allergic skin reaction to poison ivy plant causing itchy rash.",
    "Psoriasis": "Autoimmune condition causing rapid skin cell buildup with scaly patches.",
    "Ringworm": "Fungal infection causing circular, red, itchy patches.",
    "Rosacea": "Chronic skin condition causing facial redness and visible blood vessels.",
    "Shingles": "Viral infection causing painful rash, usually on one side of body.",
    "Urticaria": "Hives - raised, itchy welts on the skin due to allergic reaction.",
    "Vascular Lesion": "Abnormalities in blood vessels visible on skin surface.",
    "Vasculitis": "Inflammation of blood vessels causing skin changes.",
    "Warts": "Small, rough growths caused by human papillomavirus (HPV)."
}

# ==================================================================
# THE FIX: Custom Classes to handle Colab -> Windows transition
# ==================================================================

@keras.saving.register_keras_serializable(package="Fix")
class SafeInputLayer(InputLayer):
    def __init__(self, batch_shape=None, **kwargs):
        # Fix the 'batch_shape' bug
        if batch_shape is not None:
            kwargs['batch_input_shape'] = batch_shape
        super().__init__(**kwargs)

@keras.saving.register_keras_serializable(package="Fix")
class SafeRescaling(Rescaling):
    @classmethod
    def from_config(cls, config):
        # Fix the 'dtype' bug (removes complex dictionary config)
        if 'dtype' in config:
            config['dtype'] = 'float32'
        return super().from_config(config)

# ==================================================================

# Load Model
model = None
if os.path.exists(MODEL_PATH):
    print(f"Loading model from {MODEL_PATH}...")
    try:
        # Use the custom classes to safely load the file
        model = keras.models.load_model(
            MODEL_PATH,
            custom_objects={
                'InputLayer': SafeInputLayer,
                'Rescaling': SafeRescaling
            },
            compile=False
        )
        print("SUCCESS: Model loaded correctly.")
    except Exception as e:
        print("\n" + "="*50)
        print(f"CRITICAL ERROR: {e}")
        print("="*50 + "\n")
else:
    print(f"ERROR: Model file '{MODEL_PATH}' not found.")

def process_image(image):
    # 1. Ensure RGB
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # 2. Resize
    img_resized = image.resize(IMG_SIZE)
    img_array = np.array(img_resized, dtype=np.float32)
    
    # 3. Preprocess (Standard EfficientNet preprocessing)
    img_array = preprocess_input(img_array)
    
    # 4. Expand dimensions to create batch: (1, 300, 300, 3)
    img_batch = np.expand_dims(img_array, axis=0)
    return img_batch

# MongoDB is initialized in database.py

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

@app.route('/')
def home():
    return redirect(FRONTEND_URL)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data received!"}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required!"}), 400
    
    # Check if user already exists
    if db.get_user_by_username(username):
        return jsonify({"success": False, "message": "Username already exists!"}), 400
    
    if db.get_user_by_email(email):
        return jsonify({"success": False, "message": "Email already exists!"}), 400
    
    # Create user
    try:
        user_id = db.create_user(username, email, password)
        if user_id:
            return jsonify({"success": True, "message": "Registration successful!"}), 201
        else:
            return jsonify({"success": False, "message": "Registration failed! Please try again."}), 500
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/register', methods=['GET'])
def register():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/register')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = db.get_user_by_username(username)
    
    if user and db.verify_password(user, password):
        session['user_id'] = str(user['_id'])
        session['username'] = user['username']
        return jsonify({"success": True, "message": "Login successful!", "username": user['username']}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password!"}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully!"}), 200

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({"authenticated": True, "username": session.get('username')}), 200
    return jsonify({"authenticated": False}), 200

@app.route('/login', methods=['GET'])
def login():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/login')

@app.route('/logout')
def logout():
    # Redirect to React frontend
    return redirect(FRONTEND_URL)

@app.route('/analyze')
def analyze():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/analyze')

@app.route('/report')
def report():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/report')

@app.route('/faq')
def faq():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/faq')

@app.route('/history')
def history():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/history')

@app.route('/api/history')
def api_history():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    analyses = db.get_user_analyses(session['user_id'], limit=20)
    
    # Convert ObjectId to string for JSON serialization
    for analysis in analyses:
        analysis['_id'] = str(analysis['_id'])
        analysis['user_id'] = str(analysis['user_id'])
        if analysis.get('created_at'):
            analysis['created_at'] = analysis['created_at'].isoformat()
    
    return jsonify({"success": True, "analyses": analyses})

@app.route('/profile')
def profile():
    # Redirect to React frontend
    return redirect(f'{FRONTEND_URL}/profile')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Check terminal logs."}), 500
    
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(file.stream)
        processed_image = process_image(image)

        predictions = model.predict(processed_image)
        
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        
        results = []
        for idx in top_3_indices:
            disease_name = CLASS_NAMES[idx]
            results.append({
                "class": disease_name,
                "confidence": float(predictions[0][idx]),
                "description": DISEASE_INFO.get(disease_name, "No description available.")
            })

        # Save analysis to database
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        db.save_analysis(session['user_id'], results, f"data:image/jpeg;base64,{img_str}")

        return jsonify({
            "success": True,
            "predictions": results
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Check terminal logs."}), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(file.stream)
        processed_image = process_image(image)

        predictions = model.predict(processed_image)
        
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        
        results = []
        for idx in top_3_indices:
            disease_name = CLASS_NAMES[idx]
            results.append({
                "class": disease_name,
                "confidence": float(predictions[0][idx]),
                "description": DISEASE_INFO.get(disease_name, "No description available.")
            })

        # Save analysis to database if user is logged in
        if 'user_id' in session:
            # Convert image to base64 for storage
            image.seek(0) if hasattr(image, 'seek') else None
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            db.save_analysis(session['user_id'], results, f"data:image/jpeg;base64,{img_str}")

        return jsonify({
            "success": True,
            "predictions": results
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download-report', methods=['POST'])
def download_report():
    try:
        data = request.json
        predictions = data.get('predictions', [])
        image_data = data.get('image', '')
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("Skin Condition Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Date and time
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Report Generated:</b> {current_time}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Add image if provided
        if image_data and image_data.startswith('data:image'):
            try:
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                img = RLImage(io.BytesIO(image_bytes), width=3*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
            except:
                pass
        
        # Analysis Results
        story.append(Paragraph("Analysis Results", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Create table for results
        table_data = [['Condition', 'Confidence', 'Status']]
        for i, pred in enumerate(predictions):
            confidence = f"{pred['confidence'] * 100:.1f}%"
            status = "Primary Diagnosis" if i == 0 else "Possible Condition"
            table_data.append([pred['class'], confidence, status])
        
        table = Table(table_data, colWidths=[3*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#eafaf1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed Information
        story.append(Paragraph("Detailed Information", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        for i, pred in enumerate(predictions):
            condition_title = f"<b>{i+1}. {pred['class']}</b> ({pred['confidence']*100:.1f}% confidence)"
            story.append(Paragraph(condition_title, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph(pred.get('description', 'No description available.'), styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
        
        # Disclaimer
        story.append(Spacer(1, 0.3*inch))
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7f8c8d'),
            borderWidth=1,
            borderColor=colors.HexColor('#e74c3c'),
            borderPadding=10,
            backColor=colors.HexColor('#fadbd8')
        )
        story.append(Paragraph(
            "<b>IMPORTANT DISCLAIMER:</b> This analysis is generated by an AI system and is for informational purposes only. "
            "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
            "Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition.",
            disclaimer_style
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'skin_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Report Generation Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)