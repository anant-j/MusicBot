from flask import Flask
import os
import time
from subprocess import check_output
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def temp():
    response=""
    now=datetime.now()
    response += now.strftime("%d-%m-%Y %H:%M:%S") + "<br/>"
    response +=measure_temp() + "<br/>"
    response +="CPU Usage: "+getCPUuse()+"%<br/>"
    ram=getRAMinfo()
    response +="Total Ram: "+str(float(ram[0])/1000)+"mb <br/>"
    response +="Used Ram: "+str(float(ram[1])/1000)+"mb <br/>"
    response +="Free Ram: "+str(float(ram[2])/1000)+"mb <br/>"
    if(get_pid("run.sh")!=0):
	response+="MusicBot is running"
    elif(get_pid("run.sh")==0):
	response+="MusicBot is Not running"
    return (response)

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp)
	

def get_pid(name):
	try:
		return check_output(["pgrep","-f",name])
	except:
		return(0)

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))


if __name__ == "__main__":
    app.run()