import tkinter as tk
from tkinter import messagebox
from Cronometer_backend import CountdownTimer, DigClock

class Clock_timer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clock and Timer")
        self.minsize(300, 150)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.clock_frame = tk.Frame(self, bg='black')
        self.clock_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.clock = DigClock(self.clock_frame)

        self.timer_frame = tk.Frame(self, bg='white')
        self.timer_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.create_timer_ui()

        self.bind("<Configure>", self.on_resize)

    def create_timer_ui(self):
        self.timer = CountdownTimer()

        self.entry = tk.Entry(self.timer_frame, width=10, font=("Arial", 20))
        self.entry.insert(0, "00:00:01")
        self.entry.pack(pady=5)

        self.display = tk.Label(self.timer_frame, text="Remaining Time: 00:00:00", font=("Arial", 20))
        self.display.pack(pady=5)

        self.button_frame = tk.Frame(self.timer_frame)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Start", command=self.start).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Pause", command=self.pause).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Continues", command=self.resume).grid(row=0, column=2, padx=5)
        tk.Button(self.button_frame, text="Stop", command=self.stop).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.button_frame, text="Reset", command=self.reset).grid(row=1, column=1, padx=5, pady=5)


    def parse_input_time(self):
        try:
            h, m, s = map(int, self.entry.get().split(":"))
            return h, m, s
        except ValueError:
            messagebox.showerror("Error", "Time must bi in format HH:MM:SS")
            return None

    def start(self):
        time_tuple = self.parse_input_time()
        if time_tuple:
            self.popup_shown = False
            self.timer.set_time(*time_tuple)
            self.timer.start(self.update_display)

    def pause(self):
        self.timer.pause()

    def resume_timer(self):
        self.timer.resume()

    def stop(self):
        self.timer.stop()
        self.update_display(0)

    def reset(self):
        self.timer.reset()
        self.popup_shown = False
        h, m, s = self.timer.get_remaining_time()
        self.display.config(text=f"Tempo rimanente: {h:02}:{m:02}:{s:02}")

    def update_display(self, remaining_seconds):
        h, m, s = self.timer._seconds_to_hms(remaining_seconds)
        self.display.config(text=f"Tempo rimanente: {h:02}:{m:02}:{s:02}")
        if remaining_seconds == 0 and not getattr(self, 'popup_shown', False):
            self.popup_shown = True
            self.show_custom_popup()

    def show_custom_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Fine")
        popup.geometry("400x200")
        popup.configure(bg="white")
        popup.grab_set()
        popup.attributes("-topmost", True)
        popup.focus_force()

        label = tk.Label(popup, text="Il tempo è scaduto!", font=("Arial", 24, "bold"), bg="white", fg="red")
        label.pack(expand=True, pady=40)

        button = tk.Button(popup, text="OK", font=("Arial", 16), command=popup.destroy)
        button.pack(pady=10)


class DigClockFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.clock = DigClock(self)
        self.clock.dig_clock.pack(pady=20, padx=10)
        tk.Button(self, text="← Menu", width=10, command=lambda: controller.show_frame("Menu")).pack(pady=10)


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Choose the modality", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Cronometer", font=("Arial", 16),
                  command=lambda: controller.show_frame("Timer")).pack(pady=10)
        tk.Button(self, text="Digital Clock", font=("Arial", 16),
                  command=lambda: controller.show_frame("Clock")).pack(pady=10)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Digital Clock-Timer App")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F, name in [(MenuFrame, "Menu"), (TimerFrame, "Timer"), (DigClockFrame, "Clock")]:
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Menu")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()