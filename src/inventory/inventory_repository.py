from datetime import datetime

from sqlalchemy import text

from src.database.connection import engine


def save_inventory_analysis(inventory_data):

    query = """

    INSERT INTO inventory_analysis
    (
        supplier_product_id,
        supplier_id,
        product_id,
        safety_stock,
        reorder_point,
        days_until_reorder,
        updated_at
    )

    VALUES
    (
        :supplier_product_id,
        :supplier_id,
        :product_id,
        :safety_stock,
        :reorder_point,
        :days_until_reorder,
        :updated_at
    )


    ON CONFLICT (supplier_id, product_id)

    DO UPDATE SET

        supplier_product_id = EXCLUDED.supplier_product_id,

        safety_stock = EXCLUDED.safety_stock,

        reorder_point = EXCLUDED.reorder_point,

        days_until_reorder = EXCLUDED.days_until_reorder,

        updated_at = EXCLUDED.updated_at;

    """


    with engine.begin() as conn:

        for row in inventory_data:

            conn.execute(
                text(query),
                {

                    "supplier_product_id":
                        row["supplier_product_id"],

                    "supplier_id":
                        row["supplier_id"],

                    "product_id":
                        row["product_id"],

                    "safety_stock":
                        row["safety_stock"],

                    "reorder_point":
                        row["reorder_point"],

                    "days_until_reorder":
                        row["days_until_reorder"],

                    "updated_at":
                        datetime.now()
                }
            )


    print("Inventory analysis saved successfully")