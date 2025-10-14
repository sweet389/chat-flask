from flask import Flask
from db import db
from dotenv import load_dotenv
from .events import socketio
import os

load_dotenv(dotenv_path='config.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB-URL')
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio.init_app(app)

db.init_app(app)

from login import lm
lm.init_app(app)
lm.login_view = 'login'

import models
from app import routes

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()