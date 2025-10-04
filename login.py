from flask_login import LoginManager
from app import app
from db import db
from models import Usuario
import hashlib
lm=LoginManager(app)

def hash(txt):
    hash_obj=hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

@lm.user_loader
def user_loader(id):
    user=db.session.query(Usuario).filter_by(id=id).first()
    return user
    