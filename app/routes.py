from app import app
from flask import render_template

@app.route('/')
@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route("/register")
def register():
    return render_template('auth/register.html')

@app.route("/chat")
def chat():
    return render_template('main/home.html')