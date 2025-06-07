from flask_restful import Resource, reqparse
from app.models.allergy import Allergy
from app.models.person import Person
from app.models.food import Food
from app import db

parser = reqparse.RequestParser()
parser.add_argument('person_id', type=int, required=True, help='Person ID is required')
parser.add_argument('food_id', type=int, required=True, help='Food ID is required')
parser.add_argument('severity', type=str, required=False, default='mild')
parser.add_argument('notes', type=str, required=False)

class AllergyListResource(Resource):
    def get(self):
        """Get all allergies"""
        allergies = Allergy.query.all()
        return {'allergies': [allergy.to_dict() for allergy in allergies]}, 200
    
    def post(self):
        """Record a new allergy"""
        args = parser.parse_args()
        
        # Verify person and food exist
        person = Person.query.get_or_404(args['person_id'], 'Person not found')
        food = Food.query.get_or_404(args['food_id'], 'Food not found')
        
        # Check if allergy already exists
        existing_allergy = Allergy.query.filter_by(
            person_id=args['person_id'],
            food_id=args['food_id']
        ).first()
        
        if existing_allergy:
            return {'message': f'Allergy record already exists for {person.name} and {food.name}'}, 400
        
        allergy = Allergy(
            person_id=args['person_id'],
            food_id=args['food_id'],
            severity=args['severity'],
            notes=args['notes']
        )
        
        db.session.add(allergy)
        db.session.commit()
        
        return {'allergy': allergy.to_dict()}, 201

class AllergyResource(Resource):
    def get(self, allergy_id):
        """Get allergy by ID"""
        allergy = Allergy.query.get_or_404(allergy_id, 'Allergy not found')
        return {'allergy': allergy.to_dict()}, 200
    
    def put(self, allergy_id):
        """Update allergy"""
        allergy = Allergy.query.get_or_404(allergy_id, 'Allergy not found')
        args = parser.parse_args()
        
        # Update fields
        allergy.person_id = args['person_id']
        allergy.food_id = args['food_id']
        allergy.severity = args['severity']
        allergy.notes = args['notes']
        
        db.session.commit()
        
        return {'allergy': allergy.to_dict()}, 200
    
    def delete(self, allergy_id):
        """Delete allergy"""
        allergy = Allergy.query.get_or_404(allergy_id, 'Allergy not found')
        db.session.delete(allergy)
        db.session.commit()
        
        return {'message': 'Allergy record deleted'}, 204

class PersonAllergyResource(Resource):
    def get(self, person_id):
        """Get all allergies for a specific person"""
        person = Person.query.get_or_404(person_id, 'Person not found')
        allergies = Allergy.query.filter_by(person_id=person_id).all()
        
        return {
            'person': person.to_dict(),
            'allergies': [allergy.to_dict() for allergy in allergies]
        }, 200