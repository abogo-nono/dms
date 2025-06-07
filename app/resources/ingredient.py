from flask_restful import Resource, reqparse
from app.models.ingredient import Ingredient
from app import db
from typing import List
from flasgger import swag_from


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)

class IngredientListResource(Resource):
    @swag_from('../docs/ingredient.yml', methods=['GET'])
    def get(self):
        ingredients: List[Ingredient] = Ingredient.query.all()
        return {'ingredients': [ingredient.to_dict() for ingredient in ingredients]}, 200

    @swag_from('../docs/ingredient.yml', methods=['POST'])
    def post(self):
        args = parser.parse_args()
        ingredient = Ingredient(**args)
        db.session.add(ingredient)
        db.session.commit()
        return {'ingredient': ingredient.to_dict()}, 201


class IngredientResource(Resource):
    @swag_from('../docs/ingredient.yml', methods=['GET'])
    def get(self, ingredient_id):
        ingredient: Ingredient = Ingredient.query.get_or_404(ingredient_id, 'Ingredient not found with this ID')
        return {'ingredient': ingredient.to_dict()}, 200

    @swag_from('../docs/ingredient.yml', methods=['PUT'])
    def put(self, ingredient_id):
        ingredient: Ingredient = Ingredient.query.get_or_404(ingredient_id, 'Ingredient not found with this ID')
        args = parser.parse_args()
        ingredient.name = args['name']
        db.session.commit()
        return {'ingredient': ingredient.to_dict()}, 201

    @swag_from('../docs/ingredient.yml', methods=['DELETE'])
    def delete(self, ingredient_id):
        ingredient: Ingredient = Ingredient.query.get_or_404(ingredient_id, 'Ingredient not found with this ID')
        db.session.delete(ingredient)
        db.session.commit()
        return {'ingredient': f'{ingredient.name} deleted!'}, 204
