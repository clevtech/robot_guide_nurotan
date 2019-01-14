import subprocess

args = ["ifconfig"]
process = subprocess.Popen(args, stdout=subprocess.PIPE)
print("Started")
data = process.stdout.readline()
print(data)
data = process.stdout.readline()
print(data)
