from turtle import position
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Company, Employee
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		data = request.form
		company_name = data.get('company_name')
		street_address = data.get('street_address')
		city = data.get('city')
		state = data.get('state')
		zip = data.get('zip')

		company = Company.query.filter_by(name=company_name).first()
		print(zip.isdigit())
		if company:
			flash("This company already exists.", category='error')
		elif len(company_name) < 1:
			flash('Company name is too short.', category='error')
		elif len(street_address) < 1:
			flash('Street address is too short.', category='error')
		elif len(city) < 1:
			flash('City is too short.', category='error')
		elif len(state) < 1:
			flash('State is too short.', category='error')
		elif len(zip) != 5 or not zip.isdigit():
			flash('Zip code should be 5 digits long.', category='error')
		else:
			new_company = Company(name=company_name, street_address=street_address, city=city, state=state, zip=zip)
			db.session.add(new_company)
			db.session.commit()
			flash('Company added!', category='success')
	companies = Company.query.all()
	
	return render_template("home.html", companies=companies)


@views.route('/company', methods=['GET','POST'])
def company():
	
	company_id = request.args.get('id')
	if not company_id:
		flash("That company does not exist.", category="error")
		return redirect(url_for('views.home'))

	company = Company.query.filter_by(id=company_id).first()
	if not company:
		flash("That company does not exist.", category="error")
		return redirect(url_for('views.home'))
			
	if request.method == 'POST':
		data = request.form
		employee_first_name = data.get('first_name')
		employee_last_name = data.get('last_name')
		employee_email = data.get('email')
		employee_position = data.get('position')

		employee = Employee.query.filter_by(first_name=employee_first_name,last_name=employee_last_name).first()
		import re
		emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		print(not re.fullmatch(emailRegex, 'asdf@sdf'))

		if employee:
			flash("This employee already exists.", category='error')
		elif (len(employee_first_name) < 1):
			flash("Please enter a valid first name.", category='error')
		elif (len(employee_last_name) < 1):
			flash("Please enter a valid last name.", category='error')
		elif (len(employee_email) < 1) or not re.fullmatch(emailRegex, employee_email):
			flash("Please enter a valid email.", category='error')
		elif (len(employee_position) < 1):
			flash("Please enter a valid position.", category='error')
		else:
			new_employee = Employee(first_name=employee_first_name, last_name=employee_last_name, email=employee_email, position=employee_position, company_id=company_id)
			db.session.add(new_employee)
			db.session.commit()
			flash('Player added', category='success')

	employees = Employee.query.filter_by(company_id=company_id).order_by(Employee.last_name.asc()).all()
	return render_template("company.html", company=company, employees=employees)