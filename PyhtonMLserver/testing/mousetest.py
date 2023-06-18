import tkinter as tk
import socket
import json
import threading
import pyautogui

UDP_IP = "0.0.0.0"
UDP_PORT = 8080

class MouseControlApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Control")
        self.root.configure(bg="#232323")

        self.is_receiving = False
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((UDP_IP, UDP_PORT))

        self.status_label = tk.Label(self.root, text="Status: Not Receiving Data", fg="white", bg="#232323", font=("Arial", 12))
        self.status_label.pack(anchor="ne", padx=10, pady=10)

    def start_receiving(self):
        self.status_label.config(text="Status: Receiving Data", fg="lime", bg="#232323")
        self.is_receiving = True
        threading.Thread(target=self.receive_data).start()

    def stop_receiving(self):
        self.is_receiving = False
        self.status_label.config(text="Status: Not Receiving Data", fg="white", bg="#232323")

    def receive_data(self):
        while self.is_receiving:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                self.status_label.config(text="Status: Receiving Data", fg="lime", bg="#232323")

                json_data = json.loads(data.decode('utf-8'))
                sensor_5_values = json_data['5']

                # Extract sensor values
                ax = sensor_5_values['ax']
                ay = sensor_5_values['ay']
                az = sensor_5_values['az']
                gx = sensor_5_values['gx']
                gy = sensor_5_values['gy']
                gz = sensor_5_values['gz']

                # Move the mouse pointer based on sensor values
                move_x = int(gx * 100)  # Scaling the gyro value for x-axis movement
                move_y = int(gy * 100)  # Scaling the gyro value for y-axis movement
                pyautogui.move(move_x, move_y)

            except socket.timeout:
                pass

    def run(self):
        print("***********SERVER-STARTED***********")
        self.root.mainloop()
        self.udp_socket.close()


if __name__ == "__main__":
    app = MouseControlApp()
    app.start_receiving()
    app.run()
