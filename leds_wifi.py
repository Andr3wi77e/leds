import numpy as np
import socket
import mss
import cv2
import config
import utils

previous_palette = [(0, 0, 0)] * config.NUM_LEDS

def get_palette(sct, monitor):
    # Преобразуем BGRA → RGB
    screenshot = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2RGB)
    height, width, _ = screenshot.shape

    vertical_top = int(height * 0.25)
    vertical_bottom = int(height * 0.75)

    zone_width = width // config.NUM_LEDS
    offset = int(zone_width * 0.2)

    palette = []

    for i in range(config.NUM_LEDS):
        start = width - (i + 1) * zone_width + offset
        end = width - i * zone_width - offset

        region = screenshot[vertical_top:vertical_bottom, start:end]
        region_resized = cv2.resize(region, (24, 24), interpolation=cv2.INTER_AREA)

        avg = tuple(map(int, np.mean(region_resized.reshape(-1, 3), axis=0)))

        avg = utils.apply_config_color_settings(*avg)

        palette.append(avg)

    return palette


def run_loop_wifi():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sct = mss.mss()
    monitor = sct.monitors[1]
    try:
        while True:
            current_palette = get_palette(sct, monitor)
            flat = bytearray()

            for i in range(config.NUM_LEDS):
                old = previous_palette[i]
                new = current_palette[i]

                if utils.color_diff(old, new) > config.THRESHOLD:
                    previous_palette[i] = new
                    flat.extend(new)
                else:
                    flat.extend(old)

            sock.sendto(flat, (config.UDP_IP, config.UDP_PORT))
    except Exception as e:
        print(f"[Wi-Fi Error] {e}")

