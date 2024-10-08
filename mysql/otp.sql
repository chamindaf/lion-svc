CREATE TABLE IF NOT EXISTS Otp (
    otp_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, 
    otp VARCHAR(255),
    attempts INT, 
    created_on DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE EVENT IF NOT EXISTS delete_expired_otp
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 23 HOUR + INTERVAL 59 MINUTE
DO
DELETE FROM Otp
WHERE TIMESTAMPDIFF(MINUTE, created_on, NOW()) > 5;
