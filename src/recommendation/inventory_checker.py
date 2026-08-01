from sqlalchemy import text
from src.database.connection import engine



def classify_inventory_status(days_until_reorder):

    if days_until_reorder < 0:
        return "HIGH_ALERT"

    elif days_until_reorder <= 2:
        return "RED"

    elif days_until_reorder <= 5:
        return "ORANGE"

    elif days_until_reorder <= 10:
        return "YELLOW"

    else:
        return "GREEN"



def check_inventory(product_id, supplier_id):

    query = """
    SELECT
        product_id,
        supplier_id,
        days_until_reorder

    FROM inventory_analysis

    WHERE product_id = :product_id
    AND supplier_id = :supplier_id
    """


    try:

        with engine.connect() as connection:

            result = connection.execute(
                text(query),
                {
                    "product_id": product_id,
                    "supplier_id": supplier_id
                }
            )

            row = result.fetchone()


            if not row:

                return {
                    "product_id": product_id,
                    "supplier_id": supplier_id,
                    "days_until_reorder": None,
                    "inventory_status": "NO_DATA"
                }


            days = row[2]


            return {

                "product_id": row[0],

                "supplier_id": row[1],

                "days_until_reorder": days,

                "inventory_status":
                    classify_inventory_status(days)

            }


    except Exception as e:

        print(
            f"Inventory checker error: {e}"
        )

        return None