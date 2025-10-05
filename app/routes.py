from app import app
from db import db
from login import hash
from flask_login import login_user, login_required, logout_user, current_user
from models import Usuario
from flask import render_template, redirect, request, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('auth/login.html')
    elif request.method=='POST':
        username=request.form['userForm']
        passwd=request.form['passForm']
        
        user=db.session.query(Usuario).filter_by(name=username, passwd=hash(passwd)).first()
        if not user:
            return render_template('auth/login.html')
        
        login_user(user)
        return redirect(url_for('chat'))
        
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('auth/register.html')
    elif request.method=='POST':
        username=request.form['userForm']
        passwd=request.form['passForm']
        new_user=Usuario(name=username, passwd=hash(passwd))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("chat"))

@app.route("/chat/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route("/chat")
@app.route('/')
@login_required
def chat():
    print(current_user, current_user.name)
    return render_template('main/home.html')

@app.route('/profile')
@login_required 
def profile():
    return render_template('main/profile.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404