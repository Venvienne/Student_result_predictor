from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
import sys

# Add current directory and parent to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

# Initialize Flask app with absolute paths
app = Flask(__name__)

# Configure template and static folders with absolute paths
app.template_folder = os.path.join(parent_dir, 'templates')
app.static_folder = os.path.join(parent_dir, 'static')

# Load trained model
model_path = os.path.join(parent_dir, 'model', 'dt_model.joblib')
model = None

try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
    else:
        print(f"Model file not found at {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Student Result Predictor</title></head>
        <body>
        <h1>Student Result Predictor</h1>
        <p>Error loading template: {str(e)}</p>
        <p>Template folder: {app.template_folder}</p>
        <p>Current directory: {os.getcwd()}</p>
        <p><a href="/test">Test API</a></p>
        </body>
        </html>
        """

@app.route('/test')
def test():
    return jsonify({
        "status": "API is working!",
        "template_folder": app.template_folder,
        "static_folder": app.static_folder,
        "model_loaded": model is not None,
        "current_dir": os.getcwd(),
        "files_in_parent": os.listdir(parent_dir) if os.path.exists(parent_dir) else "Parent dir not found"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
        
    try:
        study_hours = int(request.form.get('study_hours', 0))
        sleep_hours = int(request.form.get('sleep_hours', 0))
        absences = int(request.form.get('absences', 0))
        assignments_completed = int(request.form.get('assignments_completed', 0))
        exam_score = int(request.form.get('exam_score', 0))

        features = np.array([[study_hours, sleep_hours, absences, assignments_completed, exam_score]])
        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0]
        label = 'Pass' if pred == 1 else 'Fail'
        probability = float(prob[1]) if pred == 1 else float(prob[0])

        try:
            return render_template(
                'result.html',
                prediction=label,
                probability=round(probability * 100, 2),
                study_hours=study_hours,
                sleep_hours=sleep_hours,
                absences=absences,
                assignments_completed=assignments_completed,
                exam_score=exam_score
            )
        except Exception as template_error:
            # Fallback to JSON response if template fails
            return jsonify({
                "prediction": label,
                "probability": round(probability * 100, 2),
                "study_hours": study_hours,
                "sleep_hours": sleep_hours,
                "absences": absences,
                "assignments_completed": assignments_completed,
                "exam_score": exam_score,
                "template_error": str(template_error)
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/test-result')
def test_result():
    try:
        return render_template(
            'result.html',
            prediction='Pass',
            probability=85.67,
            study_hours=7,
            sleep_hours=8,
            absences=2,
            assignments_completed=15,
            exam_score=92
        )
    except Exception as e:
        return jsonify({
            "prediction": "Pass",
            "probability": 85.67,
            "study_hours": 7,
            "sleep_hours": 8,
            "absences": 2,
            "assignments_completed": 15,
            "exam_score": 92,
            "template_error": str(e)
        })

# Configure for production
app.config['DEBUG'] = False

# This is what Vercel looks for
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True)