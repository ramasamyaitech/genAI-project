import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

df = pd.read_csv("customer_purchase.csv")

label = LabelEncoder()

df["DiscountUsed"] = label.fit_transform(df["DiscountUsed"])
df["Purchased"] = label.fit_transform(df["Purchased"])

X = df[["Age", "Income", "Visits", "DiscountUsed"]]

y = df["Purchased"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

new_customer = [[30, 45000, 5, 1]]

prediction = model.predict(new_customer)

if prediction[0] == 1:
    print("\nCustomer Will Purchase")
else:
    print("\nCustomer Will NOT Purchase")