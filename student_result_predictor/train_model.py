import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

# Load dataset
df = pd.read_csv('data/students.csv')

# Ensure numeric types
for col in ['study_hours', 'sleep_hours', 'absences', 'assignments_completed', 'exam_score']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

# Features and labels
feature_cols = ['study_hours', 'sleep_hours', 'absences', 'assignments_completed', 'exam_score']
X = df[feature_cols]
y = df['result'].map({'Fail': 0, 'Pass': 1})

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Train Decision Tree
clf = DecisionTreeClassifier(
    random_state=42,
    max_depth=6,
    min_samples_split=10,
    class_weight='balanced'
)
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)

print("✅ Accuracy:", accuracy, "%")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/dt_model.joblib")
print("💾 Model saved to model/dt_model.joblib")

# Save accuracy to file (so Flask can display it)
with open("model/accuracy.txt", "w") as f:
    f.write(str(accuracy))

print("📊 Accuracy saved to model/accuracy.txt")
