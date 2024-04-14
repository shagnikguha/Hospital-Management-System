from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text  # Import text construct for SQL queries
from . import db
from .models import Diagnosis, Bill, Patient
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    bills = []  # Initialize bills variable

    if request.method == 'POST':
        if current_user.__class__.__name__ == 'Doctor':
            patient_id = request.form.get('patientId')
            diagnosis = request.form.get('diagnosis')
            details = request.form.get('details')
            medicine = request.form.get('medicine')

            doctor_id = current_user.id

            # Create a new diagnosis
            with db.engine.connect() as connection:
                query = text(
                    """
                    INSERT INTO diagnosis (patient_id, diagnosis, details, medicine_prescribed, doctor_id)
                    VALUES (:patient_id, :diagnosis, :details, :medicine_prescribed, :doctor_id);
                    """
                )
                connection.execute(query, {'patient_id': patient_id, 'diagnosis': diagnosis, 'details': details, 'medicine_prescribed': medicine, 'doctor_id': doctor_id})

                # Automatically create a bill with a value of 150
                query = text(
                    """
                    INSERT INTO bill (amount, patient_id, doctor_id)
                    VALUES (150, :patient_id, :doctor_id);
                    """
                )
                connection.execute(query, {'patient_id': patient_id, 'doctor_id': doctor_id})

                connection.commit()
                
            flash('Diagnosis and bill added successfully!', category='success')

            return redirect(url_for('views.home'))

    # Fetch diagnoses based on the current user's role
    if current_user.__class__.__name__ == 'Doctor':
        with db.engine.connect() as connection:
            query = text(
                """
                SELECT d.id, d.date, p.id AS patient_id, p.first_name AS patient_first_name, p.last_name AS patient_last_name, d.diagnosis, d.details, d.medicine_prescribed
                FROM diagnosis d
                JOIN patient p ON d.patient_id = p.id
                WHERE d.doctor_id = :doctor_id;
                """
            )
            diagnoses = connection.execute(query, {'doctor_id': current_user.id}).fetchall()
    elif current_user.__class__.__name__ == 'Patient':
        with db.engine.connect() as connection:
            query = text(
                """
                SELECT d.id, d.date, p.id AS patient_id, p.first_name AS patient_first_name, p.last_name AS patient_last_name, d.diagnosis, d.details, d.medicine_prescribed
                FROM diagnosis d
                JOIN patient p ON d.patient_id = p.id
                WHERE d.patient_id = :patient_id;
                """
            )
            diagnoses = connection.execute(query, {'patient_id': current_user.id}).fetchall()

            query = text(
                """
                SELECT * FROM bill WHERE patient_id = :patient_id;
                """
            )
            bills = connection.execute(query, {'patient_id': current_user.id}).fetchall()

    return render_template("home.html", diagnoses=diagnoses, bills=bills)
