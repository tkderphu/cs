# What is index

An index is a data structure maintained by the database engine that stores a mapping of column values to the location (disk block, row ID) of the data in the table.

- Without an index: the database scans every row (full table scan) → slow for large tables.

- With an index: the database searches the index (optimized) → retrieves the row directly.

# Components of an Index

Indexes consist of several components:

- Key:

    - The column(s) on which the index is created.

    - Can be a single column or composite (multi-column).

- Pointer / Row Locator:

    - References the actual data.

    - For a heap table (no clustered index): stores physical row address (file + page + slot).

    - For a table with a clustered index: stores the clustered index key.

- Data Structure:

    - Defines how the index stores keys and pointers.

    - Most common: B+ Tree, others: Hash table, GiST, SP-GiST, BRIN, GIN, Bitmap.

- Pages (Blocks):

    - Indexes are stored in database pages (like tables).

    - Root Page: entry point of the index.

    - Intermediate Pages: internal nodes for traversal.

    - Leaf Pages: contain the actual keys and pointers.

- Statistics:

    - Metadata about index distribution (e.g., number of rows, distinct keys, histogram).

    - Used by query optimizer to choose the best plan.


# Types of Indexes

## 1, By structure

Common strucure is used for building index is B-tree:

- Balanced tree with ordered keys.

- Leaf nodes linked for range scans.

- Used for equality and range queries

## By Logical Type

### 1. Clustered Index

- Defines the physical order of rows in the table.

- Each table can have only one clustered index.

- Leaf nodes contain the actual table data.

### 2. Non-Clustered Index

- Separate structure from the table.

- Leaf nodes contain pointers (row locators) to table rows.

### 3. Unique Index

- Enforces uniqueness on column(s).

### 4. Composite Index

- Indexes multiple columns together.

    - Its stores a combined key of the columns in a single B+ tree
    - usefull when queries filter or sort on multiple columns together
    - Ex:

    ```
    CREATE INDEX idx_users_name_dob 
    ON users(last_name, first_name, date_of_birth);
    ```

    Keys are ordered by lastname -> first_name, date_of_birth

- Index usage:


    - Best when the query uses the leftmost prefix of the columns.

    - Example index (last_name, first_name, date_of_birth):

    - Query on last_name → can use index.

    - Query on last_name AND first_name → can use index.

    - Query on first_name only → cannot use index (no leading column).

    - Query on first_name AND date_of_birth → cannot (skips left column).

This is called the leftmost prefix rule.

### 5. Covering Index

- An index that includes extra columns needed by a query. These extra columns are stored only at the leaf level.

- Avoids reading the table (index-only scan).

- Ex: 

```
CREATE INDEX idx_users_email_cover 
ON users(email)
INCLUDE (last_name, first_name);
```

- Now the index stores email + last_name and first_name at the leaf level.

- Execution:

    - Index lookup returns last_name and first_name directly from the index.

    - No heap access needed → Index-Only Scan.


### 6. Partial Index (PostgreSQL)

- Index only rows matching a condition (e.g., WHERE active = true).
- Intead of store all rows in index we only specific what rows will be store that meet the condition
- This make index smaller and faster to find targeted queries.

- Syntax:

```
CREATE INDEX index_name 
ON table_name(column_name)
WHERE condition; #expression that determines which rows are indexed
```

### 7. Function-Based Index

- Index on an expression or function result (e.g., LOWER(email)).

- Useful when queries apply a function to a column in the WHERE or ORDER BY clause.

- Avoids recalculating the function and allows the index to be used.


# Type of scan

Scan are how the query engine read table rows

## Major type of scans

### 1. Table Scan
    
- reading data directly one by one from table

### 2. Index scan

- using index for finding data

## 2. Table scan

### 2.1 Sequential scan

- Read every blocks of the table in order, check the row against clause `WHERE` 

### 2.2 Parallel sequential scan

- Multiple workers read different blocks in paralell

- Improve reading for big tables

## 3. Index scan

Indexes avoid scanning the whole table by traversing `B-tree+`

### 3.1 Index scan(plain)

- Traverses the index(from root -> leaf) to find matching keys

- Then fetches each row from table (via TID pointers)

- Good for small sets of rows

### 3.2 Index scan only

- Uses when the index to return data whithout accessing the table

- Work only if:

    - All required columns are in index(covering index)

### 3.3. Bitmap index scan

- Uses a bitmap to mark matching rows from index
- Then reads the required table blocks in sorted order
- Usefull when multiple indexes are combined with `AND/OR`

Example: 

```
SELECT * FROM users WHERE age = 25 AND city = 'Paris';
```

- Both age and city is indexed
- When it look up index then will mark row which match the result to 1 else 0

```
Index on age:
   Matching rows: TIDs (block 2 row 1, block 5 row 3, ...)

Index on city:
   Matching rows: TIDs (block 2 row 1, block 4 row 2, ...)

Build bitmap (bit = 1 = matching row): for age
Block 2: 1 0 0 0 0
Block 5: 0 0 1 0 0

Build bitmap for city
Block2: 1 0 0 0 0
Block4: 0 1 0 0 0

Merge bitmap dependence what type of condition

#If AND => and between bitmap
=> After and we have:
Block2: 1 0 0 0 0
Block4: 0 0 0 0 0
Block5: 0 0 0 0 0

=> Only Block 2 and row 1 is match the result =>get result

#If OR => after or we have:
Block2: 1 0 0 0 0
Block4: 0 1 0 0 0
Block5: 0 0 1 0 0

Once the merged bitmap is ready, PosgreSQL does a bitmap heap scan
```


### 3.4 Index only bitmap scan

This type of index is like index only, specific columns are exists in combine index

## 4. special scan types

### 4.1. TID scan

### 4.2. index forward vs backword scan

### 4.3 Paralell index scan

# Practice

    