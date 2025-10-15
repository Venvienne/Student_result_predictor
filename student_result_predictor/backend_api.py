from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np

app = Flask(__name__)

# Enable CORS for all routes (allow frontend from Vercel)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model', 'dt_model.joblib')

try:
    model = joblib.load(model_path) if os.path.exists(model_path) else None
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Student Result Predictor API",
        "status": "running",
        "endpoints": {
            "/": "API information",
            "/predict": "POST - Make prediction",
            "/health": "GET - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract features
        study_hours = float(data.get('study_hours', 0))
        sleep_hours = float(data.get('sleep_hours', 0))
        absences = float(data.get('absences', 0))
        assignments_completed = float(data.get('assignments_completed', 0))
        exam_score = float(data.get('exam_score', 0))
        
        # Validate inputs
        if not (0 <= study_hours <= 8):
            return jsonify({"error": "Study hours must be between 0 and 8"}), 400
        if not (4 <= sleep_hours <= 9):
            return jsonify({"error": "Sleep hours must be between 4 and 9"}), 400
        if not (0 <= absences <= 20):
            return jsonify({"error": "Absences must be between 0 and 20"}), 400
        if not (0 <= assignments_completed <= 20):
            return jsonify({"error": "Assignments must be between 0 and 20"}), 400
        if not (40 <= exam_score <= 100):
            return jsonify({"error": "Exam score must be between 40 and 100"}), 400
        
        # Make prediction
        if model is not None:
            # Use ML model
            features = np.array([[study_hours, sleep_hours, absences, assignments_completed, exam_score]])
            pred = model.predict(features)[0]
            prob = model.predict_proba(features)[0]
            
            prediction = 'Pass' if pred == 1 else 'Fail'
            probability = float(prob[1] * 100) if pred == 1 else float(prob[0] * 100)
        else:
            # Fallback heuristic prediction
            score = (study_hours * 10) + (sleep_hours * 5) - (absences * 2) + (assignments_completed * 3) + (exam_score * 0.5)
            prediction = 'Pass' if score > 400 else 'Fail'
            probability = min(95, max(5, score / 6))
        
        # Return prediction result
        return jsonify({
            "success": True,
            "prediction": prediction,
            "probability": round(probability, 2),
            "input": {
                "study_hours": study_hours,
                "sleep_hours": sleep_hours,
                "absences": absences,
                "assignments_completed": assignments_completed,
                "exam_score": exam_score
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
