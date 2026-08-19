import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load dataset
df = pd.read_csv("bank_loan.csv")

# Remove unnecessary column
df = df.drop("CustomerID", axis=1)

# Convert target to numeric
df["Default"] = df["Default"].map({
    "Yes":1,
    "No":0
})

# Features and target
X = df.drop("Default", axis=1)
y = df["Default"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LogisticRegression()

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, predictions))
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("Classification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "loan_model.pkl")

# Predict new customer
new_customer = pd.DataFrame([{
    "Age": 34,
    "Income": 58000,
    "CreditScore": 730,
    "LoanAmount": 350000
}])

prediction = model.predict(new_customer)

if prediction[0] == 1:
    print("Customer will Default")
else:
    print("Customer will NOT Default")