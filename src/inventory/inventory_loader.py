import pandas as pd

from src.database.connection import engine



def load_supplier_product():

    query = """

    SELECT

        supplier_product_id,

        supplier_id,

        product_id,

        lead_time_days

    FROM supplier_product

    """

    with engine.connect() as conn:

        df = pd.read_sql(
            query,
            conn
        )

    return df



def load_lead_time_statistics():

    query = """

    SELECT

        supplier_id,

        product_id,

        AVG(
            actual_delivery_date - order_date
        ) AS avg_actual_lead_time,

        STDDEV(
            actual_delivery_date - order_date
        ) AS lead_time_std


    FROM purchase_order


    WHERE

        po_status = 'Delivered'

        AND actual_delivery_date IS NOT NULL


    GROUP BY

        supplier_id,

        product_id

    """

    with engine.connect() as conn:

        df = pd.read_sql(
            query,
            conn
        )


    # If only one delivery exists
    # standard deviation becomes NULL

    df["lead_time_std"] = (
        df["lead_time_std"]
        .fillna(0)
    )


    return df



def load_inventory():

    query = """

    SELECT

        product_id,

        current_stock

    FROM inventory

    """


    with engine.connect() as conn:

        df = pd.read_sql(
            query,
            conn
        )

    return df



def load_product_demand():

    query = """

    SELECT

        product_id,

        avg_daily_demand,

        demand_std

    FROM product_demand_forecast

    """


    with engine.connect() as conn:

        df = pd.read_sql(
            query,
            conn
        )

    return df



def load_inventory_data():


    supplier_product = (
        load_supplier_product()
    )


    lead_time_stats = (
        load_lead_time_statistics()
    )


    inventory = (
        load_inventory()
    )


    demand = (
        load_product_demand()
    )


    # Merge supplier lead time variability

    data = supplier_product.merge(

        lead_time_stats,

        on=[
            "supplier_id",
            "product_id"
        ],

        how="left"

    )


    # Merge current stock

    data = data.merge(

        inventory,

        on="product_id",

        how="left"

    )


    # Merge demand information

    data = data.merge(

        demand,

        on="product_id",

        how="left"

    )


    # Missing lead time std = 0

    data["lead_time_std"] = (
        data["lead_time_std"]
        .fillna(0)
    )


    return data