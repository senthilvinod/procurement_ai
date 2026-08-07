from src.database.supplier_repository import get_active_suppliers
from src.ingestion.risk.tavily_client import TavilyRiskClient
from src.ingestion.risk.news_filter import filter_news
from src.ingestion.risk.risk_analyzer import analyze_risk
from src.ingestion.risk.risk_score import calculate_delivery_risk

from src.supplier.supplier_score import calculate_supplier_score
from src.ingestion.supplier_base_score.base_score import calculate_base_score

from src.database.supplier_score_repository import save_supplier_score


class SupplierAgent:

    def __init__(self):

        self.client = TavilyRiskClient()


    def run(self):

        print("Running Supplier Agent...")


        # --------------------------------------------------
        # Calculate supplier base performance score
        # --------------------------------------------------

        performance_df = calculate_base_score()


        # --------------------------------------------------
        # Fetch active suppliers
        # --------------------------------------------------

        suppliers = get_active_suppliers()


        supplier_results = []


        for supplier in suppliers:

            print("\n====================================")
            print(
                f"Evaluating Supplier: {supplier['supplier_name']}"
            )
            print(
                f"Country: {supplier['country']}"
            )
            print(
                f"State: {supplier['state']}"
            )


            # --------------------------------------------------
            # Fetch supplier news using Tavily
            # --------------------------------------------------

            data = self.client.fetch_all_news(
                company=supplier["supplier_name"],
                location=supplier["country"]
            )


            # --------------------------------------------------
            # Filter relevant news
            # --------------------------------------------------

            filtered_news = filter_news(data)



            # --------------------------------------------------
            # Analyze supplier risk using LLM
            # --------------------------------------------------

            risk_result = analyze_risk(
                supplier_name=supplier["supplier_name"],
                news_data=filtered_news
            )


            print("\n========== RISK ANALYSIS ==========")
            print(risk_result)



            # --------------------------------------------------
            # Calculate delivery risk score
            # --------------------------------------------------

            risk = calculate_delivery_risk(
                risk_result
            )


            print("\n========== DELIVERY RISK ==========")
            print(risk)



            # --------------------------------------------------
            # Get supplier performance score
            # --------------------------------------------------

            performance_score = performance_df.loc[
                performance_df["supplier_id"]
                ==
                supplier["supplier_id"],
                "base_score"
            ].iloc[0]


            print(
                "\n========== PERFORMANCE SCORE =========="
            )

            print(performance_score)



            # --------------------------------------------------
            # Calculate final supplier score
            # --------------------------------------------------

            supplier_score = calculate_supplier_score(
                performance_score,
                risk["delivery_risk_score"]
            )


            print(
                "\n========== FINAL SUPPLIER SCORE =========="
            )

            print(supplier_score)



            # --------------------------------------------------
            # Save supplier score
            # --------------------------------------------------

            save_supplier_score(
                supplier_id=supplier["supplier_id"],
                delivery_performance_score=performance_score,
                delivery_risk_score=risk["delivery_risk_score"],
                supplier_score=supplier_score
            )


            print(
                "Supplier score saved."
            )



            # --------------------------------------------------
            # Return result for orchestrator
            # --------------------------------------------------

            supplier_results.append(
                {
                    "supplier_id": supplier["supplier_id"],
                    "supplier_name": supplier["supplier_name"],
                    "delivery_performance_score": performance_score,
                    "delivery_risk_score": risk["delivery_risk_score"],
                    "supplier_score": supplier_score
                }
            )


        print("\nSupplier Agent Completed")


        return supplier_results



# --------------------------------------------------
# Orchestrator entry point
# --------------------------------------------------

def run_supplier_agent():

    agent = SupplierAgent()

    return agent.run()



# --------------------------------------------------
# Standalone execution
# --------------------------------------------------

if __name__ == "__main__":

    results = run_supplier_agent()


    print("\n========== SUPPLIER RESULTS ==========")

    for supplier in results:

        print(supplier)