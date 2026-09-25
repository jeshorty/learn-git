import tkinter as tk
from tkinter import messagebox
from Cronometer_backend import CountdownTimer

class TimerApp:
    def __init__(self, root):
        self.timer = CountdownTimer()

        self.root = root
        self.root.title("Cronometro Countdown")

        # Time input
        self.entry = tk.Entry(root, width=10, font=("Arial", 24))
        self.entry.insert(0, "00:00:01")
        self.entry.grid(row=0, column=0, columnspan=4, pady=10)

        # Display
        self.display = tk.Label(root, text="Tempo rimanente: 00:00:00", font=("Arial", 24))
        self.display.grid(row=1, column=0, columnspan=4, pady=10)

        # Buttons
        tk.Button(root, text="Start", width=10, command=self.start).grid(row=2, column=0)
        tk.Button(root, text="Pausa", width=10, command=self.pause).grid(row=2, column=1)
        tk.Button(root, text="Riprendi", width=10, command=self.resume_timer).grid(row=2, column=2)
        tk.Button(root, text="Stop", width=10, command=self.stop).grid(row=3, column=0)
        tk.Button(root, text="Ripristina", width=10, command=self.reset).grid(row=3, column=1)

    def parse_input_time(self):
        try:
            h, m, s = map(int, self.entry.get().split(":"))
            return h, m, s
        except ValueError:
            messagebox.showerror("Errore", "Inserisci il tempo nel formato HH:MM:SS")
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
        if remaining_seconds == 0 and not self.popup_shown:
            self.popup_shown = True
            self.show_custom_popup()

    def show_custom_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Fine")
        popup.geometry("400x200")
        popup.configure(bg="white")
        popup.grab_set()  # blocca l'interazione con la finestra principale

        # Rendi il popup sempre in primo piano
        popup.attributes("-topmost", True)
        popup.focus_force()

        label = tk.Label(popup, text="Il tempo è scaduto!", font=("Arial", 24, "bold"), bg="white", fg="red")
        label.pack(expand=True, pady=40)

        button = tk.Button(popup, text="OK", font=("Arial", 16), command=popup.destroy)
        button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
