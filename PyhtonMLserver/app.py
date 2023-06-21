import tkinter as tk
import socket
import json
import threading
import tensorflow as tf
import numpy as np
import os
from PIL import Image, ImageTk
import pyautogui


UDP_IP = "0.0.0.0"
UDP_PORT = 8080

# Load the trained model
model = tf.keras.models.load_model('trained_model.h5')



class GestureRecognitionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Glove")
        self.root.configure(bg="#232323")

        self.is_receiving = False
        self.active_app = "Home"

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.status_label = tk.Label(self.root, text="Status: Not Receiving Data", fg="white", bg="#232323", font=("Arial", 12))
        self.status_label.pack(anchor="ne", padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="Hand Gesture Glove!", fg="white", bg="#232323", font=("Arial", 16, "bold"))
        self.info_label.pack(pady=10)

        self.app_buttons_frame = tk.Frame(self.root, bg="#232323")
        self.app_buttons_frame.pack(pady=10)

        self.gesture_button = tk.Button(self.app_buttons_frame, text="Hand Gesture Recognition ", command=self.show_gesture_app, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.gesture_button.pack(side=tk.LEFT, padx=10)

        self.app2_button = tk.Button(self.app_buttons_frame, text="Mouse Controller", command=self.open_app2, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
        self.app2_button.pack(side=tk.LEFT, padx=10)

        self.app3_button = tk.Button(self.app_buttons_frame, text="Keyboard Controller", command=self.open_app3, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        self.app3_button.pack(side=tk.LEFT, padx=10)

        self.gesture_frame = tk.Frame(self.root, bg="#232323")

        self.start_button = tk.Button(self.gesture_frame, text="Start", command=self.start_receiving, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.gesture_frame, text="Stop", command=self.stop_receiving, bg="#F44336", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.pack()

        self.gesture_frame.pack()
        self.gesture_frame.pack_forget()

        self.image_label = tk.Label(self.gesture_frame)
        self.image_label.pack()

    def show_gesture_app(self):
        self.app_buttons_frame.pack_forget()
        self.gesture_frame.pack()
        self.reset_status()
        self.active_app = "Gesture Recognition Application"
        self.update_title("Gesture Recognition")

    def open_app2(self):
        self.reset_status()
        self.active_app = "Mouse Controller"
        self.update_title("Mouse Controller")
        # Add code to open Application 2

    def open_app3(self):
        self.reset_status()
        self.active_app = "Keyboard Controller"
        self.update_title("Keyboard Controller")



    def start_receiving(self):
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Receiving Data", fg="lime", bg="#232323")
        self.info_label.config(text="", fg="white")

        self.is_receiving = True

        threading.Thread(target=self.receive_data).start()

    def stop_receiving(self):
        self.is_receiving = False
        self.reset_status()
        self.gesture_frame.pack_forget()
        self.app_buttons_frame.pack()
        self.active_app = "Home"
        self.update_title("Hand Gesture Glove")

    def reset_status(self):
        self.start_button.config(state=tk.NORMAL)
        self.info_label.config(text="Welcome to the Hand Gesture Glove App!", fg="white")

    def receive_data(self):
        while self.is_receiving:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                self.status_label.config(text="Status: Receiving Data", fg="lime", bg="#232323")

                sensor_values = json.loads(data.decode('utf-8'))
                json_data = json.loads(data.decode('utf-8'))
                print(json_data)
                sensor_values = []
                for i in range(6):
                    sensor_values.extend(list(json_data[str(i)].values()))

                input_data = np.array(sensor_values).reshape(1, 36)
                prediction = model.predict(input_data)
                predicted_class = np.argmax(prediction)

                if self.active_app == "Keyboard Controller":
                    if predicted_class == 1:
                        pyautogui.press('w')  # Move paddle up
                    elif predicted_class == 2:
                        pyautogui.press('s')  # Move paddle down

                if self.active_app == "Mouse Controller":
                    if predicted_class == 1:
                        sensor_5_values = json_data['1']
                        gx = sensor_5_values['gx']
                        gz = sensor_5_values['gz']

                        # Move the mouse pointer based on sensor values
                        move_x = int(gx * 100)  # Scaling the gyro value for x-axis movement
                        move_y = int(gz * 100)  # Scaling the gyro value for z-axis movement
                        pyautogui.move(move_x, move_y)
                    if predicted_class == 2:
                        
                        # Left Click 
                        pyautogui.click(button='left')

                    if predicted_class == 6:

                        # Right Click
                        pyautogui.click(button='right')

                
                self.info_label.config(text=f"Predicted Value: {predicted_class}")

                # Load and display the corresponding image
                image_path = f"C:/Users/ajayp/OneDrive/Documents/PlatformIO/FinalProject_HandGlove/PyhtonMLserver/resource/symbol{predicted_class}.jpg"
                image = Image.open(image_path)
                image = image.rotate(-90, expand=True)
                self.photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=self.photo)

            except socket.timeout:
                pass

    def update_title(self, title):
        self.root.title(title)

    def run(self):
        self.udp_socket.bind((UDP_IP, UDP_PORT))
        print("***********SERVER-STARTED***********")
        self.root.mainloop()
        self.udp_socket.close()

if __name__ == "__main__":
    app = GestureRecognitionApp()
    app.run()
