from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta
from sqlalchemy.ext.hybrid import hybrid_property

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    blood_type = db.Column(db.String(10))
    
    # One-to-many relationship with Diagnosis
    diagnoses = db.relationship('Diagnosis', back_populates='patient', lazy=True)

    @hybrid_property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    specialization = db.Column(db.String(150))  # Only for Doctor table
    
    # One-to-many relationship with diagnoses
    diagnoses = db.relationship('Diagnosis', back_populates='doctor', lazy=True)

    @hybrid_property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    diagnosis = db.Column(db.String(255))  # Field for diagnosis
    details = db.Column(db.String(1000))    # Field for additional details
    medicine_prescribed = db.Column(db.String(500))  # Field for prescribed medicine
    
    # Foreign keys to link with Patient and Doctor
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
    # Define relationships
    patient = db.relationship('Patient', back_populates='diagnoses')
    doctor = db.relationship('Doctor', back_populates='diagnoses')

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # Foreign keys to link with Patient and Doctor
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
    # Define relationships
    patient = db.relationship('Patient', foreign_keys=[patient_id], backref=db.backref('bills', lazy=True))
    doctor = db.relationship('Doctor', foreign_keys=[doctor_id], backref=db.backref('bills', lazy=True))

    @hybrid_property
    def due_date(self):
        return self.date + timedelta(days=20)


    
    