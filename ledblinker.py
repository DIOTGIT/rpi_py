'''
Blinks the green LED on the Raspberry Pi 4B+ board.
'''

import time
import threading

# Path to the built-in green LED control.
# Check the path in your system with: ls /sys/class/leds/
LED_PATH = "/sys/class/leds/ACT/brightness"

class LEDBlinker:
    def __init__(self, frequency=1):
        self.frequency = frequency
        self.blink_thread = None
        self.running = False

    def set_led(self, state):
        with open(LED_PATH, 'w') as led_file:
            led_file.write('1' if state else '0')

    def blink_led(self):
        try:
            while self.running:
                # Turn on the LED
                self.set_led(True)
                time.sleep(1 / (2 * self.frequency))  # Wait for half the period

                # Turn off the LED
                self.set_led(False)
                time.sleep(1 / (2 * self.frequency))  # Wait for half the period

        except KeyboardInterrupt:
            # Turn off the LED before exiting
            self.set_led(False)

    def start(self):
        if not self.running:
            self.running = True
            self.blink_thread = threading.Thread(target=self.blink_led)
            self.blink_thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.blink_thread.join()
            self.set_led(False)

# Example usage
if __name__ == "__main__":
    blinker = LEDBlinker(frequency=0.5)
    blinker.start()

    try:
        while True:
            print("Main program is running...")
            time.sleep(2)  # Simulate some work being done

    except KeyboardInterrupt:
        blinker.stop()
