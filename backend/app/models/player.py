from app.extensions import db


class Player(db.Model):
    __tablename__ = "player"

    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Player {self.player_id} {self.first_name} {self.last_name}>"
