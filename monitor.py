import sqlite3
import sys
import time

import RPi.GPIO as GPIO
import hx711


class GandolfScale(object):
    def __init__(self, data_pin, clock_pin,
                 threshold, cb, read_iterations=2, wait_time=0.1,
                 wait_after_signal=5.0):
        self._data_pin = data_pin
        self._clock_pin = clock_pin

        GPIO.setmode(GPIO.BCM)
        self.hx = hx711.HX711(dout_pin=self._data_pin,
                              pd_sck_pin=self._clock_pin)
        self.read_iterations = read_iterations
        self.wait_time = wait_time
        self.wait_time = wait_time
        self.done = False
        self.threshold = threshold
        self.cb = cb
        self.wait_after_signal = wait_after_signal

    def run(self):
        while not self.done:
            time.sleep(self.wait_time)
            x = self.hx.get_raw_data_mean(readings=3)
            if x > self.threshold:
                self.cb()
                print("clearing")
                time.sleep(self.wait_after_signal)
                print("Ready")


def get_threshold(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    res = cur.execute("SELECT step_weight,threshold,zero_offset FROM stepalarm_scale order by creation_time LIMIT 1")
    row = res.fetchone()
    step_weight = row[0]
    threshold = row[1]
    zero_offset = row[2]
    return ((step_weight - zero_offset) * threshold) + zero_offset


def step_cb():
    print("STEPPED!")

def main():
    threshold = get_threshold(sys.argv[1])
    gs = GandolfScale(27, 17, threshold, step_cb)
    gs.run()
    return 0


if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
