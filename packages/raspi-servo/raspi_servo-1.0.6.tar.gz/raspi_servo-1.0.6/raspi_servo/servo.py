import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Servo:


	def __init__(self,num,angle):
		GPIO.setup(num,GPIO.OUT)
		self.p=GPIO.PWM(num,50)
		self.p.start(self.transfer(angle))
		
		
	def transfer(self,t):
		d=round(t*10.0/180.0+2.5,1)
		return d
		
		
	def set(self,angle):
		
		if angle<0 or angle>180:
			self.p.stop()
		else:
			self.p.ChangeDutyCycle(self.transfer(angle))
