from src.recommendation.supplier_ranker import get_supplier_rankings
from src.recommendation.inventory_checker import check_inventory


def generate_recommendation(product_id):

    """
    Generates supplier recommendation
    based on supplier reliability and inventory availability.

    Decision Logic:

    1. If GREEN supplier has >10 days inventory:
       -> Inventory SAFE, no recommendation.

    2. If no safe supplier:
       -> Prefer GREEN/YELLOW suppliers.
       -> Select supplier with highest days_until_reorder.

    3. If only RED suppliers exist:
       -> Select RED supplier with highest days_until_reorder.

    4. If all suppliers are RED:
       -> Flag product for alternate supplier evaluation.
    """


    suppliers = get_supplier_rankings(product_id)


    # -----------------------------------------
    # No supplier available
    # -----------------------------------------

    if not suppliers:

        return {
            "product_id": product_id,
            "status": "NO_SUPPLIER",
            "message": "No suppliers available"
        }



    supplier_inventory = []


    # ==================================================
    # STEP 1:
    # Fetch inventory information
    # ==================================================

    for supplier in suppliers:


        inventory = check_inventory(
            product_id,
            supplier["supplier_id"]
        )


        days = inventory["days_until_reorder"]


        if days is None:
            continue


        supplier_data = {
            **supplier,
            **inventory
        }


        supplier_inventory.append(
            supplier_data
        )



    if not supplier_inventory:

        return {

            "product_id": product_id,

            "status": "NO_INVENTORY_DATA",

            "message":
                "Inventory information unavailable"

        }



    # ==================================================
    # STEP 2:
    # Check SAFE inventory
    # ==================================================

    for supplier in supplier_inventory:


        if (

            supplier["risk_band"].upper() == "GREEN"

            and

            supplier["days_until_reorder"] > 10

        ):


            return {

                "product_id":
                    product_id,

                "status":
                    "NO_ACTION",

                "inventory_status":
                    "SAFE",

                "safe_supplier":
                    supplier["supplier_id"],

                "supplier_band":
                    supplier["risk_band"],

                "supplier_score":
                    float(
                        supplier["supplier_score"]
                    ),

                "days_until_reorder":
                    float(
                        supplier["days_until_reorder"]
                    ),

                "message":
                    "Inventory levels are healthy. "
                    "No supplier recommendation required."

            }



    # ==================================================
    # STEP 3:
    # Check supplier risk level
    # ==================================================

    all_suppliers_red = all(

        supplier["risk_band"].upper() == "RED"

        for supplier in supplier_inventory

    )


    supplier_availability_warning = None

    supplier_risk_details = None



    if all_suppliers_red:


        supplier_availability_warning = (

            "All available suppliers for this product "
            "are classified as RED risk. "
            "Alternate suppliers should be considered."

        )


        supplier_risk_details = []


        for supplier in supplier_inventory:


            supplier_risk_details.append({

                "supplier_id":
                    supplier["supplier_id"],


                "supplier_score":
                    float(
                        supplier["supplier_score"]
                    ),


                "risk_band":
                    supplier["risk_band"],


                "risk_reason":
                    "High supplier risk due to low supplier score"

            })



    # ==================================================
    # STEP 4:
    # Select supplier
    # ==================================================

    preferred_suppliers = []

    red_suppliers = []



    for supplier in supplier_inventory:


        if supplier["risk_band"].upper() in [
            "GREEN",
            "YELLOW"
        ]:

            preferred_suppliers.append(
                supplier
            )

        else:

            red_suppliers.append(
                supplier
            )



    selected_supplier = None



    # Prefer GREEN/YELLOW suppliers

    if preferred_suppliers:


        selected_supplier = max(

            preferred_suppliers,

            key=lambda x:
                x["days_until_reorder"]

        )


    # Only RED suppliers available

    elif red_suppliers:


        selected_supplier = max(

            red_suppliers,

            key=lambda x:
                x["days_until_reorder"]

        )



    # ==================================================
    # STEP 5:
    # Generate recommendation
    # ==================================================

    if selected_supplier:


        risk_warning = None



        # Inventory shortage warning

        if selected_supplier["days_until_reorder"] < 0:


            risk_warning = (

                "Supplier does not have sufficient "
                "inventory coverage. "
                "High risk of stockout."

            )


        # Supplier risk warning

        elif (
            selected_supplier["risk_band"].upper()
            == "RED"
        ):


            risk_warning = (

                "Recommended supplier belongs "
                "to RED risk category."

            )



        inventory_status = selected_supplier[
            "inventory_status"
        ]


        if selected_supplier["days_until_reorder"] < 0:

            inventory_status = "HIGH_ALERT"



        return {


            "product_id":
                product_id,


            "recommended_supplier":
                selected_supplier["supplier_id"],


            "supplier_band":
                selected_supplier["risk_band"],


            "supplier_score":
                float(
                    selected_supplier["supplier_score"]
                ),


            "lead_time_days":
                selected_supplier["lead_time_days"],


            "days_until_reorder":
                float(
                    selected_supplier["days_until_reorder"]
                ),


            "inventory_status":
                inventory_status,


            "risk_warning":
                risk_warning,


            "supplier_availability_warning":
                supplier_availability_warning,


            "supplier_risk_details":
                supplier_risk_details

        }



    return {

        "product_id":
            product_id,

        "status":
            "NO_RECOMMENDATION",

        "message":
            "Unable to determine suitable supplier"

    }