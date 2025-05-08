import time
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, master, theme_var, alarm_handler, update_alarm_status_callback):
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
        theme_optionmenu = ctk.CTkOptionMenu(self, values=["System", "Dark", "Light"], variable=self.theme_var)
        theme_optionmenu.pack(pady=5)

        # Alarme ON/OFF avec Slider
        self.alarm_on = tk.BooleanVar(value=self.alarm_handler.is_alarm_set())
        alarm_switch_frame = ctk.CTkFrame(self)
        alarm_switch_frame.pack(pady=5)
        alarm_label = ctk.CTkLabel(alarm_switch_frame, text="Alarme:")
        alarm_label.pack(side="left", padx=5)
        alarm_switch = ctk.CTkSwitch(alarm_switch_frame, text="", variable=self.alarm_on, onvalue=True, offvalue=False, command=self.toggle_alarm)
        alarm_switch.pack(side="left", padx=5)

        # Heure de l'alarme
        alarm_time_label = ctk.CTkLabel(self, text="Heure de l'alarme (HH:MM):")
        alarm_time_label.pack(pady=5)
        self.alarm_entry = ctk.CTkEntry(self)
        self.alarm_entry.pack(pady=5)
        if self.alarm_handler.alarm_time:
            self.alarm_entry.insert(0, self.alarm_handler.alarm_time)

        set_alarm_button = ctk.CTkButton(self, text="Appliquer l'alarme", command=self.apply_alarm)
        set_alarm_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Gérer la fermeture de la fenêtre

    def toggle_alarm(self):
        if self.alarm_on.get():
            if not self.alarm_handler.alarm_time:
                # Si on active l'alarme sans heure définie, on met une heure par défaut ou on demande à l'utilisateur
                self.alarm_handler.set_alarm(time.strftime("%H:%M"))  # Heure actuelle par défaut
                self.alarm_entry.insert(0, self.alarm_handler.alarm_time)
            print("Alarme activée.")
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
