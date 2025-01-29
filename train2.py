import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
DATA_PATH = "sensor_data.csv"  # Ensure this file exists in the correct location

try:
    data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Dataset file not found at {DATA_PATH}")

# Define features and labels
FEATURES = ["accelerometer_x", "accelerometer_y", "accelerometer_z", 
            "gyroscope_x", "gyroscope_y", "gyroscope_z"]

LABEL = "label"

# Ensure dataset contains required columns
missing_cols = [col for col in FEATURES + [LABEL] if col not in data.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

X = data[FEATURES]
y = data[LABEL]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

# Save the model
MODEL_PATH = "fall_detection_model.pkl"
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
