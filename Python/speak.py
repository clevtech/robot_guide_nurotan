#!/usr/bin/env python3
from flask import Flask, render_template
import apiai
import json
import cv2
import os
from googletrans import Translator
from pprint import pprint
from gtts import gTTS
import sys
import glob
import serial
import time
from langdetect import detect
import threading
from threading import Lock, Thread
import time


# Global variables
state = 0
emotion = "happy"

app = Flask(__name__)

translator = Translator()
# Initialize OpenCV
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

lock = Lock()


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


def say_answer(answer, lang1="ru"):
	tts = gTTS(text=answer, lang=lang1)
	tts.save("good.mp3")
	os.system("mpg321 good.mp3")
	os.system("rm good.mp3")



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


@app.route('/mic/<text>/') # Вывод на экраны
def ekrany2(text):
	lock.aquire()
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


@app.route('/')
def index():
	global emotion
	lock.aquire()
	lock.release()
	number = recognize_face()
	if number > 0:
		say_answer("Слушаю", lang1="ru")
		return render_template('index.html', emo = emotion)
	else:
		return render_template('index2.html', emo = emotion)


# Main
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True, ssl_context='adhoc')
