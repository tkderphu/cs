

# What is procedure

A procedure in PostgreSQL is a database object that contains a set of SQL statements that can perform actions such as inserting, updating, deleting, and transaction control (BEGIN, COMMIT, ROLLBACK).

Unlike functions, procedures do not return values and are called with CALL.


# Common structure

```
CREATE [OR REPLACE] PROCEDURE procedure_name(
    [param_name param_type [IN|OUT|INOUT], ...]
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- variable declarations
BEGIN
    -- procedural logic
END;
$$;

```

# Parameters
- IN (default): Input only

- OUT: Output only

- INOUT: Both input and output

```
(a INTEGER, b INTEGER, OUT result INTEGER)
```

# LANGUAGE plpgsql

Specifies that this is written in PL/pgSQL, the PostgreSQL procedural language.

#  AS ...

The body of the procedure goes between the dollar quotes.

# DECLARE block
Optional. Used to declare local variables.

```
DECLARE
    total INTEGER := 0;
```

# BEGIN ... END block

Required. Contains the actual code/logic.

```
BEGIN
    total := a + b;
END;
```

# Simple Procedure Example

```
CREATE OR REPLACE PROCEDURE log_user_activity(user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO user_logs(user_id, log_time)
    VALUES (user_id, CURRENT_TIMESTAMP);
END;
$$;
```

## Call it

```
CALL log_user_activity(1);  
```