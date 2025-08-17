CREATE PROCEDURE transfer_money(sender INT, receiver INT, amount NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    sender_balance NUMERIC;
BEGIN
    SELECT balance INTO sender_balance FROM accounts WHERE id = sender;

    IF sender_balance < amount THEN
        RAISE EXCEPTION 'Insufficient funds: %', sender_balance;
    END IF;

    UPDATE accounts SET balance = balance - amount WHERE id = sender;
    UPDATE accounts SET balance = balance + amount WHERE id = receiver;

    RAISE NOTICE 'Transferred % from % to %', amount, sender, receiver;
END;
$$;



create procedure get_balance(account_id numeric, out account_balance numeric)
language plpgsql
as $$
begin
    select balance into account_balance 
    from accounts 
    where id = account_id;
end
$$;


/**
 Problem Description:
You want to transfer money from one account to another, but only if:
    The sender has enough balance
    Both accounts exist
    The system should rollback if anything fails

We'll use a stored procedure to:
    Validate balances
    Update both accounts atomically
    Log the transfer
    Handle errors gracefully
**/

create or replace procedure transfer_money(sender numeric, receiver numeric, amount numeric)
language plpgsql
as $$
DECLARE
    sender_balance numeric;
begin
    begin
        start transaction;

        select balance into sender_balance
        from accounts where id = sender;

        if not found then
            raise exception 'Not found acount with id: %s', sender;
        end if;

        if balance < amount then
            raise exception 'No enough funds';
        end if;

        select 1 from accounts where id = receiver;

        if not found then 
            raise exception 'Not found account with id: %', receiver;
        end if;

        update accounts set balance = balance - amount where id = sender;
        update accounts set balance = balance + amount where id = receiver;

        commit;
    
    EXCEPTION WHEN  OTHERS THEN
        ROLLBACK;
        INSERT INTO transfer_log(sender_id, receiver_id, amount)
        values(sender, receiver, amount);

        RAISE NOTICE 'Error when transfer money from account %s to %s with error: %', sender, receiver, SQLERRM;
    end ;
end;
$$;