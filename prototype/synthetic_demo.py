import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
print("=================================")
print("        APEX DYNAMICS")
print("=================================")
print("F1 AI Race Engineering Platform")
print()

# --------------------------------
# RACE TELEMETRY DATA
# --------------------------------
# --------------------------------
# SYNTHETIC F1 TELEMETRY DATA
# --------------------------------

np.random.seed(42)

laps = np.arange(1, 101)

fuel_load = 110 - (laps * 0.9)

track_temp = 42 + np.random.normal(0, 1.5, 100)

tyre_age = laps % 25

lap_time = (
    88
    + (tyre_age * 0.12)
    + (track_temp * 0.03)
    + np.random.normal(0, 0.3, 100)
)

tyre_wear = (
    0.01
    + (tyre_age ** 1.5) * 0.004
    + np.random.normal(0, 0.005, 100)
)

data = {
    "lap": laps,
    "lap_time": lap_time,
    "tyre_age": tyre_age,
    "fuel_load": fuel_load,
    "track_temp": track_temp,
    "tyre_wear": tyre_wear
}

df = pd.DataFrame(data)



print("Race data loaded successfully!")
print()
print(df)

# --------------------------------
# MACHINE LEARNING
# --------------------------------

features = [
    "tyre_age",
    "fuel_load",
    "lap_time",
    "track_temp"
]

X = df[features]
y = df["tyre_wear"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


print()
print("=================================")
print("       MODEL ACCURACY")
print("=================================")

print(f"Mean Absolute Error: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# --------------------------------
# PREDICTION
# --------------------------------

new_lap = pd.DataFrame({
    "tyre_age": [12],
    "fuel_load": [78],
    "lap_time": [93.0],
    "track_temp": [47]
})

prediction = model.predict(new_lap)

print()
print("=================================")
print("       AI TYRE PREDICTION")
print("=================================")

print(f"Predicted tyre wear: {prediction[0]:.3f}")

# --------------------------------
# MODEL INFORMATION
# --------------------------------

print()
print("Model features:")

for feature, coefficient in zip(features, model.coef_):
    print(f"{feature}: {coefficient:.4f}")

print()
print("Apex Dynamics ML model is working!")

# --------------------------------
# PIT-STOP STRATEGY ENGINE
# --------------------------------

def estimate_race_time(pit_lap):

    total_time = 0
    tyre_age = 0

    for lap in range(1, 101):

        tyre_age += 1

        base_lap_time = df.loc[lap - 1, "lap_time"]

        degradation_penalty = (tyre_age ** 1.5) * 0.04

        if lap == pit_lap:

            total_time += base_lap_time + 22

            tyre_age = 0

        else:

            total_time += (
                base_lap_time
                + degradation_penalty
            )

    return total_time


# --------------------------------
# TEST DIFFERENT PIT-STOP LAPS
# --------------------------------

strategy_results = {}

for pit_lap in range(15, 51):

    race_time = estimate_race_time(pit_lap)

    strategy_results[pit_lap] = race_time


# --------------------------------
# FIND OPTIMAL STRATEGY
# --------------------------------

best_pit_lap = min(
    strategy_results,
    key=strategy_results.get
)

best_race_time = strategy_results[best_pit_lap]


# --------------------------------
# STRATEGY RESULTS
# --------------------------------

print("\n=================================")
print("      APEX DYNAMICS STRATEGY")
print("=================================")

print(f"Optimal pit-stop lap: {best_pit_lap}")
print(f"Predicted race time: {best_race_time:.2f} seconds")

print("\nStrategy comparison:")

for lap, time in strategy_results.items():

    if lap % 5 == 0:

        print(
            f"Pit lap {lap}: "
            f"{time:.2f} seconds"
        )