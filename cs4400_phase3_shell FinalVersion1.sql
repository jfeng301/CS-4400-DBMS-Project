-- CS4400: Introduction to Database Systems
-- Bank Management Project - Phase 3 (v2)
-- Generating Stored Procedures & Functions for the Use Cases
-- April 4th, 2022

-- implement these functions and stored procedures on the project database
use bank_management;

-- [1] create_corporation()
-- This stored procedure creates a new corporation
drop procedure if exists create_corporation;
delimiter //
create procedure create_corporation (in ip_corpID varchar(100),
    in ip_shortName varchar(100), in ip_longName varchar(100),
    in ip_resAssets integer)
p1: begin
	-- Implement your code here
    if ip_corpID not in (select ip_corpID from corporation)
    then leave p1; end if;
    
    insert into corporation values (ip_corpID, ip_shortName, ip_longName, ip_resAssets);
end //
delimiter ;

-- [2] create_bank()
-- This stored procedure creates a new bank that is owned by an existing corporation
-- The corporation must also be managed by a valid employee [being a manager doesn't leave enough time for other jobs]
drop procedure if exists create_bank;
delimiter //
create procedure create_bank (in ip_bankID varchar(100), in ip_bankName varchar(100),
	in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_resAssets integer, in ip_corpID varchar(100),
    in ip_manager varchar(100), in ip_bank_employee varchar(100))
p2: begin
	-- Implement your code here
    if ip_corpID not in (select corpID from corporation where corpID = ip_corpID)
    then leave p2; end if;
    
    if (select count(*) from bank where manager = ip_bank_employee) >= 1
    then leave p2; end if;
    
    if ip_bankID not in (select ip_bankID from bank)
    then leave p2; end if;
    
    insert into bank values (ip_bankID, ip_bankName, ip_street, ip_city, ip_state, ip_zip, ip_resAssets, ip_corpID, ip_manager);
    
    if ip_bankID not in (select ip_bankID from workFor)
    then leave p2; end if;
    
    insert into workFor values (ip_bankID, ip_bank_employee);
end //
delimiter ;

-- [3] start_employee_role()
-- If the person exists as an admin or employee then don't change the database state [not allowed to be admin along with any other person-based role]
-- If the person doesn't exist then this stored procedure creates a new employee
-- If the person exists as a customer then the employee data is added to create the joint customer-employee role
drop procedure if exists start_employee_role;
delimiter //
create procedure start_employee_role (in ip_perID varchar(100), in ip_taxID char(11),
	in ip_firstName varchar(100), in ip_lastName varchar(100), in ip_birthdate date,
    in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_dtJoined date, in ip_salary integer,
    in ip_payments integer, in ip_earned integer, in emp_password  varchar(100))
p3: begin
	-- Implement your code here
    if ip_perID in (select perID from system_admin) or ip_perID in (select perID from employee)
    then leave p3; end if;
    
    if ip_perID not in (select perID from person)
    then
    insert into person values (ip_perID, emp_password);
    insert into bank_user values (ip_perID, ip_taxID, ip_birthdate, ip_firstName, ip_lastName, ip_dtJoined, ip_street, ip_city, ip_state, ip_zip);
	insert into employee values (ip_perID, ip_salary, ip_payments, ip_earned);
    
    elseif ip_perID in (select perID from customer)
    then
    insert into employee values (ip_perID, ip_salary, ip_payment, ip_earned);
    end if;
end //
delimiter ;

-- [4] start_customer_role()
-- If the person exists as an admin or customer then don't change the database state [not allowed to be admin along with any other person-based role]
-- If the person doesn't exist then this stored procedure creates a new customer
-- If the person exists as an employee then the customer data is added to create the joint customer-employee role
drop procedure if exists start_customer_role;
delimiter //
create procedure start_customer_role (in ip_perID varchar(100), in ip_taxID char(11),
	in ip_firstName varchar(100), in ip_lastName varchar(100), in ip_birthdate date,
    in ip_street varchar(100), in ip_city varchar(100), in ip_state char(2),
    in ip_zip char(5), in ip_dtJoined date, in cust_password varchar(100))
p4: begin
	-- Implement your code here
    if ip_perID in (select perID from system_admin)  or ip_perID in (select perID from customer)
    then leave p4; end if;
    
    if ip_perID not in (select perID from person)
    then
    insert into person values (ip_perID, cust_password);
    insert into bank_user values (ip_perID, ip_taxID, ip_birthdate, ip_firstName, ip_lastName, ip_dtJoined, ip_street, ip_city, ip_state, ip_zip);
	insert into customer values (ip_perID);
    
    elseif ip_perID in (select perID from employee)
    then
    insert into customer values (ip_perID);
    end if;
end //
delimiter ;

-- [5] stop_employee_role()
-- If the person doesn't exist as an employee then don't change the database state
-- If the employee manages a bank or is the last employee at a bank then don't change the database state [each bank must have a manager and at least one employee]
-- If the person exists in the joint customer-employee role then the employee data must be removed, but the customer information must be maintained
-- If the person exists only as an employee then all related person data must be removed
drop procedure if exists stop_employee_role;
delimiter //
create procedure stop_employee_role (in ip_perID varchar(100))
p5: begin
	-- Implement your code here
	if ip_perID not in (select perID from employee) or ip_perID in (select manager from bank)
    then leave p5; end if;
    
    if 1 in ( select count(*) from workfor where bankID in ( select bankID from workfor where perID = ip_perID ) group by bankID )
    then leave p5; end if;
    
    if ip_perID in (select perID from customer)
    then 
    delete from employee where perID = ip_perID;
    delete from workfor where perID = ip_perID;
	else
    delete from workfor where perID = ip_perID;
    delete from access where perID = ip_perID;
    delete from employee where perID = ip_perID;
    delete from bank_user where perID = ip_perID;
    delete from person where perID = ip_perID;
 end if;

end //
delimiter ;

-- [6] stop_customer_role()
-- If the person doesn't exist as an customer then don't change the database state
-- If the customer is the only holder of an account then don't change the database state [each account must have at least one holder]
-- If the person exists in the joint customer-employee role then the customer data must be removed, but the employee information must be maintained
-- If the person exists only as a customer then all related person data must be removed
drop procedure if exists stop_customer_role;
delimiter //
create procedure stop_customer_role (in ip_perID varchar(100))
precedure_6: begin
	-- Implement your code here
	-- If the person exists as a employee then don't change the database state
    if ip_perID not in (select perid from customer) then leave precedure_6; 
    -- only holder? 检查唯一
    -- elseif ((select count(*) from employee) = 1)  then leave precedure_6; 
    elseif ip_perID in (select perID from access group by bankID, accountID having count(*) = 1) then leave precedure_6;    
    elseif ip_perID in (select perid from system_admin) then leave precedure_6; 
    -- only keep as customer
    elseif ip_perID in (select perid from employee) then delete from customer where perid = ip_perID; 
    
    -- If the person exists only as a customer then all related person data must be removed
    -- only as customer

    end if;
    delete from access where perID = ip_perID;
    delete from customer_contacts where perID = ip_perID;
    delete from customer where perID = ip_perID;
    delete from bank_user where perID = ip_perID;
    delete from person where perID = ip_perID;

end //
delimiter ;

-- [7] hire_worker()
-- If the person is not an employee then don't change the database state
-- If the worker is a manager then then don't change the database state [being a manager doesn't leave enough time for other jobs]
-- Otherwise, the person will now work at the assigned bank in addition to any other previous work assignments
-- Also, adjust the employee's salary appropriately
drop procedure if exists hire_worker;
delimiter //
create procedure hire_worker (in ip_perID varchar(100), in ip_bankID varchar(100),
	in ip_salary integer)
