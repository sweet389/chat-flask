from flask import Flask
from db import db
from login import lm
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='config.env')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB-URL')
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)
lm.login_view = 'login'

from app import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv('DEBUG'))