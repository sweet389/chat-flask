from db import db
from flask_login import UserMixin

class Usuario(UserMixin,db.Model):
    __tablename__ = 'users'
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(32), unique=True, nullable=False)
    passwd= db.Column(db.String(), nullable=False)
    user_ip= db.Column(db.String(), nullable=False)
    created_at= db.Column(db.String())
    
    groups_created=db.relationship('Group', backref='creator',lazy=True)
    memberships=db.relationship('GroupMember', backref='user', lazy=True)
    
class Group(db.Model):
    __tablename__='groups'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32), nullable=False)
    passwd=db.Column(db.String(), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.Column(db.Boolean,default=False)
    created_at= db.Column(db.String())
    members=db.relationship('GroupMember', backref='group',lazy=True)
    
class GroupMember(db.Model):
    __tablename__='group_members'
    
    id=db.Column(db.Integer, primary_key=True)
    group_id=db.Column(db.Integer, db.ForeignKey('groups.id', ondelete="CASCADE"))
    user_id=db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    role=db.Column(db.String(20), default='member')
    
    __table_args__ = (db.UniqueConstraint('group_id', 'user_id', name='unique_member'),)
    
    