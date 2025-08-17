# What is function

A function in PostgreSQL is a stored piece of code that performs a task and can return a value. Functions allow you to encapsulate logic, reuse it, and execute complex operations inside the database.

# Why Use Functions?

- Reusability: Write logic once and call it anywhere.

- Performance: Runs on the database server, reducing network round trips.

- Encapsulation: Hide complex logic from application code.

- Can return values or tables.

# Syntax

```
CREATE [OR REPLACE] FUNCTION function_name (param1 type, param2 type, ...)
RETURNS return_type
LANGUAGE plpgsql
AS $$
BEGIN
    -- Your logic here
    RETURN some_value;
END;
$$;
```

## Key Parts:

- CREATE FUNCTION: Define a new function.

- OR REPLACE: Optional – update an existing function.

- RETURNS: Data type of the returned value (can be void if nothing is returned).

- LANGUAGE: Language used – usually plpgsql, but can be SQL, C, etc.

- `$$ ... $$: Function body (block of code).`


## Exampple

## E1: create function calculate two number

```
create function add(x int, y int)
returns int
language plpgsql
as $$
begin
    return x + y;
end;
$$;

## call function
select add(5, 5); #return 10
```

## E2: check even

```
create function check_even(x int)
returns text
language plpgsql
as $$
begin
    if x % 2 = 0 then
        return 'Even';
    else
        return 'Odd';
    end if;
end;
$$;
```

## E3: return table

```
CREATE OR REPLACE FUNCTION get_customers_by_city(city_name TEXT)
RETURNS TABLE(id INT, name TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, name FROM customers WHERE city = city_name;
END;
$$;


#call
SELECT * FROM get_customers_by_city('New York');
```

# Different between function and procedure


- Function: Must return a value (or table).

- Procedure (introduced in PostgreSQL 11): Doesn't return values but can use transactions with CALL.