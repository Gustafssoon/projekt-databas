from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ..extensions import db
from ..models.player import Player
from ..models.team import Team
from ..models.season import Season
from ..models.game import Game
from ..models.player_team_season import PlayerTeamSeason
from ..models.player_game_stats import PlayerGameStats
from ..models.team_game_stats import TeamGameStats


def setup_admin(app):
    admin = Admin(app, name="NHL Admin")

    admin.add_view(ModelView(Player, db.session))
    admin.add_view(ModelView(Team, db.session))
    admin.add_view(ModelView(Season, db.session))
    admin.add_view(ModelView(Game, db.session))
    admin.add_view(ModelView(PlayerTeamSeason, db.session))
    admin.add_view(ModelView(PlayerGameStats, db.session))
    admin.add_view(ModelView(TeamGameStats, db.session))