p7: begin
	-- Implement your code here
    if ip_perID not in (select perID from employee) or (select count(*) from bank where manager = ip_perID) >= 1
    then leave p7; end if;

    insert into workfor values (ip_bankID, ip_perID);
    update employee 
    set salary = ifnull(salary , 0) + ip_salary
    where perID = ip_perID;
end //
delimiter ;

-- [8] replace_manager()
-- If the new person is not an employee then don't change the database state
-- If the new person is a manager or worker at any bank then don't change the database state [being a manager doesn't leave enough time for other jobs]
-- Otherwise, replace the previous manager at that bank with the new person
-- The previous manager's association as manager of that bank must be removed
-- Adjust the employee's salary appropriately
drop procedure if exists replace_manager;
delimiter //
create procedure replace_manager (in ip_perID varchar(100), in ip_bankID varchar(100),
	in ip_salary integer)
p8: begin
	-- Implement your code here
    if ip_perID not in (select perID from employee)
    then leave p8; 
    
    elseif (select count(*) from bank where manager = ip_perID) >= 1 or (select count(*) from workfor where perID = ip_perID) >= 1
    then leave p8; end if;
    
    update bank set manager = ip_perID where bankID = ip_bankID;
    update employee set salary = ifnull(salary ,0) + ip_salary where perID = ip_perID;
    
