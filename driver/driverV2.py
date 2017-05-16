import RPi.GPIO as GPIO #import RPi Library
import curses # import curses Library
import sys 
import time

pyFile = open('DriverRobotMovement.txt', 'w')

GPIO.setmode(GPIO.BOARD)
#servo pin
servoPin=11
#-----------------------------------------------------------------
#motor pins to use
motor1 =33#pwm signal
fwd =35
dck =37
#-----------------------------------------------------------------
# Define GPIO to use on Pi
GPIO_TRIGGER = 33 # set pin 33 for trigger
GPIO_ECHO    = 35 # set pin 11 as echo 
#-----------------------------------------------------------------
# Set Servo pins as output
GPIO.setup(servoPin,GPIO.OUT)
#------------------------------------------------------------------
# Set Motor pins as output
GPIO.setup(motor1,GPIO.OUT)
GPIO.setup(fwd,GPIO.OUT)
GPIO.setup(dck,GPIO.OUT)
#------------------------------------------------------------------
# Set Ultrasonic pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
#------------------------------------------------------------------
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)
#------------------------------------------------------------------
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
z = True
ff=0
rev=0
zzz=90


pwm=GPIO.PWM(11,50) #set GPIO pin 11 to 50 Hz the 'Frequency'
p = GPIO.PWM(motor1,50) #set motor1  
p.start(0)
start = 1./18.*(zzz)+2 # starting the servo at a straight positions at 90 degree
pwm.start(start)


def forward(x):
    check = ultra()
    if chech < 15.00:# if object found at 15 cm
        # stop or don't do anything

    else:
        GPIO.output(fwd, GPIO.HIGH)
        p.ChangeDutyCycle(x)
        time.sleep(2)

def reverse(x):
    GPIO.output(dck, GPIO.HIGH)
    p.ChangeDutyCycle(x)
    time.sleep(2)

def servo(x):
    global value2
    degree = 1./18.*(x)+2
    value2='%s %d%%' % ('The second value print at the following degree',degree)
    pwm.ChangeDutyCycle(degree)

def ultra():
    # Allow module to settle
    time.sleep(0.5)

    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    return distance

try:
    while True:
        char= screen.getch()
        if char == ord('q'):
            value=('quit/end')
            pwm.stop() # Stop the pulse width modulations
            GPIO.cleanup() # Clean / Clear erverthing up "Pins"
            #-----Closing/stoping pwm-----
            pwm.stop() #stop the pulse width modulations
            p.stop()
            #GPIO.cleanup() #Clean up all ports which was in use.
            break
            
        elif char ==curses.KEY_UP:
            forward(45)
                

        elif char ==curses.KEY_DOWN:
            reverse(45)

        # Logic for stering LEFT             
        elif char ==curses.KEY_LEFT:
            if (zzz>=80) and (zzz<180):
                if z== True:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING LEFT',zzz)
                elif z== False:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING LEFT',zzz)
            elif (z != True) and (zzz < 90):
                if zzz < 90:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING LEFT',zzz)

        # Logic for stering RIGHT        
        elif char ==curses.KEY_RIGHT:
            if z== True:
                # math to calculate the degree to move in degree
                zzz=zzz-10
                # calling the servo method and send in the degree to move to
                servo(zzz)
                value='%s %d' % ('STERING RIGHT',zzz)
            elif z== False:
                if zzz >=100:

                    if zzz ==100:
                        # math to calculate the degree to move in degree
                        zzz=zzz-10
                        # calling the servo method and send in the degree to move to
                        servo(zzz)
                        value='%s %d' % ('Straight',zzz)

                    else:
                        # math to calculate the degree to move in degree
                        zzz=zzz-10
                        # calling the servo method and send in the degree to move to
                        servo(zzz)
                        value='%s %d' % ('STERING RIGHT',zzz)

                elif zzz <= 90:
                    if zzz >=20:
                        # math to calculate the degree to move in degree   
                        zzz=zzz-10
                        # calling the servo method and send in the degree to move to
                        servo(zzz)
                        value='%s %d' % ('STERING RIGHT',zzz)

        z = False 

        y = (value2)
        x = (value)    
        pyFile.write(x+"\n")
        pyFile.write(y+"\n")

finally:
    #close curses properly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    pyFile.close()
    #Closing/stoping pwm
    pwm.stop() #stop the pulse width modulations
    p.stop()
    GPIO.output(fwd, GPIO.LOW)
    GPIO.output(dck, GPIO.LOW)
    GPIO.cleanup() #Clean up all ports which was in use.
