import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load dataset
df = pd.read_csv("student_placement.csv")

# Convert target column
df["Placed"] = df["Placed"].map({
    "Yes": 1,
    "No": 0
})

# One-Hot Encode Communication
df = pd.get_dummies(
    df,
    columns=["Communication"],
    dtype=int
)

# Features and target
X = df.drop("Placed", axis=1)
y = df["Placed"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
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
joblib.dump(model, "student_placement_model.pkl")

# Predict new student
new_student = pd.DataFrame([{
    "CGPA": 8.2,
    "Internships": 3,
    "Projects": 5,
    "Communication_Average": 0,
    "Communication_Excellent": 0,
    "Communication_Good": 1,
    "Communication_Poor": 0
}])

prediction = model.predict(new_student)

if prediction[0] == 1:
    print("Student Will Be Placed")
else:
    print("Student Will NOT Be Placed")