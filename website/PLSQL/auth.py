from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Doctor, Patient
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import text

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

        # Query the database for the user
        user = Doctor.query.filter_by(email=email).first()
        if user:
            # Check if the user has an associated employee ID
            if user.id != int(employee_id):
                flash('Employee ID does not match with the email provided.', category='error')
                return redirect(url_for('auth.EmployeeLogin'))
            
            # Verify password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
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

        # Query the database for the user
        user = Patient.query.filter_by(email=email).first()
        if user:
            # Check if the user has an associated patient ID
            if user.id != int(patient_id):
                flash('Patient ID does not match with the email provided.', category='error')
                return redirect(url_for('auth.PatientLogin'))
            
            # Verify password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print(f"Patient {user.id} logged in successfully!")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Invalid email.', category='error')

    return render_template("pat_login.html")

@auth.route("/logout")
@login_required
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
        date_of_birth = request.form.get('dateOfBirth')
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
            user = db.session.execute(text("SELECT * FROM patient WHERE email = :email"), {'email': email}).fetchone()
            if user:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.sign_up_page'))
        elif role == 'doctor':
            user = db.session.execute(text("SELECT * FROM doctor WHERE email = :email"), {'email': email}).fetchone()
            if user:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.sign_up_page'))

        # Start a transaction and execute the inserts
        with db.engine.connect() as connection:
            try:
                # Insert into the appropriate table (patient or doctor)
                if role == 'patient':
                    query = text(
                        """
                        INSERT INTO patient (id, email, first_name, last_name, date_of_birth, phone_number, gender, address, blood_type, password)
                        VALUES (:id, :email, :first_name, :last_name, :date_of_birth, :phone_number, :gender, :address, :blood_type, :password)
                        """
                    )
                elif role == 'doctor':
                    query = text(
                        """
                        INSERT INTO doctor (id, email, first_name, last_name, date_of_birth, phone_number, gender, address, specialization, password)
                        VALUES (:id, :email, :first_name, :last_name, :date_of_birth, :phone_number, :gender, :address, :specialization, :password)
                        """
                    )

                # Execute the insert query
                connection.execute(query, {'id': patient_id or doctor_id, 'email': email, 'first_name': first_name, 'last_name': last_name,
                                            'date_of_birth': date_of_birth, 'phone_number': phone_number,
                                            'gender': gender, 'address': address, 'blood_type': blood_type,
                                            'specialization': specialization if role == 'doctor' else None,
                                            'password': generate_password_hash(password1, method='sha256')})

                # Commit the transaction
                connection.commit()

                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.sign_up_page'))

            except Exception as e:
                # Rollback the transaction in case of an error
                connection.rollback()
                flash(f"An error occurred: {str(e)}", category='error')
                return redirect(url_for('auth.sign_up_page'))

    return render_template("signup.html")