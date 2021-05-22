import RPi.GPIO as GPIO
import pigpio
import time
import math


def moveServo(servo, start, end, delta):  #move from start to end, using delta number of seconds
     incMove=(end-start)/100.0
     incTime=delta/100.0
     for x in range(100):
          pwm.set_servo_pulsewidth(servo, int(start+x*incMove))
          time.sleep(incTime)

servo = 4
GPIO.setmode( GPIO.BCM )
GPIO.setup(servo, GPIO.OUT )
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency(servo, 50 )

#addedPulse = math.ceil((94 * 1000) / 90)
#pwm.set_servo_pulsewidth(servo, 500 + addedPulse)  
moveServo(servo, 1500, 2000, 2)
