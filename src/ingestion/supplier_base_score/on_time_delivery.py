import pandas as pd
from src.database.connection import engine


def calculate_on_time_delivery_score():
    """
    On-Time Delivery Score = (On-time deliveries / Total deliveries) * 100
    """

    query = """
        SELECT
            supplier_id,
            product_id,
            expected_delivery_date,
            actual_delivery_date
        FROM purchase_order
        WHERE actual_delivery_date IS NOT NULL;
    """

    df = pd.read_sql(query, engine)
    print("Step2")

    df["expected_delivery_date"] = pd.to_datetime(df["expected_delivery_date"])
    df["actual_delivery_date"] = pd.to_datetime(df["actual_delivery_date"])

    # Mark on-time deliveries
    df["on_time"] = (
        df["actual_delivery_date"] <= df["expected_delivery_date"]
    ).astype(int)
    print("Step 3")
    # Group by supplier-product
    result = df.groupby(["supplier_id", "product_id"]).agg(
        total_deliveries=("on_time", "count"),
        on_time_deliveries=("on_time", "sum")
    ).reset_index()
    print(result)
    # Score
    result["delivery_score"] = (
        result["on_time_deliveries"] / result["total_deliveries"]
    ) * 100

    return result