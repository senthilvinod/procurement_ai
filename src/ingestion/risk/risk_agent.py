from src.database.supplier_repository import get_active_suppliers
from src.ingestion.risk.tavily_client import TavilyRiskClient
from src.ingestion.risk.news_filter import filter_news
from src.ingestion.risk.risk_analyzer import analyze_risk
from src.ingestion.risk.risk_score import calculate_delivery_risk
from src.supplier.supplier_score import calculate_supplier_score
from src.ingestion.supplier_base_score.base_score import calculate_base_score
from src.database.supplier_score_repository import save_supplier_score
import json

client = TavilyRiskClient()

# Step 6: Calculate the delivery performance performace 
performance_df = calculate_base_score()

suppliers = get_active_suppliers()

for supplier in suppliers:
    print(supplier["supplier_name"])
    print(supplier["country"])
    print(supplier["state"])

    data = client.fetch_all_news(company=supplier["supplier_name"],location=supplier["country"])
    print(data)

    filtered_news = filter_news(data)

    # Step 2:
    # Send Tavily output to LLM
    risk_result = analyze_risk(supplier_name=supplier["supplier_name"],news_data=filtered_news)

    # Step 3:
    # Print result
    print(json.dumps(risk_result,indent=4))

    # Step 4: Score the delivery risk
    risk = calculate_delivery_risk(risk_result)
    print("===RISK===")
    print(risk)

    performance_score = performance_df.loc[
        performance_df["supplier_id"] == supplier["supplier_id"],
        "base_score"
    ].iloc[0]
    print("\n========== FINAL BASE SCORE ==========\n")
    print(performance_score)

    # Step 5: Score the supplier based on performance and delivery risk
    supplier_score = calculate_supplier_score(
        performance_score,
        risk["delivery_risk_score"]
    )

    save_supplier_score(
        supplier_id=supplier["supplier_id"],
        delivery_performance_score=performance_score,
        delivery_risk_score=risk["delivery_risk_score"],
        supplier_score=supplier_score
    )