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
