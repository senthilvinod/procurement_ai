from src.inventory.inventory_pipeline import (
    run_inventory_calculation
)


class InventoryAgent:


    def run(self):

        print("Running Inventory Agent...")


        inventory_result = (
            run_inventory_calculation()
        )


        print("\nInventory Calculation Completed")

        for row in inventory_result:
            print(row)


        return inventory_result

def run_inventory_agent():

    agent = InventoryAgent()

    result = agent.run()

    return result

if __name__ == "__main__":

    InventoryAgent().run()