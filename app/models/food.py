from app  import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    ingredients = db.relationship('FoodIngredient', back_populates='food', cascade='all, delete-orphan')
    nutrition_info = db.relationship('NutritionInfo', back_populates='food', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'image_url': self.image_url,
            'ingredients': [fi.to_dict() for fi in self.ingredients],
            'nutrition_info': self.nutrition_info.to_dict() if self.nutrition_info else None
        }