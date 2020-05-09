from flask import Flask, request
from flask import render_template
from threading import Thread
import json
import RPi.GPIO as GPIO
import time

#18 trig distance sensor
trig=18
#22 Echo sensor
echo=22
#24 leds
led=24

#33 EN A
en1=33
#35 MotorRight1
md1=35
#37 MotorRight2
md2=37

#32 EN B
en2=32
#36 Motor Left1
ms1=36
#38 Motor Left2
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
		self.leftRunning=False
		self.rightRunning=False
		self.leftPWM=GPIO.PWM(self.en2, 500)
		self.leftPWM.start(0)
		self.rightPWM=GPIO.PWM(self.en1, 500)
		self.rightPWM.start(0)
		self.leftPWMVal=0
		self.rightPWMVal=0
		self.pwmrate=10

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

	def moveTankCoords(self,x,y):
		w=(1-abs(y))*(x)+x
		v=(1-abs(x))*(y)+y
		l=(v+w)/2*100
		r=(v-w)/2*100
		print("r= "+str(r)+"\n l= "+str(l))
		

		if l>0:
			GPIO.output(self.ms1,GPIO.LOW)
			GPIO.output(self.ms2,GPIO.HIGH)
			self.leftRunning=True
		elif l<0:
			GPIO.output(self.ms1,GPIO.HIGH)
			GPIO.output(self.ms2,GPIO.LOW)
			self.leftRunning=True
		else:
			GPIO.output(self.ms1,GPIO.LOW)
			GPIO.output(self.ms2,GPIO.LOW)
			self.leftRunning=False

		if r>0:
			GPIO.output(self.md1,GPIO.LOW)
			GPIO.output(self.md2,GPIO.HIGH)
			self.rightRunning=True
		elif r<0:
			GPIO.output(self.md1,GPIO.HIGH)
			GPIO.output(self.md2,GPIO.LOW)
			self.rightRunning=True
		else:
			GPIO.output(self.md1,GPIO.LOW)
			GPIO.output(self.md2,GPIO.LOW)
			self.rightRunning=False

		print(str(self.rightRunning ))
		print(str(self.leftRunning ))

		if self.rightRunning == True:
			if self.leftPWMVal >=100:
				self.leftPWMVal=100
			else:
				if abs(self.leftPWMVal)<abs(l):
					self.leftPWMVal=self.leftPWMVal+self.pwmrate
				if abs(self.leftPWMVal)>abs(l):
					self.leftPWMVal=self.leftPWMVal-self.pwmrate
			if self.leftPWMVal <0:
				self.leftPWMVal=0
			self.leftPWM.ChangeDutyCycle(self.leftPWMVal)
		else:
			self.leftPWM.ChangeDutyCycle(0)
			self.leftPWMVal=0


		if self.leftRunning == True:
			if self.rightPWMVal >=100:
				self.rightPWMVal=100
			else:
				if abs(self.rightPWMVal)<abs(r):
					self.rightPWMVal=self.rightPWMVal+self.pwmrate
				if abs(self.rightPWMVal)>abs(r):
					self.rightPWMVal=self.rightPWMVal-self.pwmrate
			if self.rightPWMVal <0:
				self.rightPWMVal=0
			self.rightPWM.ChangeDutyCycle(self.rightPWMVal)
		else:
			self.rightPWM.ChangeDutyCycle(0)
			self.rightPWMVal=0




		




app=Flask(__name__)
masina=Car()



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/distanta')
def sendDist():
	return masina.getDistance()

@app.route('/led', methods=['POST'])
def ledFunction():
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
	
@app.route('/move', methods=['POST'])
def moveTank():
	(x,y)=str(request.data)[2:-1].split(",")
	y=-float(y)
	x=float(x)
	masina.moveTankCoords(x,y)
	return "ok"


if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0')

	except Exception as e:
		print("Some Error "+str(e))
	finally:
		GPIO.cleanup()




