DROP DATABASE IF EXISTS nhl_database;
CREATE DATABASE nhl_database;
USE nhl_database;

CREATE TABLE player (
    player_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    shoot_catches VARCHAR(20) NOT NULL,
    primary_position VARCHAR(20) NOT NULL,
    active BOOLEAN NOT NULL
);

CREATE TABLE team (
    team_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE season (
    season_id INT PRIMARY KEY,
    label VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL
);

CREATE TABLE player_team_season (
    player_team_season_id INT PRIMARY KEY,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    season_id INT NOT NULL,
    jersey_number VARCHAR(10),
    listed_position VARCHAR(20),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (season_id) REFERENCES season(season_id),
    UNIQUE KEY uq_player_team_season (player_id, team_id, season_id),
    INDEX idx_pts_player_season (player_id, season_id)
);

CREATE TABLE game (
    game_id INT PRIMARY KEY,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    season_id INT NOT NULL,
    game_date DATE NOT NULL,
    game_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    home_score INT NOT NULL,
    away_score INT NOT NULL,
    overtime_flag BOOLEAN NOT NULL,
    shootout_flag BOOLEAN NOT NULL,
    FOREIGN KEY (home_team_id) REFERENCES team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES team(team_id),
    FOREIGN KEY (season_id) REFERENCES season(season_id),
    INDEX idx_game_season_date (season_id, game_date)
);

CREATE TABLE player_game_stats (
    player_game_stats_id INT PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    goals INT NOT NULL,
    assists INT NOT NULL,
    points INT NOT NULL,
    shots INT NOT NULL,
    hits INT NOT NULL,
    pim INT NOT NULL,
    toi_seconds INT NOT NULL,
    plus_minus INT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    UNIQUE KEY uq_player_game (game_id, player_id), -- en spelares statistik i en specifik match
	INDEX idx_pgs_player_id (player_id),
	INDEX idx_pgs_game_id (game_id)
);

CREATE TABLE team_game_stats (
    team_game_stats_id INT PRIMARY KEY,
    team_id INT NOT NULL,
    game_id INT NOT NULL,
    shots INT NOT NULL,
    hits INT NOT NULL,
    pim INT NOT NULL,
    faceoff_win_pct DECIMAL(5,2) NOT NULL,
    powerplay_goals INT NOT NULL,
    powerplay_opportunities INT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    UNIQUE KEY uq_team_game (team_id, game_id)
);

-- ============
--  TRIGGERS
-- ============

DELIMITER $$

CREATE TRIGGER trg_pre_insert_player_stats
BEFORE INSERT ON player_game_stats
FOR EACH ROW
BEGIN
    SET NEW.points = NEW.goals + NEW.assists;
END$$

CREATE TRIGGER trg_pre_update_player_stats
BEFORE UPDATE ON player_game_stats
FOR EACH ROW
BEGIN
    SET NEW.points = NEW.goals + NEW.assists;
END$$

DELIMITER ;

-- ==================
-- STORED PROCEDURES
-- ==================

DELIMITER $$

CREATE PROCEDURE get_points_leaderboard_by_season(IN in_season_id INT)
BEGIN
    SELECT
        p.player_id,
        p.first_name,
        p.last_name,
        SUM(pgs.points) AS total_points
    FROM player_game_stats pgs
    JOIN player p ON p.player_id = pgs.player_id
    JOIN game g ON g.game_id = pgs.game_id
    WHERE g.season_id = in_season_id
    GROUP BY p.player_id, p.first_name, p.last_name
    ORDER BY total_points DESC;
END$$

DELIMITER ;

-- ============
--  TESTDATA
-- ============

INSERT INTO team (team_id, name, city, abbreviation)
VALUES
(1, 'Maple Leafs', 'Toronto', 'TOR'),
(2, 'Canadiens', 'Montreal', 'MTL');

INSERT INTO season (season_id, label, start_date, end_date, is_current)
VALUES
(20232024, '2023/2024', '2023-10-01', '2024-06-30', TRUE);

INSERT INTO player (player_id, first_name, last_name, birth_date, nationality, shoot_catches, primary_position, active)
VALUES
(101, 'Auston', 'Matthews', '1997-09-17', 'Canada', 'L', 'C', TRUE),
(102, 'Mitch', 'Marner', '1997-05-05', 'Canada', 'R', 'RW', TRUE),
(103, 'Nick', 'Suzuki', '1999-08-10', 'Canada', 'R', 'C', TRUE),
(104, 'Cole', 'Caufield', '2001-01-02', 'USA', 'R', 'RW', TRUE);

INSERT INTO player_team_season (
    player_team_season_id,
    player_id,
    team_id,
    season_id,
    jersey_number,
    listed_position,
    start_date,
    end_date
)
VALUES
(1, 101, 1, 20232024, '34', 'C', '2023-10-01', NULL),
(2, 102, 1, 20232024, '16', 'RW', '2023-10-01', NULL),
(3, 103, 2, 20232024, '14', 'C', '2023-10-01', NULL),
(4, 104, 2, 20232024, '22', 'RW', '2023-10-01', NULL);

INSERT INTO game (
    game_id,
    home_team_id,
    away_team_id,
    season_id,
    game_date,
    game_type,
    status,
    home_score,
    away_score,
    overtime_flag,
    shootout_flag
)
VALUES
(1001, 1, 2, 20232024, '2023-11-10', 'Regular Season', 'Final', 4, 2, FALSE, FALSE);

INSERT INTO player_game_stats (
    player_game_stats_id,
    game_id,
    player_id,
    team_id,
    goals,
    assists,
    points,
    shots,
    hits,
    pim,
    toi_seconds,
    plus_minus
)
VALUES
(1, 1001, 101, 1, 2, 1, 999, 6, 2, 0, 1260, 2),
(2, 1001, 102, 1, 1, 2, 999, 4, 1, 2, 1185, 1),
(3, 1001, 103, 2, 1, 0, 999, 5, 3, 0, 1210, -1),
(4, 1001, 104, 2, 1, 1, 999, 4, 2, 0, 1150, -1);

INSERT INTO team_game_stats (
    team_game_stats_id,
    team_id,
    game_id,
    shots,
    hits,
    pim,
    faceoff_win_pct,
    powerplay_goals,
    powerplay_opportunities
)
VALUES
(1, 1, 1001, 32, 18, 4, 52.30, 1, 3),
(2, 2, 1001, 29, 21, 2, 47.70, 0, 2);

-- =========
--  SELECTS
-- =========

SELECT * FROM player;
SELECT * FROM game;
SELECT * FROM player_game_stats;
SELECT * FROM team_game_stats;

SELECT
    p.player_id,
    p.first_name,
    p.last_name,
    SUM(pgs.points) AS total_points
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id, p.first_name, p.last_name
ORDER BY total_points DESC;

SELECT
    p.player_id,
    p.first_name,
    p.last_name,
    SUM(pgs.hits) AS total_hits
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id, p.first_name, p.last_name
ORDER BY total_hits DESC;

SELECT
    g.game_id,
    ht.name AS home_team,
    at.name AS away_team,
    g.game_date,
    g.home_score,
    g.away_score,
    g.status
FROM game g
JOIN team ht ON g.home_team_id = ht.team_id
JOIN team at ON g.away_team_id = at.team_id;

SELECT
    p.first_name,
    p.last_name,
    t.name AS team_name,
    s.label AS season_label,
    pts.jersey_number
FROM player_team_season pts
JOIN player p ON pts.player_id = p.player_id
JOIN team t ON pts.team_id = t.team_id
JOIN season s ON pts.season_id = s.season_id;
