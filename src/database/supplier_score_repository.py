from sqlalchemy import text
from src.database.connection import engine


from sqlalchemy import text
from src.database.connection import engine


def save_supplier_score(
    supplier_id,
    delivery_performance_score,
    delivery_risk_score,
    supplier_score
):
    delivery_performance_score = float(delivery_performance_score)
    delivery_risk_score = float(delivery_risk_score)
    supplier_score = float(supplier_score)

    query = text("""
        INSERT INTO supplier_score (

            supplier_id,
            delivery_performance_score,
            delivery_risk_score,
            supplier_score

        )

        VALUES (

            :supplier_id,
            :delivery_performance_score,
            :delivery_risk_score,
            :supplier_score

        )

        ON CONFLICT (supplier_id)

        DO UPDATE SET

            delivery_performance_score = EXCLUDED.delivery_performance_score,
            delivery_risk_score = EXCLUDED.delivery_risk_score,
            supplier_score = EXCLUDED.supplier_score,
            updated_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "supplier_id": supplier_id,
                "delivery_performance_score": delivery_performance_score,
                "delivery_risk_score": delivery_risk_score,
                "supplier_score": supplier_score,
            }
        )