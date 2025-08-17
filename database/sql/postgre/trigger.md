# Note about trigger

A trigger in PostgreSQL is a mechanism that automatically executes a function when a specific events occurs on a table or view.

Events can be:

- DML: About operations SELECT, UPDATE, INSERT, UPDATE, TRUNCATE,..

- DDL: About operations for definition scheme(CREATE TABLE, DROP TABLE, ALTER TABLE, ALTER COLUMN)

# Core component


A trigger has three core parts:

## 1. Trigger Function

- A function (usually written in plpgsql) that contains the logic to execute.

- Must return a special type:

    - TRIGGER for row-level triggers

        - Row-level triggers fire for each row affected by a INSERT, UPDATE, or DELETE statement.

        - Inside the trigger function, PostgreSQL provides two special variables:

            - NEW → the new row (for INSERT and UPDATE)

            - OLD → the existing row (for UPDATE and DELETE)

    - VOID for statement-level triggers
        
        - A statement-level trigger fires once per SQL statement, regardless of how many rows are affected. Ex: If you insert 100 rows, the trigger fires only once.

## 2. Trigger Event

The event(s) that activate the trigger:

- BEFORE or AFTER an INSERT, UPDATE, DELETE, or TRUNCATE

- Can be row-level (per row) or statement-level (per query)

## 3. Trigger Definition

Binds the trigger function to a table (or view) and specifies the event(s).


## Execution flows

```
1. A user/application issues a DML command:
     INSERT INTO users VALUES (...);

2. PostgreSQL checks:
     Does this table have a trigger for this event?

3. If YES:
     - Fire any BEFORE triggers first
     - Perform the actual data modification
     - Fire any AFTER triggers

4. Row-level triggers:
     Fire once per row affected.

5. Statement-level triggers:
     Fire once per statement.
```

# Example

## Row-level

```
CREATE OR REPLACE FUNCTION check_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email NOT LIKE '%@%' THEN
        RAISE EXCEPTION 'Invalid email address';
    END IF;

    RETURN NEW; -- allow insert to proceed
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_email_check
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION check_email();
```

## Statement level

```
CREATE OR REPLACE FUNCTION log_statement()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO logs(event, created_at)
    VALUES ('A statement modified the users table', NOW());
END;
$$;


CREATE TRIGGER users_stmt_log
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH STATEMENT
EXECUTE FUNCTION log_statement();

INSERT INTO users(name, age)
VALUES ('Alice', 22), ('Bob', 30);
```