-- Skapa användare
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'editor_user'@'localhost' IDENTIFIED BY 'editor123';
CREATE USER IF NOT EXISTS 'analyst_user'@'localhost' IDENTIFIED BY 'analyst123';

-- Ge admin full tillgång till databasen
GRANT ALL PRIVILEGES ON nhl_database.* TO 'admin_user'@'localhost';

-- Ge editor rätt att läsa och ändra data, men inte droppa tabeller eller hela databasen
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE
ON nhl_database.* TO 'editor_user'@'localhost';

-- Ge analytiker endast läsrättigheter
GRANT SELECT ON nhl_database.* TO 'analyst_user'@'localhost';

FLUSH PRIVILEGES;

-- Test som analyst_user:
-- SELECT * FROM player;

-- Detta ska inte fungera:
-- DELETE FROM player WHERE player_id = 1;
