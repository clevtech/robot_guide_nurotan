import os
import subprocess

subprocess.Popen("mpg321 dance.mp3", shell=True)
# os.system("mpg321 dance.mp3 &")
# os.spawnl(os.P_DETACH, 'mp321 dance.mp3')
print("Hello")
