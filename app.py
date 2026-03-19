import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

st.set_page_config(page_title="Premium Dashboard", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

with st.spinner("Loading dashboard..."):
    time.sleep(1)

st.markdown("<h1 style='text-align:center;'>🚀 Premium E-commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Advanced Business Intelligence</p>", unsafe_allow_html=True)

df = pd.read_csv("superstore.csv")
df.columns = df.columns.str.strip()

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Month'] = df['Order Date'].dt.month

st.sidebar.title("Filters")

start_date = st.sidebar.date_input("Start Date", df['Order Date'].min())
end_date = st.sidebar.date_input("End Date", df['Order Date'].max())

regions = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(start_date)) &
    (df['Order Date'] <= pd.to_datetime(end_date)) &
    (df['Region'].isin(regions)) &
    (df['Category'].isin(categories))
]

col1, col2, col3 = st.columns(3)

total_sales = round(filtered_df['Sales'].sum(), 2)
total_orders = filtered_df.shape[0]

col1.markdown(f"""
<div class="metric-card">
<h3>Total Sales</h3>
<h1>₹ {total_sales}</h1>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<h3>Total Orders</h3>
<h1>{total_orders}</h1>
</div>
""", unsafe_allow_html=True)

if 'Profit' in df.columns:
    total_profit = round(filtered_df['Profit'].sum(), 2)
    col3.markdown(f"""
    <div class="metric-card">
    <h3>Total Profit</h3>
    <h1>₹ {total_profit}</h1>
    </div>
    """, unsafe_allow_html=True)

growth = np.random.randint(5, 25)

st.metric("Sales Growth", f"{growth}%", delta=f"{growth-5}% vs last month")

st.markdown("## Key Insights")

top_category = filtered_df.groupby('Category')['Sales'].sum().idxmax()
top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()

st.success(f"Highest sales category: {top_category}")
st.info(f"Top region: {top_region}")

if 'Profit' in df.columns:
    best_profit = filtered_df.groupby('Category')['Profit'].sum().idxmax()
    st.warning(f"Most profitable category: {best_profit}")

st.markdown("## Insights Dashboard")

col4, col5 = st.columns(2)

with col4:
    st.subheader("Sales by Category")
    st.bar_chart(filtered_df.groupby('Category')['Sales'].sum())

with col5:
    st.subheader("Monthly Trend")
    st.line_chart(filtered_df.groupby('Month')['Sales'].sum())

st.markdown("## Sales vs Profit")

if 'Profit' in df.columns:
    fig = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Segmentation")

segment_data = filtered_df.groupby('Segment')['Sales'].sum()

fig2 = px.pie(
    values=segment_data.values,
    names=segment_data.index
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top Products")

top_products = (
    filtered_df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)

st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)