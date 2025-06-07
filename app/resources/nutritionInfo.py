from app import db
from flask_restful import Resource
from app.models.food import Food
from app.models.nutritionInfo import NutritionInfo
from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('food_id', type=int, required=True, help='Food ID cannot be blank')
parser.add_argument('calories', type=float, required=True, help='Calories cannot be blank')
parser.add_argument('protein', type=float, required=True, help='Protein cannot be blank')
parser.add_argument('fat', type=float, required=True, help='Fat cannot be blank')
parser.add_argument('carbohydrates', type=float, required=True, help='Carbohydrates cannot be blank')


class NutritionInfoListResource(Resource):
    def get(self):
        nutrition_info = NutritionInfo.query.all()
        return [info.to_dict() for info in nutrition_info], 200

    def post(self):
        args = parser.parse_args()

        if not Food.query.get(args['food_id']):
            return {'message': 'Food with this ID does not exist'}, 404

        if NutritionInfo.query.filter_by(food_id=args['food_id']).first():
            return {'message': 'Nutrition information for this food already exists'}, 400
        
        new_nutrition_info = NutritionInfo(
            food_id=args['food_id'],
            calories=args['calories'],
            protein=args['protein'],
            fat=args['fat'],
            carbohydrates=args['carbohydrates']
        )
        db.session.add(new_nutrition_info)
        db.session.commit()
        return new_nutrition_info.to_dict(), 201
        


class NutritionInfoResource(Resource):
    def get(self, nutrition_info_id):
        nutrition_info = NutritionInfo.query.get_or_404(nutrition_info_id)
        return nutrition_info.to_dict(), 200

    def put(self, nutrition_info_id):
        args = parser.parse_args()
        nutrition_info = NutritionInfo.query.get_or_404(nutrition_info_id)

        if not Food.query.get(args['food_id']):
            return {'message': 'Food with this ID does not exist'}, 404

        nutrition_info.food_id = args['food_id']
        nutrition_info.calories = args['calories']
        nutrition_info.protein = args['protein']
        nutrition_info.fat = args['fat']
        nutrition_info.carbohydrates = args['carbohydrates']

        db.session.commit()
        return nutrition_info.to_dict(), 200

    def delete(self, nutrition_info_id):
        nutrition_info = NutritionInfo.query.get_or_404(nutrition_info_id)
        db.session.delete(nutrition_info)
        db.session.commit()
        return {'message': 'Nutrition information deleted'}, 204