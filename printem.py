import sys
import time

import RPi.GPIO as GPIO
import hx711


def main():
    done = False
    sleep_time = 0.5
    GPIO.setmode(GPIO.BCM)

    hx = hx711.HX711(27, 17)
    while not done:
        time.sleep(sleep_time)
        try:
            x = hx.get_raw_data()
            print(x)
        except Exception as ex:
            print(ex)
    return 0


# relay pin 18
# data pin 27
# clock pin 17
if __name__ == '__main__':
    try:
        rc = main()
        sys.exit(rc)
    finally:
        print("off exit")

