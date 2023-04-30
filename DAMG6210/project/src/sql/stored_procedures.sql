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
