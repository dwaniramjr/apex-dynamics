import fastf1
import pandas as pd

fastf1.Cache.enable_cache("data/cache")

def load_race_laps(year: int, gp: str) -> pd.DataFrame:
    session = fastf1.get_session(year, gp, "R")
    session.load(telemetry=False, weather=True, messages=False)
    laps = session.laps.copy()

    laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()
    cols = ["Driver", "LapNumber", "LapTimeSec", "Compound", "TyreLife",
            "Stint", "PitInTime", "PitOutTime", "TrackStatus", "IsAccurate"]
    return laps[cols]

if __name__ == "__main__":
    df = load_race_laps(2023, "Monza")
    print(df.head(10))
    print(df.shape)
    print(df["Compound"].value_counts())