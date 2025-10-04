from db import db
from flask_login import UserMixin

class Usuario(UserMixin,db.Model):
    __tablename__ = 'users'
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(32), unique=True)
    passwd= db.Column(db.String())