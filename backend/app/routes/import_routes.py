from flask import Blueprint

from app.services.import_service import (
    import_player,
    import_team_by_abbreviation,
    import_season,
    import_games_for_team_and_season,
    import_player_team_season,
    import_team_game_stats,
    import_player_game_stats,
    import_season_basics,
    import_season_stats_limited,
)

import_bp = Blueprint("import", __name__)


@import_bp.route("/import-player/<int:player_id>")
def import_player_route(player_id):
    player = import_player(player_id)
    return {
        "message": "Player imported successfully",
        "player_id": player.player_id,
        "name": f"{player.first_name} {player.last_name}",
    }


@import_bp.route("/import-team/<string:team_code>")
def import_team_route(team_code):
    team = import_team_by_abbreviation(team_code)
    return {
        "message": "Team imported successfully",
        "team_id": team.team_id,
        "name": team.name,
        "abbreviation": team.abbreviation,
    }


@import_bp.route("/import-season/<int:season_id>")
def import_season_route(season_id):
    season = import_season(season_id)
    return {
        "message": "Season imported successfully",
        "season_id": season.season_id,
        "label": season.label,
    }


@import_bp.route("/import-games/<string:team_code>/<int:season_id>")
def import_games_route(team_code, season_id):
    count = import_games_for_team_and_season(team_code, season_id)
    return {
        "message": "Games imported successfully",
        "team_code": team_code.upper(),
        "season_id": season_id,
        "count": count,
    }


@import_bp.route("/import-roster/<string:team_code>/<int:season_id>")
def import_roster_route(team_code, season_id):
    count = import_player_team_season(team_code, season_id)
    return {
        "message": "Roster imported successfully",
        "team_code": team_code.upper(),
        "season_id": season_id,
        "count": count,
    }


@import_bp.route("/import-team-game-stats/<int:game_id>")
def import_team_game_stats_route(game_id):
    count = import_team_game_stats(game_id)
    return {
        "message": "Team game stats imported successfully",
        "game_id": game_id,
        "count": count,
    }


@import_bp.route("/import-player-game-stats/<int:game_id>")
def import_player_game_stats_route(game_id):
    count = import_player_game_stats(game_id)
    return {
        "message": "Player game stats imported successfully",
        "game_id": game_id,
        "count": count,
    }


@import_bp.route("/import-season-basics/<string:team_code>/<int:season_id>")
def import_season_basics_route(team_code, season_id):
    result = import_season_basics(team_code, season_id)
    return {
        "message": "Season basics imported successfully",
        **result,
    }


@import_bp.route("/import-season-stats-test/<string:team_code>/<int:season_id>")
def import_season_stats_test_route(team_code, season_id):
    result = import_season_stats_limited(team_code, season_id, limit=5)
    return {
        "message": "Season stats test import completed successfully",
        **result,
    }
