from flask import Blueprint, jsonify

from app.models.player import Player

basic_bp = Blueprint("basic", __name__)


@basic_bp.route("/")
def index():
    return "NHL backend running"


@basic_bp.route("/players")
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
