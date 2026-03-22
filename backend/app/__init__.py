from .routes.import_routes import import_bp
from .routes.basic_routes import basic_bp
from .models.team_game_stats import TeamGameStats
from .models.player_game_stats import PlayerGameStats
from .models.player_team_season import PlayerTeamSeason
from .models.game import Game
from .models.season import Season
from .models.team import Team
from .models.player import Player
from .admin import setup_admin
from .extensions import db, migrate
from config import Config
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    setup_admin(app)

    app.register_blueprint(basic_bp)
    app.register_blueprint(import_bp)

    return app
