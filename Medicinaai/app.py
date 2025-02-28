import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configure the PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.secret_key = os.environ.get("SESSION_SECRET")

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization to avoid circular imports
from models import User, HealthData

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    health_data = HealthData.query.filter_by(user_id=current_user.id).order_by(HealthData.timestamp.desc()).first()
    return render_template('dashboard.html', health_data=health_data)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/api/health-history', methods=['GET'])
@login_required
def get_health_history():
    health_data = HealthData.query.filter_by(user_id=current_user.id)\
        .order_by(HealthData.timestamp.desc())\
        .limit(6)\
        .all()
    
    data = [{
        'blood_pressure': h.blood_pressure,
        'heart_rate': h.heart_rate,
        'timestamp': h.timestamp.strftime('%b %d')
    } for h in reversed(health_data)]
    
    return jsonify(data)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    from ai_helper import get_chatbot_response
    message = request.json.get('message')
    response = get_chatbot_response(message)
    return jsonify({'response': response})

@app.route('/api/health-data', methods=['POST'])
@login_required
def update_health_data():
    from risk_model import predict_heart_disease_risk
    data = request.json
    health_data = HealthData(
        user_id=current_user.id,
        blood_pressure=data.get('blood_pressure'),
        heart_rate=data.get('heart_rate'),
        temperature=data.get('temperature'),
        weight=data.get('weight')
    )
    db.session.add(health_data)
    db.session.commit()

    risk_score = predict_heart_disease_risk(data)
    return jsonify({
        'message': 'Data updated successfully',
        'risk_score': risk_score
    })

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

with app.app_context():
    # Create all database tables
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)