end //
delimiter ;

-- [9] add_account_access()
-- If the account does not exist, create a new account. If the account exists, add the customer to the account
-- When creating a new account:
    -- If the person opening the account is not an admin then don't change the database state
    -- If the intended customer (i.e. ip_customer) is not a customer then don't change the database state
    -- Otherwise, create a new account owned by the designated customer
    -- The account type will be determined by the enumerated ip_account_type variable
    -- ip_account_type in {checking, savings, market}
-- When adding a customer to an account:
    -- If the person granting access is not an admin or someone with access to the account then don't change the database state
    -- If the intended customer (i.e. ip_customer) is not a customer then don't change the database state
    -- Otherwise, add the new customer to the existing account
drop procedure if exists add_account_access;
delimiter //
create procedure add_account_access (in ip_requester varchar(100), in ip_customer varchar(100),
	in ip_account_type varchar(10), in ip_bankID varchar(100),
    in ip_accountID varchar(100), in ip_balance integer, in ip_interest_rate integer,
    in ip_dtDeposit date, in ip_minBalance integer, in ip_numWithdrawals integer,
    in ip_maxWithdrawals integer, in ip_dtShareStart date)
p9: begin
	-- Implement your code here
    if ip_requester not in (select * from system_admin) 
    then leave p9; end if;
    
    if ip_customer not in (select * from customer)
    then leave p9; end if;
    
    if ip_accountID not in (select accountID from bank_account) and ip_account_type = 'checking' then 
    insert into bank_account values (ip_bankID, ip_accountID, ip_balance);
    insert into checking values (ip_bankID, ip_accountID, null, null,null, null);
    insert into access values (ip_customer, ip_bankID, ip_accountID, ip_dtShareStart, null);
    
    elseif ip_accountID not in (select accountID from bank_account) and ip_account_type = 'savings' then 
    insert into bank_account values (ip_bankID, ip_accountID, ip_balance);
    insert into interest_bearing values (ip_bankID, ip_accountID, ip_interest_rate, ip_dtDeposit);
    insert into savings values (ip_bankID, ip_accountID, ip_minBalance);
    insert into access values (ip_customer, ip_bankID, ip_accountID, ip_dtShareStart, null);
    
    elseif ip_accountID not in (select accountID from bank_account) and ip_account_type = 'market' then
    insert into bank_account values (ip_bankID, ip_accountID, ip_balance); 
    insert into interest_bearing values (ip_bankID, ip_accountID, ip_interest_rate, ip_dtDeposit);
    insert into market values (ip_bankID, ip_accountID, ip_maxWithdrawals, ip_numWithdrawals);
    insert into access values (ip_customer, ip_bankID, ip_accountID, ip_dtShareStart, null);
    
    elseif ip_accountID in (select accountID from bank_account) then
    insert into access values (ip_customer, ip_bankID, ip_accountID, ip_dtShareStart, null);
    end if;
end //
delimiter ;

-- [10] remove_account_access()
-- Remove a customer's account access. If they are the last customer with access to the account, close the account
-- When just revoking access:
    -- If the person revoking access is not an admin or someone with access to the account then don't change the database state
    -- Otherwise, remove the designated sharer from the existing account
