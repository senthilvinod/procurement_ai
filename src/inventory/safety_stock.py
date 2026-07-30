import numpy as np


def calculate_safety_stock(
        avg_daily_demand,
        demand_std,
        lead_time_days,
        lead_time_std,
        z_score=1.65
):

    variance = (
        (lead_time_days * (demand_std ** 2))
        +
        ((avg_daily_demand ** 2) * (lead_time_std ** 2))
    )


    safety_stock = (
        z_score *
        np.sqrt(variance)
    )


    return int(
        np.ceil(safety_stock)
    )