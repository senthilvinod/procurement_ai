from sqlalchemy import text
from src.database.connection import engine


# Supplier reliability priority
BAND_PRIORITY = {
    "GREEN": 1,
    "YELLOW": 2,
    "RED": 3
}


def get_supplier_rankings(product_id):
    """
    Returns ranked suppliers for a given product.

    Ranking logic:
    1. Risk Band (GREEN > YELLOW > RED)
    2. Supplier Score (Higher is better)
    3. Lead Time (Lower is better)

    Parameters:
        product_id (str)

    Returns:
        List of dictionaries containing supplier ranking
    """


    query = """
    SELECT
        sp.product_id,
        sp.supplier_id,
        sp.lead_time_days,
        s.supplier_score,
        s.risk_band

    FROM supplier_product sp

    JOIN supplier_score s
    ON sp.supplier_id = s.supplier_id

    WHERE sp.product_id = :product_id
    """


    try:

        with engine.connect() as connection:

            result = connection.execute(
                text(query),
                {
                    "product_id": product_id
                }
            )


            rows = result.fetchall()


            if not rows:
                return []


            # Convert SQL rows into dictionaries
            suppliers = []

            for row in rows:

                suppliers.append(
                    {
                        "product_id": row.product_id,
                        "supplier_id": row.supplier_id,
                        "lead_time_days": row.lead_time_days,
                        "supplier_score": row.supplier_score,
                        "risk_band": row.risk_band
                    }
                )


        # Add band priority

        for supplier in suppliers:

            supplier["band_priority"] = BAND_PRIORITY.get(
                supplier["risk_band"].upper(),
                4
            )


        # Sort suppliers

        ranked_suppliers = sorted(
            suppliers,
            key=lambda x: (
                x["band_priority"],       # GREEN first     # Higher score first
                x["lead_time_days"]            # Lower lead time first
            )
        )


        # Remove internal ranking field

        for supplier in ranked_suppliers:

            supplier.pop(
                "band_priority",
                None
            )


        return ranked_suppliers



    except Exception as e:

        print(
            f"Error while ranking suppliers: {e}"
        )

        return []