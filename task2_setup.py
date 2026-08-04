import sqlite3
import pandas as pd

# 1. Connect to SQLite (creates a database file named 'ecommerce.db')
conn = sqlite3.connect("ecommerce.db")

# 2. Load your cleaned CSV file from Task 1
df = pd.read_csv("data/processed/cleaned_orders.csv")

# 3. Save the loaded data as a SQL table named 'orders' inside the database
df.to_sql("orders", conn, if_exists="replace", index=False)

print("✅ Success! Database 'ecommerce.db' created with table 'orders'.")

# 4. Close the database connection
conn.close()
import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

# Query 1: Monthly Sales Trend
q1_monthly = """
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month ASC;
"""

# Query 2: Ranking Orders Per User (Window Function: ROW_NUMBER)
q2_window = """
WITH RankedOrders AS (
    SELECT 
        order_id, 
        user_id, 
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total_amount DESC) as rank_per_user
    FROM orders
)
SELECT * 
FROM RankedOrders 
WHERE rank_per_user = 1
LIMIT 5;
"""

print("--- Monthly Sales Trend ---")
print(pd.read_sql_query(q1_monthly, conn))

print("\n--- Top Order Per User (Window Function) ---")
print(pd.read_sql_query(q2_window, conn))

conn.close()
import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# 1. Create a View for Completed Orders
cursor.execute("""
CREATE VIEW IF NOT EXISTS v_completed_orders AS
SELECT order_id, user_id, order_date, total_amount
FROM orders
WHERE order_status = 'Completed';
""")

# 2. Create Indexes to speed up queries
cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON orders(user_id);")

conn.commit()
conn.close()

# 3. Create a clean SQL file named 'queries.sql' for your GitHub repo
sql_content = """-- ==========================================
-- TASK 2: SQL DATA EXTRACTION & ANALYTICS
-- ==========================================

-- 1. Fundamental Querying (Filtering & Sorting)
SELECT order_id, user_id, order_date, total_amount, order_status
FROM orders
WHERE order_status = 'Completed'
ORDER BY total_amount DESC
LIMIT 5;

-- 2. Aggregations & Grouping
SELECT 
    order_status,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
GROUP BY order_status;

-- 3. Monthly Sales Trends
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month ASC;

-- 4. Advanced Window Functions (Top order per user)
WITH RankedOrders AS (
    SELECT 
        order_id, 
        user_id, 
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total_amount DESC) as rank_per_user
    FROM orders
)
SELECT * 
FROM RankedOrders 
WHERE rank_per_user = 1;

-- 5. Views and Performance Optimization Indexes
CREATE VIEW IF NOT EXISTS v_completed_orders AS
SELECT order_id, user_id, order_date, total_amount
FROM orders
WHERE order_status = 'Completed';

CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_user_id ON orders(user_id);
"""

with open("queries.sql", "w") as f:
    f.write(sql_content)

print("✅ Views and Indexes created!")
print("✅ 'queries.sql' file created in your project folder!")
import sqlite3
import pandas as pd
from db_utils import execute_parameterized_query

# 1. Connect and create SQLite DB from your cleaned CSV
conn = sqlite3.connect("ecommerce.db")
df = pd.read_csv("data/processed/cleaned_orders.csv")
df.to_sql("orders", conn, if_exists="replace", index=False)
print("✅ Database created and dataset loaded!")


# 2. Example: Parameterized query using db_utils (SQL Injection Safe)
query = """
SELECT order_id, user_id, order_date, total_amount, order_status
FROM orders
WHERE order_status = :status AND total_amount > :min_amount
LIMIT 5;
"""

result_df = execute_parameterized_query(query, params={"status": "Completed", "min_amount": 50.0})
print("\n--- Query Output ---")
print(result_df)

conn.close()
import pandas as pd
df = pd.read_csv("data/processed/cleaned_orders.csv")

print("Order Statuses present:", df['order_status'].unique())
print("Min total_amount:", df['total_amount'].min())
print("Max total_amount:", df['total_amount'].max())