from app.extensions import db


class TeamGameStats(db.Model):
    __tablename__ = "team_game_stats"

    team_game_stats_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id"), nullable=False)
    shots = db.Column(db.Integer, nullable=False)
    hits = db.Column(db.Integer, nullable=False)
    pim = db.Column(db.Integer, nullable=False)
    faceoff_win_pct = db.Column(db.Numeric(5, 2), nullable=False)
    powerplay_goals = db.Column(db.Integer, nullable=False)
    powerplay_opportunities = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("team_id", "game_id", name="uq_team_game"),
    )

    def __repr__(self):
        return f"<TeamGameStats {self.team_game_stats_id}>"
