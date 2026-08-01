import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ------------------------------------------------------
# Sample Data
# Replace these with database queries later
# ------------------------------------------------------

inventory_summary = {
    "Safe": 172,
    "Plan Order (10 Days)": 28,
    "Order Soon (5 Days)": 11,
    "Immediate (2 Days)": 4
}

supplier_summary = {
    "Safe": 36,
    "Medium Risk": 5,
    "High Risk": 2
}

total_products = 215
total_suppliers = 43
orders_needed = 43
critical_orders = 15


# ------------------------------------------------------
# Inventory Health Chart
# ------------------------------------------------------

def inventory_health_chart():

    colors = [
        "#2E8B57",   # Green
        "#F4C430",   # Yellow
        "#FF8C00",   # Orange
        "#D62828"    # Red
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(inventory_summary.values()),
        y=["Inventory"],
        orientation="h",
        marker=dict(color=colors),
        text=list(inventory_summary.keys()),
        textposition="inside"
    ))

    fig.update_layout(
        barmode="stack",
        height=180,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis_title="Number of Products",
        yaxis_visible=False
    )

    return fig


# ------------------------------------------------------
# Supplier Health Chart
# ------------------------------------------------------

def supplier_health_chart():

    colors = [
        "#2E8B57",
        "#F4C430",
        "#D62828"
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(supplier_summary.keys()),
                values=list(supplier_summary.values()),
                hole=0.65,
                marker=dict(colors=colors)
            )
        ]
    )

    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )

    return fig


# ------------------------------------------------------
# Dashboard
# ------------------------------------------------------

def show_dashboard():

    st.set_page_config(
        page_title="Procurement AI Dashboard",
        layout="wide"
    )

    st.title("📊 Procurement AI Decision Dashboard")

    st.markdown("---")

    # --------------------------------------------------
    # Inventory Health
    # --------------------------------------------------

    st.subheader("📦 Inventory Health")

    st.plotly_chart(
        inventory_health_chart(),
        use_container_width=True
    )

    st.markdown("")

    # --------------------------------------------------
    # Supplier + KPI
    # --------------------------------------------------

    left, right = st.columns([1, 1.2])

    with left:

        st.subheader("🏭 Supplier Health")

        st.plotly_chart(
            supplier_health_chart(),
            use_container_width=True
        )

    with right:

        st.subheader("📈 Quick Statistics")

        c1, c2 = st.columns(2)

        c1.metric(
            "Products",
            total_products
        )

        c2.metric(
            "Suppliers",
            total_suppliers
        )

        c3, c4 = st.columns(2)

        c3.metric(
            "Orders Needed",
            orders_needed
        )

        c4.metric(
            "Critical Orders",
            critical_orders,
            delta="Immediate"
        )

    st.markdown("---")

    # --------------------------------------------------
    # AI Summary
    # --------------------------------------------------

    st.subheader("🤖 AI Executive Summary")

    st.info(
        """
**Today's Procurement Summary**

• 43 products require procurement planning.

• 15 products require immediate attention.

• 4 products are expected to reach the reorder point within the next 2 days.

• Supplier network remains healthy with only 2 suppliers classified as high risk.

**Recommendation**

Prioritize procurement of products reaching their reorder point within the next 5 days and source from low-risk suppliers with shorter lead times to minimize stockout risk.
"""
    )


if __name__ == "__main__":
    show_dashboard()