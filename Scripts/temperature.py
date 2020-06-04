import os
import time
import requests
import json
from subprocess import call
from subprocess import check_output
from datetime import datetime

PBKEY = "o.joQbY3INTmIGERoTAhV6AHH6i49XpW6X"
DEVID = "ujAx0CaPfnosjCTV4Bcnme"

def send(message):
    url = 'https://api.pushbullet.com/v2/pushes'
    content = {
        "body": message,
        "title": "Message from RPI",
        "device_iden": DEVID,
        "type": "note"}
    headers = {'Access-Token': PBKEY, 'content-type': 'application/json'}
    try:
        requests.post(url, data=json.dumps(content), headers=headers)
    except Exception as e:
        return (":( An error occurred while sending data to Pushbullet:", {e})

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

def get_pid(name):
	try:
		return check_output(["pidof","-x",name])
	except:
		return(0)

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
                               
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))



def logger(message,type):
	with open("log.txt", type) as myfile:
		myfile.write(message+"\n")

log=0
logger("Start","w")
while True:
	if (log<10):
		type="a"
	if (log>20160):
		type="w"
		log=0	
	now=datetime.now()
	dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
	logger("Log number: "+str(log),type)	
	print("Log Number: "+str(log))
	logger(dt_string,"a")
	print(dt_string)	
	temp=measure_temp()[0:-1]
	temp_val = float(temp[0:3])
	raminfo = getRAMinfo()
	ram=str(float(raminfo[1])/1000)
	cpu = getCPUuse()
	if temp_val > 80:
		(send("Temperature: "+temp+", Device extemely hot, please turn off RPI! -"+dt_string))	
	elif temp_val > 70:
		(send("Temperature: "+temp+", Getting hot, please turn fan on! -"+dt_string))	
	elif temp_val > 65:
		(send("Temperature: "+temp+", Please turn fan on! -"+dt_string))
	if(get_pid("run.sh")):
		logger("MusicBot is running","a")
		print("MusicBot is running")
	elif(get_pid("run.sh")==0):
		try:
			call(["bash", "../MusicBot/run.sh"])
		except:
			logger("MusicBot is NOT running","a")
			print("MusicBot is NOT running")	
			send("MusicBot is NOT running -"+dt_string)	        	
	logger(temp,"a")
	print(temp)
	logger("CPU Usage: "+cpu+"%","a")
	print("CPU Usage: "+cpu+"%")
	logger("RAM Usage: "+ram+" mb","a")
	print("RAM Usage: "+ram+" mb")
	logger("--------------------------------","a")
	print("--------------------------------")
	log+=1
	time.sleep(30)


