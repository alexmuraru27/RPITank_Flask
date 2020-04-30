from flask import Flask
from flask import render_template
from threading import Thread
import RPi.GPIO as GPIO
import time

#11 trig senzor distanta
trig=18
#22 Echo senzor
echo=22
#24 leduri
led=24

#33 EN A
en1=33
#35 MotorDreapta1
md1=35
#37 MotorDreapta2
md2=37

#32 EN B
en2=32
#36 Motor Stanga1
ms1=36
#38 Motor Stanga2
ms2=38

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

GPIO.setup(en1,GPIO.OUT)
GPIO.setup(md1,GPIO.OUT)
GPIO.setup(md2,GPIO.OUT)

GPIO.setup(en2,GPIO.OUT)
GPIO.setup(ms1,GPIO.OUT)
GPIO.setup(ms2,GPIO.OUT)

class Car:
	def __init__(self): 
		self.currentDistance="0"
		self.th=Thread(target=self.distanceLoop)
		self.th.start()

	def setDistance(self):
		tmp=self.currentDistance
		GPIO.output(trig,GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(trig,GPIO.LOW)
		while GPIO.input(echo)==0:
			start_t=time.time()
		while GPIO.input(echo)==1:
			stop_t=time.time()
		durata=stop_t-start_t
		dist=durata*342/2*100
		if(dist>400):
			dist=400
		self.currentDistance=str((float(dist)+float(tmp))/2)
		print("Noua distanta= "+self.currentDistance)

	def distanceLoop(self):
		while 1:
			self.setDistance()
			time.sleep(0.2)

	def getDistance(self):
		return self.currentDistance



app=Flask(__name__)
masina=Car()


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/distanta')
def sendDist():
	return masina.getDistance()


if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0')

	except Exception as e:
		print("Some Error "+str(e))
	finally:
		GPIO.cleanup()




