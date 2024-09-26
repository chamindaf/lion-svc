CREATE TABLE IF NOT EXISTS Territory_Info (
    territory_info_id INT NOT NULL AUTO_INCREMENT,
    sfa_territory_id INT NOT NULL,
    territory_code VARCHAR(4) NOT NULL,
    territory VARCHAR(40) NOT NULL,
    PRIMARY KEY (territory_info_id)
);

INSERT INTO Territory_Info (
    sfa_territory_id,
    territory_code,
    territory
) VALUES 
(1, "BORA", "Boralesgamuwa"),
(2, "NEGO", "Negombo"),
(3, "CM15", "Colombo-15"),
(4, "KAND", "Kandy"),
(5, "NUWA", "NuwaraEliya"),
(6, "ANUR", "Anuradapura"),
(7, "CM05", "Colombo-05"),
(8, "GANE", "Ganemulla"),
(9, "GALL", "Galle"),
(10, "RATN", "Rathnapura"),
(11, "CHIL", "Chilaw"),
(12, "KURU", "Kurunagela"),
(13, "TANG", "Tangalle"),
(14, "BADU", "Badulla"),
(15, "BERU", "Beruwala"),
(16, "TRIN", "Trincomalee"),
(17, "JAFF", "Jaffna"),
(18, "BATT", "Batticaloa"),
(19, "LBDI", "LB Direct-Kandy"),
(20, "LBD1", "LB Direct-Boralesgamuwa"),
(21, "LBDF", "LB DPL"),
(22, "LBHD", "LB Heladiv");

CREATE TABLE IF NOT EXISTS Channel_Info (
    channel_info_id INT NOT NULL AUTO_INCREMENT,
    sfa_channel_id INT NOT NULL,
    channel_code VARCHAR(4) NOT NULL,
    channel VARCHAR(40) NOT NULL,
    PRIMARY KEY (channel_info_id)
);

INSERT INTO Channel_Info (
    sfa_channel_id,
    channel_code,
    channel
) VALUES 
(1, "PRHO", "Premium Hotel"),
(2, "PRON", "Premium On"),
(3, "RGOF", "Regular Off"),
(4, "RGON", "Regular On"),
(5, "SUMK", "Super Market"),
(6, "TPTY", "Third Party");

CREATE TABLE IF NOT EXISTS Chain_Info (
    chain_info_id INT NOT NULL AUTO_INCREMENT,
    sfa_chain_id INT NOT NULL,
    chain_code VARCHAR(4) NOT NULL,
    chain_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (chain_info_id)
);

INSERT INTO Chain_Info (
    sfa_chain_id,
    chain_code,
    chain_name
) VALUES
(1, "ABEY", "Abeyrathna"),
(2, "ABW", "Abeyawardena Chain"),
(3, "ACH", "Achmi Chain"),
(4, "AEF", "AEF-Sanjaya Fernando"),
(5, "AEFM", "AEF - Manjula Perera"),
(6, "AEFS", "AEF - Samantha Perera");

CREATE TABLE IF NOT EXISTS Brand_Info (
    brand_info_id INT NOT NULL AUTO_INCREMENT,
    sfa_brand_id INT NOT NULL,
    brand VARCHAR(40) NOT NULL,
    PRIMARY KEY (brand_info_id)
);

INSERT INTO Brand_Info (
    sfa_brand_id,
    brand
) VALUES
(1, "Lion Lager"),
(2, "Carlsberg"),
(3, "Lion Stout"),
(4, "Strong Beer"),
(5, "Non Classified"),
(6, "Carlsberg Special Brew");

CREATE TABLE IF NOT EXISTS Outlet_Info (
    outlet_info_id INT NOT NULL AUTO_INCREMENT,
    sfa_outlet_id INT NOT NULL,
    territory_info_id INT,
    rt_code VARCHAR(8),
    rt_name VARCHAR(40),
    address_line1 VARCHAR(40),
    address_line2 VARCHAR(40),
    address_line3 VARCHAR(40),
    address_line4 VARCHAR(40),
    address_line5 VARCHAR(40),
    channel_info_id INT,
    brand_info_id INT,
    is_chain BOOLEAN,
    chain_info_id INT,
    lat VARCHAR(10),
    lng VARCHAR(11),
    PRIMARY KEY (outlet_info_id),
    FOREIGN KEY (territory_info_id) REFERENCES Territory_Info(territory_info_id),
    FOREIGN KEY (channel_info_id) REFERENCES Channel_Info(channel_info_id),
    FOREIGN KEY (brand_info_id) REFERENCES Brand_Info(brand_info_id),
    FOREIGN KEY (chain_info_id) REFERENCES Chain_Info(chain_info_id)
);

INSERT INTO Outlet_Info (
    sfa_outlet_id,
    territory_info_id,
    rt_code,
    rt_name,
    address_line1,
    address_line2,
    address_line3,
    address_line4,
    address_line5,
    channel_info_id,
    brand_info_id,
    is_chain,
    chain_info_id,
    lat,
    lng
) VALUES
(1, (SELECT territory_info_id FROM Territory_Info WHERE territory_code = "BORA"), 
    "RT000003", "LBCL Boralasgamuwa-Shop Sales", "1065/3A, Kasbawa Road,", "Katuwawala.", NULL, NULL, NULL, 
    (SELECT channel_info_id FROM Channel_Info WHERE channel_code = "RGOF"), 
    NULL, TRUE, 
    (SELECT chain_info_id FROM Chain_Info WHERE chain_code = "ABEY"), 
    "6.9271", "79.8612"),
(2, (SELECT territory_info_id FROM Territory_Info WHERE territory_code = "CM15"), 
    "RT000018", "Waters Edge Ltd.", "Sri Jayawardenapura, Kotte.", "Battaramulla.", NULL, NULL, NULL, 
    (SELECT channel_info_id FROM Channel_Info WHERE channel_code = "PRON"), 
    NULL, FALSE, 
    NULL, "7.2906", "80.6337");
