from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Diagnosis, Bill

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
            new_diagnosis = Diagnosis(patient_id=patient_id, diagnosis=diagnosis, details=details, medicine_prescribed=medicine, doctor_id=doctor_id)
            db.session.add(new_diagnosis)
            db.session.commit()

            # Automatically create a bill with a value of 150
            new_bill = Bill(amount=150, patient_id=patient_id, doctor_id=doctor_id)
            db.session.add(new_bill)
            db.session.commit()

            flash('Diagnosis and bill added successfully!', category='success')

            return redirect(url_for('views.home'))

    # Fetch diagnoses based on the current user's role
    if current_user.__class__.__name__ == 'Doctor':
        diagnoses = Diagnosis.query.filter_by(doctor_id=current_user.id).all()
    elif current_user.__class__.__name__ == 'Patient':
        diagnoses = Diagnosis.query.filter_by(patient_id=current_user.id).all()
        bills = Bill.query.filter_by(patient_id=current_user.id).all()

    return render_template("home.html", diagnoses=diagnoses, bills=bills)
