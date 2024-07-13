from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,RadioField,IntegerField,SelectField,DecimalField
from wtforms.validators import Length, Email, DataRequired, ValidationError
from applications import app
from applications.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        with app.app_context():
            user=User.query.filter_by(username=username_to_check.data).first()

            if user:
                raise ValidationError('Username Already Exists !!!')
            
    def validate_email_address(self, email_address_to_check):
        with app.app_context():
            email=User.query.filter_by(email_address=email_address_to_check.data).first()

            if email:
                raise ValidationError('Email Address already exists !!!')
            
    username = StringField(label='User Name :', validators=[Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='Email Address : ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password : ', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name : ', validators=[Length(min=2, max=20), DataRequired()])
    password = PasswordField(label='Password : ', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign In')


class CheckupForm(FlaskForm):

    username=StringField('Name',validators=[DataRequired(),Length(max=100)])
    gender=RadioField('Gender',validators=[DataRequired()],choices=['Male','Female','Others'])
    age=IntegerField('Age',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired(),Length(max=250)])
    pincode=IntegerField('Pincode',validators=[DataRequired()])
    hypertension=RadioField('Hypertension',validators=[DataRequired()],choices=['Yes','No'])
    previousHeartDisease=RadioField('Previous Heart Disease',validators=[DataRequired()],choices=['Yes','No'])
    smoking_History=SelectField("Smoking History",validators=[DataRequired()],choices=[('never','Never'),('former','Former'),('current','Current'),('notcurrent','Not Current'),('ever','Ever'),('other','Other')])
    weight=DecimalField("Weight (in kg)",validators=[DataRequired()],places=2)
    height=DecimalField("Height (in m)",validators=[DataRequired()],places=2)
    hba1clvl=SelectField("HbA1c Level",validate_choice=[DataRequired()],choices=[('3below','below 3'),('34','3-4'),('45','4-5'),('56','5-6'),('67','6-7'),('78','7-8'),('8above','above 8')])
    blood_glucose=IntegerField('Blood Glucose Level',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email(),Length(max=50)])
    phone=IntegerField('Phone Number',validators=[DataRequired()])
    submit=SubmitField('Submit')

