from src.inventory.inventory_pipeline import (
    run_inventory_calculation
)


result = run_inventory_calculation()


for row in result:
    print(row)