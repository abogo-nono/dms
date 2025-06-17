from datetime import datetime

from app import db


class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    person = db.relationship("Person", backref=db.backref("food_logs", lazy=True))
    food = db.relationship("Food", backref=db.backref("logs", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "food_id": self.food_id,
            "food_name": self.food.name if self.food else None,
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes,
        }
