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


# Initialize OpenCV
# cap = cv2.VideoCapture(0)
# cap.set(3, 640) #WIDTH
# cap.set(4, 480) #HEIGHT
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def recognize_face():
	while True:
		# ret, frame = cap.read()
		frame = cv2.imread("1.png")
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

print(recognize_face())
