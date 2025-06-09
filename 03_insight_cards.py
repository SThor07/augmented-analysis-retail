import pandas as pd

df = pd.read_csv('superstore_sales.csv', encoding='latin1')

# Convert dates to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 1. Top 5 selling products
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)

# 2. Best and worst sales months
df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()
best_month = monthly_sales.idxmax().strftime('%B %Y')
worst_month = monthly_sales.idxmin().strftime('%B %Y')

# 3. Top 3 regions by sales
top_regions = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).head(3)

# 4. Top and bottom states by profit
state_profit = df.groupby('State')['Profit'].sum().sort_values(ascending=False)
top_profit_state = state_profit.idxmax()
bottom_profit_state = state_profit.idxmin()

# 5. Most discounted products (avg discount)
most_discounted = df.groupby('Product Name')['Discount'].mean().sort_values(ascending=False).head(3)

# --- PRINT INSIGHT CARDS ---
print("\n--- INSIGHT CARDS ---")
print(f"Top 5 Selling Products:\n{top_products}\n")
print(f"Best Sales Month: {best_month} | Total Sales: ${monthly_sales.max():,.2f}")
print(f"Worst Sales Month: {worst_month} | Total Sales: ${monthly_sales.min():,.2f}")
print(f"\nTop 3 Regions by Sales:\n{top_regions}\n")
print(f"State with Highest Profit: {top_profit_state} (${state_profit.max():,.2f})")
print(f"State with Lowest Profit: {bottom_profit_state} (${state_profit.min():,.2f})")
print(f"\nMost Discounted Products (Avg Discount):\n{most_discounted}")

print("\n================= BUSINESS INSIGHT CARDS =================")

print(f"🏆 **Top-Selling Product:** '{top_products.index[0]}' led all sales with a total of ${top_products.iloc[0]:,.2f}.")
print(f"🔥 **Best Month:** Sales peaked in {best_month} with ${monthly_sales.max():,.2f} in revenue.")
print(f"🥶 **Slowest Month:** {worst_month} saw the lowest sales, totaling just ${monthly_sales.min():,.2f}.")
print(f"🌍 **Best Regions:** The highest sales were in the West (${top_regions.iloc[0]:,.2f}), followed by the East and Central regions.")
print(f"💰 **Top Profit State:** California generated the most profit at ${state_profit.max():,.2f}.")
print(f"📉 **Biggest Loss State:** Texas had the lowest total profit, losing ${-state_profit.min():,.2f}.")
print(f"🎯 **Most Discounted Products:** '{most_discounted.index[0]}' had the highest average discount ({most_discounted.iloc[0]*100:.1f}%).")
