from src.agents.forecast_agent import run_forecast_agent
from src.ingestion.risk.risk_agent import run_supplier_agent
from src.agents.inventory_agent import run_inventory_agent
from src.agents.recommendation_agent import run_recommendation_agent



def run_procurement_workflow():

    print("=" * 100)
    print("STARTING PROCUREMENT AI WORKFLOW")
    print("=" * 100)


    # --------------------------------------------------
    # 1. Forecast Agent
    # --------------------------------------------------

    print("\n========== RUNNING FORECAST AGENT ==========")

    forecast_result = run_forecast_agent()

    print("Forecast Agent Completed")


    # --------------------------------------------------
    # 2. Supplier Agent
    # --------------------------------------------------

    print("\n========== RUNNING SUPPLIER AGENT ==========")

    supplier_result = run_supplier_agent()

    print("Supplier Agent Completed")


    # --------------------------------------------------
    # 3. Inventory Agent
    # --------------------------------------------------

    print("\n========== RUNNING INVENTORY AGENT ==========")

    inventory_result = run_inventory_agent()

    print("Inventory Agent Completed")


    # --------------------------------------------------
    # 4. Recommendation Agent
    # --------------------------------------------------

    print("\n========== RUNNING RECOMMENDATION AGENT ==========")

    recommendation_result = run_recommendation_agent()

    print("Recommendation Agent Completed")


    print("\n" + "=" * 100)
    print("PROCUREMENT AI WORKFLOW COMPLETED")
    print("=" * 100)



    return {

        "forecast": forecast_result,

        "supplier": supplier_result,

        "inventory": inventory_result,

        "recommendation": recommendation_result

    }



if __name__ == "__main__":

    results = run_procurement_workflow()


    print("\n========== FINAL RECOMMENDATIONS ==========")


    recommendations = results["recommendation"][
        "recommendations"
    ]


    for recommendation in recommendations:

        print(recommendation)

        print("-" * 100)