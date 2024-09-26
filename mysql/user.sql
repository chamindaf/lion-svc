CREATE SCHEMA `lb-outlet-dev` ;

CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(255), 
    email VARCHAR(255) UNIQUE, 
    first_name VARCHAR(255), 
    last_name VARCHAR(255),
    vendor_id INT,
    company VARCHAR(255),
    contact INT,
    hashed_password VARCHAR(255), 
    is_temp_password BOOLEAN, 
    is_active BOOLEAN, 
    created_by VARCHAR(255), 
    created_on DATETIME, 
    updated_by VARCHAR(255), 
    updated_on DATETIME
);


INSERT INTO user (
    role,
    email, 
    first_name, 
    last_name,
    vendor_id,
    company,
    contact,
    hashed_password, 
    is_temp_password, 
    is_active, 
    created_by, 
    created_on, 
    updated_by, 
    updated_on
) VALUES (
    "Admin",
    'admin@example.com',
    'Admin',
    'User',
    1,
    "Lion",
    0789652635,
    '$2b$12$g7Y.yQIULLh5i4lPFh6Nr.8SCDah7yHTBhfcrbz/1kOeHfqEKsyHO',
    FALSE,
    TRUE,
    'System',
    NOW(),
    'System',
    NOW()
);


SELECT * FROM user;

UPDATE user
SET is_active = TRUE
WHERE user_id = 42;

TRUNCATE TABLE user;

DELETE FROM user WHERE user_id != 1;