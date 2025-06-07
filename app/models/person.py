from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # Relationships added implicitly:
    # food_logs = db.relationship('FoodLog', backref='person', lazy=True)
    # allergies = db.relationship('Allergy', backref='person', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
        }
        
    def to_dict_with_allergies(self):
        result = self.to_dict()
        result['allergies'] = [allergy.to_dict() for allergy in self.allergies]
        return result

