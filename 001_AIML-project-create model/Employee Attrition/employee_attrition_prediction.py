import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# ---------------------------------------
# Load Dataset
# ---------------------------------------
df = pd.read_csv("employee_attrition.csv")

# ---------------------------------------
# Encode Categorical Columns
# ---------------------------------------
overtime_encoder = LabelEncoder()
attrition_encoder = LabelEncoder()

df["Overtime"] = overtime_encoder.fit_transform(df["Overtime"])
df["Attrition"] = attrition_encoder.fit_transform(df["Attrition"])

# ---------------------------------------
# Features and Target
# ---------------------------------------
X = df[[
    "Age",
    "Salary",
    "Experience",
    "Overtime",
    "DistanceFromHome"
]]

y = df["Attrition"]

# ---------------------------------------
# Split Dataset
# ---------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------------------------------
# Train Model
# ---------------------------------------
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# ---------------------------------------
# Predict
# ---------------------------------------
y_pred = model.predict(X_test)

# ---------------------------------------
# Evaluation
# ---------------------------------------
print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ---------------------------------------
# Predict New Employee
# ---------------------------------------
new_employee = [[
    30,      # Age
    50000,   # Salary
    5,       # Experience
    overtime_encoder.transform(["Yes"])[0],
    15       # DistanceFromHome
]]

prediction = model.predict(new_employee)

if prediction[0] == 1:
    print("\nEmployee Will Leave")
else:
    print("\nEmployee Will Stay")