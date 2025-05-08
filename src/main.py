import tkinter as tk
import customtkinter as ctk
import time
import os
import json  # Pour sauvegarder les préférences
from ui.clock_frame import ClockFrame
from ui.settings_window import SettingsWindow
from utils.alarm_handler import AlarmHandler

CONFIG_FILE = "config.json"


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Horloge Personnalisée")
        self.geometry("400x200")
        self.minsize(300, 150)

        self.theme = ctk.StringVar(value="System")
        self.font_path = os.path.join("assets", "DSEG7Modern-BoldItalic.ttf")
        self.alarm_handler = AlarmHandler(os.path.join("assets", "alarm_sound_01.wav"))

        self.load_preferences()  # Charger les préférences au démarrage
        self.theme.trace_add("write", self.change_theme)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Quitter", command=self.on_closing)

        settingsmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Paramètres", menu=settingsmenu)
        settingsmenu.add_command(label="Apparence", command=self.open_settings)

        self.config(menu=menubar)

        # Cadre de l'horloge
        self.clock_frame = ClockFrame(self, font_path=self.font_path)
        self.clock_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Barre d'état pour l'alarme
        self.statusbar = ctk.CTkLabel(self, text="", fg_color="gray70", text_color="white")
        self.statusbar.pack(side="bottom", fill="x")
        self.update_alarm_status()

        self.update_clock()
        self.check_alarm()

        self.settings_window = None

    def load_preferences(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.theme.set(config.get("theme", "System"))
                self.alarm_handler.set_alarm(config.get("alarm_time"))
        except FileNotFoundError:
            print("Fichier de configuration non trouvé. Utilisation des paramètres par défaut.")
        except json.JSONDecodeError:
            print("Erreur lors de la lecture du fichier de configuration. Utilisation des paramètres par défaut.")

    def save_preferences(self):
        config = {
            "theme": self.theme.get(),
            "alarm_time": self.alarm_handler.alarm_time
        }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
            print("Préférences sauvegardées.")
        except IOError:
            print("Erreur lors de la sauvegarde des préférences.")

    def change_theme(self, *args):
        ctk.set_appearance_mode(self.theme.get())
        self.save_preferences()  # Sauvegarder le thème lors du changement

    def update_alarm_status(self):
        if self.alarm_handler.is_alarm_set():
            self.statusbar.configure(text=f"Alarme ON: {self.alarm_handler.alarm_time}", font=("Helvetica", 14, "bold"))
        else:
            # Et si l'alarme n'est pas définie, on affiche "Alarme OFF"
            self.statusbar.configure(text="Alarme OFF", font=("Helvetica", 14, "bold"))
        self.after(1000, self.update_alarm_status)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock_frame.update_time(now)
        self.after(1000, self.update_clock)

    def check_alarm(self):
        if self.alarm_handler.is_alarm_set() and self.alarm_handler.should_ring():
            self.alarm_handler.ring()
        self.after(1000, self.check_alarm)

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self, self.theme, self.alarm_handler, self.update_alarm_status)
            self.settings_window.focus()  # Mettre la fenêtre au premier plan
        else:
            self.settings_window.focus()  # Si la fenêtre existe déjà, la mettre au premier plan

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
