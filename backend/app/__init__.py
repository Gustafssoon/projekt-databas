from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa

from .models.player import Player
from .models.team import Team
from .models.season import Season
from .models.game import Game
from .models.player_team_season import PlayerTeamSeason
from .models.player_game_stats import PlayerGameStats
from .models.team_game_stats import TeamGameStats
from .extensions import db, migrate
from config import Config
from flask import Flask, jsonify
from .admin import setup_admin
from .services.import_service import (import_player, import_team_by_abbreviation,
                                      import_season, import_games_for_team_and_season, import_player_team_season, import_team_game_stats, import_player_game_stats,)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    setup_admin(app)

    @app.route("/")
    def index():
        return "NHL backend running"

    @app.route("/players")
    def get_players():
        players = Player.query.all()

        data = [
            {
                "player_id": p.player_id,
                "first_name": p.first_name,
                "last_name": p.last_name,
            }
            for p in players
        ]

        return jsonify(data)

    @app.route("/import-player/<int:player_id>")
    def import_player_route(player_id):
        player = import_player(player_id)
        return {
            "message": "Player imported successfully",
            "player_id": player.player_id,
            "name": f"{player.first_name} {player.last_name}",
        }

    @app.route("/import-team/<team_code>")
    def import_team_route(team_code):
        team = import_team_by_abbreviation(team_code)
        return {
            "message": "Team imported successfully",
            "team_id": team.team_id,
            "name": team.name,
            "abbreviation": team.abbreviation,
        }

    @app.route("/import-season/<int:season_id>")
    def import_season_route(season_id):
        season = import_season(season_id)
        return {
            "message": "Season imported successfully",
            "season_id": season.season_id,
            "label": season.label,
        }

    @app.route("/import-games/<team_code>/<int:season_id>")
    def import_games_route(team_code, season_id):
        count = import_games_for_team_and_season(team_code, season_id)
        return {
            "message": "Games imported successfully",
            "team_code": team_code.upper(),
            "season_id": season_id,
            "count": count,
        }

    @app.route("/import-roster/<team_code>/<int:season_id>")
    def import_roster_route(team_code, season_id):
        count = import_player_team_season(team_code, season_id)
        return {
            "message": "Roster imported successfully",
            "team_code": team_code.upper(),
            "season_id": season_id,
            "count": count,
        }

    @app.route("/import-team-game-stats/<int:game_id>")
    def import_team_game_stats_route(game_id):
        count = import_team_game_stats(game_id)
        return {
            "message": "Team game stats imported successfully",
            "game_id": game_id,
            "count": count,
        }

    @app.route("/import-player-game-stats/<int:game_id>")
    def import_player_game_stats_route(game_id):
        count = import_player_game_stats(game_id)
        return {
            "message": "Player game stats imported successfully",
            "game_id": game_id,
            "count": count,
        }

    return app
