from flask_restful import Resource, reqparse

from app import db
from app.models.foodIngredient import FoodIngredient

parser = reqparse.RequestParser()
parser.add_argument('food_id', type=int, required=True, help='Food ID is required')
parser.add_argument('ingredient_id', type=int, required=True, help='Ingredient ID is required')
parser.add_argument('quantity', type=str, required=True, help='Quantity is required')

class FoodIngredientListResource(Resource):
    def get(self):
        food_ingredients = FoodIngredient.query.all()
        return {'food_ingredients': [fi.to_dict() for fi in food_ingredients]}, 200

    def post(self):
        args = parser.parse_args()
        food_ingredient = FoodIngredient(**args)
        db.session.add(food_ingredient)
        db.session.commit()
        return {'food_ingredient': food_ingredient.to_dict()}, 201
    

class FoodIngredientResource(Resource):
    def get(self, food_ingredient_id):
        food_ingredient = FoodIngredient.query.get_or_404(food_ingredient_id, 'FoodIngredient not found with this ID')
        return {'food_ingredient': food_ingredient.to_dict()}, 200

    def put(self, food_ingredient_id):
        food_ingredient = FoodIngredient.query.get_or_404(food_ingredient_id, 'FoodIngredient not found with this ID')
        args = parser.parse_args()
        food_ingredient.food_id = args['food_id']
        food_ingredient.ingredient_id = args['ingredient_id']
        food_ingredient.quantity = args['quantity']
        db.session.commit()
        return {'food_ingredient': food_ingredient.to_dict()}, 201

    def delete(self, food_ingredient_id):
        food_ingredient = FoodIngredient.query.get_or_404(food_ingredient_id, 'FoodIngredient not found with this ID')
        db.session.delete(food_ingredient)
        db.session.commit()
        return {'message': f'FoodIngredient with ID {food_ingredient_id} deleted!'}, 204