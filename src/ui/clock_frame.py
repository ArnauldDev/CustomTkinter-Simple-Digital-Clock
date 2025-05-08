import os
import customtkinter as ctk
from PIL import ImageFont, Image, ImageDraw  # Importez Pillow
from customtkinter import CTkImage  # Importer CTkImage


class ClockFrame(ctk.CTkFrame):

    def __init__(self, master, font_path, **kwargs):
        super().__init__(master, **kwargs)

        try:
            # Définir le chemin absolu vers la police personnalisée
            custom_font_path = os.path.abspath(font_path)

            # Charger la police personnalisée avec Pillow
            if os.path.exists(custom_font_path):
                self.custom_font = ImageFont.truetype(custom_font_path, 48)
            else:
                raise FileNotFoundError(f"Font file not found at {custom_font_path}")
        except Exception as e:
            print(f"Error loading font: {e}. Using default font.")
            self.custom_font = None  # Aucune police personnalisée

        # Créer un label pour afficher l'heure
        self.time_label = ctk.CTkLabel(self, text="")
        self.time_label.pack(expand=True, fill="both")

        # Initialiser l'heure
        self.update_time("00:00:00")

    def update_time(self, time_str):
        # Créer une image pour afficher le texte avec la police personnalisée
        if self.custom_font:
            image_width, image_height = 300, 100  # Taille de l'image
            image = Image.new(
                "RGB", (image_width, image_height), (255, 255, 255)
            )  # Couleur de fond
            draw = ImageDraw.Draw(image)

            # Calculer la taille du texte avec textbbox
            text_bbox = draw.textbbox((0, 0), time_str, font=self.custom_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculer les coordonnées pour centrer le texte
            text_x = (image_width - text_width) // 2
            text_y = (image_height - text_height) // 2

            # Dessiner le texte centré
            draw.text(
                (text_x, text_y), time_str, font=self.custom_font, fill=(0, 0, 0)
            )  # Texte noir

            # Convertir l'image PIL en CTkImage
            ctk_image = CTkImage(light_image=image, size=(image_width, image_height))
            self.time_label.configure(
                image=ctk_image, text=""
            )  # Supprime le texte par défaut
            self.time_label.image = ctk_image  # Empêche le garbage collection
        else:
            # Utiliser le texte par défaut si la police personnalisée n'est pas chargée
            self.time_label.configure(text=time_str)


if __name__ == "__main__":
    app = ctk.CTk()
    font_path = "assets/DSEG7Modern-BoldItalic.ttf"  # Chemin vers la police
    clock_frame = ClockFrame(master=app, font_path=font_path)
    clock_frame.pack(padx=20, pady=20)
    app.mainloop()
