from app.extensions import db


class PlayerGameStats(db.Model):
    __tablename__ = "player_game_stats"

    player_game_stats_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey(
        "player.player_id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id"), nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    shots = db.Column(db.Integer, nullable=False)
    hits = db.Column(db.Integer, nullable=False)
    pim = db.Column(db.Integer, nullable=False)
    toi_seconds = db.Column(db.Integer, nullable=False)
    plus_minus = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("game_id", "player_id", name="uq_player_game"),
        db.Index("idx_pgs_player_id", "player_id"),
        db.Index("idx_pgs_game_id", "game_id"),
    )

    def __repr__(self):
        return f"<PlayerGameStats {self.player_game_stats_id}>"
