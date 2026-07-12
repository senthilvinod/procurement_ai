import pandas as pd
from src.database.connection import engine


def calculate_quality_score():
    """
    Quality Score = (Accepted Quantity / Total Received) * 100
    """

    query = """
        SELECT
            supplier_id,
            product_id,
            quantity_received,
            quantity_rejected
        FROM purchase_order;
    """

    df = pd.read_sql(query, engine)

    # Replace nulls with 0 (important for safety)
    df["quantity_received"] = df["quantity_received"].fillna(0)
    df["quantity_rejected"] = df["quantity_rejected"].fillna(0)
    print("Step 2")
    # Avoid division errors
    df = df[df["quantity_received"] > 0]

    # Calculate accepted quantity
    df["quantity_accepted"] = (
        df["quantity_received"] - df["quantity_rejected"]
    )

    # Quality ratio
    df["quality_score"] = (
        df["quantity_accepted"] / df["quantity_received"]
    ) * 100

    # Safety clamp (in case of data issues)
    df["quality_score"] = df["quality_score"].clip(0, 100)
    print("Step 3")
    # Aggregate at supplier-product level
    result = df.groupby(
        ["supplier_id", "product_id"]
    ).agg(
        total_received=("quantity_received", "sum"),
        total_rejected=("quantity_rejected", "sum"),
        quality_score=("quality_score", "mean")
    ).reset_index()

    return result