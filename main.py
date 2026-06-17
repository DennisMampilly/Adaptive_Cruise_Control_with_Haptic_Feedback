import threading
import time
import cv2
import RPi.GPIO as GPIO

from ultrasonic import get_distance
from lane_detection import detect_lane
from lcd_display import show_message

HAPTIC = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(HAPTIC, GPIO.OUT)

obstacle_alert = False
lane_alert = False

camera = cv2.VideoCapture(0)

def ultrasonic_loop():

    global obstacle_alert

    while True:

        distance = get_distance()

        if distance != -1 and distance < 50:

            obstacle_alert = True

        else:

            obstacle_alert = False

        time.sleep(0.3)

def camera_loop():

    global lane_alert

    while True:

        ret, frame = camera.read()

        if not ret:
            continue

        lane_alert = detect_lane(frame)

try:

    threading.Thread(
        target=ultrasonic_loop,
        daemon=True
    ).start()

    threading.Thread(
        target=camera_loop,
        daemon=True
    ).start()

    last_message = ""

    while True:

        if lane_alert:

            message = "CROSSED"

        elif obstacle_alert:

            message = "OBSTRUCTION"

        else:

            message = "SAFE"

        GPIO.output(
            HAPTIC,
            lane_alert or obstacle_alert
        )

        if message != last_message:

            show_message(message)

            last_message = message

        time.sleep(0.1)

except KeyboardInterrupt:

    pass

finally:

    GPIO.cleanup()

    camera.release()
