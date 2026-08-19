import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load dataset
df = pd.read_csv("heart_disease.csv")

# Convert categorical columns
df["Gender"] = df["Gender"].map({
    "Male": 1,
    "Female": 0
})

df["Disease"] = df["Disease"].map({
    "Yes": 1,
    "No": 0
})

# Features and target
X = df.drop("Disease", axis=1)
y = df["Disease"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Logistic Regression model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "heart_disease_model.pkl")

# Predict a new patient
new_patient = pd.DataFrame([{
    "Age": 50,
    "Gender": 1,
    "Cholesterol": 240,
    "BloodPressure": 145,
    "HeartRate": 90
}])

prediction = model.predict(new_patient)

if prediction[0] == 1:
    print("Heart Disease Detected")
else:
    print("No Heart Disease")