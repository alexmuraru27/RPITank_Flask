from flask import Flask, request
from flask import render_template
from threading import Thread
import RPi.GPIO as GPIO
import time

#18 trig senzor distanta
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



class Car:
	def __init__(self):
		self.trig=18
		self.echo=22
		self.led=24
		self.en1=33
		self.md1=35
		self.md2=37
		self.en2=32
		self.ms1=36
		self.ms2=38
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(self.trig, GPIO.OUT)
		GPIO.setup(self.echo,GPIO.IN)
		GPIO.setup(self.led,GPIO.OUT)
		GPIO.setup(self.en1,GPIO.OUT)
		GPIO.setup(self.md1,GPIO.OUT)
		GPIO.setup(self.md2,GPIO.OUT)
		GPIO.setup(self.en2,GPIO.OUT)
		GPIO.setup(self.ms1,GPIO.OUT)
		GPIO.setup(self.ms2,GPIO.OUT)
		self.currentDistance="0"
		self.blinkDelay=0.2
		self.blink=False
		self.ledState=0

		self.th=Thread(target=self.distanceLoop)
		self.th.start()
		self.ledTh=Thread(target=self.LEDloop)
		self.ledTh.start()
		self.stopLED()
		

	def setDistance(self):
		tmp=self.currentDistance
		GPIO.output(self.trig,GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.trig,GPIO.LOW)
		while GPIO.input(self.echo)==0:
			start_t=time.time()
		while GPIO.input(self.echo)==1:
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

	def LEDloop(self):
		while 1:
			if self.blink is True:
				if(self.ledState == 0):
					GPIO.output(self.led,GPIO.HIGH)
					self.ledState=1
				else:
					GPIO.output(self.led,GPIO.LOW)
					self.ledState=0
			time.sleep(self.blinkDelay)

	def startLED(self):
		self.stopBlink()
		GPIO.output(self.led,GPIO.HIGH)

	def stopLED(self):
		self.stopBlink()
		GPIO.output(self.led,GPIO.LOW)

	def startBlink(self):
		self.blink=True

	def stopBlink(self):
		self.blink=False




app=Flask(__name__)
masina=Car()



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/distanta')
def sendDist():
	return masina.getDistance()

@app.route('/led', methods=['POST'])
def functieLed():
	default_name = '0'
	data = request.form.get('led', default_name)
	if data=='on':
		masina.startLED()
		return render_template('index.html',ledstate="on")
	elif data=='off':
		masina.stopLED()
		return render_template('index.html',ledstate="off")
	elif data=='flash':
		masina.startBlink()
		return render_template('index.html',ledstate="flash")
	return render_template('index.html',ledstate="no")
	



if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0')

	except Exception as e:
		print("Some Error "+str(e))
	finally:
		GPIO.cleanup()




