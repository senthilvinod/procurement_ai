from .cost_competitiveness import calculate_cost_score
from .on_time_delivery import calculate_on_time_delivery_score
from .quality_score import calculate_quality_score
from .operational_stability import calculate_operational_stability_score



def calculate_base_score():

    # -----------------------------
    # Step 1: Load all scores
    # -----------------------------
    cost_df = calculate_cost_score()
    delivery_df = calculate_on_time_delivery_score()
    quality_df = calculate_quality_score()
    stability_df = calculate_operational_stability_score()

    print("\nAll modules loaded successfully")

    # -----------------------------
    # Step 2: Create master frame (IMPORTANT)
    # -----------------------------
    base = cost_df[["supplier_id", "product_id"]].drop_duplicates()

    # -----------------------------
    # Step 3: Merge all metrics
    # -----------------------------
    df = base \
        .merge(cost_df, on=["supplier_id", "product_id"], how="left") \
        .merge(delivery_df, on=["supplier_id", "product_id"], how="left") \
        .merge(quality_df, on=["supplier_id", "product_id"], how="left") \
        .merge(stability_df, on=["supplier_id", "product_id"], how="left")

    # -----------------------------
    # Step 4: Fill missing values
    # -----------------------------
    df = df.fillna(0)

    # -----------------------------
    # Step 5: Apply weights
    # -----------------------------
    df["base_score"] = (
        0.10 * df["cost_score"] +
        0.30 * df["delivery_score"] +
        0.25 * df["quality_score"] +
        0.35 * df["operational_stability_score"]
    )

    # -----------------------------
    # Step 6: Normalize
    # -----------------------------
    df["base_score"] = df["base_score"].clip(0, 100)

    return df

result = calculate_base_score()

print("\n========== FINAL BASE SCORE ==========\n")
print(result.sort_values("base_score", ascending=False).reset_index(drop=True))
