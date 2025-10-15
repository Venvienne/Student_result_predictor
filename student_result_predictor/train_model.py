import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np

# ------------------ Load Dataset Safely ------------------ #

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "students.csv")

print("Looking for file at:", csv_path)

df = pd.read_csv(csv_path)

# Ensure numeric types
for col in ['study_hours', 'sleep_hours', 'absences', 'assignments_completed', 'exam_score']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

# Features and labels
feature_cols = ['study_hours', 'sleep_hours', 'absences', 'assignments_completed', 'exam_score']
X = df[feature_cols]

# ------------------ Classification Model (Pass/Fail) ------------------ #

y_class = df['result'].map({'Fail': 0, 'Pass': 1})

X_train, X_test, y_train_cls, y_test_cls = train_test_split(
    X, y_class, test_size=0.25, random_state=42, stratify=y_class
)

clf = DecisionTreeClassifier(random_state=42, max_depth=6, min_samples_split=10, class_weight='balanced')
clf.fit(X_train, y_train_cls)

y_pred_cls = clf.predict(X_test)
accuracy = round(accuracy_score(y_test_cls, y_pred_cls) * 100, 2)

print("✅ Classification Accuracy:", accuracy, "%")
print("\nConfusion Matrix:\n", confusion_matrix(y_test_cls, y_pred_cls))
print("\nClassification Report:\n", classification_report(y_test_cls, y_pred_cls))

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/dt_classifier.joblib")
with open("model/accuracy.txt", "w") as f:
    f.write(str(accuracy))

# ------------------ Regression Model (Grade Prediction) ------------------ #

y_reg = df['exam_score']  # Or replace with actual grade column if you have one

X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X, y_reg, test_size=0.25, random_state=42
)

reg = DecisionTreeRegressor(random_state=42, max_depth=6, min_samples_split=10)
reg.fit(X_train, y_train_reg)

y_pred_reg = reg.predict(X_test)

# Regression Metrics
mae = mean_absolute_error(y_test_reg, y_pred_reg)
mse = mean_squared_error(y_test_reg, y_pred_reg)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_reg, y_pred_reg)

print("\n📈 Regression Model Performance:")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 2))

# Save regression model & score
joblib.dump(reg, "model/dt_regressor.joblib")
with open("model/regression_r2.txt", "w") as f:
    f.write(str(round(r2, 2)))

# ------------------ Visualization ------------------ #

# Classification Tree
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=feature_cols, class_names=['Fail', 'Pass'], filled=True)
plt.title("Decision Tree - Classification (Pass/Fail)")
plt.savefig("model/decision_tree_classifier.png")
plt.show()

# Regression Tree
plt.figure(figsize=(12, 8))
plot_tree(reg, feature_names=feature_cols, filled=True)
plt.title("Decision Tree - Regression (Grade Prediction)")
plt.savefig("model/decision_tree_regressor.png")
plt.show()

# ------------------ Actual vs Predicted Scatter Plot ------------------ #

plt.figure(figsize=(8, 6))
plt.scatter(y_test_reg, y_pred_reg, alpha=0.7)
plt.xlabel("Actual Grades")
plt.ylabel("Predicted Grades")
plt.title("Actual vs Predicted Grades (Regression)")
plt.savefig("model/actual_vs_predicted_regression.png")
plt.show()
