from app.extensions import db


class Game(db.Model):
    __tablename__ = "game"

    game_id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id"), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey(
        "season.season_id"), nullable=False)
    game_date = db.Column(db.Date, nullable=False)
    game_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    overtime_flag = db.Column(db.Boolean, nullable=False)
    shootout_flag = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.Index("idx_game_season_date", "season_id", "game_date"),
    )

    def __repr__(self):
        return f"<Game {self.game_id}>"
