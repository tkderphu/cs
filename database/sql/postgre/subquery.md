# Node about subquery

A subquery is a query appear in other sql query. It can appear in:

- Select
- From
- WHERE, HAVING
- JOIN
-EXISTS, IN

# SQL Subquery execution

When the query has subqueries, SQL does this:

```
1. Parse SQL → Build AST
2. Rewrite (e.g., subquery flattening, CTE inlining)
3. Plan (cost-based optimizer):
    - Estimate cost of each path
    - Choose best plan
4. Execute (run actual plan)
```

The subquery is evaluated first, and the result is used by the outer query (unless optimization changes this).

## Example

```
SELECT name
FROM employees
WHERE department_id = (
    SELECT id FROM departments WHERE name = 'IT'
);
```

1. Run query

```
SELECT id FROM departments WHERE name = 'IT'

#result 5 => give outer query
```

2. Substitute into the outer query:

```
SELECT name FROM employees WHERE department_id = 5;
```

# Scalar query

Scalar query is the query that only return one value (one row, one column). You can use it anywhere a value is expected.

## Ex1:

```
SELECT
  name,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
FROM customers c;
```

- SELECT COUNT(*) FROM orders WHERE ... is a scalar subquery.

- It returns one value per outer row.

- This example is correlated because it references c.id.

## Ex2:

```
SELECT *
FROM employees e
WHERE e.salary > (
  SELECT AVG(salary) FROM employees
);
```

- The subquery returns a single number: average salary.

- All employees above that are returned.

- This is an uncorrelated scalar subquery — evaluated once.

#  Problem with Correlated Scalar Subqueries

## 1. Inefficient Version:

```
SELECT name,
       (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) AS order_count
FROM customers c;
```

- PostgreSQL executes the inner query for every row in customers.

- For 100,000 customers, this runs 100,000 subqueries.

- Even with indexes, this is slow for large tables.

## 2. Optimized with JOIN + GROUP BY

```
SELECT c.id, c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id;
```

- Faster because:

    - One scan of each table

    - Uses efficient join algorithm

    - No repeated execution


## 3. Common Table Expressions (CTEs)

A Common Table Expression is a temporary result set defined using WITH that can be referenced within the same query.

```
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
```

Think of it like defining a subquery but giving it a name you can reuse.

## 1. Ex:

```
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '7 days'
)
SELECT customer_id, COUNT(*) 
FROM recent_orders 
GROUP BY customer_id;
```

## 2. Recursive CTEs

Use when you need to work with hierarchical or tree-structured data (e.g., org charts, folder structures, dependencies).

Example: Employee hierarchy

```
WITH RECURSIVE employee_hierarchy AS (
    -- Anchor member (top-level boss)
    SELECT id, name, manager_id
    FROM employees
    WHERE id = 1

    UNION ALL

    -- Recursive member
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN employee_hierarchy h ON e.manager_id = h.id
)
SELECT * FROM employee_hierarchy;
```

##  3. Multiple CTEs

You can define more than one CTE:

```
WITH orders_last_month AS (
    SELECT * FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '1 month'
),
high_value_orders AS (
    SELECT * FROM orders_last_month WHERE total_amount > 1000
)
SELECT customer_id, COUNT(*) FROM high_value_orders GROUP BY customer_id;
```

##  4. Modularizing Complex Queries

CTEs break down big, messy queries into readable blocks.

Instead of this:

```
SELECT customer_id, COUNT(*) 
FROM (
    SELECT * 
    FROM orders 
    WHERE total_amount > 1000 
    AND order_date > CURRENT_DATE - INTERVAL '30 days'
) AS o
GROUP BY customer_id;
```

Use this:

```
WITH filtered_orders AS (
    SELECT * FROM orders 
    WHERE total_amount > 1000 
    AND order_date > CURRENT_DATE - INTERVAL '30 days'
)
SELECT customer_id, COUNT(*) 
FROM filtered_orders 
GROUP BY customer_id;
```

# Practice optimazition

```
#100,000 rows
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    city TEXT
);
#500,000 rows
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    amount NUMERIC(10, 2),
    status TEXT,
    created_at TIMESTAMP
);

#Insert
INSERT INTO customers (name, city)
SELECT
    'Customer ' || gs,
    CASE
        WHEN gs % 10 = 0 THEN 'New York'
        WHEN gs % 10 = 1 THEN 'Los Angeles'
        WHEN gs % 10 = 2 THEN 'Chicago'
        WHEN gs % 10 = 3 THEN 'Houston'
        WHEN gs % 10 = 4 THEN 'Phoenix'
        ELSE 'City ' || (gs % 100)
    END
FROM generate_series(1, 100000) AS gs;

INSERT INTO orders (customer_id, amount, status, created_at)
SELECT
    (random() * 99999 + 1)::INT,  -- customer_id from 1 to 100000
    round((random() * 1000 + 10)::numeric, 2), -- amount between 10 and 1010, rounded to 2 decimals
    CASE
        WHEN random() < 0.7 THEN 'COMPLETED'
        WHEN random() < 0.9 THEN 'PENDING'
        ELSE 'CANCELLED'
    END,
    NOW() - (random() * INTERVAL '365 days')  -- Random date within last year
FROM generate_series(1, 500000);

```

## Scalar query(very slow)

```
SELECT c.id, c.name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
FROM customers c
LIMIT 100;
```

## Optimized join version:

```
SELECT c.id, c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id
LIMIT 100;
```