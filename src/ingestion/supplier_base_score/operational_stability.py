import pandas as pd
import numpy as np
from src.database.connection import engine


def calculate_operational_stability_score():

    query = """
        SELECT
            po.supplier_id,
            po.product_id,
            po.order_date,
            po.expected_delivery_date,
            po.actual_delivery_date,
            po.po_status,
            sp.lead_time_days AS proposed_lead_time
        FROM purchase_order po
        LEFT JOIN supplier_product sp
            ON po.supplier_id = sp.supplier_id
            AND po.product_id = sp.product_id;
    """

    df = pd.read_sql(query, engine)

    # -----------------------------
    # Date conversion
    # -----------------------------
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["actual_delivery_date"] = pd.to_datetime(df["actual_delivery_date"])

    # -----------------------------
    # Actual lead time
    # -----------------------------
    df["actual_lead_time"] = (
        df["actual_delivery_date"] - df["order_date"]
    ).dt.days

    # -----------------------------
    # Delivery deviation vs promised lead time
    # -----------------------------
    df["lead_time_deviation"] = (
        df["actual_lead_time"] - df["proposed_lead_time"]
    ).abs()

    # -----------------------------
    # Delivery Stability (AAD of deviation)
    # -----------------------------
    stability_df = df.groupby(
        ["supplier_id", "product_id"]
    )["lead_time_deviation"].mean().reset_index()

    stability_df.columns = [
        "supplier_id",
        "product_id",
        "aad_deviation"
    ]

    max_aad = stability_df["aad_deviation"].max() + 1

    stability_df["delivery_stability"] = 100 * (
        1 - (stability_df["aad_deviation"] / max_aad)
    )

    # -----------------------------
    # Cancellation Reliability
    # -----------------------------
    df["po_status"] = df["po_status"].str.lower()

    df["supplier_fault"] = df["po_status"].isin([
        "cancelled by supplier"
    ]).astype(int)

    cancel_df = df.groupby(
        ["supplier_id", "product_id"]
    ).agg(
        total_orders=("po_status", "count"),
        supplier_fault_cancellations=("supplier_fault", "sum")
    ).reset_index()

    cancel_df["cancellation_reliability"] = (
        (cancel_df["total_orders"] - cancel_df["supplier_fault_cancellations"])
        / cancel_df["total_orders"]
    ) * 100

    # -----------------------------
    # Merge both components
    # -----------------------------
    stability = stability_df.merge(
        cancel_df,
        on=["supplier_id", "product_id"]
    )

    # -----------------------------
    # Final Operational Stability Score
    # -----------------------------
    stability["operational_stability_score"] = (
        0.4 * stability["delivery_stability"] +
        0.6 * stability["cancellation_reliability"]
    )

    stability["operational_stability_score"] = stability[
        "operational_stability_score"
    ].clip(0, 100)

    return stability[
        [
            "supplier_id",
            "product_id",
            "delivery_stability",
            "cancellation_reliability",
            "operational_stability_score"
        ]
    ]