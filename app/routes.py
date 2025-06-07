from app.resources.food import FoodListResource, FoodResource, RandomMenuResource
from app.resources.foodIngredient import FoodIngredientListResource, FoodIngredientResource
from app.resources.ingredient import IngredientResource, IngredientListResource
from app.resources.nutritionInfo import NutritionInfoListResource, NutritionInfoResource
from app.resources.person import PersonResource, PersonListResource
from app.resources.foodLog import FoodLogResource, PersonFoodLogResource
from app.resources.allergy import AllergyListResource, AllergyResource, PersonAllergyResource
from flask_restful import Api

def register_routes(api):
    api.add_resource(PersonListResource, '/people', endpoint='people_list')
    api.add_resource(PersonResource, '/people/<int:person_id>', endpoint='people')

    api.add_resource(IngredientListResource, '/ingredients', endpoint='ingredient_list')
    api.add_resource(IngredientResource, '/ingredients/<int:ingredient_id>', endpoint='ingredient')

    api.add_resource(FoodIngredientListResource, '/food_ingredients', endpoint='food_ingredient_list')
    api.add_resource(FoodIngredientResource, '/food_ingredients/<int:food_ingredient_id>', endpoint='food_ingredient')

    api.add_resource(NutritionInfoListResource, '/nutrition_info', endpoint='nutrition_info_list')
    api.add_resource(NutritionInfoResource, '/nutrition_info/<int:nutrition_info_id>', endpoint='nutrition_info')

    api.add_resource(FoodListResource, '/foods', endpoint='food_list')
    api.add_resource(FoodResource, '/foods/<int:food_id>', endpoint='food')
    
    api.add_resource(FoodLogResource, '/food_log', endpoint='food_log')
    api.add_resource(PersonFoodLogResource, '/people/<int:person_id>/food_history', endpoint='food_history')
    
    api.add_resource(AllergyListResource, '/allergies', endpoint='allergy_list')
    api.add_resource(AllergyResource, '/allergies/<int:allergy_id>', endpoint='allergy')
    api.add_resource(PersonAllergyResource, '/people/<int:person_id>/allergies', endpoint='person_allergies')
    
    food_view = api.app.view_functions['food']
    food_view.view_class.get_calories = lambda self, food_id: FoodResource.get_calories(self, food_id)
    food_view.view_class.list_ingredients = lambda self, food_id: FoodResource.list_ingredients(self, food_id)
    
    api.add_resource(FoodResource, '/foods/<int:food_id>/calories', endpoint='food_calories')
    api.add_resource(FoodResource, '/foods/<int:food_id>/ingredients', endpoint='food_ingredients')
    
    api.add_resource(RandomMenuResource, '/people/<int:person_id>/menu_suggestions', endpoint='random_menu')
