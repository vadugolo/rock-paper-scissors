from __future__ import division
import time
import random
import RPi.GPIO as GPIO
import os

gpio_pin_number=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
a=[240,160,-168,200,150]
b=[330,160,340,170,170] # y = a*x+b

# finger: 1 - thumb, 5 - little finger
# closepct: 0 - open finger, 100 - closed finger
def setfingerpos(finger, closepct):
    global a,b
    channel=finger-1
    if closepct==100:
        closepct=105
        offval=a[channel]*closepct//100+b[channel]
        pwm.set_pwm(channel, 0, offval)
        time.sleep(0.2)
        closepct=95
        offval=a[channel]*closepct//100+b[channel]
        pwm.set_pwm(channel, 0, offval)
    elif closepct==0:
        closepct=-5
        offval=a[channel]*closepct//100+b[channel]
        pwm.set_pwm(channel, 0, offval)
        time.sleep(0.2)
        closepct=5
        offval=a[channel]*closepct//100+b[channel]
        pwm.set_pwm(channel, 0, offval)
    else:
        # ez igy onmagaban hosszu tavon leegeti a servo motorokat
        # ezert csak akkor allitja be pontosan a kivant erteket
        # ha nem kell teljesen kinyitni/becsukni az ujjat
        offval=a[channel]*closepct//100+b[channel]
        pwm.set_pwm(channel, 0, offval)
    #print("offval=",offval)
    time.sleep(0.05)

def showone():
    print('egy')
    setfingerpos(1,0)
    setfingerpos(2,100)
    setfingerpos(3,100)
    setfingerpos(4,100)
    setfingerpos(5,100)

def showtwo():
    print('ketto')
    setfingerpos(1,0)
    setfingerpos(2,0)
    setfingerpos(3,100)
    setfingerpos(4,100)
    setfingerpos(5,100)

def showthree():
    print('harom')
    setfingerpos(1,0)
    setfingerpos(2,0)
    setfingerpos(3,0)
    setfingerpos(4,100)
    setfingerpos(5,100)

def showrock():
    print('ko')
    setfingerpos(1,100)
    setfingerpos(2,100)
    setfingerpos(3,100)
    setfingerpos(4,100)
    setfingerpos(5,100)


def showpaper():
    print('papir')
    setfingerpos(1,0)
    setfingerpos(2,0)
    setfingerpos(3,0)
    setfingerpos(4,0)
    setfingerpos(5,0)

def showscissors():
    print('ollo')
    setfingerpos(1,100)
    setfingerpos(2,0)
    setfingerpos(3,0)
    setfingerpos(4,100)
    setfingerpos(5,100)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

while True:
    showrock()
    time.sleep(0.5)
    showone()
    time.sleep(1)
    showtwo()
    time.sleep(1)
    showthree()
    time.sleep(1)
    r=random.randrange(3)
    if r==0:
        showrock()
    elif r==1:
        showpaper()
    else:
        showscissors()
    try:
        #GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
        if not GPIO.input(gpio_pin_number):
            print("sudo shutdown -h now")
            os.system("sudo shutdown -h now")
    except:
        pass
    time.sleep(3)

GPIO.cleanup()
