import tkinter as tk
from PIL import Image, ImageTk
import os


PATH = "C:/Users/ajayp/OneDrive/Documents/PlatformIO/FinalProject_HandGlove/PyhtonMLserver/resource"

class TestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test App")

        self.image_files = os.listdir(PATH)
        self.current_image_index = 0

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_image)
        self.previous_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.show_current_image()

    def show_current_image(self):
        image_name = self.image_files[self.current_image_index]
        image_path = os.path.join(PATH, image_name)
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.show_current_image()

    def previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.show_current_image()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TestApp()
    app.run()
