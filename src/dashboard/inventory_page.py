import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================================
# SAMPLE DATA
# Replace later with database query
# ==========================================================

data = [
    {
        "Product_ID": "PRD00001",
        "Product": "Brake Pad",
        "Days Remaining": 2,
        "Current Stock": 120,
        "Safety Stock": 40,
        "ROP": 85,
        "Recommended Supplier": "Bosch",
        "Lead Time": 5,
        "Status": "Immediate",
        "Action": "Order Today"
    },
    {
        "Product_ID": "PRD00002",
        "Product": "Wheel Rim",
        "Days Remaining": 4,
        "Current Stock": 180,
        "Safety Stock": 50,
        "ROP": 95,
        "Recommended Supplier": "Valeo",
        "Lead Time": 6,
        "Status": "Order Soon",
        "Action": "Order in 2 Days"
    },
    {
        "Product_ID": "PRD00003",
        "Product": "Tyre",
        "Days Remaining": 8,
        "Current Stock": 310,
        "Safety Stock": 70,
        "ROP": 110,
        "Recommended Supplier": "Michelin",
        "Lead Time": 7,
        "Status": "Plan Order",
        "Action": "Plan Purchase"
    },
    {
        "Product_ID": "PRD00004",
        "Product": "Steering Assembly",
        "Days Remaining": 18,
        "Current Stock": 620,
        "Safety Stock": 120,
        "ROP": 180,
        "Recommended Supplier": "Bosch",
        "Lead Time": 5,
        "Status": "Safe",
        "Action": "Monitor"
    }
]

df = pd.DataFrame(data)

# ==========================================================
# STATUS ORDER
# ==========================================================

status_order = {
    "Immediate": 0,
    "Order Soon": 1,
    "Plan Order": 2,
    "Safe": 3
}

df["Sort"] = df["Status"].map(status_order)

df = df.sort_values(["Sort", "Days Remaining"]).drop(columns="Sort")


# ==========================================================
# DOWNLOAD FUNCTION
# ==========================================================

def convert_to_excel(dataframe):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False)

    return output.getvalue()


# ==========================================================
# PAGE
# ==========================================================

def show_inventory():

    st.title("📦 Inventory Status")

    st.markdown("### Inventory Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🟢 Safe", len(df[df.Status == "Safe"]))
    c2.metric("🟡 Plan Order", len(df[df.Status == "Plan Order"]))
    c3.metric("🟠 Order Soon", len(df[df.Status == "Order Soon"]))
    c4.metric("🔴 Immediate", len(df[df.Status == "Immediate"]))

    st.divider()

# -----------------------------------------------------
# FILTERS
# -----------------------------------------------------

col1, col2 = st.columns([3, 1])

# Create a dictionary for dropdown display
product_map = {
    f"{row['Product']} ({row['Product_ID']})": row["Product_ID"]
    for _, row in df.iterrows()
}

# Product Dropdown
selected_product = col1.selectbox(
    "🔍 Select Product",
    options=["All Products"] + list(product_map.keys()),
    index=0
)

# Status Dropdown
selected_status = col2.selectbox(
    "Status",
    [
        "All",
        "Safe",
        "Plan Order",
        "Order Soon",
        "Immediate"
    ],
    index=0
)

# -----------------------------------------------------
# APPLY FILTERS
# -----------------------------------------------------

filtered = df.copy()

# Product Filter
if selected_product != "All Products":

    selected_product_id = product_map[selected_product]

    filtered = filtered[
        filtered["Product_ID"] == selected_product_id
    ]

# Status Filter
if selected_status != "All":

    filtered = filtered[
        filtered["Status"] == selected_status
    ]

    # -----------------------------------------------------
    # STATUS DISPLAY
    # -----------------------------------------------------

    status_display = {
        "Safe": "🟢 Safe",
        "Plan Order": "🟡 Plan Order",
        "Order Soon": "🟠 Order Soon",
        "Immediate": "🔴 Immediate"
    }

    filtered["Status"] = filtered["Status"].map(status_display)

    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={

            "Product": st.column_config.TextColumn(
                "Product"
            ),

            "Days Remaining": st.column_config.ProgressColumn(
                "Days Remaining",
                help="Estimated days before reaching reorder point",
                min_value=0,
                max_value=30,
                format="%d Days"
            ),

            "Current Stock": st.column_config.NumberColumn(
                "Current Stock"
            ),

            "Safety Stock": st.column_config.NumberColumn(
                "Safety Stock"
            ),

            "ROP": st.column_config.NumberColumn(
                "ROP"
            ),

            "Recommended Supplier": st.column_config.TextColumn(
                "Recommended Supplier"
            ),

            "Lead Time": st.column_config.NumberColumn(
                "Lead Time (Days)"
            ),

            "Status": st.column_config.TextColumn(
                "Criticality"
            ),

            "Action": st.column_config.TextColumn(
                "Recommended Action"
            )
        }
    )

    st.divider()

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    excel = convert_to_excel(filtered)

    st.download_button(
        label="📥 Download Inventory Report",
        data=excel,
        file_name="Inventory_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    show_inventory()