-- ================================================================
-- Drop bank_db (If Exists)
-- ================================================================

DROP DATABASE IF EXISTS bank_db;




-- ================================================================
-- Create bank_db
-- ================================================================

-- database
CREATE DATABASE bank_db;
USE bank_db;

-- tables
CREATE TABLE customer (
    customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(100),
    contact_information VARCHAR(50),
    date_of_birth DATE
);

CREATE TABLE branch (
    branch_ID INT AUTO_INCREMENT PRIMARY KEY,
    branch_address VARCHAR(100),
    contact_information VARCHAR(50)
);

CREATE TABLE employee (
    employee_ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    job_title VARCHAR(50),
    hire_date DATE,
    contact_information VARCHAR(50),
    branch_ID INT,
    FOREIGN KEY (branch_ID) REFERENCES branch(branch_ID)
);

CREATE TABLE account (
    account_number INT PRIMARY KEY,
    account_type VARCHAR(20),
    balance DECIMAL(15, 2),
    date_opened DATE,
    customer_ID INT,
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID)
);

CREATE TABLE transaction (
    transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type VARCHAR(20),
    transaction_amount DECIMAL(15, 2),
    transaction_date DATE,
    account_number INT,
    FOREIGN KEY (account_number) REFERENCES account(account_number)
);

CREATE TABLE loan (
    loan_ID INT AUTO_INCREMENT PRIMARY KEY,
    loan_amount DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    term INT,
    repayment_schedule DATE,
    customer_ID INT,
    employee_ID INT,
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID),
    FOREIGN KEY (employee_ID) REFERENCES employee(employee_ID)
);




-- ================================================================
-- Create Stored Procedures
-- ================================================================

-- set delimiter
DELIMITER //

-- account
CREATE PROCEDURE create_account(
    IN p_account_number INT,
    IN p_account_type VARCHAR(20),
    IN p_balance DECIMAL(15, 2),
    IN p_date_opened DATE,
    IN p_customer_ID INT
)
BEGIN
    INSERT INTO account(account_number, account_type, balance, date_opened, customer_ID)
    VALUES (p_account_number, p_account_type, p_balance, p_date_opened, p_customer_ID);
END //

-- customer
CREATE PROCEDURE add_customer(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_address VARCHAR(100),
    IN p_contact_information VARCHAR(50),
    IN p_date_of_birth DATE
)
BEGIN
    INSERT INTO customer(first_name, last_name, address, contact_information, date_of_birth)
    VALUES (p_first_name, p_last_name, p_address, p_contact_information, p_date_of_birth);
END //

CREATE PROCEDURE update_customer(
    IN p_customer_ID INT,
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_address VARCHAR(100),
    IN p_contact_information VARCHAR(50),
    IN p_date_of_birth DATE
)
BEGIN
    UPDATE customer
    SET
        first_name = p_first_name,
        last_name = p_last_name,
        address = p_address,
        contact_information = p_contact_information,
        date_of_birth = p_date_of_birth
    WHERE customer_ID = p_customer_ID;
END //

CREATE PROCEDURE delete_customer(
    IN p_customer_ID INT
)
BEGIN
    START TRANSACTION;
        DELETE FROM transaction WHERE account_number IN (SELECT account_number FROM account WHERE customer_ID = p_customer_ID);
        DELETE FROM account WHERE customer_ID = p_customer_ID;
        DELETE FROM loan WHERE customer_ID = p_customer_ID;
        DELETE FROM customer WHERE customer_ID = p_customer_ID;
    COMMIT;
END //

-- transfer funds
CREATE PROCEDURE transfer_funds(
    IN p_from_account_number INT,
    IN p_to_account_number INT,
    IN p_amount DECIMAL(15, 2)
)
BEGIN
    DECLARE p_transaction_ID INT;
    START TRANSACTION;
        -- withdraw from the source
        UPDATE account SET balance = balance - p_amount WHERE account_number = p_from_account_number;
        -- deposit to the destination
        UPDATE account SET balance = balance + p_amount WHERE account_number = p_to_account_number;
        -- record the transaction
        INSERT INTO transaction(transaction_type, transaction_amount, transaction_date, account_number)
        VALUES ('Transfer', p_amount, NOW(), p_from_account_number);
        SET p_transaction_ID = LAST_INSERT_ID();
        INSERT INTO transaction(transaction_type, transaction_amount, transaction_date, account_number)
        VALUES ('Deposit', p_amount, NOW(), p_to_account_number);
    COMMIT;
    SELECT * FROM transaction WHERE transaction_ID = p_transaction_ID;
END //

-- loan
CREATE PROCEDURE create_loan(
    IN p_customer_ID INT,
    IN p_loan_amount DECIMAL(15, 2),
    IN p_interest_rate DECIMAL(5, 2),
    IN p_term INT,
    IN p_repayment_schedule DATE,
    IN p_employee_ID INT
)
BEGIN
    INSERT INTO loan(customer_ID, loan_amount, interest_rate, term, repayment_schedule, employee_ID)
    VALUES (p_customer_ID, p_loan_amount, p_interest_rate, p_term, p_repayment_schedule, p_employee_ID);
END //

-- reset delimeter
DELIMITER ;




-- ================================================================
-- Create Views
-- ================================================================

CREATE VIEW employees_with_branch AS
SELECT
    e.employee_ID,
    e.first_name,
    e.last_name,
    e.job_title,
    e.hire_date,
    e.contact_information,
    b.branch_ID,
    b.branch_address
FROM employee e
JOIN branch b ON e.branch_ID = b.branch_ID;


CREATE VIEW customer_account_balances AS
SELECT
    c.customer_ID,
    c.first_name,
    c.last_name,
    SUM(a.balance) as total_balance
FROM customer c
JOIN account a ON c.customer_ID = a.customer_ID
GROUP BY c.customer_ID, c.first_name, c.last_name;


CREATE VIEW transactions_with_account_customer_details AS
SELECT
    t.transaction_ID,
    t.transaction_type,
    t.transaction_amount,
    t.transaction_date,
    a.account_number,
    a.account_type,
    c.customer_ID,
    c.first_name,
    c.last_name
FROM transaction t
JOIN account a ON t.account_number = a.account_number
JOIN customer c ON a.customer_ID = c.customer_ID;


CREATE VIEW loans_with_customer_details AS
SELECT
    l.loan_ID,
    l.customer_ID,
    c.first_name,
    c.last_name,
    l.loan_amount,
    l.interest_rate,
    l.term,
    l.repayment_schedule,
    l.employee_ID
FROM loan l
JOIN customer c ON l.customer_ID = c.customer_ID;




-- ================================================================
-- Init
-- ================================================================

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




-- ================================================================
-- Testing
-- ================================================================

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
