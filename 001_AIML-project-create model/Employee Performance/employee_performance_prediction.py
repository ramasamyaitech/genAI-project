import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load data
df = pd.read_csv("employee_performance.csv")

# Remove ID column
df = df.drop("EmployeeID", axis=1)

# Convert Department to numeric columns
df = pd.get_dummies(df, columns=["Department"])

# Features and Target
X = df.drop("PerformanceScore", axis=1)
y = df["PerformanceScore"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluation
print("MAE:", mean_absolute_error(y_test, predictions))
print("MSE:", mean_squared_error(y_test, predictions))
print("R2 Score:", r2_score(y_test, predictions))

# Save model
joblib.dump(model, "employee_model.pkl")

# Predict a new employee
new_employee = pd.DataFrame([{
    "Age": 29,
    "Experience": 5,
    "ProjectsCompleted": 7,
    "Department_Finance": 0,
    "Department_HR": 0,
    "Department_IT": 1,
    "Department_Sales": 0
}])

prediction = model.predict(new_employee)
print("Predicted Performance Score:", prediction)