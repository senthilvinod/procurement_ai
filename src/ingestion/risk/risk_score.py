def get_risk_level(score):

    if score < 0.20:
        return "Very Low"

    elif score < 0.40:
        return "Low"

    elif score < 0.60:
        return "Moderate"

    elif score < 0.80:
        return "High"

    return "Critical"


def calculate_delivery_risk(risk_result):

    logistics = risk_result["risk_breakdown"]["logistics_risk"]["score"]
    geopolitical = risk_result["risk_breakdown"]["geopolitical_risk"]["score"]
    financial = risk_result["risk_breakdown"]["financial_risk"]["score"]

    score = round(
        logistics * 0.60 +
        geopolitical * 0.30 +
        financial * 0.10,
        2
    )

    risk_result["delivery_risk_score"] = score
    risk_result["risk_level"] = get_risk_level(score)

    return risk_result