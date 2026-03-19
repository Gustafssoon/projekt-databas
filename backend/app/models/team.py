from app.extensions import db


class Team(db.Model):
    __tablename__ = "team"

    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<Team {self.team_id} {self.abbreviation}>"
