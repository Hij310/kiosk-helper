import time
import threading
import configparser
import ctypes
import os
import sys


def block_input():
    """Blokkeer toetsenbord en muis."""
    ctypes.windll.user32.BlockInput(True)


def unblock_input():
    """Deblokkeer toetsenbord en muis."""
    ctypes.windll.user32.BlockInput(False)


def shutdown_system():
    """Schakel het systeem uit."""
    os.system("shutdown /s /t 1")


def monitor_uptime(max_uptime_hours):
    """Controleer uptime en sluit het systeem af indien nodig."""
    start_time = time.time()
    max_uptime_seconds = max_uptime_hours * 3600
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_uptime_seconds:
            print("De maximale uptime is bereikt. Het systeem wordt afgesloten.")
            shutdown_system()
            break
        time.sleep(1)


def main():
    # Lees configuratie-instellingen
    config = configparser.ConfigParser()
    config.read("config.ini")

    block_input_enabled = config.getboolean("Settings", "block_input", fallback=False)
    max_uptime_hours = config.getint("Settings", "max_uptime_hours", fallback=72)

    # Blokkeer toetsenbord/muis indien ingeschakeld
    if block_input_enabled:
        print("Toetsenbord en muis worden geblokkeerd.")
        block_input()

    # Start thread voor het controleren van de uptime
    print(f"Systeem mag niet langer aanstaan dan {max_uptime_hours} uur.")
    threading.Thread(target=monitor_uptime, args=(max_uptime_hours,), daemon=True).start()

    try:
        while True:
            time.sleep(1)  # Houd de applicatie actief
    except KeyboardInterrupt:
        print("Applicatie wordt afgesloten.")
        if block_input_enabled:
            unblock_input()


if __name__ == "__main__":
    main()
