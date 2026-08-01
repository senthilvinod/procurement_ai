from sqlalchemy import text
from src.database.connection import get_engine


def get_active_suppliers():

    query = text("""
        SELECT
            supplier_id,
            supplier_name,
            state,
            country
        FROM supplier
        WHERE supplier_status = 'Active'
        ORDER BY supplier_name
    """)

    with get_engine().connect() as conn:
        return conn.execute(query).mappings().all()