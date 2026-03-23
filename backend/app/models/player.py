from app.extensions import db


class Player(db.Model):
    __tablename__ = "player"

    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    shoot_catches = db.Column(db.String(20), nullable=False)
    primary_position = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    headshot_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Player {self.player_id} {self.first_name} {self.last_name}>"
