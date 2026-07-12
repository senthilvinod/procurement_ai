import pandas as pd
from src.database.connection import engine


def calculate_cost_score():
    """
    Calculates the cost competitiveness score for each supplier-product combination.
    Formula:
        Cost Score = (Lowest Price / Supplier Price) * 100
    """

    query = """
        SELECT
            supplier_id,
            product_id,
            unit_price
        FROM supplier_product;
    """

    df = pd.read_sql(query, engine)
    print("Step 2")
    print(df)
    # Find the lowest price for each product
    df["lowest_price"] = (
        df.groupby("product_id")["unit_price"]
        .transform("min")
    )
    print(df)
    # Calculate Cost Competitiveness Score
    df["cost_score"] = (
        df["lowest_price"] / df["unit_price"]
    ) * 100
    print(df)
    return df[
        [
            "supplier_id",
            "product_id",
            "unit_price",
            "lowest_price",
            "cost_score"
        ]
    ]