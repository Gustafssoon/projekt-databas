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

    return app
