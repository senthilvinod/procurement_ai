import math


def calculate_days_until_reorder(
        current_stock,
        reorder_point,
        avg_daily_demand
):

    if avg_daily_demand <= 0:
        return None


    days = (
        current_stock - reorder_point
    ) / avg_daily_demand


    return math.ceil(days)