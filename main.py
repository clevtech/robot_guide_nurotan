import speech_recognition as sr
import socket
import sys
import random
import apiai
import signal
import json
import glob # + (part of the Arduino part)
import serial # + (part of the Arduino part)
import time # + (part of the Arduino part)
from gtts import gTTS
import os
#################### Initial settings of the code #####################

r = sr.Recognizer()
r.energy_threshold = 4000
#r.dynamic_energy_threshold = True

#################### Sending emotion and response to client #####################

def send_to_display(top_conn, phrase, emotion):
    res = str(emotion) + "#ru-RU#" + phrase
    vysl = res.encode("utf8")
    top_conn.sendall(vysl)  # send it to client

#################### Receiving request from client #####################

def from_display(conn, MAX_BUFFER_SIZE = 4096):

    # the input is in bytes, so decode it
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input_from_client_bytes)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    print("Input from client is " + str(input_from_client))
    return input_from_client


#################### Initiating server side #####################

def start_server(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket 1 created')

    try:                #print(text)
        soc.bind((ip, port))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    # Start listening on socket
    soc.listen(1)
    print('Socket now listening')
    # this will make an infinite loop needed for
    # not reseting server for every client
    conn, addr = soc.accept()
    ip, port = str(addr[0]), str(addr[1])
    print('Accepting connection 1 from ' + ip + ':' + port)
    return conn, soc


#################### Listening questions #####################

def listen_question():
    audio = None
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('Скажите что нибудь')
        audio = r.record(source, duration = 3)
        try:
            text = r.recognize_google(audio, language='ru-RU')
            print('Вы сказали : {}'.format(text))
        except sr.UnknownValueError:
            text = None
        return text


###################################
#Answering the people using library (needed)
###################################

def say_answer(answer, lang1="ru"):
    if answer == "Я слушаю":
        time.sleep(1)
        return 0
    tts = gTTS(text=answer[0:int(len(answer)*3/5)], lang=lang1, slow=False)
    tts.save("good.mp3")
    some_command = "mpg321 good.mp3"
    os.system(some_command)
    os.system("rm good.mp3")



#################### Chat phase of the code #####################

def talking():
    number = arduino()
    if number > 0:
        open_phrase = "Задавайте вопросы, я вам помогу"
        print(open_phrase)
        send_to_display(top_conn, open_phrase, "Happy")
        say_answer(open_phrase)
        from_display(top_conn)
        while True:
            lis_phrase = "Я слушаю"
            send_to_display(top_conn, lis_phrase, "Thinking")
            say_answer(lis_phrase)
            question = listen_question()
            if question != None:
                answer, emotion = give_answer(question)
                send_to_display(top_conn, answer, emotion)
                say_answer(answer)
                from_display(top_conn)
            else:
                print('Не было вопроса')
                number = arduino()
                print(number)
                if number != 1:
                    #send_to_display(top_conn, "Куда ушел падла", "Angry")
                    break
                else:
                    sad_phrase = "Пожалуйста, повторите вопрос"
                    send_to_display(top_conn, sad_phrase, "Sad")
                    say_answer(sad_phrase)
                    from_display(top_conn)
    elif number == 0:
        if random.randint(1, 1000) == 1:
            catch_phrase = "Пожалуйста, подходите ко мне, " \
                           "я вам всё покажу, всё расскажу."
            send_to_display(top_conn, catch_phrase, "Happy")
            say_answer(catch_phrase)
            from_display(top_conn)


#################### Answering to the person #####################


def give_answer(question):
	request = apiai.ApiAI('c444a990e8b94f92ac13206b034a8f5a').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = question # Посылаем запрос к ИИ с сообщением от юзера
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
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
	return answer, emotion.capitalize()



#################### Listening to the IR sensor #####################

def arduino():
    ard.write(b'9')
    ardResponse = ard.readline().decode("utf-8").replace("\r\n", "")
    print(ardResponse)
    if(ardResponse == "2"):
        #print('Arduino true')
        digResponse = '1'
    elif(ardResponse == "3"):
        #print('Arduino false')
        digResponse = '0'
    else:
        print('Arduino else')
        digResponse = "0"
    return int(digResponse)


#################### Main part of the code - microphone initiation #####################


top_port = 6666
top_conn, top_soc = start_server("0.0.0.0", top_port)
port = '/dev/ttyUSB0'
try:
    ard = serial.Serial(port, 9600, timeout=4)
except:
    port = "/dev/ttyUSB1"
    ard = serial.Serial(port, 9600, timeout=4)

if from_display(top_conn) == "Hello":
    print("Face is connected")

send_to_display(top_conn, "Я подключена!", "Happy")
say_answer("Инициализация всей системы, протокол Зарождение")


while True:
    try:
        talking()
    except:
        talking()
