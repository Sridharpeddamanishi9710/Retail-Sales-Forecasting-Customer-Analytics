# Configuring the Streamlit page and defining the professional dark retail analytics theme

import pandas as pd
import streamlit as st
import plotly.express as px


# Configuring the Streamlit page settings for the retail analytics dashboard

st.set_page_config(
    page_title="Retail Sales Forecasting & Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Defining the professional color palette used throughout the dashboard

TEAL = "#2A9D8F"
LIGHT_TEAL = "#52B8A9"
AMBER = "#E9C46A"
ORANGE = "#F4A261"
CORAL = "#E76F51"
BLUE = "#5DADE2"
PURPLE = "#9B7EDE"


# Defining the common Plotly chart styling used throughout the dashboard

PLOTLY_LAYOUT = {
    "paper_bgcolor": "#0E1117",
    "plot_bgcolor": "#0E1117",
    "font": {
        "color": "#D1D5DB"
    },
    "title_font": {
        "color": "#FFFFFF",
        "size": 20
    },
    "margin": {
        "l": 20,
        "r": 20,
        "t": 60,
        "b": 30
    }
}


# Loading all processed datasets required for the interactive retail analytics dashboard
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


# Loading each processed dataset into its own variable for dashboard analysis

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

df = pd.read_csv(DATA_DIR / "cleaned_data.csv")

forecast = pd.read_csv(DATA_DIR / "2024_sales_forecast.csv")

forecast_comparison = pd.read_csv(
    DATA_DIR / "forecast_model_comparison.csv"
)

rfm_segments = pd.read_csv(
    DATA_DIR / "customer_rfm_segments.csv"
)

customer_segment_summary = pd.read_csv(
    DATA_DIR / "customer_segment_summary.csv"
)

product_performance = pd.read_csv(
    DATA_DIR / "product_performance.csv"
)

product_group_summary = pd.read_csv(
    DATA_DIR / "product_group_summary.csv"
)

# Converting the primary order date column into datetime format for filtering

df["Order Date"] = pd.to_datetime(df["Order Date"])





# Applying custom CSS styling to create a clean dark professional dashboard layout

st.markdown(
    """
    <style>

    /* Main application background */

    .stApp {
        background-color: #0E1117;
    }


    /* Main content spacing */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* Main dashboard title */

    h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }


    /* Section headings */

    h2, h3 {
        color: #FFFFFF !important;
        font-weight: 600;
    }


    /* Normal text */

    p {
        color: #D1D5DB;
    }


    /* Improving the KPI card styling for a polished professional dashboard appearance */

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #161B22,
            #131820
        );
        border: 1px solid #2A343D;
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 105px;
        box-shadow: 0px 5px 16px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #2A9D8F;
    }


    /* Styling the KPI labels and values for improved visual hierarchy */

    div[data-testid="stMetricLabel"] {
        color: #AEB6C2 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 27px !important;
        font-weight: 700 !important;
    }


    /* Styling the horizontal separators */

    hr {
        border-color: #252C35;
    }


    /* Styling the dashboard sidebar */

    section[data-testid="stSidebar"] {
        background-color: #11161D;
        border-right: 1px solid #252C35;
    }


    /* Styling the sidebar text */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #D1D5DB !important;
    }


    /* Styling dashboard dataframes */

    div[data-testid="stDataFrame"] {
        border: 1px solid #252C35;
        border-radius: 10px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Creating the polished dashboard header and project description using native Streamlit elements

st.title(
    "🛍️ Retail Sales Forecasting & Customer Analytics"
)

st.markdown(
    "Data-driven analysis of retail sales, customer behavior, "
    "product performance, and future demand."
)

st.markdown(
    "**📊 Sales Analytics**  •  "
    "**🔮 Forecasting**  •  "
    "**👥 Customer Segmentation**  •  "
    "**📦 Product Analytics**"
)

st.markdown("---")


# Preparing the retail dataset and customer segment information for interactive filtering

df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)


filter_data = df.merge(
    rfm_segments[
        [
            "Customer ID",
            "Customer_Segment"
        ]
    ],
    on="Customer ID",
    how="left"
)


# Creating the polished sidebar filter section for interactive dashboard analysis

st.sidebar.markdown(
    """
    <div style="
        padding: 8px 0px 14px 0px;
        border-bottom: 1px solid #2A9D8F;
        margin-bottom: 16px;
    ">
        <h2 style="
            color: #FFFFFF;
            font-size: 22px;
            margin: 0px;
        ">
            🔎 Dashboard Filters
        </h2>
        <p style="
            color: #AEB6C2;
            font-size: 13px;
            margin: 5px 0px 0px 0px;
        ">
            Refine the dashboard analysis using the controls below.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Creating the date range filter

min_date = filter_data["Order Date"].min().date()
max_date = filter_data["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Creating the region filter

region_options = sorted(
    filter_data["Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "🌍 Region",
    options=region_options,
    default=region_options
)


# Creating the category filter

category_options = sorted(
    filter_data["Category of Goods"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "🛒 Category",
    options=category_options,
    default=category_options
)


# Creating the subcategory filter

subcategory_options = sorted(
    filter_data["Sub-Category"].dropna().unique()
)

selected_subcategories = st.sidebar.multiselect(
    "📦 Subcategory",
    options=subcategory_options,
    default=subcategory_options
)


# Creating the customer segment filter

segment_options = sorted(
    filter_data["Customer_Segment"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "👥 Customer Segment",
    options=segment_options,
    default=segment_options
)


# Calculating the main retail business KPIs

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

total_quantity = df["Quantity"].sum()

total_orders = df["Order ID"].nunique()

profit_margin = (
    total_profit / total_sales
) * 100


# Displaying the main business KPIs in professional dashboard cards

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "Quantity Sold",
    f"{total_quantity:,}"
)

col4.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col5.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)


# Creating the monthly sales dataset for historical trend analysis

monthly_sales = (
    df.groupby(
        "Year-Month",
        as_index=False
    )["Sales"]
    .sum()
)

monthly_sales["Year-Month"] = pd.to_datetime(
    monthly_sales["Year-Month"]
)


# Creating the monthly sales trend chart using the primary teal color

fig_sales_trend = px.line(
    monthly_sales,
    x="Year-Month",
    y="Sales",
    title="📈 Monthly Sales Trend",
    labels={
        "Year-Month": "Month",
        "Sales": "Sales (₹)"
    },
    color_discrete_sequence=[
        TEAL
    ],
    template="plotly_dark"
)


# Improving the monthly sales trend appearance

fig_sales_trend.update_traces(
    line=dict(
        width=3
    )
)


# Applying the common professional Plotly styling to the monthly sales trend

fig_sales_trend.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    hovermode="x unified",
    xaxis=dict(
        title="Month",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


st.plotly_chart(
    fig_sales_trend,
    use_container_width=True
)


# Creating the yearly sales and profit summary

yearly_summary = (
    df.groupby(
        "Year",
        as_index=False
    )[["Sales", "Profit"]]
    .sum()
)


# Creating the yearly sales and profit comparison chart

fig_yearly = px.bar(
    yearly_summary,
    x="Year",
    y=["Sales", "Profit"],
    barmode="group",
    title="💰 Yearly Sales and Profit",
    labels={
        "value": "Amount (₹)",
        "variable": "Metric",
        "Year": "Year"
    },
    color_discrete_map={
        "Sales": TEAL,
        "Profit": AMBER
    },
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the yearly sales and profit chart

fig_yearly.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    legend_title_text="Metric",
    xaxis=dict(
        title="Year",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Amount (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


st.plotly_chart(
    fig_yearly,
    use_container_width=True
)


# Creating two columns for regional and category-level sales analysis

col1, col2 = st.columns(2)


# Creating the regional sales summary

region_sales = (
    df.groupby(
        "Region",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


# Creating the regional sales chart using the blue-teal business color

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="🌍 Sales by Region",
    labels={
        "Sales": "Sales (₹)",
        "Region": "Region"
    },
    color_discrete_sequence=[
        BLUE
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the regional sales chart

fig_region.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    xaxis=dict(
        title="Region",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


col1.plotly_chart(
    fig_region,
    use_container_width=True
)


# Creating the category sales summary

category_sales = (
    df.groupby(
        "Category of Goods",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


# Creating the category sales chart using the coral accent color

fig_category = px.bar(
    category_sales,
    x="Category of Goods",
    y="Sales",
    title="🛒 Sales by Category",
    labels={
        "Sales": "Sales (₹)",
        "Category of Goods": "Category"
    },
    color_discrete_sequence=[
        CORAL
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the category sales chart

fig_category.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    xaxis=dict(
        title="Category",
        tickangle=-25,
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


col2.plotly_chart(
    fig_category,
    use_container_width=True
)


# Creating the customer segment distribution data and calculating the actual segment percentages

segment_data = (
    customer_segment_summary
    .copy()
    .sort_values(
        "Customer_Count",
        ascending=False
    )
    .reset_index(drop=True)
)

segment_data["Calculated_Percentage"] = (
    segment_data["Customer_Count"]
    / segment_data["Customer_Count"].sum()
    * 100
)

segment_data["Percentage_Label"] = (
    segment_data["Calculated_Percentage"]
    .map(lambda x: f"{x:.2f}%")
)


# Creating the customer segmentation chart with the calculated percentage labels

fig_segments = px.bar(
    segment_data,
    x="Customer_Segment",
    y="Customer_Count",
    title="👥 Customer Segmentation",
    labels={
        "Customer_Segment": "Customer Segment",
        "Customer_Count": "Number of Customers"
    },
    color="Customer_Segment",
    color_discrete_map={
        "Recent High-Value": TEAL,
        "Recent Low-Value": BLUE,
        "Inactive High-Value": AMBER,
        "Inactive Low-Value": CORAL
    },
    text="Percentage_Label",
    template="plotly_dark"
)


# Formatting the customer segmentation chart labels and layout

fig_segments.update_traces(
    textposition="outside",
    cliponaxis=False
)


# Applying the common professional Plotly styling to the customer segmentation chart

fig_segments.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Customer Segment",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Number of Customers",
        tickformat=",",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the customer segmentation chart in the dashboard

st.plotly_chart(
    fig_segments,
    use_container_width=True
)


# Creating the customer segment profile table for detailed RFM analysis

segment_profile = customer_segment_summary[
    [
        "Customer_Segment",
        "Customer_Count",
        "Customer_Percentage",
        "Average_Recency",
        "Average_Monetary",
        "Average_RFM_Score"
    ]
].copy()


# Creating a separate display copy of the segment profile dataframe for formatted presentation

segment_profile_display = segment_profile.copy()


# Renaming the segment profile display columns for clear dashboard presentation

segment_profile_display.columns = [
    "Customer Segment",
    "Customers",
    "Percentage",
    "Avg. Recency (Days)",
    "Avg. Monetary (₹)",
    "Avg. RFM Score"
]


# Formatting the customer segment profile display values

segment_profile_display["Customers"] = (
    segment_profile_display["Customers"]
    .apply(lambda x: f"{x:,}")
)

segment_profile_display["Percentage"] = (
    segment_profile_display["Percentage"]
    .apply(lambda x: f"{x:.2f}%")
)

segment_profile_display["Avg. Recency (Days)"] = (
    segment_profile_display["Avg. Recency (Days)"]
    .apply(lambda x: f"{x:,.2f}")
)

segment_profile_display["Avg. Monetary (₹)"] = (
    segment_profile_display["Avg. Monetary (₹)"]
    .apply(lambda x: f"₹{x:,.2f}")
)

segment_profile_display["Avg. RFM Score"] = (
    segment_profile_display["Avg. RFM Score"]
    .apply(lambda x: f"{x:.2f}")
)


# Displaying the customer segment profile table in the dashboard

st.subheader("📋 Customer Segment Profiles")

st.dataframe(
    segment_profile_display,
    use_container_width=True,
    hide_index=True
)


# Creating the top 10 products by sales for product performance analysis

top_products_sales = (
    product_performance
    .sort_values(
        "Total_Sales",
        ascending=False
    )
    .head(10)
)


# Creating the top product sales chart using the professional teal color

fig_top_products = px.bar(
    top_products_sales.sort_values(
        "Total_Sales",
        ascending=True
    ),
    x="Total_Sales",
    y="Product Name",
    orientation="h",
    title="🏆 Top 10 Products by Sales",
    labels={
        "Total_Sales": "Total Sales (₹)",
        "Product Name": "Product"
    },
    color_discrete_sequence=[
        TEAL
    ],
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the top products by sales chart

fig_top_products.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Total Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Product",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the top 10 products by sales chart

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)


# Creating the top 10 products by profit for profitability analysis

top_products_profit = (
    product_performance
    .sort_values(
        "Total_Profit",
        ascending=False
    )
    .head(10)
)


# Creating the top product profit chart using the professional amber color

fig_top_profit = px.bar(
    top_products_profit.sort_values(
        "Total_Profit",
        ascending=True
    ),
    x="Total_Profit",
    y="Product Name",
    orientation="h",
    title="💰 Top 10 Products by Profit",
    labels={
        "Total_Profit": "Total Profit (₹)",
        "Product Name": "Product"
    },
    color_discrete_sequence=[
        AMBER
    ],
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the top products by profit chart

fig_top_profit.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Total Profit (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Product",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the top 10 products by profit chart

st.plotly_chart(
    fig_top_profit,
    use_container_width=True
)


# Identifying products with high sales but comparatively low profit for business analysis

high_sales_low_profit = product_performance[
    (
        product_performance["Total_Sales"]
        >= product_performance["Total_Sales"].median()
    )
    &
    (
        product_performance["Total_Profit"]
        < product_performance["Total_Profit"].median()
    )
].copy()


# Selecting the top 10 high-sales low-profit products by sales value

high_sales_low_profit = (
    high_sales_low_profit
    .sort_values(
        "Total_Sales",
        ascending=False
    )
    .head(10)
)


# Creating the high-sales low-profit product chart

fig_sales_low_profit = px.bar(
    high_sales_low_profit.sort_values(
        "Total_Sales",
        ascending=True
    ),
    x="Total_Sales",
    y="Product Name",
    orientation="h",
    title="⚠️ High-Sales, Low-Profit Products",
    labels={
        "Total_Sales": "Total Sales (₹)",
        "Product Name": "Product"
    },
    color_discrete_sequence=[
        CORAL
    ],
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the high-sales low-profit chart

fig_sales_low_profit.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Total Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Product",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the high-sales low-profit product analysis

st.plotly_chart(
    fig_sales_low_profit,
    use_container_width=True
)


# Creating the discount versus profit margin analysis for product-level profitability insights

fig_discount_margin = px.scatter(
    product_performance,
    x="Average_Discount",
    y="Profit_Margin",
    title="🏷️ Discount vs Profit Margin",
    labels={
        "Average_Discount": "Average Discount",
        "Profit_Margin": "Profit Margin (%)"
    },
    color_discrete_sequence=[
        PURPLE
    ],
    template="plotly_dark"
)


# Formatting discount values as percentages on the horizontal axis

fig_discount_margin.update_xaxes(
    tickformat=".0%"
)


# Applying the common professional Plotly styling to the discount versus profit margin chart

fig_discount_margin.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    hovermode="closest",
    xaxis=dict(
        title="Average Discount",
        tickformat=".0%",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Profit Margin (%)",
        ticksuffix="%",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the discount versus profit margin relationship

st.plotly_chart(
    fig_discount_margin,
    use_container_width=True
)


# Displaying the observed correlation between discount and profit margin

discount_margin_correlation = (
    product_performance[
        [
            "Average_Discount",
            "Profit_Margin"
        ]
    ]
    .corr()
    .loc[
        "Average_Discount",
        "Profit_Margin"
    ]
)

st.caption(
    f"Observed product-level correlation between discount and profit margin: "
    f"{discount_margin_correlation:.4f}. "
    "This indicates a moderate negative relationship and does not by itself establish causation."
)


# Creating the subcategory-level performance summary directly from the cleaned retail dataset

subcategory_performance = (
    df.groupby(
        "Sub-Category",
        as_index=False
    )
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
)

subcategory_performance["Profit_Margin"] = (
    subcategory_performance["Total_Profit"]
    / subcategory_performance["Total_Sales"]
) * 100

subcategory_performance = subcategory_performance.sort_values(
    "Total_Sales",
    ascending=False
)


# Creating two columns for subcategory sales and profitability analysis

col1, col2 = st.columns(2)


# Creating the subcategory sales chart

fig_subcategory_sales = px.bar(
    subcategory_performance.sort_values(
        "Total_Sales",
        ascending=True
    ),
    x="Total_Sales",
    y="Sub-Category",
    orientation="h",
    title="📦 Sales by Subcategory",
    labels={
        "Total_Sales": "Total Sales (₹)",
        "Sub-Category": "Subcategory"
    },
    color_discrete_sequence=[
        TEAL
    ],
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the subcategory sales chart

fig_subcategory_sales.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Total Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Subcategory",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the subcategory sales chart

col1.plotly_chart(
    fig_subcategory_sales,
    use_container_width=True
)


# Creating the subcategory profit margin chart

fig_subcategory_margin = px.bar(
    subcategory_performance.sort_values(
        "Profit_Margin",
        ascending=True
    ),
    x="Profit_Margin",
    y="Sub-Category",
    orientation="h",
    title="📊 Profit Margin by Subcategory",
    labels={
        "Profit_Margin": "Profit Margin (%)",
        "Sub-Category": "Subcategory"
    },
    color_discrete_sequence=[
        AMBER
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the subcategory profit margin chart

fig_subcategory_margin.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    xaxis=dict(
        title="Profit Margin (%)",
        ticksuffix="%",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Subcategory",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the subcategory profit margin chart

col2.plotly_chart(
    fig_subcategory_margin,
    use_container_width=True
)


# Creating a polished product performance table for detailed product-level analysis

st.markdown("#### 📋 Product Performance Summary")

product_table = product_performance[
    [
        "Product Name",
        "Total_Sales",
        "Total_Profit",
        "Total_Quantity",
        "Transaction_Count",
        "Average_Discount",
        "Profit_Margin"
    ]
].copy()

product_table = product_table.sort_values(
    "Total_Sales",
    ascending=False
).head(15)

product_table.columns = [
    "Product",
    "Sales (₹)",
    "Profit (₹)",
    "Quantity",
    "Transactions",
    "Avg. Discount",
    "Profit Margin"
]

product_table["Sales (₹)"] = product_table[
    "Sales (₹)"
].apply(
    lambda x: f"₹{x:,.2f}"
)

product_table["Profit (₹)"] = product_table[
    "Profit (₹)"
].apply(
    lambda x: f"₹{x:,.2f}"
)

product_table["Quantity"] = product_table[
    "Quantity"
].apply(
    lambda x: f"{x:,}"
)

product_table["Transactions"] = product_table[
    "Transactions"
].apply(
    lambda x: f"{x:,}"
)

product_table["Avg. Discount"] = product_table[
    "Avg. Discount"
].apply(
    lambda x: f"{x:.2%}"
)

product_table["Profit Margin"] = product_table[
    "Profit Margin"
].apply(
    lambda x: f"{x:.2f}%"
)


# Displaying the product performance summary in a polished dashboard table

st.dataframe(
    product_table,
    use_container_width=True,
    hide_index=True
)


# Creating the 2024 sales forecast section and calculating the main forecast indicators

forecast_data = forecast.copy()

forecast_date_column = forecast_data.columns[0]
forecast_sales_column = forecast_data.columns[1]

forecast_data[forecast_date_column] = pd.to_datetime(
    forecast_data[forecast_date_column]
)

total_forecast_sales = forecast_data[
    forecast_sales_column
].sum()

average_forecast_sales = forecast_data[
    forecast_sales_column
].mean()

highest_forecast_row = forecast_data.loc[
    forecast_data[forecast_sales_column].idxmax()
]

lowest_forecast_row = forecast_data.loc[
    forecast_data[forecast_sales_column].idxmin()
]


# Displaying the 2024 sales forecast section heading

st.subheader("🔮 2024 Sales Forecast")

st.caption(
    "The 2024 values are forecast estimates generated using the selected "
    "Seasonal Naive forecasting model."
)


# Creating KPI cards for the 2024 sales forecast

forecast_col1, forecast_col2, forecast_col3, forecast_col4 = st.columns(4)

with forecast_col1:
    st.metric(
        "Forecast Sales",
        f"₹{total_forecast_sales:,.0f}"
    )

with forecast_col2:
    st.metric(
        "Average Monthly Sales",
        f"₹{average_forecast_sales:,.0f}"
    )

with forecast_col3:
    st.metric(
        "Highest Forecast Month",
        highest_forecast_row[
            forecast_date_column
        ].strftime("%b %Y")
    )

with forecast_col4:
    st.metric(
        "Lowest Forecast Month",
        lowest_forecast_row[
            forecast_date_column
        ].strftime("%b %Y")
    )


# Creating the monthly 2024 sales forecast chart

fig_forecast = px.line(
    forecast_data,
    x=forecast_date_column,
    y=forecast_sales_column,
    markers=True,
    title="📈 Monthly Sales Forecast — 2024",
    labels={
        forecast_date_column: "Month",
        forecast_sales_column: "Forecast Sales (₹)"
    },
    color_discrete_sequence=[
        BLUE
    ],
    template="plotly_dark"
)


# Applying the common professional Plotly styling to the 2024 sales forecast chart

fig_forecast.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    hovermode="x unified",
    xaxis=dict(
        title="Month",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Forecast Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the 2024 sales forecast chart

st.plotly_chart(
    fig_forecast,
    use_container_width=True
)


# Creating the forecast model comparison section and preparing the model evaluation results

model_comparison = forecast_comparison.copy()

model_column = model_comparison.columns[0]
mae_column = model_comparison.columns[1]
rmse_column = model_comparison.columns[2]
mape_column = model_comparison.columns[3]


# Displaying the forecast model comparison section heading

st.subheader("📊 Forecast Model Comparison")

st.caption(
    "The forecasting models are compared using MAE, RMSE, and MAPE "
    "on the 2023 test period."
)


# Creating three columns for the model evaluation charts

comparison_col1, comparison_col2, comparison_col3 = st.columns(3)


# Creating the MAE comparison chart

fig_mae = px.bar(
    model_comparison,
    x=model_column,
    y=mae_column,
    title="MAE",
    labels={
        model_column: "Model",
        mae_column: "MAE (₹)"
    },
    color_discrete_sequence=[
        TEAL
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the MAE comparison chart

fig_mae.update_layout(
    **PLOTLY_LAYOUT,
    height=400,
    xaxis=dict(
        title="Model",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="MAE (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the MAE comparison chart

comparison_col1.plotly_chart(
    fig_mae,
    use_container_width=True
)


# Creating the RMSE comparison chart

fig_rmse = px.bar(
    model_comparison,
    x=model_column,
    y=rmse_column,
    title="RMSE",
    labels={
        model_column: "Model",
        rmse_column: "RMSE (₹)"
    },
    color_discrete_sequence=[
        AMBER
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the RMSE comparison chart

fig_rmse.update_layout(
    **PLOTLY_LAYOUT,
    height=400,
    xaxis=dict(
        title="Model",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="RMSE (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the RMSE comparison chart

comparison_col2.plotly_chart(
    fig_rmse,
    use_container_width=True
)


# Creating the MAPE comparison chart

fig_mape = px.bar(
    model_comparison,
    x=model_column,
    y=mape_column,
    title="MAPE",
    labels={
        model_column: "Model",
        mape_column: "MAPE (%)"
    },
    color_discrete_sequence=[
        BLUE
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the MAPE comparison chart

fig_mape.update_layout(
    **PLOTLY_LAYOUT,
    height=400,
    xaxis=dict(
        title="Model",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="MAPE (%)",
        ticksuffix="%",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the MAPE comparison chart

comparison_col3.plotly_chart(
    fig_mape,
    use_container_width=True
)


# Formatting the forecast model evaluation results into a polished comparison table

st.markdown("#### 📋 Model Evaluation Results")

model_evaluation_display = model_comparison.copy()

model_evaluation_display.columns = [
    "Model",
    "MAE (₹)",
    "RMSE (₹)",
    "MAPE (%)"
]

model_evaluation_display["MAE (₹)"] = (
    model_evaluation_display["MAE (₹)"]
    .apply(lambda x: f"₹{x:,.2f}")
)

model_evaluation_display["RMSE (₹)"] = (
    model_evaluation_display["RMSE (₹)"]
    .apply(lambda x: f"₹{x:,.2f}")
)

model_evaluation_display["MAPE (%)"] = (
    model_evaluation_display["MAPE (%)"]
    .apply(lambda x: f"{x:.2f}%")
)

st.dataframe(
    model_evaluation_display,
    use_container_width=True,
    hide_index=True
)


# Creating the business insights and recommendations section from the completed analysis

st.markdown("---")

st.subheader("💡 Business Insights & Recommendations")

st.write(
    "The following insights are derived from the historical sales analysis, "
    "customer segmentation, product performance, profitability analysis, "
    "and 2024 sales forecast."
)


# Creating the first row of business insight cards

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.markdown("### 📈 Sales & Profitability")

    st.markdown(
        """
        - Total historical sales reach approximately **₹2.51 billion**.
        - Total profit is approximately **₹375.53 million**.
        - The overall profit margin is approximately **14.97%**.
        - Annual sales remain relatively stable from 2019 to 2023.
        - The **East region** records the highest overall sales.
        """
    )


with insight_col2:

    st.markdown("### 👥 Customer Insights")

    st.markdown(
        """
        - **Recent High-Value** customers represent about **24.85%** of customers.
        - **Inactive High-Value** customers represent about **25.30%**.
        - Inactive high-value customers represent an important opportunity
          for targeted re-engagement.
        - Customer segmentation is based on **recency and monetary value**
          because every customer has only one transaction in this dataset.
        """
    )


# Creating the second row of business insight cards

insight_col3, insight_col4 = st.columns(2)

with insight_col3:

    st.markdown("### 📦 Product Insights")

    st.markdown(
        """
        - **Mops** record the highest subcategory sales.
        - **Microwaves** have the highest subcategory profit margin.
        - **Tables** have the lowest subcategory profit margin.
        - High-sales, low-profit products require profitability monitoring.
        - The observed product-level correlation between discount and profit
          margin is approximately **-0.49**, indicating a moderate negative
          relationship without establishing causation.
        """
    )


with insight_col4:

    st.markdown("### 🔮 Forecasting Insights")

    st.markdown(
        """
        - The 2024 forecast estimates total sales of approximately
          **₹502.27 million**.
        - Average monthly forecast sales are approximately **₹41.86 million**.
        - **May 2024** has the highest forecast value.
        - **February 2024** has the lowest forecast value.
        - Seasonal Naive produces the lowest test error among the evaluated
          forecasting models.
        """
    )


# Creating the business recommendations section

st.markdown("### 🎯 Business Recommendations")

recommendation_col1, recommendation_col2 = st.columns(2)

with recommendation_col1:

    st.markdown(
        """
        **1. Re-engage inactive high-value customers**

        Develop targeted offers and personalized campaigns for customers
        with high historical monetary value but long periods since their
        last transaction.

        **2. Monitor high-sales, low-profit products**

        Review pricing, discounts, procurement costs, and margins for
        products generating strong sales but comparatively lower profits.

        **3. Optimize discount strategies**

        Evaluate discount levels carefully because higher discounts are
        associated with lower product-level profit margins in the analyzed
        data.
        """
    )


with recommendation_col2:

    st.markdown(
        """
        **4. Prioritize high-margin products**

        Give greater promotional and inventory attention to products and
        subcategories that combine healthy sales with stronger profit
        margins.

        **5. Use forecasts for inventory planning**

        Use the monthly 2024 sales forecast as a planning input for
        inventory, procurement, and resource allocation.

        **6. Monitor regional performance**

        Track regional sales and profitability regularly and investigate
        differences in product demand, pricing, and customer behavior
        across regions.
        """
    )


# Displaying the final dashboard insight statement

st.info(
    "Overall, the analysis supports a data-driven retail strategy focused "
    "on demand forecasting, customer re-engagement, product profitability, "
    "discount optimization, and regional performance monitoring."
)


# Applying the selected dashboard filters to create the filtered retail dataset

if len(selected_dates) == 2:

    selected_start_date = pd.to_datetime(
        selected_dates[0]
    )

    selected_end_date = (
        pd.to_datetime(selected_dates[1])
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

else:

    selected_start_date = pd.to_datetime(
        selected_dates[0]
    )

    selected_end_date = (
        selected_start_date
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )


# Filtering the retail data using the selected date range and categorical filters

filtered_df = filter_data[
    (filter_data["Order Date"] >= selected_start_date)
    & (filter_data["Order Date"] <= selected_end_date)
    & (filter_data["Region"].isin(selected_regions))
    & (filter_data["Category of Goods"].isin(selected_categories))
    & (filter_data["Sub-Category"].isin(selected_subcategories))
    & (filter_data["Customer_Segment"].isin(selected_segments))
].copy()


# Displaying the number of records remaining after applying the filters

st.sidebar.markdown("---")

st.sidebar.metric(
    "Filtered Records",
    f"{len(filtered_df):,}"
)


# Creating the filtered dashboard analysis using the records selected through the interactive filters

st.markdown("---")

st.subheader("🔎 Filtered Dashboard Analysis")

st.caption(
    "The following KPIs and charts update according to the selected "
    "date, region, category, subcategory, and customer segment filters."
)


# Calculating the filtered business KPIs

filtered_sales = filtered_df["Sales"].sum()

filtered_profit = filtered_df["Profit"].sum()

filtered_quantity = filtered_df["Quantity"].sum()

filtered_orders = filtered_df["Order ID"].nunique()

filtered_profit_margin = (
    filtered_profit / filtered_sales * 100
    if filtered_sales > 0
    else 0
)


# Creating the filtered KPI cards

filtered_col1, filtered_col2, filtered_col3, filtered_col4, filtered_col5 = st.columns(5)

with filtered_col1:
    st.metric(
        "Filtered Sales",
        f"₹{filtered_sales:,.0f}"
    )

with filtered_col2:
    st.metric(
        "Filtered Profit",
        f"₹{filtered_profit:,.0f}"
    )

with filtered_col3:
    st.metric(
        "Filtered Quantity",
        f"{filtered_quantity:,}"
    )

with filtered_col4:
    st.metric(
        "Filtered Orders",
        f"{filtered_orders:,}"
    )

with filtered_col5:
    st.metric(
        "Filtered Margin",
        f"{filtered_profit_margin:.2f}%"
    )


# Creating the filtered monthly sales trend

filtered_monthly_sales = (
    filtered_df
    .groupby(
        "Year-Month",
        as_index=False
    )["Sales"]
    .sum()
)

filtered_monthly_sales["Year-Month"] = pd.to_datetime(
    filtered_monthly_sales["Year-Month"]
)


# Creating the filtered monthly sales chart

fig_filtered_sales = px.line(
    filtered_monthly_sales,
    x="Year-Month",
    y="Sales",
    markers=True,
    title="📈 Filtered Monthly Sales Trend",
    labels={
        "Year-Month": "Month",
        "Sales": "Sales (₹)"
    },
    color_discrete_sequence=[
        TEAL
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the filtered monthly sales chart

fig_filtered_sales.update_layout(
    **PLOTLY_LAYOUT,
    height=430,
    hovermode="x unified",
    xaxis=dict(
        title="Month",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the filtered monthly sales chart

st.plotly_chart(
    fig_filtered_sales,
    use_container_width=True
)


# Creating filtered region and category sales summaries

filtered_region_sales = (
    filtered_df
    .groupby(
        "Region",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)

filtered_category_sales = (
    filtered_df
    .groupby(
        "Category of Goods",
        as_index=False
    )["Sales"]
    .sum()
    .sort_values(
        "Sales",
        ascending=False
    )
)


# Creating two columns for filtered regional and category analysis

filtered_col6, filtered_col7 = st.columns(2)


# Creating the filtered regional sales chart

fig_filtered_region = px.bar(
    filtered_region_sales,
    x="Region",
    y="Sales",
    title="🌍 Filtered Sales by Region",
    labels={
        "Region": "Region",
        "Sales": "Sales (₹)"
    },
    color_discrete_sequence=[
        BLUE
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the filtered regional sales chart

fig_filtered_region.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    xaxis=dict(
        title="Region",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the filtered regional sales chart

filtered_col6.plotly_chart(
    fig_filtered_region,
    use_container_width=True
)


# Creating the filtered category sales chart

fig_filtered_category = px.bar(
    filtered_category_sales,
    x="Category of Goods",
    y="Sales",
    title="🛒 Filtered Sales by Category",
    labels={
        "Category of Goods": "Category",
        "Sales": "Sales (₹)"
    },
    color_discrete_sequence=[
        CORAL
    ],
    template="plotly_dark"
)


# Applying the common professional styling to the filtered category sales chart

fig_filtered_category.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    xaxis=dict(
        title="Category",
        tickangle=-25,
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    ),
    yaxis=dict(
        title="Sales (₹)",
        tickformat=",.0f",
        gridcolor="#252C35",
        zerolinecolor="#252C35"
    )
)


# Displaying the filtered category sales chart

filtered_col7.plotly_chart(
    fig_filtered_category,
    use_container_width=True
)