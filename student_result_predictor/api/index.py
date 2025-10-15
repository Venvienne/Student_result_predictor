from flask import Flask, render_template, request, jsonify
import os
import sys

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Simple Flask app setup for Vercel
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Simple model loading (create a dummy model for now to test)
try:
    import joblib
    import numpy as np
    model_path = os.path.join(BASE_DIR, 'model', 'dt_model.joblib')
    model = joblib.load(model_path) if os.path.exists(model_path) else None
except ImportError:
    model = None
    joblib = None
    np = None

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback HTML if template fails
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Student Result Predictor</title></head>
        <body>
            <h1>Student Result Predictor</h1>
            <p>Template error: {str(e)}</p>
            <p>Template folder: {app.template_folder}</p>
            <p>Files exist: {os.path.exists(app.template_folder)}</p>
            <form action="/predict" method="post">
                <p>Study hours: <input type="number" name="study_hours" min="0" max="8" value="5"></p>
                <p>Sleep hours: <input type="number" name="sleep_hours" min="4" max="9" value="7"></p>
                <p>Absences: <input type="number" name="absences" min="0" max="20" value="2"></p>
                <p>Assignments: <input type="number" name="assignments_completed" min="0" max="10" value="8"></p>
                <p>Exam Score: <input type="number" name="exam_score" min="40" max="100" value="85"></p>
                <p><button type="submit">Predict</button></p>
            </form>
        </body>
        </html>
        """

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or joblib is None:
        # Simple fallback prediction logic
        study_hours = int(request.form.get('study_hours', 0))
        sleep_hours = int(request.form.get('sleep_hours', 0))
        absences = int(request.form.get('absences', 0))
        assignments_completed = int(request.form.get('assignments_completed', 0))
        exam_score = int(request.form.get('exam_score', 0))
        
        # Simple heuristic prediction
        score = (study_hours * 10) + (sleep_hours * 5) - (absences * 2) + (assignments_completed * 3) + (exam_score * 0.5)
        prediction = 'Pass' if score > 400 else 'Fail'
        probability = min(95, max(5, score / 6))
        
        try:
            return render_template(
                'result.html',
                prediction=prediction,
                probability=round(probability, 2),
                study_hours=study_hours,
                sleep_hours=sleep_hours,
                absences=absences,
                assignments_completed=assignments_completed,
                exam_score=exam_score
            )
        except Exception as e:
            return jsonify({
                "prediction": prediction,
                "probability": round(probability, 2),
                "study_hours": study_hours,
                "sleep_hours": sleep_hours,
                "absences": absences,
                "assignments_completed": assignments_completed,
                "exam_score": exam_score,
                "error": f"Template error: {str(e)}"
            })
    
    # ML model prediction (if available)
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
        return jsonify({"error": str(e)}), 400

@app.route('/test')
def test():
    return jsonify({
        "status": "API is working!",
        "template_folder": app.template_folder,
        "static_folder": app.static_folder,
        "template_exists": os.path.exists(os.path.join(app.template_folder, 'index.html')),
        "static_exists": os.path.exists(os.path.join(app.static_folder, 'style.css')),
        "model_loaded": model is not None,
        "current_dir": os.getcwd(),
        "python_version": sys.version
    })

# For Vercel - export the app
app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run(debug=True)