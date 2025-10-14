from app import app
from db import db
from login import hash
from flask_login import login_user, login_required, logout_user, current_user
from models import Usuario, Group, GroupMember
from flask import render_template, redirect, request, url_for, session

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
    print(request.form.keys())
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

@app.route('/profile', methods=['POST', 'GET'])
@login_required 
def profile():
    if request.method=='GET':
        return render_template('main/profile.html')
    elif request.method=='POST':
        user=db.session.query(Usuario).filter_by(id=current_user.id).first()
        user.name=request.form['userForm']
        db.session.commit()
        return redirect(url_for('profile'))

@app.route('/group/create', methods=['POST', 'GET'])
@login_required
def create_group():
    if request.method=='POST':
        name=request.form['group_name']
        _passwd=request.form['passwd']
        public=request.form.get('public')
        print(public)
        if public=='on': 
            group = Group(name=name, created_by=current_user.id, public=True)
            db.session.add(group)
            db.session.flush()
            membership = GroupMember(group_id=group.id, user_id=current_user.id, role='owner')
            db.session.add(membership)
        elif public==None:
            group = Group(name=name,passwd=hash(_passwd), created_by=current_user.id,public=False)
            db.session.add(group)
            db.session.flush()
            membership = GroupMember(group_id=group.id, user_id=current_user.id, role='owner')
            db.session.add(membership)
        db.session.commit()
        return redirect(url_for('create_group'))
    elif request.method=='GET':
        return render_template('group/create.html')

@app.route('/group/search', methods=['GET', 'POST'])
@login_required
def search_group():
    if request.method=='GET':
        lista_grupos=db.session.query(Group).filter_by(public=True).all()
        lista_grupospv=db.session.query(Group).join(GroupMember).filter(GroupMember.user_id == current_user.id,Group.public.is_(False)).all()
        return render_template('group/search.html', groups_public=lista_grupos, groups_private=lista_grupospv)
    elif request.method=='POST':
        print(request.form['group_name'], request.form['group_pass'])
        add_member(request.form['group_name'], request.form['group_pass'])
        return redirect(url_for('search_group'))
    
@app.route('/group/<int:group_id>')
@login_required
def public_group(group_id):
    group = Group.query.filter_by(id=group_id, public=True).first()
    if not group:
        return redirect(url_for("search_group"))
    return render_template('group/group.html', group=group, user=current_user.name)

@app.route('/g/<int:group_id>')
@login_required
def private_group(group_id):
    group = Group.query.filter_by(id=group_id, public=False).first()
    print(db.session.query(GroupMember).join(Group).filter(GroupMember.user_id == current_user.id, Group.public.is_(False), Group.id==group_id).first())
    if not group or  not db.session.query(GroupMember).join(Group).filter(GroupMember.user_id == current_user.id, Group.public.is_(False), Group.id==group_id).first():
        print(f"{current_user.name} kicked from {group_id}")
        return redirect(url_for("search_group"))
    return render_template('group/group.html', group=group, user=current_user.name)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def add_member(name, passwd):
    group=db.session.query(Group).filter_by(name=name, passwd=hash(passwd), public=False).first()
    membership = GroupMember(group_id=group.id, user_id=current_user.id, role='member')
    db.session.add(membership)
    db.session.commit()