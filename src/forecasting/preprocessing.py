import pandas as pd
def preprocess(df):

    df["demand_date"] = pd.to_datetime(
        df["demand_date"]
    )

    df = (
        df
        .groupby("demand_date")
        ["quantity"]
        .sum()
        .reset_index()
    )

    return df