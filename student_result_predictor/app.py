from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model_path = os.path.join('model', 'dt_model.joblib')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}. Run train_model.py first.")

model = joblib.load(model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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

if __name__ == '__main__':
    app.run(debug=True)
