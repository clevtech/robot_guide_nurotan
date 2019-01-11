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

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blabla'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
r = sr.Recognizer()
translator = Translator()
# Initialize OpenCV
cap = cv2.VideoCapture(0)
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def recognize_face():

	# TODO: тут надо прописать количество людей от ИК сенсора

	while True:
		ret, frame = cap.read()

		# Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		try:
			number = len(faces)
			size = [faces[0][2], faces[0][3]]
			position = [faces[0][0], faces[0][1]]
			if size[0] < 110:
				number = 0
			break
		except:
			a = 1

	return size, position, number


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


def listen_question(state, lang):
	with sr.Microphone() as source:
		# r.adjust_for_ambient_noise(source)
		duration = 1  # second
		freq = 440  # Hz
		# os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
		# os.system('say "Слушаю"')
		audio = r.listen(source)
		# os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
		# os.system('say "Думаю"')
		try:
			if state == 0:
				en = r.recognize_google(audio, language = "en-US")
				ru = r.recognize_google(audio, language = "ru-RU")
				print("Google Speech Recognition thinks you said in English: -  " + en)
				print("Google Speech Recognition thinks you said in Russian: -  " + ru)
				if en == "hello":
					lang = "en"
					question = en
				else:
					lang = "ru"
					question = ru
			else:
				if lang == "en":
					question = r.recognize_google(audio, language = "en-US")
				else:
					question = r.recognize_google(audio, language = "ru-RU")
			return question, lang
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return 1, lang
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			return 2, lang



def show_emotion(emotion):
	print(emotion)
	src = "/static/" + emotion.lower() + ".png"
	socketio.emit('my_response',
				  {'src': src},
				  namespace='/test')


def say_answer(answer, lang="ru"):
	print('say "' + str(answer) + '"')
	if lang == "en":
		os.system('say -v Karen "' + str(answer) + '"')
	else:
		os.system('say -v Milena "' + str(answer) + '"')
	# Send socks
	return True


def speak():
	# 1 = dialogues, 2 - fair, 3 - go to position A, 4 - go charge
	emotions = ["Angry", "Happy", "Normal", "Sexy", "Suprised", "Thinking"]
	lang = "ru"
	while True:
		show_emotion("Normal")
		size, position, number = recognize_face()
		if number > 0:
			open_phrase = "Для русского языка скажите привет"
			say_answer(open_phrase)
			say_answer("english say hello", "en")
			state = 0
			while True:
				question, lang = listen_question(state, lang)
				if question != 1 and question != 2:
					if lang == "en":
						question = translator.translate(question, dest='ru', src='en').text
					answer, emotion = give_answer(question)
					show_emotion(emotion)
					if lang == "en":
						answer = translator.translate(answer, dest='en', src='ru').text
						say_answer(answer, "en")
					else:
						say_answer(answer)
					state = 1
					size, position, number = recognize_face()
					if number < 1:
						break
				elif question == 1:
					size, position, number = recognize_face()
					if number < 1:
						break
					else:
						if lang == "en":
							say_answer("I cannot hear you. Louder, please.", "en")
						else:
							say_answer("Повторите, пожалуйста, Вас не слышно.")
				else:
					say_answer("Я поломалась. Мне надо на ремонт.")


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=speak)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == '__main__':
    socketio.run(app, port=7777, debug=True)
