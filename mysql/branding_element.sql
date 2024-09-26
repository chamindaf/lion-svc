CREATE TABLE IF NOT EXISTS Branding_Elements (
    branding_element_id INT AUTO_INCREMENT PRIMARY KEY,
    req_branding_elements_type_id INT,
    request_id INT,
    branding_element VARCHAR(255),
    created_by VARCHAR(255),
    created_on DATETIME,
    FOREIGN KEY (req_branding_elements_type_id) REFERENCES Request_Branding_Elements_Type(req_branding_elements_type_id),
    FOREIGN KEY (request_id) REFERENCES Request(request_id)
);
