from applications import db, login_manager
from applications import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=30), nullable=False, unique=True)
    email_address=db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash=db.Column(db.String(length=60), nullable=False)
    checkups=db.relationship('Checkup', backref='patient_checked', lazy=True)
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    

class Checkup(db.Model):
    form_id=db.Column(db.Integer(), primary_key=True)
    age=db.Column(db.Integer(), nullable=False)
    gender=db.Column(db.String(), nullable=False)
    hypertension=db.Column(db.Integer(), nullable=False)
    heart_disease=db.Column(db.Integer(), nullable=False)
    blood_glucose=db.Column(db.Float(), nullable=False)
    weight=db.Column(db.Float(), nullable=False)
    height=db.Column(db.Float(), nullable=False)
    hba1c=db.Column(db.Float(), nullable=False)
    diabetes=db.Column(db.Integer(), nullable=False)
    patient_id=db.Column(db.Integer(), db.ForeignKey('user.id'))