-- When closing the account:
    -- If the customer to be removed from the account is NOT the last remaining owner/sharer then don't close the account
    -- If the person closing the account is not an admin or someone with access to the account then don't change the database state
    -- Otherwise, the account must be closed
drop procedure if exists remove_account_access;
delimiter //
create procedure remove_account_access (in ip_requester varchar(100), in ip_sharer varchar(100),
	in ip_bankID varchar(100), in ip_accountID varchar(100))
p10: begin
	-- Implement your code here
    if ip_requester not in (select perID from system_admin) and 
    ip_requester not in (select perID from access where bankID = ip_bankID and accountID =ip_accountID)
    then leave p10; end if;
    
    if (select user_count from
    (select count(distinct perID) as user_count, bankID, accountID from access group by bankID, accountID) as counts 
    where bankID = ip_bankID and accountID = ip_accountID)  > 1 
    
    then 
    delete from access where perID = ip_sharer and bankID = ip_bankID and accountID = ip_accountID;
    
    elseif (select user_count from
    (select count(distinct perID) as user_count, bankID, accountID from access group by bankID, accountID) as counts 
    where bankID = ip_bankID and accountID = ip_accountID)  = 1
    
    then
    delete from access where perID = ip_sharer and bankID = ip_bankID and accountID = ip_accountID;
    delete from checking where bankID = ip_bankID and accountID = ip_accountID;
    delete from savings where bankID = ip_bankID and accountID = ip_accountID;
    delete from market where bankID = ip_bankID and accountID = ip_accountID;
    delete from interest_bearing_fees where bankID = ip_bankID and accountID = ip_accountID;
    delete from interest_bearing where bankID = ip_bankID and accountID = ip_accountID;
    delete from bank_account where bankID = ip_bankID and accountID = ip_accountID;
	end if;
    
    
end //
delimiter ;

-- [11] create_fee()
drop procedure if exists create_fee;
delimiter //
create procedure create_fee (in ip_bankID varchar(100), in ip_accountID varchar(100),
	in ip_fee_type varchar(100))
begin
	-- Implement your code here
    insert into interest_bearing_fees values (ip_bankID, ip_accountID, ip_fee_type);
end //
delimiter ;

-- [12] start_overdraft()
drop procedure if exists start_overdraft;
delimiter //
create procedure start_overdraft (in ip_requester varchar(100),
	in ip_checking_bankID varchar(100), in ip_checking_accountID varchar(100),
    in ip_savings_bankID varchar(100), in ip_savings_accountID varchar(100))
p12: begin
	-- Implement your code here 
    if ip_requester not in (select perID from access where bankID = ip_savings_bankID and accountID =ip_savings_accountID)
    then leave p12; end if;
    
    update checking 
    set protectionBank = ip_savings_bankID, protectionAccount = ip_savings_accountID
    where bankID = ip_checking_bankID and accountID = ip_checking_accountID;
    
    
end //
delimiter ;

-- [13] stop_overdraft()
drop procedure if exists stop_overdraft;
delimiter //
create procedure stop_overdraft (in ip_requester varchar(100),
	in ip_checking_bankID varchar(100), in ip_checking_accountID varchar(100))
p13: begin
	-- Implement your code here
    if ip_requester not in (select perID from access where bankID = ip_checking_bankID and accountID =ip_checking_accountID)
    then leave p13; end if;
    
    update checking 
    set protectionBank = null, protectionAccount = null
    where bankID = ip_checking_bankID and accountID = ip_checking_accountID;
end //
delimiter ;

-- [14] account_deposit()
-- If the person making the deposit does not have access to the account then don't change the database state
-- Otherwise, the account balance and related info must be modified appropriately
drop procedure if exists account_deposit;
delimiter //
create procedure account_deposit (in ip_requester varchar(100), in ip_deposit_amount integer,
	in ip_bankID varchar(100), in ip_accountID varchar(100), in ip_dtAction date)
