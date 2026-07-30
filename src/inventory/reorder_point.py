import math


def calculate_reorder_point(
        avg_daily_demand,
        lead_time_days,
        safety_stock
):

    reorder_point = (
        (avg_daily_demand * lead_time_days)
        +
        safety_stock
    )

    return math.ceil(
        reorder_point
    )