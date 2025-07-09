import time
import threading
from time import strftime
import tkinter as tk

class CountdownTimer:
    def __init__(self):
        self.initial_seconds = 0
        self.remaining_seconds = 0
        self.running = False
        self._callback = None
        self._thread = None

    def set_time(self, hours, minutes, seconds):
        self.initial_seconds = hours * 3600 + minutes * 60 + seconds
        self.remaining_seconds = self.initial_seconds

    def start(self, callback=None):
        if not self.running and self.remaining_seconds > 0:
            self.running = True
            self._callback = callback
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

    def _run(self):
        while self.running and self.remaining_seconds > 0:
            time.sleep(1)
            self.remaining_seconds -= 1
            if self._callback:
                self._callback(self.remaining_seconds)
        if self.remaining_seconds == 0 and self._callback:
            self._callback(0)  # trigger finish

    def pause(self):
        self.running = False

    def resume(self):
        if not self.running and self.remaining_seconds > 0:
            self.start(self._callback)

    def stop(self):
        self.running = False
        self.remaining_seconds = 0

    def reset(self):
        self.running = False
        self.remaining_seconds = self.initial_seconds

    def get_remaining_time(self):
        return self._seconds_to_hms(self.remaining_seconds)

    def _seconds_to_hms(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return hours, minutes, seconds
    
class DigClock:
    def __init__(self, parent):
        self.dig_clock = tk.Label(font=('calibri', 25, 'bold'), background='black', foreground='white')
        self.dig_clock.pack(pady=20, padx=10)
        self.update_time()  

    def update_time(self):
        str_time = strftime('%d-%b-%Y\n%H:%M:%S\n%Z:%z')
        self.dig_clock.config(text=str_time)
        self.dig_clock.after(1000, self.update_time)
