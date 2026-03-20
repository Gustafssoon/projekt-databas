from app.models.game import Game
from app.models.season import Season
from app.services.mappers import build_season
from app.extensions import db
from app.models.player import Player
from app.models.team import Team
from app.services.nhl_client import get_player, get_teams, get_team_schedule
from app.services.mappers import map_player, map_team, map_game


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
