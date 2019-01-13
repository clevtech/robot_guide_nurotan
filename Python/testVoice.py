#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import glob
import serial
import time
import urllib.request


def serial_ports():
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


# types: Sonar - sonar arduino, Box - box controlling arduino
# returns serial connection
def connect():
	arduinos = serial_ports()
	print(arduinos)
	ser = []
	top, bot = 0, 0
	for i in range(len(arduinos)):
		ser.append(serial.Serial(arduinos[i], 115200))
		time.sleep(1)
		ser[i].write("3".encode())
		# time.sleep(0.1)
		types = ser[i].readline().strip().decode("utf-8")
		print(types)
		if types == "1":
			bot = ser[i]
		elif types == "0":
			top = ser[i]
	return bot, top


connect()
