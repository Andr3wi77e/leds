import leds_wifi
import led_control
import tkinter as tk
from tkinter import ttk
import threading
import time
import config

def start(mode):
    if mode == "serial":
        t = threading.Thread(target=led_control.run_loop_serial, daemon=True)
    else:
        t = threading.Thread(target=leds_wifi.run_loop_wifi, daemon=True)
    t.start()

def create_gui():
    root = tk.Tk()
    root.title("Ambilight Sender")

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    ttk.Label(frame, text="Выберите режим подключения:").grid(column=0, row=0, columnspan=2)

    ttk.Button(frame, text="Serial (USB)", command=lambda: start("serial")).grid(column=0, row=1)
    ttk.Button(frame, text="Wi-Fi", command=lambda: start("wifi")).grid(column=1, row=1)

    ttk.Label(frame, text=f"Serial port: {config.PORT}").grid(column=0, row=2, columnspan=2)
    ttk.Label(frame, text=f"WiFi: {config.UDP_IP}:{config.UDP_PORT}").grid(column=0, row=3, columnspan=2)

    ttk.Button(frame, text="Выход", command=root.destroy).grid(column=0, row=4, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()