from app import db
from app.models.ingredient import Ingredient
from app.models.food import Food
from flask_restful import Resource, reqparse
from flask import request, abort
from typing import List
import os
from werkzeug.utils import secure_filename
from flasgger import swag_from
from random import sample
from app.models.allergy import Allergy
import random

from app.models.person import Person

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('description', type=str, required=False)
parser.add_argument('image_url', type=str, required=False)


class FoodListResource(Resource):
    @swag_from('../docs/food.yml', endpoint='food_list')
    def get(self):
        foods: List[Food] = Food.query.all()
        return {'foods': [food.to_dict() for food in foods]}, 200

    @swag_from('../docs/food.yml', endpoint='food_list')
    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        image = request.files.get('image')

        if not name:
            abort(400, description="Name is required.")
        if Food.query.filter_by(name=name).first():
            abort(400, description="Food with this name already exists.")

        image_url = None
        if image:
            upload_folder = 'static/uploads/food_images'
            os.makedirs(upload_folder, exist_ok=True)
            filename = name.replace(' ', '_') + '.' + image.filename.rsplit('.', 1)[-1]
            filepath = os.path.join(upload_folder, filename)
            image.save(filepath)
            image_url = '/' + filepath

        food = Food(name=name, description=description, image_url=image_url)
        db.session.add(food)
        db.session.commit()
        return {'food': food.to_dict()}, 201


class FoodResource(Resource):
    @swag_from('../docs/food.yml', endpoint='food')
    def get(self, food_id):
        food: Food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        return {'food': food.to_dict()}, 200

    @swag_from('../docs/food.yml', endpoint='food')
    def put(self, food_id):
        food: Food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        name = request.form.get('name')
        description = request.form.get('description')
        image = request.files.get('image')

        if name:
            food.name = name
        if description:
            food.description = description

        if image:
            upload_folder = 'static/uploads/food_images'
            os.makedirs(upload_folder, exist_ok=True)
            filename = (name or food.name).replace(' ', '_') + '.' + image.filename.rsplit('.', 1)[-1]
            filepath = os.path.join(upload_folder, filename)
            image.save(filepath)
            food.image_url = '/' + filepath

        db.session.commit()
        return {'food': food.to_dict()}, 200
    
    @swag_from('../docs/food.yml', endpoint='food')
    def delete(self, food_id):
        food: Food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        db.session.delete(food)
        db.session.commit()
        return {'food': f'{food.name} deleted!'}, 204

    def calories(self, food_id):
        food: Food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        if not food.nutrition_info:
            return {'message': 'No nutrition information available for this food'}, 404
        return {'calories': food.nutrition_info.calories}, 200

    def ingredients(self, food_id):
        food: Food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        ingredients = [fi.ingredient.to_dict() for fi in food.ingredients]
        return {'ingredients': ingredients}, 200

    def get_calories(self, food_id):
        """Get calories for a specific food (getCalories)"""
        food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        
        if not food.nutrition_info:
            return {'message': 'No nutrition information available for this food'}, 404
        
        return {
            'food': food.name,
            'calories': food.nutrition_info.calories
        }, 200

    def list_ingredients(self, food_id):
        """List ingredients for a specific food (listFoodIngredient)"""
        food = Food.query.get_or_404(food_id, 'Food not found with this ID')
        
        if not food.ingredients:
            return {'message': 'No ingredients found for this food'}, 404
        
        ingredients = []
        for food_ingredient in food.ingredients:
            ingredients.append({
                'name': food_ingredient.ingredient.name,
                'quantity': food_ingredient.quantity
            })
        
        return {
            'food': food.name,
            'ingredients': ingredients
        }, 200


class RandomMenuResource(Resource):
    def get(self, person_id):
        """Get random menu suggestions for a person"""
        person = Person.query.get_or_404(person_id, 'Person not found')
        
        # Get all foods the person is allergic to
        allergic_food_ids = [allergy.food_id for allergy in person.allergies]
        
        # Get all available foods that the person is not allergic to
        safe_foods = Food.query.filter(~Food.id.in_(allergic_food_ids)).all()
        
        if len(safe_foods) < 3:
            # Not enough foods to create a menu
            return {
                'message': 'Not enough non-allergic foods available for a menu',
                'available_foods': [food.to_dict() for food in safe_foods]
            }, 200
        
        # Randomly select 3 foods
        menu_foods = random.sample(safe_foods, 3)
        
        return {
            'person': person.to_dict(),
            'menu_suggestions': [food.to_dict() for food in menu_foods]
        }, 200

