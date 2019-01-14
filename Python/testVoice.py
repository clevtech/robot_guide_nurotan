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


r = sr.Recognizer()

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

while 1:
	with sr.Microphone(device_index=3) as source:
		print("Started: ")
		# r.adjust_for_ambient_noise(source)
		# duration = 1  # second
		# freq = 440  # Hz
		# os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
		# os.system('say "Слушаю"')
		audio = r.listen(source)
		en = r.recognize_google(audio, language = "en-US")
		print(en)
