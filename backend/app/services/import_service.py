from app.models.game import Game
from app.models.season import Season
from app.models.player import Player
from app.models.team import Team
from app.models.team_game_stats import TeamGameStats
from app.models.player_team_season import PlayerTeamSeason
from app.models.player_game_stats import PlayerGameStats
from app.extensions import db
from app.services.nhl_client import get_player, get_teams, get_team_schedule, get_team_roster, get_game_right_rail, get_game_boxscore
from app.services.mappers import map_player, map_team, map_game, build_season, map_player_team_season, extract_team_game_stats, map_team_game_stats, map_player_game_stats


def import_player(player_id: int) -> Player:
    api_data = get_player(player_id)
    mapped = map_player(api_data)

    existing_player = db.session.get(Player, player_id)

    if existing_player:
        for key, value in mapped.items():
            setattr(existing_player, key, value)
        db.session.commit()
        return existing_player

    player = Player(**mapped)
    db.session.add(player)
    db.session.commit()
    return player


def import_team_by_abbreviation(team_code: str) -> Team:
    data = get_teams()
    teams = data.get("data", [])

    match = next((team for team in teams if team.get(
        "triCode") == team_code.upper()), None)
    if not match:
        raise ValueError(f"Team not found: {team_code}")

    mapped = map_team(match)

    existing_team = db.session.get(Team, mapped["team_id"])

    if existing_team:
        for key, value in mapped.items():
            setattr(existing_team, key, value)
        db.session.commit()
        return existing_team

    team = Team(**mapped)
    db.session.add(team)
    db.session.commit()
    return team


def import_season(season_id: int) -> Season:
    mapped = build_season(season_id)

    existing_season = Season.query.get(season_id)

    if existing_season:
        for key, value in mapped.items():
            setattr(existing_season, key, value)
        db.session.commit()
        return existing_season

    season = Season(**mapped)
    db.session.add(season)
    db.session.commit()
    return season


def import_team_by_id(team_id: int) -> Team:
    data = get_teams()
    teams = data.get("data", [])

    match = next((team for team in teams if team.get("id") == team_id), None)
    if not match:
        raise ValueError(f"Team not found with id: {team_id}")

    mapped = map_team(match)

    existing_team = db.session.get(Team, mapped["team_id"])

    if existing_team:
        for key, value in mapped.items():
            setattr(existing_team, key, value)
        db.session.commit()
        return existing_team

    team = Team(**mapped)
    db.session.add(team)
    db.session.commit()
    return team


def import_games_for_team_and_season(team_code: str, season_id: int) -> int:
    import_season(season_id)

    data = get_team_schedule(team_code, season_id)
    games = data.get("games", [])
    imported_count = 0

    for raw_game in games:
        mapped = map_game(raw_game)

        import_team_by_id(mapped["home_team_id"])
        import_team_by_id(mapped["away_team_id"])

        existing_game = db.session.get(Game, mapped["game_id"])

        if existing_game:
            for key, value in mapped.items():
                setattr(existing_game, key, value)
        else:
            db.session.add(Game(**mapped))

        imported_count += 1

    db.session.commit()
    return imported_count


def import_player_team_season(team_code: str, season_id: int) -> int:
    import_season(season_id)

    team = import_team_by_abbreviation(team_code)
    roster_data = get_team_roster(team_code, season_id)

    imported_count = 0

    all_players = []

    for group in roster_data.values():
        if isinstance(group, list):
            all_players.extend(group)

    for player_data in all_players:
        player_id = player_data["id"]

        import_player(player_id)

        mapped = map_player_team_season(
            player_id=player_id,
            team_id=team.team_id,
            season_id=season_id,
            player_data=player_data,
        )

        existing = PlayerTeamSeason.query.filter_by(
            player_id=mapped["player_id"],
            team_id=mapped["team_id"],
            season_id=mapped["season_id"],
        ).first()

        if existing:
            existing.jersey_number = mapped["jersey_number"]
            existing.listed_position = mapped["listed_position"]
            existing.start_date = mapped["start_date"]
            existing.end_date = mapped["end_date"]
        else:
            next_id = db.session.query(db.func.coalesce(db.func.max(
                PlayerTeamSeason.player_team_season_id), 0)).scalar() + 1
            mapped["player_team_season_id"] = next_id
            db.session.add(PlayerTeamSeason(**mapped))

        imported_count += 1

    db.session.commit()
    return imported_count


