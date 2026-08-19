import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("car_price.csv")

brand_encoder = LabelEncoder()
fuel_encoder = LabelEncoder()
transmission_encoder = LabelEncoder()

df["Brand"] = brand_encoder.fit_transform(df["Brand"])
df["Fuel"] = fuel_encoder.fit_transform(df["Fuel"])
df["Transmission"] = transmission_encoder.fit_transform(df["Transmission"])

X = df[["Brand", "Year", "Kilometers", "Fuel", "Transmission"]]
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

new_car = [[
    brand_encoder.transform(["Hyundai"])[0],
    2023,
    12000,
    fuel_encoder.transform(["Petrol"])[0],
    transmission_encoder.transform(["Automatic"])[0]
]]

predicted_price = model.predict(new_car)

print("Predicted Price:", predicted_price[0])