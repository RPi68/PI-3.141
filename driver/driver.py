import RPi.GPIO as GPIO #import RPi Library
import curses # import curses Library
import sys 
import time

pyFile = open('DriverRobotMovement.txt', 'w')

GPIO.setmode(GPIO.BOARD)
servoPin=11
fwdPin= 33
bckPin= 11
GPIO.setup(servoPin,GPIO.OUT)
GPIO.setup(fwdPin,GPIO.OUT)
#GPIO.setup(bckPin,GPIO.OUT)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
z = True
ff=0
rev=0
zzz=90


pwm=GPIO.PWM(11,50) #set GPIO pin 11 to 50 Hz the 'Frequency'
start = 1./18.*(zzz)+2 # starting the servo at a straight positions at 90 degree
pwm.start(start)
sleeptime=1

drive = GPIO.PWM(fwdPin,207)

drive.start(0)

def forward(x):

    drive=ChangeDutyCycle(x)

def reverse(x):
    #GPIO.setmode(bckPin, GPIO.High)
    #time.sleep(x)
    #GPIO.setmode(bckPin, GPIO.LOW)

def servo(x):
    global value2
    degree = 1./18.*(x)+2
    value2='%s %d%%' % ('The second value print at the following degree',degree)
    pwm.ChangeDutyCycle(degree)


try:
    while True:
        char= screen.getch()
        if char == ord('q'):
            value=('quit/end')
            pwm.stop() # Stop the pulse width modulations
            GPIO.cleanup() # Clean / Clear erverthing up "Pins"
            #-----Closing/stoping pwm-----
            pwm.stop() #stop the pulse width modulations
            drive.stop()
            #GPIO.cleanup() #Clean up all ports which was in use.
            break
            
        elif char ==curses.KEY_UP:

            if (ff <= 90) and rev == 0:

                if z == True:
                    ff=ff+10
                    forward(ff)
                    value='%s %d%%' % ('FORWARD',ff)

                elif z== False:
                    ff=ff+10
                    value='%s %d%%' % ('FORWARD',ff)

            elif (z != True) and (rev !=0):

                if rev == 10:
                    rev = rev-10
                    value='%s %d%%' % ('STOP/BREAKING',rev)

                elif rev > 10:
                    rev = rev-10
                    value='%s %d%%' % ('REVERSE',rev)    
                

        elif char ==curses.KEY_DOWN:
            if ff != 0:

                if ff == 10:
                    ff=ff-10
                    forward(ff)
                    value='%s %d%%' % ('STOP/BREAKING',ff)

                elif ff > 10:   
                    ff=ff-10
                    forward(ff)
                    value='%s %d%%' % ('FORWARD',ff)

            elif ff == 0:
                
                if rev <= 90:
                    rev = rev+10
                    value='%s %d%%' % ('REVERSE',rev)

        # Logic for stering right             
        elif char ==curses.KEY_RIGHT:
            if (zzz>=80) and (zzz<180):
                if z== True:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING RIGHT',zzz)
                elif z== False:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING RIGHT',zzz)
            elif (z != True) and (zzz < 90):
                if zzz < 90:
                    # math to calculate the degree to move in degree
                    zzz=zzz+10
                    # calling the servo method and send in the degree to move to
                    servo(zzz)
                    value='%s %d' % ('STERING LEFT',zzz)

        # Logic for stering Left        
        elif char ==curses.KEY_LEFT:
            if z== True:
                # math to calculate the degree to move in degree
                zzz=zzz-10
                # calling the servo method and send in the degree to move to
                servo(zzz)
                value='%s %d' % ('STERING LEFT',zzz)
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
                        value='%s %d' % ('STERING LEFT',zzz)

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
    drive.stop()
    GPIO.cleanup() #Clean up all ports which was in use.
