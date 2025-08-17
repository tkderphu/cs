# Postgre SQL

- PostgreSQL is an advanced relational database system.

- PostgreSQL supports both relational (SQL) and non-relational (JSON) queries.

- PostgreSQL is free and open-source.

# Some common commands


## Show all databases

```
/l or /list
```

## Show all tables in specific database

```
\dt
```

## Switching among databases

```
\c database_name 
```

## Create database

```
CREATE TABLE TABLE_NAME (
  column_name DATA_TYPE
);
```

Example:

```
CREATE TABLE Products(
    id INT,
    name VARCHAR(255)
);
```

## Insert data

```
INSERT INTO Products(id, name)
VALUES (1, 'Test'), (2, 'TEST 2');
```

## Fetch data

```
SELECT id FROM Products; #only fetch id
SELECT * FROM Products; #fetch all column
```

## Add New Column

```
ALTER TABLE Products
ADD description VARCHAR(255);
```

## Update data

```
UPDATE Products SET description = 'hello guys'
WHERE id = 1

## update multiple column

UPDATE Products set name='test23232', description='dasd'
WHERE id = 1
```

## Alter column

- The ALTER TABLE statement is used to add, delete, or modify columns in an existing table.

- The ALTER TABLE statement is also used to add and drop various constraints on an existing table.

Change data type

```
ALTER TABLE Products
ALTER COLUMN id TYPE VARCHAR(4);
```

## Drop column

```
ALTER TABLE products
DROP COLUMN price;
```

## Delete record

```
delete from products
where id = '1'

## Delete all record

delete from products

# we can also achive this method by using truncate

truncate table products
```

## Drop table

```
DROP TABLE Products;
```

# Operator

- =	Equal to
- <	Less than
- $>	Greater than
- <=	Less than or equal to
- $>=	Greater than or equal to
- <>	Not equal to
- !=	Not equal to
- LIKE	Check if a value matches a pattern (case sensitive)
- ILIKE	Check if a value matches a pattern (case insensitive)
- AND	Logical AND
- OR	Logical OR
- IN	Check if a value is between a range of values
- BETWEEN	Check if a value is between a range of values
- IS NULL	Check if a value is NULL
- NOT	Makes a negative result e.g. NOT LIKE, NOT IN, NOT BETWEEN


## The SELECT DISTINCT Statement

The SELECT DISTINCT statement is used to return only distinct (different) values.

# The LIMIT Clause

The LIMIT clause is used to limit the maximum number of records to return.

```
SELECT * FROM customers
LIMIT 20;
```

## Offset

Usually offset is used with limit for start fetching data

```
SELECT * FROM table LIMIT n OFFSET m;

# Start fetch data from (m) records to (m   + n)
```


## Like

The LIKE operator is used in a WHERE clause to search for a specified pattern in a column.

There are two wildcards often used in conjunction with the LIKE operator:

- % The percent sign represents zero, one, or multiple characters
- _ The underscore sign represents one, single character

```
select * from categories where description like '_r%';

# get all records which has second character of description is r
```

## Between

```
select * from products where price between 100 and 200
```

## Alias

```
select count(*) as total_products  from products 

Or 
select count(*) as "Total products"  from products 

# concat two field

select product_name || ' ' || product_price as "Name and Price" from products
```

## CASE claude

Case will through expression and check if true then return.

In case all condition in CASE false then it go to ELSE

If it isn't return value then it should be null

```
SELECT product_name,
CASE
  WHEN price < 10 THEN 'Low price product'
  WHEN price > 50 THEN 'High price product'
ELSE
  'Normal product'
END
FROM products;
```