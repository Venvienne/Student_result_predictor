from flask import Flask, render_template, request
import joblib
import numpy as np
import os
import sys

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'dt_model.joblib')
try:
    model = joblib.load(model_path)
except FileNotFoundError:
    # If model not found, we'll handle this gracefully
    model = None
    print(f"Warning: Model not found at {model_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Error: Model not loaded. Please check model file.", 500
        
    try:
        study_hours = int(request.form['study_hours'])
        sleep_hours = int(request.form['sleep_hours'])
        absences = int(request.form['absences'])
        assignments_completed = int(request.form['assignments_completed'])
        exam_score = int(request.form['exam_score'])

        features = np.array([[study_hours, sleep_hours, absences, assignments_completed, exam_score]])
        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0]
        label = 'Pass' if pred == 1 else 'Fail'
        probability = float(prob[1]) if pred == 1 else float(prob[0])

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
    except Exception as e:
        return f"Error: {e}", 400

@app.route('/test-result')
def test_result():
    # Sample data for testing the result page design
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

# Configure for production
app.config['DEBUG'] = False

# For local development
if __name__ == '__main__':
    app.run(debug=True)