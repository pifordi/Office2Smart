'''
IoT Hackathon Izmir - Office2Smart by Semih YILDIRIM
Hackathon is evaluated in Depark Beta/Izmir/Turkey at 3-4 March 2016
Event Page: https://iotizmir.splashthat.com/

Intel Edison and Seeed Studio Grove Starter Kit Plus for Galileo Gen2(Intel IoT Edition) was used.
Unboxing Intel Edison + Seeed Studio Grove Starter Kit Plus for Galileo Gen2(Intel IoT Edition) on my blog page in Turkish:
https://yildirimsemih.wordpress.com/2016/02/06/seeed-grove-sensor-kitintel-edison-kutu-acilimiilk-bakis/
Seeed Studio Grove Kit wiki page: http://www.seeedstudio.com/wiki/Main_Page

Server side source codes by using Flask for server framework, mraa for pin programming
Related blog post in here: https://yildirimsemih.wordpress.com/2016/03/05/iot-hackathon-izmir-office2smart/

Twitter: @SemihYILDIRIMTR
'''



import mraa #you can also use wiring-x86
import math
from flask import Flask,render_template
from datetime import datetime #update your machine's time before executing
app = Flask(__name__)

app.debug = True 


sensor2 = {"sensor": "ldr", "data": "0", "date": ""} #you can use this dict type method to send json response to client
sensor3 = {"sensor": "microfon", "data": "0", "date": ""}
sensor4 = {"sensor": "temperature", "data": "0", "date": ""}

y = mraa.Aio(1) #set A1 pin as analog input for light sensor v1.1, http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
z = mraa.Aio(2) #set A2 pin on Grove Base Shield v2.0 for sound sensor v1.6, http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
t = mraa.Aio(3) #set A3 pin on Grove Base Shield v2.0 for temperature sensor v1.2, http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor

def ldr():
        sensorValue = int(y.read())
        #from sensorValue to LUX was taken from Grove Starter Kit book

        if(sensorValue == 0):
                lux = 0                         #0
        if(0 < sensorValue <= 100):
                lux = str(lower than 1)         #lower than 1 LUX
        elif(100 < sensorValue <= 200):
                lux = 1                         #almost 1 LUX, Full moon overhead at tropical latitudes 
        elif(200 < sensorValue <= 300):
                lux = 3                         #almost 3 LUX, Twilight in the city
        elif(300 < sensorValue <= 400):
                lux = 6                         #almost 6 LUX
        elif(400 < sensorValue <= 500):
                lux = 10                        #almost 10 LUX
        elif(500 < sensorValue <= 600):
                lux = 15                        #almost 15 LUX
        elif(600 < sensorValue <= 700):
                lux = 35                         #almost 35 LUX, Family living room
        elif(700 < sensorValue <= 800):
                lux = 80                         #almost 80 LUX, Office building light in hallway
        elif(800 < sensorValue <= 900):
                lux = str(higher than 100        #almost 100 LUX, Very dark or Overcast day

	sensor2_data["data"] = lux
	sensor2_data["date"] = datetime.now() #read time and write on sensor data

def microfon():
        sensorValue = z.read()          #read analog value from sensor
        dB = (20 * math.log10(10)) * (sensorValue / 5) #convert analog sensorValue to dB 
	sensor3_data["data"] = dB
	sensor3_data["date"] = datetime.now()

def temperature():
        B = 4275                       #B value of the thermistor
        R0 = 100000                    # R0 = 100k

        sensorValue = t.read()         #read analog value from sensor input
 
        float R = 1023.0/((float)sensorValue)-1.0;
        R = 100000.0*R;
 
        float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15; #convert to temperature via datasheet 
 
	sensor4_data["data"] = temperature
	sensor4_data["date"] = datetime.now() #update sensor reading time

@app.route("/", methods=["GET", "POST"]) #home page, accept only get and post requests
def home():
        # a is Light sensor value on html file
        # b is Sound sensor value on html file
        # c is Temperature sensor value on html file
        # d is Date on html file                  
	return render_template('home.html', a=sensor2.get('data'), b=sensor3.get('data'), c=sensor4.get('data'), d=sensor4.get("date"));
        #return templating html with updated values



if __name__ == '__main__':
	app.run(host = '192.168.1.27') #update ip address with your machine's ip address
