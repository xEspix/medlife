from applications import app, db
from applications.forms import RegisterForm, LoginForm,CheckupForm, OtpForm
from flask import render_template, redirect, url_for, flash, request
from applications.models import User, Checkup
from flask_login import login_user, logout_user, login_required,current_user
from applications.mails import send_email
import numpy as np
import pickle
import random

phone=0
name=[]
email=""
pincode=0
result=[]
user_details=[]
get_otp=[]
pred=0
model = pickle.load(open('Medicalmainapp-main/applications/static/model.pkl', 'rb'))
scaler = pickle.load(open('Medicalmainapp-main/applications/static/scaler.pkl', 'rb'))

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html",username=current_user)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/otpverify',methods=['GET','POST'])
def otp():
    otpform=OtpForm()
    if otpform.validate_on_submit():
        global user_details
        global get_otp
        print("IN OTP")
        # Access form data
        otpnum=otpform.otp.data
        print(otpnum)
        print(get_otp)
        flash("OTP Submited!", category='success')
        if(otpnum==get_otp[0]):
            with app.app_context():
                user_data=User(username=user_details[0],
                                email_address=user_details[1],
                                password=user_details[2])
                            
                db.session.add(user_data)
                db.session.commit()
                login_user(user_data)
            
            user_details.pop()
            user_details.pop()
            user_details.pop()
            get_otp.pop()
            return redirect(url_for('dashboard'))
        flash(f"Wrong OTP entered !!! Please enter a valid OTP !!!", category='error')
    return render_template('modal.html',otpform=otpform)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user=User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'You have successfully logged in as : {attempted_user.username}' , category='success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Username and password do not match ! Please try again', category='error')
                flash(f'OTP does not match', category='error')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    form=RegisterForm()
    if form.validate_on_submit():
        global user_details
        user_details.append(form.username.data)
        user_details.append(form.email_address.data)
        user_details.append(form.password1.data)
        global otp
        otp=random.randint(100000, 999999)
        get_otp.append(otp)
        send_email(form.email_address.data,"Medassis Verification", f"Welcome to Medassis !!!\n Your OTP for verification is {otp}. Please enter your OTP to create an account.")
        return redirect(url_for('otp'))
            
        #else:
           # flash(f"Wrong OTP eneted !!! Please enter it correctly", category='error')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='error')
        

        
        
    return render_template('signup.html', form=form)


@app.route('/checkup',methods=['GET','POST'])
def check_up():
    
    myform=CheckupForm()
    if myform.validate_on_submit():
        # Access form data
        username=myform.username.data
        global name
        name.append(username)
        gender=myform.gender.data
        age=myform.age.data
        address=myform.address.data
        global pincode
        global email
        global phone
        
        pincode = myform.pincode.data
        hypertension = myform.hypertension.data
        previousHeartDisease = myform.previousHeartDisease.data
        smoking_History = myform.smoking_History.data
        weight = myform.weight.data
        height = myform.height.data
        hba1clvl = myform.hba1clvl.data
        blood_glucose = myform.blood_glucose.data
        email = myform.email.data
        phone = myform.phone.data

        if len(username) < 2:
            flash("Username must be greater than 4 characters.", category='error')
        elif (age) >= 150:
            flash("Age value exceeded", category='error')
        elif (height)>3:
            flash("Invalid Height Input.", category='error')
        elif (blood_glucose) > 700:
            flash("Invalid blood glucose level", category='error')
        else:
            flash("Form Submited!", category='success')
            if hypertension=="Yes":
                hypertension_int=1
            else:
                hypertension_int=0
            
            if previousHeartDisease=="Yes":
                heart_disease=1
            else:
                heart_disease=0

            if gender=="Male":
                gender_int=1
            else:
                gender_int=0

            if smoking_History=="Other":
                smk_curr=0
                smk_ever=0
                smk_former=0
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="Current":
                smk_curr=1
                smk_ever=0
                smk_former=0
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="Ever":
                smk_curr=0
                smk_ever=1
                smk_former=0
                smk_never=0
                smk_nt_curr=0
            
            elif smoking_History=="Former":
                smk_curr=0
                smk_ever=0
                smk_former=1
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="Never":
                smk_curr=0
                smk_ever=0
                smk_former=0
                smk_never=1
                smk_nt_curr=0

            else:
                smk_curr=0
                smk_ever=0
                smk_former=0
                smk_never=0
                smk_nt_curr=1

            bmi=weight/(height*height)
            if bmi>34:
                wgt_over=1
                wgt_under=0
            
            elif bmi<14:
                wgt_over=0
                wgt_under=1

            else:
                wgt_over=0
                wgt_under=0

            if hba1clvl=="3":
                hba1c_4=0
                hba1c_5=0
                hba1c_6=0
                hba1c_7=0
                hba1c_8=0
                hba1c_9=0

            elif hba1clvl=="34":
                hba1c_4=1
                hba1c_5=0
                hba1c_6=0
                hba1c_7=0
                hba1c_8=0
                hba1c_9=0

            elif hba1clvl=="45":
                hba1c_4=0
                hba1c_5=1
                hba1c_6=0
                hba1c_7=0
                hba1c_8=0
                hba1c_9=0

            elif hba1clvl=="56":
                hba1c_4=0
                hba1c_5=0
                hba1c_6=1
                hba1c_7=0
                hba1c_8=0
                hba1c_9=0

            elif hba1clvl=="67":
                hba1c_4=0
                hba1c_5=0
                hba1c_6=0
                hba1c_7=1
                hba1c_8=0
                hba1c_9=0

            elif hba1clvl=="78":
                hba1c_4=0
                hba1c_5=0
                hba1c_6=0
                hba1c_7=0
                hba1c_8=1
                hba1c_9=0

            else:
                hba1c_4=0
                hba1c_5=0
                hba1c_6=0
                hba1c_7=0
                hba1c_8=0
                hba1c_9=1

            query = np.array([age,hypertension_int,heart_disease,blood_glucose,gender_int,smk_curr,smk_ever,smk_former,smk_never,smk_nt_curr,wgt_over,wgt_under,hba1c_4,hba1c_5,hba1c_6,hba1c_7,hba1c_8,hba1c_9])

            query = query.reshape(1,18)
            input_trf=scaler.transform(query)
            prediction=model.predict(input_trf)
            global pred
            pred=prediction
            print(pred)

            
            with app.app_context():
                checkup_data=Checkup(age=age,
                                    name=username,
                                    gender=gender,
                                    hypertension=hypertension,
                                    heart_disease=previousHeartDisease,
                                    smoking_history=smoking_History,
                                    blood_glucose=blood_glucose,
                                    weight=weight,
                                    height=height,
                                    hba1c=hba1clvl,
                                    diabetes=pred,
                                    patient_id=current_user.id)
                db.session.add(checkup_data)
                db.session.commit()
                

                if prediction[0]==0:
                    flash(f"Your chances of diabetes is low !!!", category="success")
                else:
                    flash(f"Your cances of diabetes is high !!!", category="error")   
                
            return redirect(url_for('results'))
            
        
    return render_template('checkup.html',form=myform)

@app.route('/result')
@login_required
def results():
    global phone
    global pincode
    global email
    global name
    global pred
    with app.app_context():
        user_data=Checkup.query.filter_by(name=name[0]).first()
    name.pop()
    
    return render_template('result.html', user_data=user_data, current_user=current_user, phone=phone, pincode=pincode, email=email, pred=pred)



@app.route('/logout')
@login_required
def logout():
    print("Logout")
    logout_user()
    return redirect(url_for('home_page'))

