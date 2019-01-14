#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, Cleverest Technologies"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import gevent.monkey
gevent.monkey.patch_all()
import requests
import glob
import os
from flask import Flask, render_template, session, request, json, jsonify, url_for, Markup, redirect
import random
import re
from pprint import pprint
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
import random
from threading import Lock
import json
import socket
from pymongo import*
from pymongo import MongoClient


async_mode = None
app = Flask(__name__)

@app.route('/mic/') # Вывод на экраны
def ekrany():
	return "1"

@app.route('/mic/<text>') # Вывод на экраны
def ekrany2(text):
	print(text)
	return "1"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777)
