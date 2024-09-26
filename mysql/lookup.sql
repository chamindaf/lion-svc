CREATE TABLE IF NOT EXISTS Lookup (
    lookup_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255), 
    display_value VARCHAR(255), 
    sort INT, 
    is_active BOOLEAN, 
    created_by VARCHAR(255), 
    created_on DATETIME
);

INSERT INTO Lookup (category, display_value, sort, is_active, created_by, created_on) 
VALUES 
('UserRole', 'Admin', 1, TRUE, 'system', NOW()),
('UserRole', 'Designer', 2, TRUE, 'system', NOW()),
('UserRole', 'Supplier', 3, TRUE, 'system', NOW()),
('UserRole', 'TM', 4, TRUE, 'system', NOW()),
('UserRole', 'CDM', 5, TRUE, 'system', NOW()),
('UserRole', 'Auditor', 6, TRUE, 'system', NOW()),
('Status', 'New', 1, TRUE, 'system', NOW());