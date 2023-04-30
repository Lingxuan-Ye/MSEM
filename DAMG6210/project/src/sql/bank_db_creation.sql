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
