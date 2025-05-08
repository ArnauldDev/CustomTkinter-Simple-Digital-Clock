#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CustomTkinter Simple Digital Clock

This is a simple digital clock application using CustomTkinter.
It displays the current time and allows the user to set an alarm.
"""


# =============================================================================
# INFO DEVELOPPEUR
# =============================================================================
__status__ = "Development"
__version__ = "1.0.0"
__license__ = "GNU GPLv3"
__company__ = "Service commun d'électronique du laboratoire Laplace"
__author__ = ["Arnauld BIGANZOLI"]
__email__ = "arnauld.biganzoli@laplace.univ-tlse.fr"
__maintainer__ = "Arnauld BIGANZOLI"
__developer__ = __author__
__credits__ = ["Arnauld BIGANZOLI"]
__copyright__ = "Copyright (c) 2025 LAPLACE, UMR INP-UPS-CNRS N°5213"


import tkinter as tk
import customtkinter as ctk
import time
import os
import json  # Pour sauvegarder les préférences
from ui.clock_frame import ClockFrame
from ui.settings_window import SettingsWindow
from utils.alarm_handler import AlarmHandler

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

import tkinter.font as tkfont
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Augmenter la taille de police des menus
        default_menu_font = tkfont.nametofont("TkMenuFont")
        default_menu_font.configure(size=14)

        self.title("Horloge Personnalisée")
        # self.geometry("250, 150")  # Augmenter la hauteur pour le bouton
        self.default_geometry = self.geometry()  # Sauvegarde la taille d'origine
        self.minsize(250, 150)

        self.update_idletasks()  # S'assure que la géométrie est à jour
        width = self.winfo_width()
        height = self.winfo_height()
        self.default_size = f"{width}x{height}"  # Sauvegarde uniquement la taille

        self.theme = ctk.StringVar(value="System")
        self.font_path = os.path.join("assets", "DSEG7Modern-BoldItalic.ttf")
        self.alarm_handler = AlarmHandler(os.path.join("assets", "alarm_sound_01.wav"))

        self.load_preferences()  # Charger les préférences au démarrage
        self.theme.trace_add("write", self.change_theme)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.ack_button = ctk.CTkButton(
            self,
            text="Acquitter l'alarme",
            command=self.acknowledge_alarm,
            width=240,
            fg_color="red",  # Couleur rouge
            hover_color="#b30000",  # Rouge foncé au survol
            text_color="white",
        )
        self.ack_button.pack(side="bottom")
        self.ack_button.pack_forget()  # Masqué par défaut

        # Menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Quitter", command=self.on_closing)

        # Ajouter la propriété default_menu_font pour les labels du menu
        filemenu.entryconfig(0, font=default_menu_font)  # Quitter
        # filemenu.entryconfig(1, font=default_menu_font) # Autre option
        # filemenu.entryconfig(2, font=default_menu_font) # Option supplémentaire

        settingsmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Paramètres", menu=settingsmenu)
        settingsmenu.add_command(label="Apparence", command=self.open_settings)

        # Ajouter la propriété default_menu_font pour les labels du menu
        settingsmenu.entryconfig(0, font=default_menu_font)  # Apparence
        # settingsmenu.entryconfig(1, font=default_menu_font) # Autre option
        # settingsmenu.entryconfig(2, font=default_menu_font) # Option supplémentaire

        self.config(menu=menubar)

        # Cadre de l'horloge
        self.clock_frame = ClockFrame(self, font_path=self.font_path)
        self.clock_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Barre d'état pour l'alarme
        self.statusbar = ctk.CTkLabel(
            self, text="", fg_color="gray70", text_color="white"
        )
        self.statusbar.pack(side="bottom", fill="x")

        self._programmatic_resize = (
            False  # Ajouté pour différencier les redimensionnements
        )
        self.alarm_active = False  # Ajouté pour suivre l'état de l'alarme
        self.update_alarm_status()
        self.update_clock()
        self.check_alarm()
        self.bind(
            "<Configure>", self.on_configure
        )  # Pour suivre les redimensionnements
        self.settings_window = None

    def load_preferences(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                print(f"Chargement des préférences depuis {CONFIG_FILE} : {config}")
                self.theme.set(config.get("theme", "System"))
                # Appliquer le thème CustomTkinter immédiatement
                ctk.set_appearance_mode(config.get("theme", "System"))
                self.alarm_handler.set_alarm(config.get("alarm_time"))
                alarm_sound = config.get("alarm_sound")
                if alarm_sound:
                    ringtone_dir = os.path.join(os.path.dirname(__file__), "assets")
                    self.alarm_handler.sound_path = os.path.join(
                        ringtone_dir, alarm_sound
                    )
                print("Préférences chargées avec succès.")
        except FileNotFoundError:
            print(
                f"Fichier de configuration non trouvé ({CONFIG_FILE}). Utilisation des paramètres par défaut."
            )
        except json.JSONDecodeError as e:
            print(
                f"Erreur lors de la lecture du fichier de configuration : {e}. Utilisation des paramètres par défaut."
            )

    def change_theme(self, *args):
        ctk.set_appearance_mode(self.theme.get())
        self.save_preferences()  # Sauvegarder le thème lors du changement

    def on_configure(self, event):
        # Met à jour la taille par défaut si l'utilisateur redimensionne la fenêtre
        if event.widget == self and not self._programmatic_resize:
            self.default_size = f"{self.winfo_width()}x{self.winfo_height()}"

    def update_alarm_status(self):
        if self.alarm_handler.is_alarm_set():
            self.statusbar.configure(
                text=f"Alarme ON: {self.alarm_handler.alarm_time}",
                font=("Helvetica", 14, "bold"),
            )
        else:
            # Et si l'alarme n'est pas définie, on affiche "Alarme OFF"
            self.statusbar.configure(text="Alarme OFF", font=("Helvetica", 14, "bold"))
        self.after(1000, self.update_alarm_status)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock_frame.update_time(now)
        self.after(1000, self.update_clock)

    def apply_alarm(self):
        alarm_time_str = self.alarm_entry.get()
        self.alarm_handler.set_alarm(alarm_time_str if self.alarm_on.get() else None)
        # Mettre à jour la sonnerie
        ringtone_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.alarm_handler.sound_path = os.path.join(
            ringtone_dir, self.ringtone_var.get()
        )
        self.update_alarm_status_callback()
        # Sauvegarder les préférences après modification
        if hasattr(self.master, "save_preferences"):
            self.master.save_preferences()

    def check_alarm(self):
        alarm_should_ring = (
            self.alarm_handler.is_alarm_set() and self.alarm_handler.should_ring()
        )
        if alarm_should_ring and not self.alarm_active:
            self.alarm_handler.ring()
            self.ack_button.pack(side="bottom", pady=2)
            self._programmatic_resize = True
            self.geometry("280x240")  # Agrandir la fenêtre pour le bouton
            self._programmatic_resize = False
            self.alarm_active = True
        elif not alarm_should_ring and self.alarm_active:
            self.ack_button.pack_forget()
            self._programmatic_resize = True
            self.geometry(self.default_size)  # Restaure uniquement la taille
            self._programmatic_resize = False
            self.alarm_active = False
        elif not alarm_should_ring:
            self.ack_button.pack_forget()
            self.alarm_active = False
        self.after(1000, self.check_alarm)

    def acknowledge_alarm(self):
        self.alarm_handler.stop()
        self.alarm_handler.set_alarm(None)
        self.ack_button.pack_forget()
        print(f"Default size: {self.default_size}")
        self._programmatic_resize = True
        self.geometry(self.default_size)
        self._programmatic_resize = False
        self.alarm_active = False
        self.save_preferences()

    def save_preferences(self):
        config = {
            "theme": self.theme.get(),
            "alarm_time": self.alarm_handler.alarm_time,
            "alarm_sound": os.path.basename(self.alarm_handler.sound_path),
        }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
            print("Préférences sauvegardées.")
        except IOError:
            print("Erreur lors de la sauvegarde des préférences.")

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(
                self, self.theme, self.alarm_handler, self.update_alarm_status
            )
            self.settings_window.focus()  # Mettre la fenêtre au premier plan
        else:
            self.settings_window.focus()  # Si la fenêtre existe déjà, la mettre au premier plan

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
