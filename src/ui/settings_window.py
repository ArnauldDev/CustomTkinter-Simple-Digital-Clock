import os
# import time
import customtkinter as ctk
import tkinter as tk
# from tkinter import ttk

import glob


# ...existing code...
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, theme_var, alarm_handler, update_alarm_status_callback):
        """
        Fenêtre de paramètres pour changer le thème et configurer l'alarme.
        :param master: Fenêtre principale.
        :param theme_var: Variable pour le thème.
        :param alarm_handler: Gestionnaire d'alarme.
        :param update_alarm_status_callback: Fonction de rappel pour mettre à jour le statut de l'alarme.
        """
        super().__init__(master)
        self.title("Paramètres")
        self.geometry("300x250")  # Augmenter un peu la hauteur pour le slider
        self.resizable(False, False)

        self.theme_var = theme_var
        self.alarm_handler = alarm_handler
        self.update_alarm_status_callback = update_alarm_status_callback

        # Thème
        theme_label = ctk.CTkLabel(self, text="Thème:")
        theme_label.pack(pady=5)
        theme_optionmenu = ctk.CTkOptionMenu(
            self, values=["System", "Dark", "Light"], variable=self.theme_var
        )
        theme_optionmenu.pack(pady=5)

        # Alarme ON/OFF avec Slider
        self.alarm_on = tk.BooleanVar(value=self.alarm_handler.is_alarm_set())
        alarm_switch_frame = ctk.CTkFrame(self)
        alarm_switch_frame.pack(pady=5)
        alarm_label = ctk.CTkLabel(alarm_switch_frame, text="Alarme:")
        alarm_label.pack(side="left", padx=5)
        alarm_switch = ctk.CTkSwitch(
            alarm_switch_frame,
            text="",
            variable=self.alarm_on,
            onvalue=True,
            offvalue=False,
            command=self.toggle_alarm,
        )
        alarm_switch.pack(side="left", padx=5)

        # Heure de l'alarme
        alarm_time_label = ctk.CTkLabel(self, text="Heure de l'alarme (HH:MM):")
        alarm_time_label.pack(pady=5)
        self.alarm_entry = ctk.CTkEntry(self)
        self.alarm_entry.pack(pady=5)
        if self.alarm_handler.alarm_time:
            self.alarm_entry.insert(0, self.alarm_handler.alarm_time)

        set_alarm_button = ctk.CTkButton(
            self, text="Appliquer l'alarme", command=self.apply_alarm
        )
        set_alarm_button.pack(pady=10)

        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Gérer la fermeture de la fenêtre
        
        # Liste des sonneries
        ringtone_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        ringtones = [
            os.path.basename(f) for f in glob.glob(os.path.join(ringtone_dir, "*.wav"))
        ]
        self.ringtone_var = tk.StringVar(
            value=os.path.basename(self.alarm_handler.sound_path)
        )
        ringtone_label = ctk.CTkLabel(self, text="Sonnerie :")
        ringtone_label.pack(pady=5)
        ringtone_menu = ctk.CTkOptionMenu(
            self, values=ringtones, variable=self.ringtone_var
        )
        ringtone_menu.pack(pady=5)
        # ...dans apply_alarm...

    def apply_alarm(self):
        alarm_time_str = self.alarm_entry.get()
        self.alarm_handler.set_alarm(alarm_time_str if self.alarm_on.get() else None)
        # Mettre à jour la sonnerie
        ringtone_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.alarm_handler.sound_path = os.path.join(
            ringtone_dir, self.ringtone_var.get()
        )
        self.update_alarm_status_callback()




    def toggle_alarm(self):
        if self.alarm_on.get():
            # Ne rien faire ici, attendre l'appui sur "Appliquer l'alarme"
            pass
        else:
            self.alarm_handler.set_alarm(None)
            print("Alarme désactivée.")
        self.update_alarm_status_callback()

    def apply_alarm(self):
        alarm_time_str = self.alarm_entry.get()
        self.alarm_handler.set_alarm(alarm_time_str if self.alarm_on.get() else None)
        self.update_alarm_status_callback()

    def on_closing(self):
        self.destroy()
