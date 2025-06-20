from PIL import ImageGrab
import numpy as np
import serial
import time
import config
import utils

previous_palette = [(0, 0, 0)] * config.NUM_LEDS

def get_palette():
    screen = ImageGrab.grab()
    width, height = screen.size

    vertical_top = int(height * 0.25)
    vertical_bottom = int(height * 0.75)

    zone_width = width // config.NUM_LEDS
    offset = int(zone_width * 0.2)

    palette = []

    for i in range(config.NUM_LEDS):
        start = width - (i + 1) * zone_width + offset
        end = width - i * zone_width - offset

        region = screen.crop((start, vertical_top, end, vertical_bottom)).resize((24, 24))
        pixels = np.array(region).reshape(-1, 3)
        avg = tuple(map(int, np.mean(pixels, axis=0)))
        avg = utils.apply_config_color_settings(*avg)
        palette.append(avg)

    return palette


def run_loop_serial():
    ser = serial.Serial(config.PORT, config.BAUD)
    time.sleep(2)

    try:
        while True:
            current_palette = get_palette()
            flat = bytearray()

            for i in range(config.NUM_LEDS):
                old = previous_palette[i]
                new = current_palette[i]

                if utils.color_diff(old, new) > config.THRESHOLD:
                    previous_palette[i] = new
                    flat.extend(new)
                else:
                    flat.extend(old)

            ser.write(flat)
            ser.flush()
    except Exception as e:
        print(f"[Serial Error] {e}")

