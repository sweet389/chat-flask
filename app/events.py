from sock import socketio
from flask_socketio import emit
from flask import request
from flask_login import current_user
from flask_socketio import leave_room, join_room, send
users={}
users_group={}


@socketio.on("connect")
def handle_connection():
    print("Cliente Conectado!")
    
    
@socketio.on("user_connect")
def handle_user_join(user, group_id):
    print(f"{user} Joined on {group_id}")
    users[user]=request.sid
    users_group[request.sid] = group_id
    print(users)
    join_room(group_id)
    emit("chat", {
        "message": f"{user} has entered the room",
        'username': "System"
    },to=group_id)
      
@socketio.on("disconnect")
def handle_user_disconnect():
    user=None
    sid=request.sid
    group_id= users_group.get(sid)
    for u, s in users.items():
        if s == sid:
            user = u
            break
    print(f"{user} Left at {group_id}")
    emit("chat", {
        "message": f"{user} has left the room",
        'username': "System"
    },to=group_id)

    if user:
        del users[user]
    if sid in users_group:
        del users_group[sid]
    if group_id:
        leave_room(group_id)
        send({"name": user, "message": "has left the room"}, to=group_id)
    
@socketio.on('new_message')
def new_menssage(message, group_id):
    username=current_user.name
    emit("chat", {
        "message": message,
        'username': username
    },to=group_id)
    print(f"{message} sended by {username} to {group_id}")
    

