from sqlalchemy import text

from src.database.connection import engine


def save_product_demand_forecast(product_statistics):
    """
    Insert or update product demand forecast.

    If a product already exists in the table,
    only the demand-related fields are updated.

    Parameters
    ----------
    product_statistics : pd.DataFrame
    """

    query = text("""
        INSERT INTO product_demand_forecast
        (
            product_id,
            avg_daily_demand,
            total_monthly_demand,
            demand_std,
            forecast_start,
            forecast_end,
            updated_at
        )

        VALUES
        (
            :product_id,
            :avg_daily_demand,
            :total_monthly_demand,
            :demand_std,
            :forecast_start,
            :forecast_end,
            CURRENT_TIMESTAMP
        )

        ON CONFLICT (product_id)

        DO UPDATE SET

            avg_daily_demand = EXCLUDED.avg_daily_demand,
            total_monthly_demand = EXCLUDED.total_monthly_demand,
            demand_std = EXCLUDED.demand_std,
            forecast_start = EXCLUDED.forecast_start,
            forecast_end = EXCLUDED.forecast_end,
            updated_at = CURRENT_TIMESTAMP;
    """)

    records = product_statistics.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(query, records)

    print(f"{len(records)} product demand forecasts saved successfully.")