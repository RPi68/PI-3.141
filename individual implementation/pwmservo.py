# The python script
import RPI.GPIO as GPIO # import RPi Library 
GPIO.setmode(GPIO.BOARD)
servo=11
GPIO.setup(servo,GPIO.OUT)
pwm=GPIO.PWM(11,50) #set GPIO pin 11 to 50 Hz”frequency”
pwm.start(5)
for i in range (0,20):
	Position=input(“where do you want the servo? 0 - 108 ”)
	degree = 1./18.*(Position)+2 
	pwm.ChangeDutyCycle(degree)

pwm.stop() #stop the pulse width modulations 
GPIO.cleanup() #to clear everything up