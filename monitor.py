import sqlite3
import subprocess
import sys
import time

import gpiozero
import RPi.GPIO as GPIO
import hx711


class GandolfScale(object):
    def __init__(self, data_pin, clock_pin,
                 threshold, cb, read_iterations=2, wait_time=0.03,
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
            try:
                load_cell_readings = self.hx.get_raw_data()
                x = sum(load_cell_readings) / len(load_cell_readings)
                if x > self.threshold:
                    self.cb()
                    print("clearing")
                    time.sleep(self.wait_after_signal)
                    print("Ready")
            except Exception as ex:
               print(ex)


def get_threshold(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    res = cur.execute("SELECT step_weight,threshold,zero_offset FROM stepalarm_scale order by creation_time LIMIT 1")
    row = res.fetchone()
    step_weight = row[0]
    threshold = row[1]
    zero_offset = row[2]

    print(f"{step_weight} {zero_offset} {threshold}")
    return ((step_weight - zero_offset) * threshold) + zero_offset


RELAY_PIN = 18
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=True)

print("Turning the relay off")
relay.off()


def step_cb():
    print("STEPPED!")
    print("relay on step_cb")
    relay.on()
    subprocess.call("/home/bresnaha/Dev/buzzstep/welcome.sh", shell=True)
    time.sleep(10)
    print("relay off step_cb")
    relay.off()


def main():
    threshold = get_threshold(sys.argv[1])
    gs = GandolfScale(27, 17, threshold, step_cb)
    gs.run()
    return 0


# relay pin 18
# data pin 27
# clock pin 17

if __name__ == '__main__':
    try:
        rc = main()
        sys.exit(rc)
    finally:
        print("relay off exit")
        relay.off()