p14: begin
	-- Implement your code here	
	-- No Access?
    if ip_requester not in (select perid from access where bankID=ip_bankID and accountID= ip_accountID) then leave p14; 
    end if;

    UPDATE bank_account SET balance=ifnull(balance,0)+ip_deposit_amount where bankID= ip_bankID and accountID = ip_accountID; 
    UPDATE access SET dtAction = ip_dtAction where perID=ip_requester and bankID= ip_bankID and accountID = ip_accountID;

end //
delimiter ;

-- [15] account_withdrawal()
-- If the person making the withdrawal does not have access to the account then don't change the database state
-- If the withdrawal amount is more than the account balance for a savings or market account then don't change the database state [the account balance must be positive]
-- If the withdrawal amount is more than the account balance + the overdraft balance (i.e., from the designated savings account) for a checking account then don't change the database state [the account balance must be positive]
-- Otherwise, the account balance and related info must be modified appropriately (amount deducted from the primary account first, and second from the overdraft account as needed)
drop procedure if exists account_withdrawal;
delimiter //
create procedure account_withdrawal (in ip_requester varchar(100), in ip_withdrawal_amount integer,
	in ip_bankID varchar(100), in ip_accountID varchar(100), in ip_dtAction date)

p15: begin
	-- Implement your code here
       if ip_requester not in ( select perID from access where bankID = ip_bankID and accountID = ip_accountID ) 
       then leave p15;
    end if;
    
    if ip_dtAction is not null
    then
 update access
    set dtAction = ip_dtAction
    where perID = ip_requester and bankID = ip_bankID and accountID = ip_accountID;
    end if;
    
    if ip_accountID in ( select accountID from bank_account where accountID like ('%savings%') )
    then
  if ip_withdrawal_amount > (select ifnull(balance,0) from bank_account where bankID = ip_bankID and accountID = ip_accountID ) 
   then leave p15;
        else
   update bank_account
   set balance = balance - ip_withdrawal_amount
   where bankID = ip_bankID and accountID = ip_accountID;
  end if;
  end if;
     
 if ip_accountID in ( select accountID from market )
    then
  if ip_withdrawal_amount <= (select ifnull(balance,0) from bank_account where bankID = ip_bankID and accountID = ip_accountID ) 
        then
   update bank_account
   set balance = balance - ip_withdrawal_amount
   where bankID = ip_bankID and accountID = ip_accountID;
            
            update market
            set numWithdrawals = numWithdrawals + 1
            where bankID = ip_bankID and accountID = ip_accountID;
            
        else leave p15;
  end if;
  end if;
           
    if ip_accountID in ( select accountID from checking)
    then
  if ip_withdrawal_amount > (select ifnull(balance,0) from bank_account where bankID = ip_bankID and accountID=ip_accountID)
        + (select ifnull(balance,0) from bank_account 
           where bankID in (select protectionBank from checking where bankID = ip_bankID) 
           and accountID in (select protectionAccount from checking where accountID = ip_accountID))
  then leave p15;
  
   elseif ip_withdrawal_amount > (select ifnull(balance,0) from bank_account where bankID = ip_bankID and accountID=ip_accountID)
      and ip_withdrawal_amount <= (select ifnull(balance,0) from bank_account where bankID = ip_bankID and accountID=ip_accountID)
          + (select ifnull(balance,0) from bank_account 
             where bankID in (select protectionBank from checking where bankID = ip_bankID) 
                   and accountID in (select protectionAccount from checking where accountID = ip_accountID))
  then
   update checking , bank_account
   set checking.amount = ip_withdrawal_amount - bank_account.balance , checking.dtOverdraft = ip_dtAction , bank_account.balance = 0
   where checking.bankID = ip_bankID and checking.accountID = ip_accountID and bank_account.bankID = ip_bankID and bank_account.accountID = ip_accountID;
            
            update checking , bank_account
            set balance = balance - amount
            where checking.bankID = ip_bankID and checking.accountID = ip_accountID and bank_account.bankID in (select protectionBank from checking where bankID = ip_bankID) 
           and bank_account.accountID in (select protectionAccount from checking where accountID = ip_accountID);
   
   update checking , access
            set dtAction = ip_dtAction
            where access.bankID in (select protectionBank from checking where bankID = ip_bankID) and access.accountID in (select protectionAccount from checking where accountID = ip_accountID);

 else
   update bank_account
   set balance = balance - ip_withdrawal_amount
   where bankID = ip_bankID and accountID = ip_accountID;
   end if;
 end if;

