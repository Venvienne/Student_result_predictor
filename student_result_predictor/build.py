#!/usr/bin/env python3
"""
Build script for Vercel deployment
Ensures the model is properly trained and ready for deployment
"""

import os
import sys
import subprocess

def ensure_model_exists():
    """Ensure the ML model exists, create it if it doesn't"""
    model_path = os.path.join('model', 'dt_model.joblib')
    
    if not os.path.exists(model_path):
        print("Model not found. Training model...")
        try:
            # Run the training script
            subprocess.run([sys.executable, 'train_model.py'], check=True)
            print("Model trained successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error training model: {e}")
            return False
        except FileNotFoundError:
            print("train_model.py not found. Creating minimal model...")
            create_minimal_model()
    else:
        print("Model already exists.")
    
    return True

def create_minimal_model():
    """Create a minimal model if training script is not available"""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import joblib
    import numpy as np
    
    # Create synthetic data for demo
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'study_hours': np.random.randint(0, 9, n_samples),
        'sleep_hours': np.random.randint(4, 10, n_samples),
        'absences': np.random.randint(0, 21, n_samples),
        'assignments_completed': np.random.randint(0, 21, n_samples),
        'exam_score': np.random.randint(40, 101, n_samples)
    }
    
    # Simple logic to create target variable
    df = pd.DataFrame(data)
    df['result'] = ((df['study_hours'] >= 5) & 
                   (df['sleep_hours'] >= 6) & 
                   (df['absences'] <= 10) & 
                   (df['assignments_completed'] >= 10) & 
                   (df['exam_score'] >= 60)).astype(int)
    
    # Prepare features and target
    X = df[['study_hours', 'sleep_hours', 'absences', 'assignments_completed', 'exam_score']]
    y = df['result']
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/dt_model.joblib')
    print("Minimal model created and saved!")

if __name__ == "__main__":
    ensure_model_exists()