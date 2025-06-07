from app import db
from app.models.ingredient import Ingredient
from app.models.food import Food

class FoodIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    food = db.relationship('Food', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='food_ingredients')

    def to_dict(self):
        return {
            'id': self.id,
            'food_id': self.food_id,
            'ingredient_id': self.ingredient_id,
            'quantity': self.quantity
        }
