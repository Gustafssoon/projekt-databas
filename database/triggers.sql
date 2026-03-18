DELIMITER $$

-- Sätter points automatiskt vid INSERT
CREATE TRIGGER trg_pre_insert_player_stats
BEFORE INSERT ON player_game_stats
FOR EACH ROW
BEGIN
    SET NEW.points = NEW.goals + NEW.assists;
END$$

-- Sätter points automatiskt vid UPDATE
CREATE TRIGGER trg_pre_update_player_stats
BEFORE UPDATE ON player_game_stats
FOR EACH ROW
BEGIN
    SET NEW.points = NEW.goals + NEW.assists;
END$$

DELIMITER ;
