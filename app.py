from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import os

app = Flask(__name__)
# Change this to a secure random string in a production environment
app.secret_key = 'astralearn_secure_key_2026'

# Load the Machine Learning Model
MODEL_PATH = 'student_model.pkl'
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("Warning: student_model.pkl not found. Predictions will fail until the model is trained.")

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. Landing Page Route
@app.route('/')
def home():
    # Bypass landing page if already authenticated
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# 2. Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Secure the password
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, hashed_password))
            conn.commit()
            flash('Workspace account registered successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email is already associated with an account.', 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

# 3. Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        # Validate credentials against hashed password
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

# 4. Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 5. Main Dashboard (Input Form)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Authentication required to access the workspace.', 'error')
        return redirect(url_for('login'))
        
    return render_template('dashboard.html', username=session['username'])

# 6. Inference and Results Route
@app.route('/predict', methods=['POST'])
def predict():
    # Security check
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if not model:
        flash('The prediction engine is currently offline. Model file missing.', 'error')
        return redirect(url_for('dashboard'))

    try:
        # Extract features from the HTML form
        attendance = float(request.form['attendance'])
        study_hours = float(request.form['study_hours'])
        prev_grade = float(request.form['prev_grade'])
        extracurricular = int(request.form['extracurricular'])
        sleep_hours = float(request.form['sleep_hours'])
        social_media = float(request.form['social_media'])

        # Format into a 2D NumPy array for the Random Forest model
        features = np.array([[attendance, study_hours, prev_grade, extracurricular, sleep_hours, social_media]])
        
        # Execute prediction
        raw_prediction = model.predict(features)[0]
        
        # Mathematical boundary enforcement (0 to 100 range)
        final_grade = max(0.0, min(100.0, raw_prediction))
        
        # Metric scaling for uniform Chart.js rendering
        study_index = min(100, study_hours * 15)
        rest_index = min(100, sleep_hours * 10)
        distraction_index = min(100, social_media * 15)
        
        # Pass all calculated values to the results template
        return render_template('results.html', 
                               grade=round(final_grade, 2),
                               attendance=attendance,
                               study_index=study_index,
                               prev_grade=prev_grade,
                               rest_index=rest_index,
                               distraction_index=distraction_index,
                               sleep_hours=sleep_hours,
                               social_media=social_media)
                               
    except Exception as e:
        flash('Error processing prediction array. Please ensure all inputs are valid numbers.', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)