import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load dataset
df = pd.read_csv("employee_promotion.csv")

# Convert target column to numeric
df["Promoted"] = df["Promoted"].map({
    "Yes": 1,
    "No": 0
})

# Features and target
X = df.drop("Promoted", axis=1)
y = df["Promoted"]

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

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "employee_promotion_model.pkl")

# Predict a new employee
new_employee = pd.DataFrame([{
    "Age": 32,
    "Experience": 7,
    "TrainingHours": 40,
    "PerformanceRating": 5
}])

prediction = model.predict(new_employee)

if prediction[0] == 1:
    print("Employee is likely to be Promoted")
else:
    print("Employee is NOT likely to be Promoted")