import RPi.GPIO as GPIO

def transfer(Num):
	fm=10.0/180.0
	Num=Num*fm+2.5
	Num=int(Num*10)/10.0
	return Num
	
def Servo(num,angle):
	p=GPIO.PWM(num,50)
	p.start(2.5)
	if Num<0 or Num>180:
		p.stop()
		exit()
	else:
		p.ChangeDutyCycle(transfer(angle))
