from app import db


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    severity = db.Column(db.String(20), default="mild")  # mild, moderate, severe
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    person = db.relationship("Person", backref=db.backref("allergies", lazy=True))
    food = db.relationship("Food", backref=db.backref("allergies", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "food_id": self.food_id,
            "food_name": self.food.name if self.food else None,
            "severity": self.severity,
            "notes": self.notes,
        }
