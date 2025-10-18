from flask_socketio import SocketIO

socketio=SocketIO(async_mode='eventlet', cors_allowed_origins="https://chat-flask-se3g.onrender.com")