import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

np.random.seed(42)
n_students = 1500

# Generating multi-variable complex dataset attributes
attendance = np.random.uniform(60, 100, n_students)
daily_study_hours = np.random.uniform(0.5, 6, n_students)
prev_grade = np.random.uniform(45, 100, n_students)
extracurricular = np.random.choice([0, 1], size=n_students, p=[0.4, 0.6])
sleep_hours = np.random.uniform(4, 9, n_students)
social_media = np.random.uniform(0.5, 6, n_students)

# Behavioral output calibration mapping formula
final_score = (
    (attendance * 0.25) + 
    (daily_study_hours * 6.5) + 
    (prev_grade * 0.35) + 
    (extracurricular * 3.5) + 
    (7.5 - np.abs(sleep_hours - 7.5)) * 2.5 - 
    (social_media * 1.8) + 
    np.random.normal(0, 2.5, n_students)
)
final_score = np.clip(final_score, 0, 100)

dataset = pd.DataFrame({
    'attendance': attendance,
    'daily_study_hours': daily_study_hours,
    'prev_grade': prev_grade,
    'extracurricular': extracurricular,
    'sleep_hours': sleep_hours,
    'social_media': social_media
})

model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(dataset, final_score)

with open('student_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Advanced 6-Feature Random Forest Brain trained successfully!")