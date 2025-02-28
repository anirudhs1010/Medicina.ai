import logging
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def validate_blood_pressure(bp_string):
    """
    Validate blood pressure string format (e.g., '120/80')
    Returns tuple of (systolic, diastolic) if valid, None if invalid
    """
    try:
        if not bp_string or '/' not in bp_string:
            return None
        
        systolic, diastolic = map(int, bp_string.split('/'))
        
        # Basic range validation
        if 70 <= systolic <= 200 and 40 <= diastolic <= 130:
            return (systolic, diastolic)
        return None
    except ValueError:
        return None

def validate_heart_rate(hr):
    """
    Validate heart rate value
    Returns heart rate if valid, None if invalid
    """
    try:
        hr = int(hr)
        if 30 <= hr <= 220:
            return hr
        return None
    except (ValueError, TypeError):
        return None

def validate_temperature(temp):
    """
    Validate temperature in Celsius
    Returns temperature if valid, None if invalid
    """
    try:
        temp = float(temp)
        if 35.0 <= temp <= 42.0:
            return temp
        return None
    except (ValueError, TypeError):
        return None

def validate_weight(weight):
    """
    Validate weight in kilograms
    Returns weight if valid, None if invalid
    """
    try:
        weight = float(weight)
        if 20.0 <= weight <= 300.0:
            return weight
        return None
    except (ValueError, TypeError):
        return None

def validate_email(email):
    """
    Validate email format
    Returns True if valid, False if invalid
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))

def format_date(date):
    """
    Format datetime object to string
    """
    return date.strftime('%Y-%m-%d %H:%M:%S')

def calculate_bmi(weight, height):
    """
    Calculate BMI given weight (kg) and height (m)
    """
    try:
        bmi = weight / (height ** 2)
        return round(bmi, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return None

def get_bmi_category(bmi):
    """
    Get BMI category based on BMI value
    """
    if bmi is None:
        return "Unknown"
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def format_blood_pressure_reading(systolic, diastolic):
    """
    Format blood pressure reading with classification
    """
    try:
        if systolic < 120 and diastolic < 80:
            category = "Normal"
        elif 120 <= systolic < 130 and diastolic < 80:
            category = "Elevated"
        elif 130 <= systolic < 140 or 80 <= diastolic < 90:
            category = "Stage 1 Hypertension"
        elif systolic >= 140 or diastolic >= 90:
            category = "Stage 2 Hypertension"
        else:
            category = "Unknown"
        
        return f"{systolic}/{diastolic} mmHg ({category})"
    except (TypeError, ValueError):
        return "Invalid reading"

def log_health_update(user_id, data_type, value):
    """
    Log health data updates for auditing
    """
    logger.info(f"Health data update - User: {user_id}, Type: {data_type}, Value: {value}, Time: {datetime.utcnow()}")

def format_risk_score(score):
    """
    Format risk score with interpretation
    """
    percentage = score * 100
    if percentage < 20:
        level = "Low"
        advice = "Maintain healthy lifestyle"
    elif 20 <= percentage < 40:
        level = "Moderate"
        advice = "Consider lifestyle improvements"
    elif 40 <= percentage < 60:
        level = "Increased"
        advice = "Consult healthcare provider"
    else:
        level = "High"
        advice = "Urgent medical attention recommended"
    
    return {
        "percentage": round(percentage, 1),
        "level": level,
        "advice": advice
    }

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS
    """
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Convert special characters to HTML entities
    text = text.replace('&', '&amp;')\
               .replace('<', '&lt;')\
               .replace('>', '&gt;')\
               .replace('"', '&quot;')\
               .replace("'", '&#x27;')
    return text
