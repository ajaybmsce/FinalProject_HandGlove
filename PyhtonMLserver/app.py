import tkinter as tk
import socket
import json
import threading
import tensorflow as tf
import numpy as np

UDP_IP = "0.0.0.0"
UDP_PORT = 8080

# Load the trained model
model = tf.keras.models.load_model('C:/Users/ajayp/OneDrive/Documents/PlatformIO/FinalProject_HandGlove/PyhtonMLserver/trained_model.h5')

class GestureRecognitionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Recognition App")
        self.root.configure(bg="#232323")

        self.is_receiving = False

        self.status_label = tk.Label(self.root, text="Status: Not Receiving Data", fg="white", bg="#232323", font=("Arial", 12))
        self.status_label.pack(anchor="ne", padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="Welcome to the Hand Gesture Recognition App!", fg="white", bg="#232323", font=("Arial", 16, "bold"))
        self.info_label.pack(pady=10)

        self.app_buttons_frame = tk.Frame(self.root, bg="#232323")
        self.app_buttons_frame.pack(pady=10)

        self.gesture_button = tk.Button(self.app_buttons_frame, text="Hand Gesture Recognition", command=self.show_gesture_app, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.gesture_button.pack(side=tk.LEFT, padx=10)

        self.app1_button = tk.Button(self.app_buttons_frame, text="Application 1", bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.app1_button.pack(side=tk.LEFT, padx=10)

        self.app2_button = tk.Button(self.app_buttons_frame, text="Application 2", bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
        self.app2_button.pack(side=tk.LEFT, padx=10)

        self.gesture_frame = tk.Frame(self.root, bg="#232323")

        self.start_button = tk.Button(self.gesture_frame, text="Start", command=self.start_receiving, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.gesture_frame, text="Stop", command=self.stop_receiving, bg="#F44336", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.pack()

        self.gesture_frame.pack()
        self.gesture_frame.pack_forget()

    def show_gesture_app(self):
        self.app_buttons_frame.pack_forget()
        self.gesture_frame.pack()
        self.reset_status()

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

    def reset_status(self):
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Not Receiving Data", fg="white", bg="#232323")
        self.info_label.config(text="Welcome to the Hand Gesture Recognition App!", fg="white")

    def receive_data(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((UDP_IP, UDP_PORT))

        while self.is_receiving:
            try:
                data, addr = udp_socket.recvfrom(1024)
                sensor_values = json.loads(data.decode('utf-8'))

                json_data = json.loads(data.decode('utf-8'))
                sensor_values = []
                for i in range(6):
                    sensor_values.extend(list(json_data[str(i)].values()))

                input_data = np.array(sensor_values).reshape(1, 36)
                prediction = model.predict(input_data)
                predicted_class = np.argmax(prediction)

                self.info_label.config(text=f"Predicted Value: {predicted_class}")
            except socket.timeout:
                pass

        udp_socket.close()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GestureRecognitionApp()
    app.run()
