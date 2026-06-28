import pandas as pd
from src.database.connection import engine


def load_demand():

    query = """
    SELECT
        demand_date,
        quantity
    FROM vehicle_demand_history
    ORDER BY demand_date
    """

    return pd.read_sql(query, engine)