from flask import Flask, render_template, session
from flask_socketio import SocketIO, join_room, emit


# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('my_response', username + ' has entered the room.', room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
