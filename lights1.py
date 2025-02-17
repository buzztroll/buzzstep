import logging
import random
import sys
import time

import board
import neopixel


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_g_logger = logging.getLogger(__file__)


huffel_color = (210, 65, 10)
gryp_color = (224, 2, 2)
raven_color = (2, 2, 224)
slither_color = (2, 224, 2)

g_houses = [
        huffel_color,
        gryp_color,
        raven_color,
        slither_color
        ]

def pick_house():
    random.seed()
    number = random.randint(0, 3)
    return g_houses[number]


def random_colors(pixels):
    for i in range(0, 50):
        c = pick_house()
        pixels[i] = c
        pixels.show()
        time.sleep(.02)


def main():
    random.seed()
    pixels = neopixel.NeoPixel(board.D21, 50, auto_write=False)

    try:
        random_colors(pixels)
        time.sleep(3)
        c = pick_house()
        pixels.fill(c)
        pixels.show()
        time.sleep(90)
    finally:
        _g_logger.info("off")
        pixels.fill((0, 0, 0))
        pixels.show()


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
