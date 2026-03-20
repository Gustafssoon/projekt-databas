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
from .services.import_service import import_player, import_team_by_abbreviation, import_season


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

    return app
