'''
from src.recommendation.recommendation_engine import generate_recommendation
result = generate_recommendation("PRD00001")
print(result)
'''

'''
from src.recommendation.supplier_ranker import get_supplier_rankings
suppliers = get_supplier_rankings("PRD00005")
for supplier in suppliers:
    print(supplier)
'''
'''
from src.recommendation.inventory_checker import check_inventory
# Test product and supplier combination
result = check_inventory(
    "PRD00006",
    "SUP00002")
print(result)
'''
'''
from src.recommendation.recommendation_engine import generate_recommendation
from src.recommendation.llm_explainer import generate_explanation


def main():

    # Change this to any product in your database
    product_id = "PRD00028"

    # Generate recommendation
    recommendation = generate_recommendation(product_id)

    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print(recommendation)

    # Generate LLM explanation
    print("\nGenerating LLM explanation...\n")

    explanation = generate_explanation(recommendation)

    print("=" * 80)
    print("LLM EXPLANATION")
    print("=" * 80)
    print(explanation)


if __name__ == "__main__":
    main()
    '''

from src.agents.recommendation_agent import run_recommendation_agent


result = run_recommendation_agent()

print("=" * 100)
print("RECOMMENDATIONS")
print("=" * 100)

for recommendation in result["recommendations"]:

    print()

    print(recommendation)

    print("-" * 100)


print("\n")
print("=" * 100)
print("PRODUCTS WITHOUT SUPPLIERS")
print("=" * 100)

for product in result["products_without_suppliers"]:

    print(product)