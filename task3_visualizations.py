import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Ensure export directory exists
os.makedirs("visualizations", exist_ok=True)

# ---------------------------------------------------------
# 1. LOAD DATA FROM ECOMMERCE DATABASE
# ---------------------------------------------------------
try:
    conn = sqlite3.connect("ecommerce.db")
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    
    # Ensure order_date is datetime
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])
except Exception as e:
    print(f"Warning: Could not read from database ({e}). Generating sample data.")
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    categories = ['Electronics', 'Clothing', 'Home', 'Books']
    regions = ['North', 'South', 'East', 'West']
    
    df = pd.DataFrame({
        'order_id': range(1, 101),
        'order_date': np.random.choice(dates, 100),
        'category': np.random.choice(categories, 100),
        'region': np.random.choice(regions, 100),
        'quantity': np.random.randint(1, 10, 100),
        'price': np.random.uniform(10.0, 500.0, 100),
    })
    df['total_amount'] = df['quantity'] * df['price']

print("Data loaded successfully! Total records:", len(df))

# ---------------------------------------------------------
# 2. MATPLOTLIB VISUALIZATIONS (2x2 Subplots)
# ---------------------------------------------------------
print("Generating Matplotlib grid...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Chart 1: Line Plot (Daily Sales Trend)
daily_sales = df.groupby('order_date')['total_amount'].sum().reset_index()
axes[0, 0].plot(daily_sales['order_date'], daily_sales['total_amount'], color='#1f77b4', linewidth=2)
axes[0, 0].set_title('Daily Revenue Trend', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Revenue ($)')

# Chart 2: Bar Chart (Sales by Category)
cat_sales = df.groupby('category')['total_amount'].sum().reset_index()
axes[0, 1].bar(cat_sales['category'], cat_sales['total_amount'], color='#ff7f0e')
axes[0, 1].set_title('Revenue by Category', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Category')
axes[0, 1].set_ylabel('Revenue ($)')

# Chart 3: Histogram (Order Value Distribution)
axes[1, 0].hist(df['total_amount'], bins=15, color='#2ca02c', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Order Total Distribution', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Order Amount ($)')
axes[1, 0].set_ylabel('Frequency')

# Chart 4: Scatter Plot (Price vs Quantity)
axes[1, 1].scatter(df['price'], df['quantity'], color='#d62728', alpha=0.6)
axes[1, 1].set_title('Price vs Quantity Sold', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Price ($)')
axes[1, 1].set_ylabel('Quantity')

plt.tight_layout()
plt.savefig("visualizations/matplotlib_summary.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 3. SEABORN ADVANCED VISUALIZATIONS
# ---------------------------------------------------------
print("Generating Seaborn charts...")

# Heatmap: Correlation Matrix
plt.figure(figsize=(8, 6))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', fmt=".2f")
plt.title('Correlation Matrix Heatmap', fontweight='bold')
plt.savefig("visualizations/seaborn_heatmap.png", dpi=300)
plt.close()

# Pairplot: Multi-variable Relationships
pairplot_fig = sns.pairplot(df[['quantity', 'price', 'total_amount']], diag_kind='kde')
pairplot_fig.fig.suptitle('Pairplot Matrix', y=1.02, fontweight='bold')
pairplot_fig.savefig("visualizations/seaborn_pairplot.png", dpi=300)
plt.close()

# Boxen Plot: Large Dataset Distribution Across Categories
plt.figure(figsize=(10, 6))
sns.boxenplot(data=df, x='category', y='total_amount', palette='Set2')
plt.title('Distribution of Total Amounts per Category (Boxen Plot)', fontweight='bold')
plt.savefig("visualizations/seaborn_boxenplot.png", dpi=300)
plt.close()

# FacetGrid: Revenue Trend per Region
g = sns.FacetGrid(df, col='region', hue='region', col_wrap=2, height=3.5, aspect=1.5)
g.map(sns.scatterplot, 'price', 'total_amount')
g.add_legend()
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Price vs Total Amount faceted by Region', fontweight='bold')
g.savefig("visualizations/seaborn_facetgrid.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# 4. PLOTLY INTERACTIVE VISUALIZATIONS
# ---------------------------------------------------------
print("Generating Plotly interactive graphics...")

# Interactive Line Chart
fig_line = px.line(
    daily_sales, 
    x='order_date', 
    y='total_amount', 
    title='Interactive Daily Sales Trend',
    labels={'order_date': 'Date', 'total_amount': 'Total Revenue ($)'}
)
fig_line.update_xaxes(rangeslider_visible=True)
fig_line.write_html("visualizations/plotly_sales_trend.html")

# Interactive Bar Chart
fig_bar = px.bar(
    cat_sales, 
    x='category', 
    y='total_amount', 
    color='category',
    title='Interactive Category Revenue Breakdown'
)
fig_bar.write_html("visualizations/plotly_category_sales.html")

# Interactive Scatter Plot
fig_scatter = px.scatter(
    df, 
    x='price', 
    y='total_amount', 
    color='category', 
    size='quantity',
    hover_data=['order_id'],
    title='Price vs Total Amount by Category'
)
fig_scatter.write_html("visualizations/plotly_price_scatter.html")

print("\nTask 3 Python Visualizations successfully executed and exported to /visualizations folder!")