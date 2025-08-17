# 1. What is transaction

A transaction is a group of SQL statements that execute as a single unit.

- Either all succeed (COMMIT)

- Or all fail and rollback (ROLLBACK)

This guarantees data integrity.


#  2. Basic Transaction Syntax


```
BEGIN;             -- Start the transaction
   SQL statement;
   SQL statement;
COMMIT;            -- Save all changes permanently
```

or using the alias:

```
START TRANSACTION;
   SQL statements...
COMMIT;
```

# 3. Rollback on Error

```
BEGIN;
   SQL statement 1;
   SQL statement 2;   -- Something goes wrong here
ROLLBACK;             -- Undo all changes
```

Example:

```
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```
### If one UPDATE fails, you can run ROLLBACK; to undo everything.

# 4. Savepoints (Partial Rollback)

A savepoint lets you mark a point in a transaction that you can roll back to without canceling the entire transaction.


```
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;

SAVEPOINT sp1;

UPDATE accounts SET balance = balance + 100 WHERE id = 999;  -- fails

ROLLBACK TO sp1;  -- Undo only the failed update

COMMIT;           -- Commit the first update
```

# 5. Transaction inside Procedures

Procedures (unlike functions) can control transactions.

```
CREATE OR REPLACE PROCEDURE test_proc()
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO logs(msg) VALUES('Step 1');

    COMMIT;  -- allowed (procedure ends current transaction)

    INSERT INTO logs(msg) VALUES('Step 2');

EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    RAISE NOTICE 'eRROR';
END;
$$;
```