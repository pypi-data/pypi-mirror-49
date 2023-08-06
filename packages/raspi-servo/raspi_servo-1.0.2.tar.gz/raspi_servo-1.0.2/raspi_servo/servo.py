import RPi.GPIO as GPIO

def transfer(t):
	f=10.0/180.0
	t=t*f+2.5
	t=int(t*10)/10.0
	return t
	
def set(num,angle):
	p=GPIO.PWM(num,50)
	p.start(2.5)
	if num<0 or num>180:
		p.stop()
		exit()
	else:
		p.ChangeDutyCycle(transfer(angle))
