-- drop and reconstruct
DROP DATABASE IF EXISTS bank_db;
source ./src/sql/bank_db_creation.sql;
source ./src/sql/stored_procedures.sql;
source ./src/sql/views.sql;


-- add data
INSERT INTO customer (first_name, last_name, address, contact_information, date_of_birth)
VALUES
    ('Thrall', 'Doomhammer', 'Orgrimmar', 'thrall@example.com', '1977-01-01'),
    ('Jaina', 'Proudmoore', 'Theramore', 'jaina@example.com', '1985-05-05'),
    ('Varian', 'Wrynn', 'Stormwind', 'varian@example.com', '1978-12-31'),
    ('Sylvanas', 'Windrunner', 'Undercity', 'sylvanas@example.com', '1998-08-15'),
    ('Illidan', 'Stormrage', 'Outland', 'illidan@example.com', '1975-03-22');

INSERT INTO branch (branch_address, contact_information)
VALUES
    ('Orgrimmar Bank', '555-1234'),
    ('Theramore Bank', '555-5678'),
    ('Stormwind Bank', '555-9012'),
    ('Undercity Bank', '555-3456'),
    ('Shattrath Bank', '555-7890');

INSERT INTO employee (first_name, last_name, job_title, hire_date, contact_information, branch_ID)
VALUES
    ('Garrosh', 'Hellscream', 'Teller', '2020-01-01', 'garrosh@example.com', 1),
    ('Uther', 'Lightbringer', 'Manager', '2010-01-01', 'uther@example.com', 2),
    ('Cairne', 'Bloodhoof', 'Loan Officer', '2015-01-01', 'cairne@example.com', 3),
    ('Arthas', 'Menethil', 'Teller', '2018-01-01', 'arthas@example.com', 4),
    ('Khadgar', 'The Great', 'Manager', '2005-01-01', 'khadgar@example.com', 5);

INSERT INTO account (account_number, account_type, balance, date_opened, customer_ID)
VALUES
    (10001, 'Checking', 1000.00, '2022-01-01', 1),
    (10002, 'Savings', 5000.00, '2021-01-01', 2),
    (10003, 'Checking', 2500.00, '2020-01-01', 3),
    (10004, 'Savings', 10000.00, '2023-01-01', 4),
    (10005, 'Checking', 500.00, '2024-01-01', 5);

INSERT INTO transaction (transaction_type, transaction_amount, transaction_date, account_number)
VALUES
    ('Deposit', 100.00, '2022-02-01', 10001),
    ('Withdrawal', 50.00, '2022-03-01', 10001),
    ('Deposit', 5000.00, '2022-04-01', 10002),
    ('Withdrawal', 1000.00, '2022-05-01', 10002),
    ('Deposit', 250.00, '2022-06-01', 10003),
    ('Withdrawal', 500.00, '2022-07-01', 10003),
    ('Deposit', 20000.00, '2022-08-01', 10004),
    ('Withdrawal', 5000.00, '2022-09-01', 10004),
    ('Deposit', 100.00, '2022-10-01', 10005),
    ('Withdrawal', 25.00, '2022-11-01', 10005);

INSERT INTO loan (loan_amount, interest_rate, term, repayment_schedule, customer_ID, employee_ID)
VALUES
    (10000.00, 0.05, 12, '2023-01-01', 1, 1),
    (5000.00, 0.04, 6, '2022-12-01', 2, 2),
    (25000.00, 0.07, 24, '2024-01-01', 3, 3),
    (100000.00, 0.08, 36, '2025-01-01', 4, 4),
    (500.00, 0.02, 3, '2022-11-01', 5, 5);


-- show tables
\! echo Tables
\! echo ================================
\! echo Customer
SELECT * FROM customer;
\! echo Branch
SELECT * FROM branch;
\! echo Employee
SELECT * FROM employee;
\! echo Account
SELECT * FROM account;
\! echo Transaction
SELECT * FROM transaction;
\! echo Loan
SELECT * FROM loan;


-- test stored procedures
CALL create_account(99999, 'Savings', 5000.00, '2022-01-01', 1);
CALL add_customer('Arthas', 'Menethil', 'Lordaeron City', 'arthas@wow.com', '1979-03-20');
CALL update_customer(1, 'Jaina', 'Proudmoore', 'Theramore Island', 'jaina@wow.com', '1982-06-10');
CALL delete_customer(2);
CALL transfer_funds(10001, 99999, 1000.00);
CALL create_loan(3, 25000.00, 0.07, 24, '2024-01-01', 3);


-- show tables
\! echo Stored Procedures Results
\! echo ================================
\! echo Customer
SELECT * FROM customer;
\! echo Branch
SELECT * FROM branch;
\! echo Employee
SELECT * FROM employee;
\! echo Account
SELECT * FROM account;
\! echo Transaction
SELECT * FROM transaction;
\! echo Loan
SELECT * FROM loan;


-- show views
\! echo Views
\! echo ================================
\! echo Employees With Branch
SELECT * FROM employees_with_branch;
\! echo Customer Account Balances
SELECT * FROM customer_account_balances;
\! echo Transactions With Account Customer Details
SELECT * FROM transactions_with_account_customer_details;
\! echo Loans With Customer Details
SELECT * FROM loans_with_customer_details;


\! echo Test Finished