end //
delimiter ;

-- call account_withdrawal('owalter6', 1500, 'BA_West', "checking_A", "2022-02-02");

-- [16] account_transfer()
-- If the person making the transfer does not have access to both accounts then don't change the database state
-- If the withdrawal amount is more than the account balance for a savings or market account then don't change the database state [the account balance must be positive]
-- If the withdrawal amount is more than the account balance + the overdraft balance (i.e., from the designated savings account) for a checking account then don't change the database state [the account balance must be positive]
-- Otherwise, the account balance and related info must be modified appropriately (amount deducted from the withdrawal account first, and second from the overdraft account as needed, and then added to the deposit account)
drop procedure if exists account_transfer;
delimiter //
create procedure account_transfer (in ip_requester varchar(100), in ip_transfer_amount integer,
	in ip_from_bankID varchar(100), in ip_from_accountID varchar(100),
    in ip_to_bankID varchar(100), in ip_to_accountID varchar(100), in ip_dtAction date)
precedure_16: begin
	-- Implement your code here
	-- cmaxbalance in (select minBalance from saving where bankID = ip_from_bankID);
    -- No Access?
    if ip_requester not in (select perid from access where bankID=ip_from_bankID and accountID= ip_from_accountID) then leave precedure_16; 
    end if;
    if ip_requester not in (select perid from access where bankID=ip_to_bankID and accountID= ip_to_accountID) then leave precedure_16; 
    end if;
    -- no enough account balance for savings
    -- no enough account balance for marketing
    -- bank_account
    if ip_transfer_amount > (select ifnull(balance,0) from bank_account where bankID = ip_from_bankID and accountID=ip_from_accountID)  
    then leave precedure_16; 
    end if;
    
     if ip_transfer_amount > (select ifnull(balance,0) from bank_account where bankID = ip_from_bankID and accountID=ip_from_accountID)
   + (select ifnull(balance,0) from bank_account 
   where bankID in (select protectionBank from checking where bankID = ip_from_bankID) 
   and accountID in (select protectionAccount from checking where accountID = ip_from_accountID))
   then leave precedure_16; 
   
   update checking set dtOverdraft=ip_dtAction where bankID=ip_from_bankID and accountID=ip_from_accountID;
   end if;
   
   UPDATE bank_account SET balance=ifnull(balance,0)-ip_transfer_amount where bankID= ip_from_bankID and accountID = ip_from_accountID; 
   UPDATE bank_account SET balance=ifnull(balance,0)+ip_transfer_amount where bankID=ip_to_bankID and accountID= ip_to_accountID; 
   UPDATE access SET dtAction = ip_dtAction where perID=ip_requester and bankID= ip_from_bankID and accountID = ip_from_accountID;
   UPDATE access SET dtAction = ip_dtAction where perID=ip_requester and bankID=ip_to_bankID and accountID= ip_to_accountID; 

end //
delimiter ;

-- [17] pay_employees()
-- Increase each employee's pay earned so far by the monthly salary
-- Deduct the employee's pay from the banks reserved assets
-- If an employee works at more than one bank, then deduct the (evenly divided) monthly pay from each of the affected bank's reserved assets
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists pay_employees;
delimiter //
create procedure pay_employees ()
begin
    -- Implement your code here
    update employee 
    set earned = case when salary is null then earned
					  when salary is not null then earned + salary
                      end,
	    payments  = case when payments is null then 1
						 when payments is not null then payments + 1
                         end;
        
	with new_pays as (select b.bankID as new_bankID, ifnull(resAssets,0)- pays as new_assets from bank as b left join 
    (select bankID, perID, sum(truncate(split,0)) as pays 
    from workFor natural left join 
    (select perID, salary/count(*) as split 
    from workFor natural left join employee 
    group by perID) as sp group by bankID) as p on b.bankID = p.bankID)
    
    update bank
    left join new_pays on bank.bankID = new_pays.new_bankID
    set bank.resAssets = new_pays.new_assets;
    
    
