import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
motor1=31
motor2=33
motor3=35
motor4=37

GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)
GPIO.setup(motor3, GPIO.OUT)
GPIO.setup(motor4, GPIO.OUT)

m1 = GPIO.PWM(motor1, 1000)
m2 = GPIO.PWM(motor2, 1000)
m3 = GPIO.PWM(motor3, 1000)
m4 = GPIO.PWM(motor4, 1000)

def start_motors():
    print "starting motors\n\r",

def vibrate_motor(motor, intensity, t):
    if motor == 1:
        m1.start(intensity)
        time.sleep(t)
        m1.stop()
    elif motor == 2:
        m2.start(intensity)
        time.sleep(t)
        m2.stop()
    elif motor == 3:
        m3.start(intensity)
        time.sleep(t)
        m3.stop()
    elif motor == 4:
        m4.start(intensity)
        time.sleep(t)
        m4.stop()
        

def stop_motors():
    GPIO.cleanup()



vibrate_motor(1,80,0.2)
vibrate_motor(2,80,0.2)
vibrate_motor(1,80,0.2)
vibrate_motor(2,80,0.2)
vibrate_motor(1,100,0.2)
vibrate_motor(2,80,0.2)
vibrate_motor(1,80,0.2)
vibrate_motor(2,80,0.2)
vibrate_motor(1,80,0.2)
vibrate_motor(2,80,0.2)

stop_motors()

    
