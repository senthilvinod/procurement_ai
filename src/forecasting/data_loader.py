import pandas as pd
from src.database.connection import engine


def load_demand():

    query = """
    SELECT
        demand_date,
        shipped_quantity
    FROM demand
    ORDER BY demand_date
    """

    return pd.read_sql(query, engine)