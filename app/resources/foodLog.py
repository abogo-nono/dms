from flask_restful import Resource, reqparse
from app.models.foodLog import FoodLog
from app.models.person import Person
from app.models.food import Food
from app.models.allergy import Allergy
from app import db
from flask import jsonify, request
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('person_id', type=int, required=True, help='Person ID is required')
parser.add_argument('food_id', type=int, required=True, help='Food ID is required')
parser.add_argument('notes', type=str, required=False)

class FoodLogResource(Resource):
    def post(self):
        """Log food consumed by a person (logFood)"""
        args = parser.parse_args()
        
        # Verify person and food exist
        person = Person.query.get_or_404(args['person_id'], 'Person not found')
        food = Food.query.get_or_404(args['food_id'], 'Food not found')
        
        # Check if person is allergic to this food
        allergy = Allergy.query.filter_by(
            person_id=args['person_id'], 
            food_id=args['food_id']
        ).first()
        
        # Create the food log
        food_log = FoodLog(
            person_id=args['person_id'],
            food_id=args['food_id'],
            notes=args['notes']
        )
        
        db.session.add(food_log)
        db.session.commit()
        
        result = {
            'success': True,
            'food_log': food_log.to_dict()
        }
        
        # Add allergy warning if applicable
        if allergy:
            result['warning'] = f"Warning: You have a {allergy.severity} allergy to {food.name}"
            
        return result, 201

class PersonFoodLogResource(Resource):
    def get(self, person_id):
        """View food history for a person (viewHistory)"""
        person = Person.query.get_or_404(person_id, 'Person not found')
        
        # Optional date filtering
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = FoodLog.query.filter_by(person_id=person_id).order_by(FoodLog.timestamp.desc())
        
        if start_date:
            start_datetime = datetime.fromisoformat(start_date)
            query = query.filter(FoodLog.timestamp >= start_datetime)
            
        if end_date:
            end_datetime = datetime.fromisoformat(end_date)
            query = query.filter(FoodLog.timestamp <= end_datetime)
        
        logs = query.all()
        
        return {
            'person': person.to_dict(),
            'logs': [log.to_dict() for log in logs]
        }, 200