import eventlet
eventlet.monkey_patch()
from flask import Flask
from db import db
from app import email
from dotenv import load_dotenv
from .events import socketio
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
load_dotenv(dotenv_path='config.env')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB-URL')
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

limiter = Limiter(
    get_remote_address,
    app=app,
)
app.permanent_session_lifetime = timedelta(minutes=15)

email_log=email.KeywordEmailHandler("Baltrota")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
email_log.setFormatter(formatter)
app.logger.addHandler(email_log)
app.logger.setLevel(logging.INFO)

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