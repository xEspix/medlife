from applications import app, db
from applications.forms import RegisterForm, LoginForm,CheckupForm
from flask import render_template, redirect, url_for, flash, request
from applications.models import User, Checkup
from flask_login import login_user, logout_user, login_required,current_user
import numpy as np
import pickle


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
                print("Username and password do not match ! Please try again")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    form=RegisterForm()
    if form.validate_on_submit():
        with app.app_context():
            user_data=User(username=form.username.data,
                        email_address=form.email_address.data,
                        password=form.password1.data)
            
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data)
        
        return redirect(url_for('dashboard'))
    
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
        gender=myform.gender.data
        age=myform.age.data
        address=myform.address.data

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

            if smoking_History=="other":
                smk_curr=0
                smk_ever=0
                smk_former=0
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="current":
                smk_curr=1
                smk_ever=0
                smk_former=0
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="ever":
                smk_curr=0
                smk_ever=1
                smk_former=0
                smk_never=0
                smk_nt_curr=0
            
            elif smoking_History=="former":
                smk_curr=0
                smk_ever=0
                smk_former=1
                smk_never=0
                smk_nt_curr=0

            elif smoking_History=="never":
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

            if hba1clvl=="3below":
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

            print(prediction[0])

            

            with app.app_context():
                checkup_data=Checkup(age=age,
                                    gender=gender,
                                    hypertension=hypertension,
                                    heart_disease=previousHeartDisease,
                                    blood_glucose=blood_glucose,
                                    weight=weight,
                                    height=height,
                                    hba1c=hba1clvl,
                                    diabetes=prediction[0],
                                    patient_id=current_user.id)
                db.session.add(checkup_data)
                db.session.commit()
                if prediction[0]==0:
                    flash(f"Your chances of diabetes is low !!!", category="info")
                else:
                    flash(f"Your cances of diabetes is high !!!", category="info")

            return redirect(url_for('dashboard'))
            
        
        

        
    return render_template('checkup.html',form=myform)



@app.route('/logout')
@login_required
def logout():
    print("Logout")
    logout_user()
    return redirect(url_for('home_page'))