end //
delimiter ;

-- [18] penalize_accounts()
-- For each savings account that is below the minimum balance, deduct the smaller of $100 or 10% of the current balance from the account
-- For each market account that has exceeded the maximum number of withdrawals, deduct the smaller of $500 per excess withdrawal or 20% of the current balance from the account
-- Add all deducted amounts to the reserved assets of the bank that owns the account
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists penalize_accounts;
delimiter //
create procedure penalize_accounts ()
begin
	-- Implement your code here
    update bank
    set resAssets = 0
    where resAssets is null;
    
	update bank
	left join bank_account 
	on  bank.bankID = bank_account.bankID 
	left join savings
	on bank_account.bankID = savings.bankID and bank_account.accountID = savings.accountID
	left join market
	on bank_account.bankID = market.bankID and bank_account.accountID = market.accountID
    set bank.resAssets = truncate(ifnull(bank.resAssets,0) + least(ifnull(bank_account.balance * 0.1,0), 100),0)
    where ifnull(bank_account.balance,0) < ifnull(savings.minBalance,0);
    
	update bank
	left join bank_account  
	on  bank.bankID = bank_account.bankID 
	left join savings
	on bank_account.bankID = savings.bankID and bank_account.accountID = savings.accountID
	left join market
	on bank_account.bankID = market.bankID and bank_account.accountID = market.accountID
    set bank.resAssets = truncate(ifnull(bank.resAssets,0) + least(ifnull(bank_account.balance,0) * 0.2, (ifnull(numWithdrawals,0)-ifnull(maxWithdrawals,0))* 500),0)
    where ifnull(market.numWithdrawals,0) > ifnull(market.maxWithdrawals,0);
    
    update bank_account 
    left join savings using (bankID, accountID)
    set bank_account.balance = truncate(ifnull(bank_account.balance,0) - least(ifnull(bank_account.balance * 0.1,0), 100),0)
    where ifnull(bank_account.balance,0) < ifnull(savings.minBalance,0);
    
    update bank_account 
    left join market using (bankID, accountID)
    set bank_account.balance = truncate(bank_account.balance - least(ifnull(bank_account.balance,0) * 0.2, (ifnull(numWithdrawals,0)-ifnull(maxWithdrawals,0))* 500),0)
    where ifnull(market.numWithdrawals,0) > ifnull(market.maxWithdrawals,0);
 
end //
delimiter ;

-- [19] accrue_interest()
-- For each interest-bearing account that is "in good standing", increase the balance based on the designated interest rate
-- A savings account is "in good standing" if the current balance is equal to or above the designated minimum balance
-- A market account is "in good standing" if the current number of withdrawals is less than or equal to the maximum number of allowed withdrawals
-- Subtract all paid amounts from the reserved assets of the bank that owns the account                                                                       
-- Truncate any fractional results to an integer before further calculations
drop procedure if exists accrue_interest;
delimiter //
create procedure accrue_interest ()
begin
	-- Implement your code here
    update bank
    set resAssets = 0
    where resAssets is null;
    
	update bank
	join bank_account 
	on bank.bankID = bank_account.bankID 
	right join savings
	on bank_account.bankID = savings.bankID and bank_account.accountID = savings.accountID
    join interest_bearing
	on bank_account.bankID = interest_bearing.bankID and bank_account.accountID = interest_bearing.accountID
    set bank.resAssets = ifnull(bank.resAssets,0) - ifnull(truncate(bank_account.balance  * interest_rate/100, 0),0)
    where bank_account.balance >= savings.minBalance;
    
	update bank
	join bank_account  
	on  bank.bankID = bank_account.bankID 
	right join market
	on bank_account.bankID = market.bankID and bank_account.accountID = market.accountID
    join interest_bearing
	on bank_account.bankID = interest_bearing.bankID and bank_account.accountID = interest_bearing.accountID
    set bank.resAssets = ifnull(bank.resAssets,0) - ifnull(truncate(bank_account.balance  * interest_rate/100, 0),0)
    where ifnull(market.numWithdrawals,0) <= ifnull(market.maxWithdrawals,0);
    
    update bank_account 
    right join savings using (bankID, accountID)
    join interest_bearing
	on bank_account.bankID = interest_bearing.bankID and bank_account.accountID = interest_bearing.accountID
    set bank_account.balance = ifnull(bank_account.balance,0) + ifnull(truncate(bank_account.balance  * interest_rate/100, 0),0)
    where bank_account.balance >= savings.minBalance;
    
    update bank_account 
    right join market using (bankID, accountID)
    join interest_bearing
	on bank_account.bankID = interest_bearing.bankID and bank_account.accountID = interest_bearing.accountID
    set bank_account.balance = ifnull(bank_account.balance,0) + ifnull(truncate(bank_account.balance  * interest_rate/100, 0),0)
    where ifnull(market.numWithdrawals,0) <= ifnull(market.maxWithdrawals,0);
