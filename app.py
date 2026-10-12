from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'ultra_secure_premium_key'

model = pickle.load(open('student_model.pkl', 'rb'))

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

## --- AUTHENTICATION ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username or Email already exists!"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

## --- PAGE 1: INPUT FORM DASHBOARD ---

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        attendance = float(request.form['attendance'])
        daily_study_hours = float(request.form['daily_study_hours'])
        prev_grade = float(request.form['prev_grade'])
        extracurricular = float(request.form['extracurricular'])
        sleep_hours = float(request.form['sleep_hours'])
        social_media = float(request.form['social_media'])
        
        # ML Prediction array processing
        input_features = np.array([[attendance, daily_study_hours, prev_grade, extracurricular, sleep_hours, social_media]])
        prediction = model.predict(input_features)[0]
        prediction = max(0.0, min(100.0, prediction))
        
        # AI Recommendations Generator
        advisories = []
        if attendance < 75:
            advisories.append("Critical: Attendance falls beneath compliance targets. Prioritize physical lecture attendance.")
        if daily_study_hours < 2.5:
            advisories.append("Study Gap: Daily independent study metrics are shallow. Aim for at least 3 hours daily.")
        if sleep_hours < 6.5:
            advisories.append("Sleep Deprivation Risk: Rest cycles are constraining cognitive processing. Target 7.5 hours.")
        if social_media > 3.0:
            advisories.append("Attention Fragmentation: High screen times dilute deep focus endurance cycles.")
            
        if not advisories:
            advisories.append("Optimal behavior balance achieved! Maintain this exact profile matrix.")

        # Save calculations to temporary memory session (No history logging to DB)
        session['last_result'] = {
            'score': round(prediction, 2),
            'status': "Excellent / Safe" if prediction >= 75 else ("Pass / Moderate" if prediction >= 50 else "Academic Risk Warning"),
            'advisories': advisories,
            'metrics': [attendance, daily_study_hours * 15, prev_grade, sleep_hours * 10, social_media * 15]
        }
        return redirect(url_for('results'))
        
    return render_template('dashboard.html')

## --- PAGE 2: SEPARATE ANALYTICS RESULTS ---

@app.route('/results')
def results():
    if 'user_id' not in session or 'last_result' not in session:
        return redirect(url_for('dashboard'))
        
    data = session.get('last_result')
    return render_template('results.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)