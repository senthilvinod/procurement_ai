from src.ingestion.risk.tavily_client import TavilyRiskClient
from src.ingestion.risk.risk_analyzer import analyze_risk

import json

client = TavilyRiskClient()

company = "TSMC"

data = client.fetch_all_news(
    company=company,
    location="Taiwan"
)
print(data)

# Step 2:
# Send Tavily output to LLM

risk_result = analyze_risk(
    supplier_name=company,
    news_data=data
)


# Step 3:
# Print result

print(
    json.dumps(
        risk_result,
        indent=4
    )
)