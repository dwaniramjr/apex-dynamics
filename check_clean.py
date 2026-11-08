from src.data_loader import load_race_laps
from src.cleaning import clean_laps

raw = load_race_laps(2023, "Monza")
df = clean_laps(raw)

print(f"{len(raw)} raw laps -> {len(df)} clean laps")
print(df["Compound"].value_counts())
print(df.groupby("Driver").size().sort_values())