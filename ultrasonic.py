import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(TRIG, False)

def get_distance():

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

        if time.time() - start_time > 0.04:
            return -1

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

        if time.time() - start_time > 0.04:
            return -1

    distance = (pulse_end - pulse_start) * 17150

    return round(distance, 2)