def import_team_game_stats(game_id: int) -> int:
    data = get_game_right_rail(game_id)

    game = db.session.get(Game, game_id)
    if not game:
        raise ValueError(f"Game {game_id} does not exist in database")

    away_team_id = game.away_team_id
    home_team_id = game.home_team_id

    raw_team_stats = data.get("teamGameStats", [])

    away_stats = extract_team_game_stats(raw_team_stats, "away")
    home_stats = extract_team_game_stats(raw_team_stats, "home")

    rows = [
        map_team_game_stats(game_id, away_team_id, away_stats),
        map_team_game_stats(game_id, home_team_id, home_stats),
    ]

    imported_count = 0

    for mapped in rows:
        existing = TeamGameStats.query.filter_by(
            game_id=mapped["game_id"],
            team_id=mapped["team_id"],
        ).first()

        if existing:
            existing.shots = mapped["shots"]
            existing.hits = mapped["hits"]
            existing.pim = mapped["pim"]
            existing.faceoff_win_pct = mapped["faceoff_win_pct"]
            existing.powerplay_goals = mapped["powerplay_goals"]
            existing.powerplay_opportunities = mapped["powerplay_opportunities"]
        else:
            next_id = (
                db.session.query(
                    db.func.coalesce(db.func.max(
                        TeamGameStats.team_game_stats_id), 0)
                ).scalar()
                + 1
            )

            mapped["team_game_stats_id"] = next_id
            db.session.add(TeamGameStats(**mapped))

        imported_count += 1

    db.session.commit()
    return imported_count


def import_player_game_stats(game_id: int) -> int:
    data = get_game_boxscore(game_id)

    game = db.session.get(Game, game_id)
    if not game:
        raise ValueError(f"Game {game_id} does not exist in database")

    away_team_id = game.away_team_id
    home_team_id = game.home_team_id

    away_team_players = data.get("playerByGameStats", {}).get("awayTeam", {})
    home_team_players = data.get("playerByGameStats", {}).get("homeTeam", {})

    imported_count = 0

    def process_team_players(team_data: dict, team_id: int):
        nonlocal imported_count

        for group_name in ["forwards", "defense", "goalies"]:
            players = team_data.get(group_name, [])

            for player_data in players:
                player_id = player_data["playerId"]

                import_player(player_id)

                mapped = map_player_game_stats(game_id, team_id, player_data)

                existing = PlayerGameStats.query.filter_by(
                    game_id=mapped["game_id"],
                    player_id=mapped["player_id"],
                ).first()

                if existing:
                    existing.team_id = mapped["team_id"]
                    existing.goals = mapped["goals"]
                    existing.assists = mapped["assists"]
                    existing.points = mapped["points"]
                    existing.shots = mapped["shots"]
                    existing.hits = mapped["hits"]
                    existing.pim = mapped["pim"]
                    existing.toi_seconds = mapped["toi_seconds"]
                    existing.plus_minus = mapped["plus_minus"]
                else:
                    next_id = (
                        db.session.query(
                            db.func.coalesce(
                                db.func.max(
                                    PlayerGameStats.player_game_stats_id), 0
                            )
                        ).scalar()
                        + 1
                    )

                    mapped["player_game_stats_id"] = next_id
                    db.session.add(PlayerGameStats(**mapped))

                imported_count += 1

    process_team_players(away_team_players, away_team_id)
    process_team_players(home_team_players, home_team_id)

    db.session.commit()
    return imported_count


def import_season_basics(team_code: str, season_id: int) -> dict:
    import_season(season_id)
    team = import_team_by_abbreviation(team_code)
    roster_count = import_player_team_season(team_code, season_id)
    games_count = import_games_for_team_and_season(team_code, season_id)

    return {
        "team_code": team_code.upper(),
        "season_id": season_id,
        "team_id": team.team_id,
        "roster_count": roster_count,
        "games_count": games_count,
    }


def import_season_stats_limited(team_code: str, season_id: int, limit: int = 5) -> dict:
    team = import_team_by_abbreviation(team_code)

    games = Game.query.filter_by(season_id=season_id).filter(
        (Game.home_team_id == team.team_id) | (
            Game.away_team_id == team.team_id)
    ).limit(limit).all()

    team_game_stats_count = 0
    player_game_stats_count = 0

    for game in games:
        print(f"Importing stats for game {game.game_id}")
        team_game_stats_count += import_team_game_stats(game.game_id)
        player_game_stats_count += import_player_game_stats(game.game_id)

    return {
        "team_code": team_code.upper(),
        "season_id": season_id,
        "games_processed": len(games),
        "team_game_stats_count": team_game_stats_count,
        "player_game_stats_count": player_game_stats_count,
    }
