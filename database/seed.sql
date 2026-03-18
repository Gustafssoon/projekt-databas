-- Lägger in två NHL-lag som ska användas i testmatchen
INSERT INTO team (team_id, name, city, abbreviation)
VALUES
(1, 'Maple Leafs', 'Toronto', 'TOR'),
(2, 'Canadiens', 'Montreal', 'MTL');

-- Lägger in en säsong som matchen och spelarna kopplas till
INSERT INTO season (season_id, label, start_date, end_date, is_current)
VALUES
(20232024, '2023/2024', '2023-10-01', '2024-06-30', TRUE);

-- Lägger in fyra spelare som används i testdatan
INSERT INTO player (player_id, first_name, last_name, birth_date, nationality, shoot_catches, primary_position, active)
VALUES
(101, 'Auston', 'Matthews', '1997-09-17', 'Canada', 'L', 'C', TRUE),
(102, 'Mitch', 'Marner', '1997-05-05', 'Canada', 'R', 'RW', TRUE),
(103, 'Nick', 'Suzuki', '1999-08-10', 'Canada', 'R', 'C', TRUE),
(104, 'Cole', 'Caufield', '2001-01-02', 'USA', 'R', 'RW', TRUE);

-- Kopplar varje spelare till rätt lag och rätt säsong
INSERT INTO player_team_season (player_team_season_id, player_id, team_id, season_id, jersey_number, listed_position, start_date, end_date) 
VALUES
(1, 101, 1, 20232024, '34', 'C', '2023-10-01', NULL),
(2, 102, 1, 20232024, '16', 'RW', '2023-10-01', NULL),
(3, 103, 2, 20232024, '14', 'C', '2023-10-01', NULL),
(4, 104, 2, 20232024, '22', 'RW', '2023-10-01', NULL);

-- Lägger in en match mellan Toronto (hemmalag) och Montreal (bortalag)
INSERT INTO game (game_id, home_team_id, away_team_id, season_id, game_date, game_type, status, home_score, away_score, overtime_flag, shootout_flag)
VALUES
(1001, 1, 2, 20232024, '2023-11-10', 'Regular Season', 'Final', 4, 2, FALSE, FALSE);

-- Points sätts automatiskt av triggern; värdet 999 används bara för att testa att triggern fungerar
INSERT INTO player_game_stats (player_game_stats_id, game_id, player_id, team_id, goals, assists, points, shots, hits, pim, toi_seconds, plus_minus)
VALUES
(1, 1001, 101, 1, 2, 1, 999, 6, 2, 0, 1260, 2),
(2, 1001, 102, 1, 1, 2, 999, 4, 1, 2, 1185, 1),
(3, 1001, 103, 2, 1, 0, 999, 5, 3, 0, 1210, -1),
(4, 1001, 104, 2, 1, 1, 999, 4, 2, 0, 1150, -1);

-- Lägger in lagstatistik för samma match
-- Varje rad representerar ett lags sammanlagda statistik i matchen
INSERT INTO team_game_stats (team_game_stats_id, team_id, game_id, shots, hits, pim, faceoff_win_pct, powerplay_goals, powerplay_opportunities)
VALUES
(1, 1, 1001, 32, 18, 4, 52.30, 1, 3),
(2, 2, 1001, 29, 21, 2, 47.70, 0, 2);
