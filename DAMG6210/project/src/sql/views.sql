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
