from enum import unique
from . import db
from sqlalchemy.sql import func

class Company(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True)
	street_address = db.Column(db.String(150))
	city = db.Column(db.String(150))
	state = db.Column(db.String(150))
	zip = db.Column(db.String(150))
	employees = db.relationship('Employee')
	
class Employee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(150))
	last_name = db.Column(db.String(150))
	email = db.Column(db.String(150), unique=True)
	position = db.Column(db.String(150))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id'))