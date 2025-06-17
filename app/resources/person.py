from typing import List

from flasgger import swag_from
from flask_restful import Resource, abort, reqparse

from app import db
from app.models.person import Person

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("gender", type=str, required=True)
parser.add_argument("age", type=int, required=True)


class PersonResource(Resource):
    @swag_from("../docs/person.yml", endpoint="people")
    def get(self, person_id):
        person: Person | None = Person.query.get_or_404(person_id, "Person not found")
        return {"person": person.to_dict()}, 200

    @swag_from("../docs/person.yml", endpoint="people")
    def put(self, person_id):
        person: Person = Person.query.get_or_404(person_id, "Person not found")
        args = parser.parse_args()
        person.name = args["name"]
        person.gender = args["gender"]
        person.age = args["age"]
        db.session.commit()
        return {"person": person.to_dict()}, 201

    @swag_from("../docs/person.yml", endpoint="people")
    def delete(self, person_id):
        person: Person = Person.query.get_or_404(person_id, "Person not found")
        db.session.delete(person)
        db.session.commit()
        return {"message": f"`{person.name}` has been deleted!"}, 204


class PersonListResource(Resource):
    @swag_from("../docs/person.yml", endpoint="people_list")
    def get(self):
        people: List[Person] = Person.query.all()
        return {"people": [person.to_dict() for person in people]}, 200

    @swag_from("../docs/person.yml", endpoint="people_list")
    def post(self):
        args = parser.parse_args()
        if Person.query.filter_by(name=args["name"]).first():
            abort(400, description="This name is already exists!")
        person = Person(**args)
        db.session.add(person)
        db.session.commit()
        return {"person": person.to_dict()}, 201
