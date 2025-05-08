import time
import datetime
import winsound  # Module spécifique à Windows pour la lecture de sons


class AlarmHandler:

    def __init__(self, sound_path):
        self.alarm_time = None
        self.sound_path = sound_path

    def set_alarm(self, time_str):
        if time_str:
            try:
                datetime.datetime.strptime(time_str, "%H:%M")
                self.alarm_time = time_str
                print(f"Alarme définie pour {self.alarm_time}")
            except ValueError:
                print("Format d'heure invalide (HH:MM).")
                self.alarm_time = None
        else:
            self.alarm_time = None
            print("Alarme désactivée.")

    def is_alarm_set(self):
        return self.alarm_time is not None

    def should_ring(self):
        if self.is_alarm_set():  # Utiliser la méthode is_alarm_set
            now = datetime.datetime.now().strftime("%H:%M")
            return now == self.alarm_time
        return False

    def ring(self):
        try:
            winsound.PlaySound(self.sound_path, winsound.SND_ASYNC | winsound.SND_LOOP)  # Lecture en boucle
            print("ALARME !!!")
            # Vous pourriez ajouter une méthode pour arrêter la sonnerie
        except Exception as e:
            print(f"Erreur lors de la lecture du son : {e}")

    def stop(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
