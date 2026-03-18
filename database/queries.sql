-- Visa alla spelare
SELECT * FROM player;
-- Visa alla matcher
SELECT * FROM game;
-- Visa spelarstatistik för matchen
SELECT * FROM player_game_stats;
-- Visa lagstatistik för matchen
SELECT * FROM team_game_stats;

-- Visar vilka spelare som har flest poäng under den valda säsongen
SELECT p.player_id, p.first_name, p.last_name, SUM(pgs.points) AS total_points
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id, p.first_name, p.last_name
ORDER BY total_points DESC;

-- Visar vilka spelare som har flest tacklingar under den valda säsongen
SELECT p.player_id, p.first_name, p.last_name, SUM(pgs.hits) AS total_hits
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id, p.first_name, p.last_name
ORDER BY total_hits DESC;

-- Visar matchinformation tillsammans med hemma- och bortalag
SELECT g.game_id, ht.name AS home_team, at.name AS away_team, g.game_date, g.home_score, g.away_score, g.status
FROM game g
JOIN team ht ON g.home_team_id = ht.team_id
JOIN team at ON g.away_team_id = at.team_id;

-- Visar vilket lag varje spelare tillhör under den aktuella säsongen
SELECT p.first_name, p.last_name, t.name AS team_name, s.label AS season_label, pts.jersey_number
FROM player_team_season pts
JOIN player p ON pts.player_id = p.player_id
JOIN team t ON pts.team_id = t.team_id
JOIN season s ON pts.season_id = s.season_id;

-- Poängliga via stored procedure
CALL get_points_leaderboard_by_season(20232024);
