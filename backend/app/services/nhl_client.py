import requests


BASE_URL = "https://api-web.nhle.com/v1"
STATS_BASE_URL = "https://api.nhle.com/stats/rest/en"


def get_player(player_id: int) -> dict:
    url = f"{BASE_URL}/player/{player_id}/landing"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_teams() -> dict:
    url = f"{STATS_BASE_URL}/team"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_team_schedule(team_code: str, season_id: int) -> dict:
    url = f"{BASE_URL}/club-schedule-season/{team_code}/{season_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_game_landing(game_id: int) -> dict:
    url = f"{BASE_URL}/gamecenter/{game_id}/landing"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_game_right_rail(game_id: int) -> dict:
    url = f"{BASE_URL}/gamecenter/{game_id}/right-rail"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_team_roster(team_code: str, season_id: int) -> dict:
    url = f"{BASE_URL}/roster/{team_code}/{season_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_game_boxscore(game_id: int) -> dict:
    url = f"{BASE_URL}/gamecenter/{game_id}/boxscore"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
