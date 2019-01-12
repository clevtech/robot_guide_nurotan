from gtts import gTTS
import os


tts = gTTS(text='Good morning', lang='en')
tts.save("good.mp3")
os.system("mpg321 good.mp3")
os.system("rm good.mp3")

tts = gTTS(text='Привет друг', lang='ru')
tts.save("good.mp3")
os.system("mpg321 good.mp3")
os.system("rm good.mp3")
