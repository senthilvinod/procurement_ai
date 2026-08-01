from sqlalchemy import text

from src.database.connection import get_engine
from src.recommendation.recommendation_engine import generate_recommendation
from src.recommendation.llm_explainer import generate_explanation


def get_all_products():
    """
    Fetch all product IDs from the database.
    """

    engine = get_engine()

    query = text("""
        SELECT product_id
        FROM product
        ORDER BY product_id
    """)

    with engine.connect() as connection:

        result = connection.execute(query)

        products = result.mappings().all()

    return products


def run_recommendation_agent():
    """
    Runs the recommendation process for all products.

    Returns:
    {
        "recommendations": [...],
        "products_without_suppliers": [...]
    }
    """

    products = get_all_products()

    recommendations = []
    products_without_suppliers = []

    for product in products:

        product_id = product["product_id"]

        recommendation = generate_recommendation(product_id)

        # -----------------------------------------
        # Products with no suppliers
        # -----------------------------------------

        if recommendation.get("status") == "NO_SUPPLIER":

            products_without_suppliers.append({
                "product_id": product_id,
                "message": recommendation["message"]
            })

            continue

        # -----------------------------------------
        # Generate LLM explanation
        # -----------------------------------------

        explanation = generate_explanation(recommendation)

        recommendation["llm_explanation"] = explanation

        recommendations.append(recommendation)

    return {
        "recommendations": recommendations,
        "products_without_suppliers": products_without_suppliers
    }


if __name__ == "__main__":

    results = run_recommendation_agent()

    print("=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)

    for recommendation in results["recommendations"]:

        print(recommendation)
        print("-" * 100)

    print("\n")

    print("=" * 100)
    print("PRODUCTS WITHOUT SUPPLIERS")
    print("=" * 100)

    for product in results["products_without_suppliers"]:

        print(product)