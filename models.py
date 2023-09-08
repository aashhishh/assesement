from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

jwt_expiration_mins = int(os.getenv('JWT_EXPIRATION_TIME'))

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=jwt_expiration_mins)

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate=Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    mobile = db.Column(db.String(10), unique = True,nullable =False)
    role=db.db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(36))


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50))
    desc = db.Column(db.String(1000))
    category = db.Column(db.String(30))


