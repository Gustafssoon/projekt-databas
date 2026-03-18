DELIMITER $$

CREATE PROCEDURE get_points_leaderboard_by_season(IN in_season_id INT)
BEGIN
    SELECT p.player_id, p.first_name, p.last_name, SUM(pgs.points) AS total_points FROM player_game_stats pgs
    JOIN player p ON p.player_id = pgs.player_id
    JOIN game g ON g.game_id = pgs.game_id
    WHERE g.season_id = in_season_id
    GROUP BY p.player_id, p.first_name, p.last_name
    ORDER BY total_points DESC;
END$$

DELIMITER ;
