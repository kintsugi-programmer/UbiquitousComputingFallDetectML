from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
import joblib
import numpy as np
from dotenv import load_dotenv
import smtplib

# Load environment variables
load_dotenv()
email_user = os.getenv('MAIL_USERNAME')
email_pass = os.getenv('MAIL_PASSWORD')
recipient = os.getenv('MAIL_RECIPIENT')

# Send service started email
def send_startup_email():
    try:
        message = "Subject: SecondGuardian | Service Started\n\nRest Assured, Service Started."
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, recipient, message)
        print("Service Started Email Sent!")
    except Exception as e:
        print(f"Failed to send startup email: {e}")

send_startup_email()

# Initialize Flask app
app = Flask(__name__)

# Load model
MODEL_PATH = "fall_detection_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
except Exception as e:
    raise ValueError(f"Error loading model: {str(e)}")

@app.route('/')
def home():
    return "<h1>Welcome to the Fall Detection API</h1>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        feature_order = ["accelerometer_x", "accelerometer_y", "accelerometer_z",
                         "gyroscope_x", "gyroscope_y", "gyroscope_z"]

        missing_features = [f for f in feature_order if f not in data]
        if missing_features:
            return jsonify({"error": f"Missing features: {missing_features}"}), 400

        features = np.array([data[feature] for feature in feature_order]).reshape(1, -1)
        prediction = model.predict(features)[0]

        # return jsonify({"prediction": str(prediction)})
        return prediction

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emg', methods=['POST'])
def send_emergency_mail():
    try:
        message = "Subject: Emergency | SecondGuardian \n\nFall Detected."
        
        # Open a new SMTP connection for each request
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, recipient, message)
        
        return jsonify({"success": "Emergency email sent successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
