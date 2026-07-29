import pandas as pd
from sqlalchemy import text

from src.database.connection import engine


def load_bom() -> pd.DataFrame:
    """
    Load the Bill of Materials (BOM) from the database.

    Returns
    -------
    pd.DataFrame
        Columns:
        - product_id
        - quantity_required
    """

    query = text("""
        SELECT
            product_id,
            quantity_required
        FROM bill_of_material
    """)

    with engine.connect() as conn:
        bom_df = pd.read_sql(query, conn)

    return bom_df