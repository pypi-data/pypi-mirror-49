import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Servo:
	def __init__(self,num,angle):
		GPIO.setup(num,GPIO.OUT)
		p=GPIO.PWM(num,angle)
		self.angle = angle
		p.start(2.5)
		
		
	def transfer(self,t):
		f=10.0/180.0
		t=t*f+2.5
		t=int(t*10)/10.0
		return t
		
		
	def set(self,angle):
		if angle<0 or angle>180:
			p.stop()
		else:
			p.ChangeDutyCycle(transfer(angle))
