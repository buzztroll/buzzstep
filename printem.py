import statistics
import sys
import time

import RPi.GPIO as GPIO
import hx711


def stat_values(hx):
    print("================")

    raw = hx.get_raw_data(times=8)
    print(raw)
    data = [x for x in raw if x >= 0]

    print(data)
    median_value = statistics.median(data)
    mean = sum(data) / len(data)
    lowest = min(data)
    highest = max(data)
    stdev = statistics.stdev(data)
    filtered = [n for n in data if abs(n - mean) <= stdev]
    print(filtered)
    new_mean = sum(filtered) / len(filtered)

    print(f"Highest: \t{highest}")
    print(f"Lowest: \t{lowest}")
    print(f"Average: \t{mean}")
    print(f"Fixed Avg: \t{new_mean}")
    print(f"Median: \t{median_value}")

    return new_mean


def main():
    done = False
    sleep_time = 0.5
    GPIO.setmode(GPIO.BCM)

    hx = hx711.HX711(27, 17)
    while not done:
        time.sleep(sleep_time)
        try:
            stat_values(hx)
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

