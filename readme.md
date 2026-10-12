# Student Performance Prediction System Using Machine Learning

An AI-driven full-stack web application designed to analyze, evaluate, and predict student academic outcomes based on lifestyle distributions and prior scholastic parameters. Moving away from traditional retrospective reporting, this platform provides an interactive workspace leveraging a serialized Random Forest Regressor to compute performance metrics in real time alongside a rule-based AI prescriptive consultative engine.

## 🚀 Core Features

- **Asymmetric Authentication Gateway:** Secure user workspace provisioning with salted PBKDF2 cryptography (150,000 computation rounds) and signed session validation loops.
- **Operational Feature Matrix Dashboard:** An interactive parameters input terminal parsing 6 distinct behavioral and academic feature parameters with boundary condition filtering.
- **Dynamic Diagnostic Assessment Reports:** Real-time client-side rendering engines using Chart.js to animate radial grade gauges and multi-dataset horizontal bar charts comparing student performance profiles directly against institutional targets.
- **Automated Consultative AI Insights:** A rule-based diagnostic layer that automatically flags sleep deficiency, attendance vulnerabilities, and attention fragmentation with tailored performance-remediation prescriptions.

---

## 🛠️ Technology Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Backend Core** | Flask (Python) | Server-side request routing, controller logic, and session encryption. |
| **Database Engine** | SQLite3 | Local Relational Database management tracking multi-tenant user profiles. |
| **Machine Learning** | Scikit-Learn / NumPy | Numerical array array parsing and Random Forest model inference. |
| **Frontend Framework** | Tailwind CSS v4 | Utility-first, high-density dashboard layouts and focus management interfaces. |
| **Data Visualization** | Chart.js | Client-side HTML5 canvas data charting and radial metric tracking. |
| **Security Handling** | Werkzeug | Secure multi-round password hashing (`generate_password_hash`). |

---

## 📂 Project Directory Structure

```text
student-performance-prediction/
├── app.py                 # Core Flask Web Controller application logic
├── init_db.py             # SQLite3 Relational schema initialization script
├── train_model.py         # Model pipeline training execution logic script
├── database.db            # Local multi-tenant SQLite database (auto-generated)
├── student_model.pkl      # Serialized Random Forest Regressor binary (pickle)
└── templates/             # Jinja2 HTML rendering templates
    ├── login.html         # Authentication Access Gateway UI
    ├── register.html      # Account Creation Gateway UI
    ├── dashboard.html     # Feature Matrix Input Panel UI
    └── results.html       # Diagnostic Report Analysis Visualizer UI