-- ==========================================
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
