from src.database.connection import engine

def save_forecast(df):

    df.to_sql(
        name="demand_forecast",
        con=engine,
        if_exists="append",
        index=False
    )