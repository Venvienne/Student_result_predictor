import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

# Number of students
n = 1000

# Generate data
study_hours = np.random.randint(0, 9, n)   # 0-8 hours/day
sleep_hours = np.random.randint(4, 10, n)  # 4-9 hours/day
absences = np.random.randint(0, 21, n)     # 0-20 days absent
assignments_completed = np.random.randint(0, 11, n)  # 0-10 assignments
exam_score = np.random.randint(40, 101, n)  # 40 - 100

# Performance logic (penalize more absences)
performance_score = (
    (study_hours * 5) +
    (sleep_hours * 2) -
    (absences * 2) +
    (assignments_completed * 3) +
    (exam_score * 0.6)
)

# Label pass/fail
result = np.where(performance_score >= 100, "Pass", "Fail")

# Build DataFrame
df = pd.DataFrame({
    "study_hours": study_hours,
    "sleep_hours": sleep_hours,
    "absences": absences,
    "assignments_completed": assignments_completed,
    "exam_score": exam_score,
    "result": result
})

# Save to CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/students.csv", index=False)

print("✅ Dataset generated with absences instead of attendance")
print(df.head(10))
