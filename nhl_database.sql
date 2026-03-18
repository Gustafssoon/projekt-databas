DROP DATABASE nhl_database;
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
    abbreviation VARCHAR(10) NOT NULL
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
