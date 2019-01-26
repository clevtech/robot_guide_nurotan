#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO, send

import apiai
import json # + (part of the dialog part)
#import cv2 (unnecessary)
import os # + (part of the dialog part)
#from googletrans import Translator
from pprint import pprint # + (part of the dialog part)
from gtts import gTTS # + (main library of the dialog part)
import sys # + (part of Arduino library)
#import glob # + (part of the Arduino part)
#import serial # + (part of the Arduino part)
#import time # + (part of the Arduino part)
from langdetect import detect # ? (language detection, do we need translation)
#import threading # (unnecessary)
#from threading import Lock, Thread # (unnecessary)
#import time # ? (why do we import it two times?)

'''

# Classes

###################################
#Arduino initialization (necessary)
###################################

class arduino():
	def __init__(self, name="1"):
		self.ser = self.connect(name)
	def connect(self, name="1"):
		arduinos = self.serial_ports()
		ser = []
		bot = 0
		for i in range(len(arduinos)):
			ser.append(serial.Serial(arduinos[i], 115200))
			time.sleep(1)
			ser[i].write("3".encode())
			# time.sleep(0.1)
			types = ser[i].readline().strip().decode("utf-8")
			print(types)
			if types == "1":
				bot = ser[i]
		return bot
	def serial_ports(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/ttyACM*')
			print(ports)
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.usbmodem*')
		else:
			raise EnvironmentError('Unsupported platform')
		result = ports
		return result

translator
# Global variables
state = 0
run = 0
raz = 0
emotion = "happy"
# ard = arduino()
# bot = ard.ser

'''

###################################
#Flask initialization
###################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'noSecretJustEasternEgg!'

'''

translator = Translator()
# Initialize OpenCV
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

lock = Lock()

############################
#Sending commmands to arduino to control the hands (unnecessary)
############################

# Functions
# def handup(message="0", ard=bot, hand="r"):
# 	if hand=="l":
# 		message="1"
# 	ard.write(message.encode())
# 	out = ard.readline().strip().decode("utf-8")
# 	return out
#
#
# def handdown(message="2", ard=bot, hand="r"):
# 	if hand=="l":
# 		message="4"
# 	ard.write(message.encode())
# 	out = ard.readline().strip().decode("utf-8")
# 	return out
#

###################################
$Face recognition (unnecessary)
###################################

def recognize_face():
	while True:
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		try:
			number = len(faces)
			if number == 0:
				return 0
			size = [faces[0][2], faces[0][3]]
			if size[0] < 110:
				number = 0
			break
		except:
			pass
	return number

'''

###################################
#Answering the people using library (needed)
###################################

def say_answer(answer, lang1="ru"):
	tts = gTTS(text=answer, lang=lang1)
	tts.save("good.mp3")
	os.system("mpg321 good.mp3")
	os.system("rm good.mp3")

###################################
#Questioning people based on the aswers
###################################

def give_answer(question):
	print("Question: ")
	print(question)
	request = apiai.ApiAI('c444a990e8b94f92ac13206b034a8f5a').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = question # Посылаем запрос к ИИ с сообщением от юзера
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	pprint(responseJson)
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	# Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
	if response:
		answer = str(responseJson['result']['fulfillment']['speech'])
		try:
			emotion = str(responseJson['result']['parameters']['Emotion'])
		except:
			emotion = "Normal"
	else:
		answer = "Простите, я Вас не поняла. Можете перефразировать, я только учусь."
		emotion = "Thinking"
	return answer, emotion

'''
###################################
#Part of the face detection
###################################

# Threads
class search_faces(threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self.cap = cv2.VideoCapture(0)
	def run(self):
		while 1:
			global number
			time.sleep(1)
			lock.acquire()
			number = recognize_face()
			print("Number is: " + str(number))
			try:
				lock.release()
			except:
				pass


# main_thread = search_faces(1)
# main_thread.start()

# Flask routes

###################################
#Sending face emotion to FE (front-end)
###################################

@app.route('/mic/')
def ekrany():
	return "0happy.png"


###################################
#Part of the face recognition system (must be rewritten)
###################################

@app.route('/mic/<text>/') # Вывод на экраны
def ekrany2(text):
	global state
	global emotion
	global run
	global number
	global raz
	lock.acquire()
	if text[0] == "!":
		number = recognize_face()
		if number < 1:
			raz = 0
			run = 1
			try:
				lock.release()
			except:
				pass
			return "ok"
		else:
			say_answer("Повторите, пожалуйста, Вас не слышно.")
			state = 1
			emotion = "thinking"
			try:
				lock.release()
			except:
				pass
			return "ok"
	lang = detect(text)
	if lang == "en":
		text = translator.translate(text, dest='ru', src='en').text
	answer, emotion = give_answer(text)
	if lang == "en":
		answer = translator.translate(answer, dest='en', src='ru').text
		try:
			lock.release()
		except:
			pass
		say_answer(answer, "en")
	else:
		try:
			lock.release()
		except:
			pass
		say_answer(answer)
	if number < 1:
		print("Человек ушел")
		run = 1
		raz = 0
		try:
			lock.release()
		except:
			pass
	try:
		lock.release()
	except:
		pass
	return "ok"

'''

###################################
#Index html initialization
###################################


@app.route('/')
def index():
	# main_thread.start()
	return render_template('beka.html')

'''

###################################
#Start of the SocketIO functionВывод на экраны
def ekrany2(text):
	global state
	global emotion
	global run
	global number
	global raz
	lock.acquire()
	if text[0] == "!":
###################################normal

'''

socketio = SocketIO(app)

def arduinoListen():
	person = input('Is there a person?: ')
	print(person)
	return person

@socketio.on('hasConnected')
def handleMessage(message):
	print(message)
	person = '0'
	while (person == '0'):
		person = arduinoListen()
	socketio.emit('someoneApproached')

@socketio.on('initialFace')
def handlePerson():
	socketio.emit('message', 'Happy')

@socketio.on("chat message")
def handleChatMessage(message):
	print('Received chat message is: ' + message)
	if (message == 'no-speech'):
		socketio.emit('noSpeech', 'Normal')
	else:
		answer, emotion = give_answer(message)
		print("answer: " + answer)
		print("emotion: " + emotion)
		socketio.emit('message', emotion)

# Main
if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=7777, debug=True, ssl_context='adhoc')
	socketio.run(app) #host='0.0.0.0', port=5000, use_reloader=True, use_debugger=False)
