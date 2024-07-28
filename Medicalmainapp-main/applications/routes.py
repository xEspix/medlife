from applications import app, db
from applications.forms import RegisterForm, LoginForm,CheckupForm, OtpForm
from flask import render_template, redirect, url_for, flash, request, jsonify
from applications.models import User, Checkup
from flask_login import login_user, logout_user, login_required,current_user
from applications.mails import send_email
import numpy as np
import pickle
import random
import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly.express as px
from flask import Flask, render_template
import json

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

            send_email(email,"Medassis Report", f"Name : {username}\n Gender : {gender}\n Age : {age}\n Hypertension : {hypertension}\n Previous Heart Disease : {previousHeartDisease}\n Weight : {weight}\n Height : {height}\n HBA1C Level : {hba1clvl}\n Blood Glucose : {blood_glucose}\n Diabetes : {pred}\n")   
                
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

@app.route('/plot1')
def index():
   
    df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')
    
    diabetes_data = df[df['diabetes'] == 1].head(500)  

    bmi = diabetes_data['bmi']
    age = diabetes_data['age']
    hbA1c = diabetes_data['HbA1c_level']

   
    fig = go.Figure(data=[go.Surface(z=[bmi, age, hbA1c], colorscale='Viridis')])

    fig.update_layout(
        title='Surface Plot of BMI, Age, and HbA1c Level for People with Diabetes',
        scene=dict(
            xaxis_title='BMI',
            yaxis_title='Age',
            zaxis_title='HbA1c Level'
        ),
        width=1200,  
        height=800   
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index2.html', plot=graphJSON)

@app.route('/plot2')
def index2():
    return render_template('index4.html')

@app.route('/bubble_plot')
def bubble_plot():
    
    df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')
    diabetes_data = df[df['diabetes'] == 1]

    diabetes_sample = diabetes_data.sample(n=200, random_state=42)

    colors = diabetes_sample['smoking_history'].apply(lambda x: 'green' if x == 'never' else 'red')

    fig = px.scatter_3d(diabetes_sample, x='age', y='HbA1c_level', z='blood_glucose_level',
                        color=colors, size='blood_glucose_level', opacity=0.6,
                        color_discrete_map={'green': 'green', 'red': 'red'})

    fig.update_layout(
        title='3D Bubble Plot of Blood Glucose Levels by Age and HbA1c Level with Smoking History for Diabetic Patients',
        scene=dict(
            xaxis_title='Age',
            yaxis_title='HbA1c Level',
            zaxis_title='Blood Glucose Level'
        ),
        legend_title='Smoking History',
        width=1000,
        height=800
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/plot3')
def index3():
    return render_template('index6.html')

@app.route('/histogram')
def histogram():
    df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')

    diabetes_data = df[df['diabetes'] == 1]

    age_bins = np.arange(0, diabetes_data['age'].max() + 5, 5)

    fig = px.histogram(diabetes_data, x='age', color='gender', 
                       title='Histogram of Age by Gender for Diabetic Patients',
                       labels={'age': 'Age Groups', 'count': 'Frequency of Diabetes'},
                       nbins=len(age_bins))

    fig.update_layout(
        bargap=0.1,  
        bargroupgap=0.2,  
        width=800,
        height=600
    )

    graphJSON = fig.to_json()

    return jsonify(graphJSON)

@app.route('/plot4')
def index4():
    return render_template('index8.html')

@app.route('/scatter_plot')
def scatter_plot():
    df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')

    diabetes_data = df[df['diabetes'] == 1].sample(n=200, random_state=42)
    non_diabetes_data = df[df['diabetes'] == 0].sample(n=200, random_state=42)
    fig = px.scatter_3d(
        pd.concat([diabetes_data, non_diabetes_data]),
        x='age', y='bmi', z='HbA1c_level',
        color=np.where(pd.concat([diabetes_data, non_diabetes_data])['diabetes'] == 1, 'Non-Diabetes', 'Diabetes'),
        symbol=np.where(pd.concat([diabetes_data, non_diabetes_data])['diabetes'] == 1, 'Non-Diabetes', 'Diabetes'),
        opacity=0.7,
        size_max=20,
        labels={'age': 'Age', 'bmi': 'BMI', 'HbA1c_level': 'HbA1c Level'},
        title='Scatter Plot of Age vs BMI vs HbA1c Level with Diabetes Status'
    )

    fig.update_traces(marker=dict(color='blue'), selector=dict(type='scatter3d', name='Non-Diabetes'))
    fig.update_traces(marker=dict(color='red'), selector=dict(type='scatter3d', name='Diabetes'))

    fig.update_layout(
        scene=dict(xaxis_title='Age', yaxis_title='BMI', zaxis_title='HbA1c Level'),
        height=800  
    )

    graphJSON = fig.to_json()

    return jsonify(graphJSON=graphJSON)

@app.route('/plot5')
def index5():
    try:
        df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')

        diabetes_data = df[df['diabetes'] == 1].head(1000)  

        if diabetes_data.empty:
            raise ValueError("No data found for people with diabetes.")

        bmi = diabetes_data['bmi']
        age = diabetes_data['age']
        hbA1c = diabetes_data['HbA1c_level']

        fig = go.Figure(data=[go.Mesh3d(x=bmi, y=age, z=hbA1c, opacity=0.5)])

        fig.update_layout(
            title='3D Mesh Plot of BMI, Age, and HbA1c Level for People with Diabetes',
            scene=dict(
                xaxis_title='BMI',
                yaxis_title='Age',
                zaxis_title='HbA1c Level'
            ),
            width=1200,  
            height=800  
        )

        graphJSON = fig.to_json()

        return render_template('index9.html', plot=graphJSON)

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/plot6')
def index6():

    df = pd.read_csv('Medicalmainapp-main/applications/static/diabetes_prediction_dataset.csv')

    diabetes_data = df[df['diabetes'] == 1]
    non_diabetes_data = df[df['diabetes'] == 0]

    diabetes_counts = {
        'Smoking History': diabetes_data['smoking_history'].value_counts(),
        'Heart Disease': diabetes_data['heart_disease'].value_counts()
    }

    non_diabetes_counts = {
        'Smoking History': non_diabetes_data['smoking_history'].value_counts(),
        'Heart Disease': non_diabetes_data['heart_disease'].value_counts()
    }

    fig_diabetes_smoking = go.Figure(data=[go.Pie(labels=diabetes_counts['Smoking History'].index, values=diabetes_counts['Smoking History'].values, name='Smoking History - Diabetes')])
    fig_diabetes_heart = go.Figure(data=[go.Pie(labels=diabetes_counts['Heart Disease'].index, values=diabetes_counts['Heart Disease'].values, name='Heart Disease - Diabetes')])

    fig_non_diabetes_smoking = go.Figure(data=[go.Pie(labels=non_diabetes_counts['Smoking History'].index, values=non_diabetes_counts['Smoking History'].values, name='Smoking History - Non-Diabetes')])
    fig_non_diabetes_heart = go.Figure(data=[go.Pie(labels=non_diabetes_counts['Heart Disease'].index, values=non_diabetes_counts['Heart Disease'].values, name='Heart Disease - Non-Diabetes')])

    graphJSON_diabetes_smoking = json.dumps(fig_diabetes_smoking, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_diabetes_heart = json.dumps(fig_diabetes_heart, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_non_diabetes_smoking = json.dumps(fig_non_diabetes_smoking, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_non_diabetes_heart = json.dumps(fig_non_diabetes_heart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index10.html', graphJSON_diabetes_smoking=graphJSON_diabetes_smoking,
                           graphJSON_diabetes_heart=graphJSON_diabetes_heart,
                           graphJSON_non_diabetes_smoking=graphJSON_non_diabetes_smoking,
                           graphJSON_non_diabetes_heart=graphJSON_non_diabetes_heart)


@app.route('/logout')
@login_required
def logout():
    print("Logout")
    logout_user()
    return redirect(url_for('home_page'))

