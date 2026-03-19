from app.extensions import db


class Season(db.Model):
    __tablename__ = "season"

    season_id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Season {self.season_id} {self.label}>"
