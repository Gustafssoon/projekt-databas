from app.extensions import db


class PlayerTeamSeason(db.Model):

    __tablename__ = "player_team_season"

    player_team_season_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(
        "player.player_id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id"), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey(
        "season.season_id"), nullable=False)

    jersey_number = db.Column(db.String(10), nullable=True)
    listed_position = db.Column(db.String(20), nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "player_id",
            "team_id",
            "season_id",
            name="uq_player_team_season",
        ),
        db.Index("idx_pts_player_season", "player_id", "season_id"),
    )

    def __repr__(self):
        return f"<PlayerTeamSeason {self.player_team_season_id}>"
