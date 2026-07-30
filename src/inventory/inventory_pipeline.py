from src.inventory.inventory_loader import load_inventory_data

from src.inventory.safety_stock import (
    calculate_safety_stock
)

from src.inventory.reorder_point import (
    calculate_reorder_point
)

from src.inventory.days_until_reorder import (
    calculate_days_until_reorder
)

from src.inventory.inventory_repository import (
    save_inventory_analysis
)


def run_inventory_calculation():


    # ---------------------------------------
    # Load inventory input data
    # ---------------------------------------

    inventory_df = load_inventory_data()


    results = []


    # ---------------------------------------
    # Calculate for every supplier-product
    # ---------------------------------------

    for _, row in inventory_df.iterrows():


        # Safety Stock

        safety_stock = calculate_safety_stock(

            avg_daily_demand=row["avg_daily_demand"],

            demand_std=row["demand_std"],

            lead_time_days=row["lead_time_days"],

            lead_time_std=row["lead_time_std"]

        )


        # Reorder Point

        reorder_point = calculate_reorder_point(

            avg_daily_demand=row["avg_daily_demand"],

            lead_time_days=row["lead_time_days"],

            safety_stock=safety_stock

        )


        # Days Until Reorder

        days_until_reorder = calculate_days_until_reorder(

            current_stock=row["current_stock"],

            reorder_point=reorder_point,

            avg_daily_demand=row["avg_daily_demand"]

        )


        results.append({

            "supplier_product_id":
                row["supplier_product_id"],


            "supplier_id":
                row["supplier_id"],


            "product_id":
                row["product_id"],


            "safety_stock":
                safety_stock,


            "reorder_point":
                reorder_point,


            "days_until_reorder":
                days_until_reorder

        })


    save_inventory_analysis(results)

    return results