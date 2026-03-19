from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa

from .models.player import Player
from .extensions import db, migrate
from config import Config
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

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
