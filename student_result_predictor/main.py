from flask import Flask, render_template, request, jsonify
import os

# Simple Flask app
app = Flask(__name__)

# Set template and static folders
app.template_folder = 'templates'
app.static_folder = 'static'

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Student Result Predictor</title></head>
    <body>
        <h1>Student Result Predictor</h1>
        <form action="/predict" method="post">
            <p>Study hours (0-8): <input type="number" name="study_hours" min="0" max="8" value="5" required></p>
            <p>Sleep hours (4-9): <input type="number" name="sleep_hours" min="4" max="9" value="7" required></p>
            <p>Absences (0-20): <input type="number" name="absences" min="0" max="20" value="2" required></p>
            <p>Assignments (0-10): <input type="number" name="assignments_completed" min="0" max="10" value="8" required></p>
            <p>Exam Score (40-100): <input type="number" name="exam_score" min="40" max="100" value="85" required></p>
            <p><button type="submit">Predict</button></p>
        </form>
        <p><a href="/test">Test API</a></p>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    try:
        study_hours = int(request.form.get('study_hours', 0))
        sleep_hours = int(request.form.get('sleep_hours', 0))
        absences = int(request.form.get('absences', 0))
        assignments_completed = int(request.form.get('assignments_completed', 0))
        exam_score = int(request.form.get('exam_score', 0))
        
        # Simple prediction logic
        score = (study_hours * 10) + (sleep_hours * 5) - (absences * 2) + (assignments_completed * 3) + (exam_score * 0.5)
        prediction = 'Pass' if score > 400 else 'Fail'
        probability = min(95, max(5, score / 6))
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Prediction Result</title></head>
        <body>
            <h1>Prediction Result</h1>
            <h2>Result: {prediction}</h2>
            <p>Confidence: {probability:.1f}%</p>
            <h3>Your Input:</h3>
            <p>Study Hours: {study_hours}</p>
            <p>Sleep Hours: {sleep_hours}</p>
            <p>Absences: {absences}</p>
            <p>Assignments Completed: {assignments_completed}</p>
            <p>Exam Score: {exam_score}</p>
            <p><a href="/">Try Again</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}", 400

@app.route('/test')
def test():
    return jsonify({
        "status": "Working!",
        "message": "Flask app is running on Vercel",
        "routes": ["/", "/predict", "/test"],
        "current_dir": os.getcwd(),
        "template_folder": app.template_folder,
        "static_folder": app.static_folder
    })

if __name__ == '__main__':
    app.run(debug=True)