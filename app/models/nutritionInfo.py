from sqlalchemy.orm import relationship

from app import db


class NutritionInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)

    food = relationship("Food", back_populates="nutrition_info")

    def to_dict(self):
        return {
            "id": self.id,
            "food_id": self.food_id,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "carbohydrates": self.carbohydrates,
        }
