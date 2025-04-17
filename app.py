import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://chatroomfront.onrender.com"}})
socketio = SocketIO(app, cors_allowed_origins="https://chatroomfront.onrender.com")

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': 'Server', 'message': f'{username} has joined the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'username': 'Server', 'message': f'{username} has left the room.'}, room=room)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    emit('message', {'username': username, 'message': message}, room=room)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) 
    socketio.run(app, host='0.0.0.0', port=port)
