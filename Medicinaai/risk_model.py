import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load and prepare the model once
df = pd.read_csv('heart.csv')
X = df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak']]
y = df['target']

# Split and scale data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

def predict_heart_disease_risk(data):
    """
    Predict heart disease risk using trained model

    Args:
        data (dict): Dictionary containing health metrics
            Required keys: age, blood_pressure, cholesterol, heart_rate
            Optional: st_depression (oldpeak)

    Returns:
        float: Risk score between 0 and 1
    """
    try:
        # Extract and validate features
        features = []

        # Age
        age = float(data.get('age', 0))
        if not (20 <= age <= 100):
            raise ValueError("Age must be between 20 and 100")
        features.append(age)

        # Blood pressure (systolic)
        bp = data.get('blood_pressure', '')
        try:
            systolic = float(bp.split('/')[0])
            if not (80 <= systolic <= 200):
                raise ValueError
        except (ValueError, IndexError):
            raise ValueError("Invalid blood pressure format. Expected format: '120/80'")
        features.append(systolic)

        # Cholesterol
        chol = float(data.get('cholesterol', 0))
        if not (100 <= chol <= 600):
            raise ValueError("Cholesterol must be between 100 and 600")
        features.append(chol)

        # Heart rate
        hr = float(data.get('heart_rate', 0))
        if not (40 <= hr <= 200):
            raise ValueError("Heart rate must be between 40 and 200")
        features.append(hr)

        # ST depression (oldpeak)
        oldpeak = float(data.get('st_depression', 0))
        if not (0 <= oldpeak <= 6):
            raise ValueError("ST depression must be between 0 and 6")
        features.append(oldpeak)

        # Scale features
        features_scaled = scaler.transform(np.array(features).reshape(1, -1))

        # Get probability of heart disease
        risk_score = model.predict_proba(features_scaled)[0][1]

        return float(risk_score)

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return 0.0