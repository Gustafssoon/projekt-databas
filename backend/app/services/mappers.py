from datetime import date, datetime
from datetime import datetime


def parse_birth_date(value):
    if not value:
        return None

    # NHL API brukar ge datum som YYYY-MM-DD
    return datetime.strptime(value, "%Y-%m-%d").date()


def map_player(api_data: dict) -> dict:
    return {
        "player_id": api_data["playerId"],
        "first_name": api_data["firstName"]["default"],
        "last_name": api_data["lastName"]["default"],
        "birth_date": parse_birth_date(api_data.get("birthDate")),
        "nationality": api_data.get("birthCountry", "Unknown"),
        "shoot_catches": api_data.get("shootsCatches", "Unknown"),
        "primary_position": api_data.get("position", "Unknown"),
        "active": api_data.get("isActive", True),
    }


def map_team(api_team: dict) -> dict:
    return {
        "team_id": api_team["id"],
        "name": api_team["fullName"],
        # tillfällig fallback, byt om du hittar bättre city-fält
        "city": api_team["triCode"],
        "abbreviation": api_team["triCode"],
    }


def build_season(season_id: int) -> dict:
    season_str = str(season_id)
    start_year = int(season_str[:4])
    end_year = int(season_str[4:])

    return {
        "season_id": season_id,
        "label": f"{start_year}/{end_year}",
        "start_date": date(start_year, 10, 1),
        "end_date": date(end_year, 6, 30),
        "is_current": False,
    }


def parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def map_game(game_data: dict) -> dict:
    return {
        "game_id": game_data["id"],
        "home_team_id": game_data["homeTeam"]["id"],
        "away_team_id": game_data["awayTeam"]["id"],
        "season_id": game_data["season"],
        "game_date": parse_date(game_data["gameDate"]),
        "game_type": str(game_data.get("gameType", "Unknown")),
        "status": game_data.get("gameState", "Unknown"),
        "home_score": game_data["homeTeam"].get("score", 0),
        "away_score": game_data["awayTeam"].get("score", 0),
        "overtime_flag": game_data.get("periodDescriptor", {}).get("periodType") == "OT",
        "shootout_flag": game_data.get("gameOutcome", {}).get("lastPeriodType") == "SO",
    }


def map_player_team_season(player_id: int, team_id: int, season_id: int, player_data: dict) -> dict:
    return {
        "player_id": player_id,
        "team_id": team_id,
        "season_id": season_id,
        "jersey_number": str(player_data.get("sweaterNumber")) if player_data.get("sweaterNumber") else None,
        "listed_position": player_data.get("positionCode"),
        "start_date": None,
        "end_date": None,
    }
