
from src.recommendation.recommendation_engine import generate_recommendation
result = generate_recommendation("PRD00001")
print(result)

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