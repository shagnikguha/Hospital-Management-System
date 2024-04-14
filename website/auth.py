from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Doctor, Patient
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route("/emp_login", methods=['GET', 'POST'])
def EmployeeLogin():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the employee ID (assuming it's a numeric value)
        if not employee_id.isdigit():
            flash('Invalid employee ID format.', category='error')
            return redirect(url_for('auth.EmployeeLogin'))

        # Searching for specific entry in the database 
        user = Doctor.query.filter_by(email=email).first()
        if user:
            # Check if the user has an associated employee ID
            if user.id != int(employee_id):
                flash('Employee ID does not match with the email provided.', category='error')
                return redirect(url_for('auth.EmployeeLogin'))
            
            # As we have stored password as a hash, we can only check it using this function
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Logs user in until web server restarts or user logs out
                login_user(user, remember=True)
                print(f"Employee {user.id} logged in successfully!")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Invalid email.', category='error')

    return render_template("emp_login.html")

@auth.route("/pat_login", methods=['GET', 'POST'])
def PatientLogin():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the patient ID (assuming it's a numeric value)
        if not patient_id.isdigit():
            flash('Invalid patient ID format.', category='error')
            return redirect(url_for('auth.PatientLogin'))

        # Searching for specific entry in the database 
        user = Patient.query.filter_by(email=email).first()
        if user:
            # Check if the user has an associated patient ID
            if user.id != int(patient_id):
                flash('Patient ID does not match with the email provided.', category='error')
                return redirect(url_for('auth.PatientLogin'))
            
            # As we have stored password as a hash, we can only check it using this function
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Logs user in until web server restarts or user logs out
                login_user(user, remember=True)
                print(f"Patient {user.id} logged in successfully!")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Invalid email.', category='error')

    return render_template("pat_login.html")

@auth.route("/logout")
@login_required      # makes it so that this page is inaccessible until a user is logged in
def logout_page():
    logout_user()
    flash("Logged out.", category='success')
    return redirect(url_for('views.home'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up_page():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        date_of_birth = datetime.strptime(request.form.get('dateOfBirth'), '%Y-%m-%d').date()
        phone_number = request.form.get('phone')
        gender = request.form.get('gender')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')
        patient_id = request.form.get('patientId')
        doctor_id = request.form.get('doctorId')
        specialization = request.form.get('specialization')
        blood_type = request.form.get('bloodType')
        
        # Check if the email already exists
        if role == 'patient':
            user = Patient.query.filter_by(email=email).first()
        elif role == 'doctor':
            user = Doctor.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif len(first_name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password should be at least 7 characters', category='error')
        else:
            # Creating a new user object
            if role == 'patient':
                new_user = Patient(email=email, first_name=first_name, last_name=last_name, 
                                   date_of_birth=date_of_birth, phone_number=phone_number, 
                                   gender=gender, address=address, blood_type=blood_type,
                                   password=generate_password_hash(password1, method='sha256'))
                if patient_id:
                    new_user.id = patient_id
            elif role == 'doctor':
                new_user = Doctor(email=email, first_name=first_name, last_name=last_name, 
                                   date_of_birth=date_of_birth, phone_number=phone_number, 
                                   gender=gender, address=address, specialization=specialization, 
                                   password=generate_password_hash(password1, method='sha256'))
                if doctor_id:
                    new_user.id = doctor_id

            # Add new user object to the session
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category='success')

            # Redirect to sign-in page
            return redirect(url_for('views.home'))

    return render_template("signup.html")

