import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('superstore_sales.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year

# --- Sidebar filters ---
st.sidebar.header("Filter Data")
region_options = ["All"] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", region_options)
year_options = ["All"] + sorted(df['Year'].unique().astype(str).tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]

# --- Generate insights from filtered data ---
if filtered_df.empty:
    st.warning("No data matches your filter selection. Please adjust filters.")
else:
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)
    filtered_df['Month'] = filtered_df['Order Date'].dt.to_period('M')
    monthly_sales = filtered_df.groupby('Month')['Sales'].sum()
    if not monthly_sales.empty:
        best_month = monthly_sales.idxmax().strftime('%B %Y')
        worst_month = monthly_sales.idxmin().strftime('%B %Y')
    else:
        best_month = worst_month = "N/A"
    top_regions = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).head(3)
    state_profit = filtered_df.groupby('State')['Profit'].sum().sort_values(ascending=False)
    most_discounted = filtered_df.groupby('Product Name')['Discount'].mean().sort_values(ascending=False).head(3)

    st.title("Augmented Analytics: Retail Sales Insights Dashboard")
    st.header("Business Insight Cards")

    # Create 3 columns for the first row of cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"🏆\n**Top-Selling Product**\n\n'{top_products.index[0]}'\n\n**${top_products.iloc[0]:,.2f}**")
    with col2:
        st.info(f"🔥\n**Best Month**\n\n{best_month}\n\n**${monthly_sales.max():,.2f}**")
    with col3:
        st.info(f"🥶\n**Slowest Month**\n\n{worst_month}\n\n**${monthly_sales.min():,.2f}**")

    # Second row for more cards
    col4, col5, col6 = st.columns(3)
    with col4:
        st.success(f"🌍\n**Best Region**\n\n{top_regions.index[0]}\n\n**${top_regions.iloc[0]:,.2f}**")
    with col5:
        st.success(f"💰\n**Top Profit State**\n\n{state_profit.idxmax()}\n\n**${state_profit.max():,.2f}**")
    with col6:
        st.error(f"📉\n**Biggest Loss State**\n\n{state_profit.idxmin()}\n\n**${-state_profit.min():,.2f}**")

    # Third row for discounted product
    col7, _, _ = st.columns(3)
    with col7:
        st.warning(
            f"🎯\n**Most Discounted Product**\n\n'{most_discounted.index[0]}'\n\n**{most_discounted.iloc[0] * 100:.1f}%**")

    # Optionally, add a divider
    st.markdown("---")

    # Sales by Region
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig_region = px.bar(region_sales, x='Region', y='Sales', title='Sales by Region', text_auto='.2s')
    st.plotly_chart(fig_region, use_container_width=True)

    # Monthly Sales Trend
    if not filtered_df.empty:
        monthly_sales_df = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly_sales_df['Order Date'] = monthly_sales_df['Order Date'].astype(str)
        fig_month = px.line(monthly_sales_df, x='Order Date', y='Sales', title='Monthly Sales Trend')
        st.plotly_chart(fig_month, use_container_width=True)


    st.header("Explore Raw Data (Filtered)")
    st.dataframe(filtered_df.head(20))

    st.header("⬇️ Download Your Insights/Data")

    # Download filtered data as CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_sales_data.csv',
        mime='text/csv',
    )

    # Download insight cards as TXT
    insight_txt = f"""Top-Selling Product: {top_products.index[0]} - ${top_products.iloc[0]:,.2f}
    Best Month: {best_month} - ${monthly_sales.max():,.2f}
    Slowest Month: {worst_month} - ${monthly_sales.min():,.2f}
    Best Region: {top_regions.index[0]} - ${top_regions.iloc[0]:,.2f}
    Top Profit State: {state_profit.idxmax()} - ${state_profit.max():,.2f}
    Biggest Loss State: {state_profit.idxmin()} - ${state_profit.min():,.2f}
    Most Discounted Product: {most_discounted.index[0]} - {most_discounted.iloc[0] * 100:.1f}%
    """
    st.download_button(
        label="Download Insights as TXT",
        data=insight_txt,
        file_name='insight_cards.txt',
        mime='text/plain',
    )

    st.caption("Made by Shrivatsasingh Rathore")
