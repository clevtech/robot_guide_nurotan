#!/usr/bin/env python3
import gevent.monkey
gevent.monkey.patch_all()
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
import random
import apiai
import json
import cv2
import os
import speech_recognition as sr
from googletrans import Translator
from pprint import pprint
from gtts import gTTS
import os
import sys
import glob
import serial
import time
import urllib.request


async_mode = None
app = Flask(__name__)

nums = random.random()

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


## Socket
@socketio.on('message', namespace="/bla") # Принимать сигналы и отправлять
def handle_my_custom_namespace_event():
	print("Sent")
	socketio.sleep(0.1)
	socketio.send("1", namespace="/type")

	# socketio.sleep(0.1)

@socketio.on('my event', namespace="/bla") # Принимать сигналы и отправлять
def handle_message(json1):
	print("Input is: ")
	print(json1)


## Render
@app.route('/') # Вывод на планшеты
def tablet():
	# return render_template('index.html', async_mode=socketio.async_mode, ip=ip)
	return render_template('test.html', async_mode=socketio.async_mode)



if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8888, debug=True)
