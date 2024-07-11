from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///model.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '89d2be80b2a972451fda9bf50e85c94cc374fc79239b966d'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"

from applications import routes