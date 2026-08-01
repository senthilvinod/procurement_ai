import numpy as np 

PERFORMANCE_WEIGHT = 0.70
RISK_WEIGHT = 0.30


def calculate_supplier_score(
    performance_score: float,
    delivery_risk_score: float
):

    risk_reliability = (1 - delivery_risk_score)*100

    supplier_score = (
        PERFORMANCE_WEIGHT * performance_score
        +
        RISK_WEIGHT * risk_reliability
    )

    return float(np.round(supplier_score, 2))