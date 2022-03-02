import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
hand_pwm = GPIO.PWM(26, 50)
hand_pwm.start(0)
time.sleep(0.1)
# Move to initial position
hand_pwm.ChangeDutyCycle(2)
time.sleep(2)
hand_pwm.ChangeDutyCycle(12)
time.sleep(2)
hand_pwm.ChangeDutyCycle(2)
# Stop the servos in initial position (prevents twitching)
GPIO.cleanup()
