import pandas as pd


def calculate_product_statistics(
    product_demand_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate product demand statistics from the daily product demand.

    Parameters
    ----------
    product_demand_df : pd.DataFrame

        Expected columns:
            - forecast_date
            - product_id
            - product_demand

    Returns
    -------
    pd.DataFrame

        Columns:
            - product_id
            - avg_daily_demand
            - total_monthly_demand
            - demand_std
            - forecast_start
            - forecast_end
    """

    forecast_start = product_demand_df["forecast_date"].min()
    forecast_end = product_demand_df["forecast_date"].max()

    product_statistics = (
        product_demand_df
        .groupby("product_id", as_index=False)
        .agg(
            avg_daily_demand=("product_demand", "mean"),
            total_monthly_demand=("product_demand", "sum"),
            demand_std=("product_demand", "std")
        )
    )

    # If only one forecast value exists, std() returns NaN
    product_statistics["demand_std"] = (
        product_statistics["demand_std"]
        .fillna(0)
    )

    # Round values for cleaner storage
    product_statistics["avg_daily_demand"] = (
        product_statistics["avg_daily_demand"]
        .round(2)
    )

    product_statistics["total_monthly_demand"] = (
        product_statistics["total_monthly_demand"]
        .round(2)
    )

    product_statistics["demand_std"] = (
        product_statistics["demand_std"]
        .round(2)
    )

    product_statistics["forecast_start"] = forecast_start
    product_statistics["forecast_end"] = forecast_end

    return product_statistics