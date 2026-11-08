import pandas as pd

def clean_laps(laps: pd.DataFrame) -> pd.DataFrame:
    df = laps.copy()
    df = df.dropna(subset=["LapTimeSec", "Compound", "TyreLife"])
    df = df[df["LapNumber"] > 1]                                  # standing start
    df = df[df["PitInTime"].isna() & df["PitOutTime"].isna()]     # in/out laps
    df = df[df["TrackStatus"] == "1"]                             # green flag only
    df = df[df["IsAccurate"] == True]
    df = df[df["Compound"].isin(["SOFT", "MEDIUM", "HARD"])]

    stint_median = df.groupby(["Driver", "Stint"])["LapTimeSec"].transform("median")
    df = df[df["LapTimeSec"] < stint_median * 1.05]               # slow outliers
    return df.reset_index(drop=True)