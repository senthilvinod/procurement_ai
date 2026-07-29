import pandas as pd


def explode_bom(
    forecast_df: pd.DataFrame,
    bom_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Explode the vehicle demand forecast into daily product demand
    using the Bill of Materials (BOM).

    Parameters
    ----------
    forecast_df : pd.DataFrame
        Expected columns:
            - forecast_date
            - predicted_demand

    bom_df : pd.DataFrame
        Expected columns:
            - product_id
            - quantity_required

    Returns
    -------
    pd.DataFrame
        Columns:
            - forecast_date
            - product_id
            - product_demand
    """

    # Merge forecast with BOM
    product_demand = forecast_df.merge(
        bom_df,
        how="cross"
    )

    # Calculate product demand
    product_demand["product_demand"] = (
        product_demand["predicted_demand"]
        * product_demand["quantity_required"]
    )

    # Aggregate demand for products used in multiple car models
    product_demand = (
        product_demand
        .groupby(
            ["forecast_date", "product_id"],
            as_index=False
        )
        .agg(
            product_demand=("product_demand", "sum")
        )
        .sort_values(
            ["forecast_date", "product_id"]
        )
        .reset_index(drop=True)
    )

    return product_demand