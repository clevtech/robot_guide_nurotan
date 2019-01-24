#!/usr/bin/env python3
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import random


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# То что крутиться на заднем фоне
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        # Спит 0.1 секунду
        socketio.sleep(0.1)
        count += 1
        x = input("Value is: ")
        socketio.emit("chat message", x)


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@app.route('/')
def index():
    return render_template('beka.html', async_mode=socketio.async_mode)



if __name__ == '__main__':
    socketio.run(app, debug=True)