end //
delimiter ;

-- [20] display_account_stats()
-- Display the simple and derived attributes for each account, along with the owning bank
create or replace view display_account_stats as
    -- Uncomment above line and implement your code here
	select bankName as Name_of_bank, ba.accountID as account_identifier ,max(balance) as account_assets, count(*) as number_of_owner 
	from bank_account as ba
	right join bank as b on b.bankID=ba.bankID
	right join access as a on a.accountID=ba.accountID and b.bankID=a.bankID
	group by ba.bankID, ba.accountID;
-- [21] display_bank_stats()
-- Display the simple and derived attributes for each bank, along with the owning corporation
create or replace view display_bank_stats as
    -- Uncomment above line and implement your code here
	select b.bankID as bank_identifier, shortName as name_of_corporation, bankName as name_of_bank, street, city, state, zip, NULLIF(count(accountID), 0) as number_of_account, b.resAssets as bank_assets , ifnull(b.resAssets, 0) + ifnull(sum(balance),0) as total_assets
	from bank as b
	join corporation as c on b.corpID=c.corpID
	left join bank_account as ba on ba.bankID=b.bankID
	group by b.bankID;
-- [22] display_corporation_stats()
-- Display the simple and derived attributes for each corporation
create or replace view display_corporation_stats as
    -- Uncomment above line and implement your code here
	select c.corpID as corporation_identifier, shortName as short_name, longName as formal_name, NULLIF(count(b.bankID),0) as number_of_banks, c.resAssets as corporation_assets, ifnull(sum(bs.total_assets),0)+ c.resAssets as total_assets
	from corporation as c 
	left join bank as b on b.corpID=c.corpID
	left join display_bank_stats as bs on bs.bank_identifier=b.bankID
	group by c.corpID;
-- [23] display_customer_stats()
-- Display the simple and derived attributes for each customer
create or replace view display_customer_stats as
    -- Uncomment above line and implement your code here
	select c.perID as person_identifier, taxID as tax_identifier, concat(firstName, " ", lastName) as customer_name, birthdate as date_of_birth, dtJoined as joined_system, street, city, state, zip, NULLIF(count(ba.accountID),0) as number_of_accounts, IFNULL(sum(balance),0) as customer_assets
	from access as a
	right join customer as c on a.perID=c.perID
	left join bank_user as bu on c.perID=bu.perID
	left join bank_account as ba on ba.bankID=a.bankID and ba.accountID=a.accountID
	group by c.perID;
-- [24] display_employee_stats()
-- Display the simple and derived attributes for each employee
create or replace view display_employee_stats as
    -- Uncomment above line and implement your code here
	select e.perID as person_identifier, taxID as tax_identifier, concat(firstName, " ", lastName) as customer_name, birthdate as date_of_birth, dtJoined as joined_system, bu.street, bu.city, bu.state, bu.zip, NULLIF(count(b.bankID),0) as number_of_banks, sum(bs.total_assets) as bank_assets
    from employee as e
	left join bank_user as bu on e.perID=bu.perID
	left join workfor as w on w.perID=e.perID
	left join bank as b on b.bankID=w.bankID
	left join display_bank_stats as bs on bs.bank_identifier=b.bankID
	group by e.perID;