import tkinter as tk
import random

import tkinter as tk
import socket
import json
import threading
import tensorflow as tf
import numpy as np
import os
from PIL import Image, ImageTk
import pyautogui

WIDTH = 800
HEIGHT = 400
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_SPEED = 10

class PingPongGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ping Pong Game")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.paddle1 = self.canvas.create_rectangle(
            50, HEIGHT//2 - PADDLE_HEIGHT//2,
            50 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2,
            fill="white"
        )
        self.paddle2 = self.canvas.create_rectangle(
            WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2,
            WIDTH - 50, HEIGHT//2 + PADDLE_HEIGHT//2,
            fill="white"
        )
        self.ball = self.canvas.create_oval(
            WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS,
            WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS,
            fill="white"
        )
        self.ball_dx = 2
        self.ball_dy = 2
        self.score1 = 0
        self.score2 = 0
        self.score_label = self.canvas.create_text(
            WIDTH//2, 30, text="0 : 0", fill="white", font=("Arial", 20)
        )
        self.canvas.focus_set()
        self.ai_move_up = False
        self.ai_move_down = False
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.after(1000, self.ai_move)

        # Timer variables
        self.timer = 180  # Default timer of 3 minutes (180 seconds)
        self.timer_label = self.canvas.create_text(
            WIDTH - 80, 30, text="3:00", fill="white", font=("Arial", 20)
        )

        # Home button
        self.home_button = tk.Button(
            self.root, text="Home", command=self.return_home
        )
        self.home_button.pack()

    def move_paddle(self, paddle, dy):
        paddle_pos = self.canvas.coords(paddle)
        if paddle_pos[1] + dy >= 0 and paddle_pos[3] + dy <= HEIGHT:
            self.canvas.move(paddle, 0, dy)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)
        if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
            self.ball_dy *= -1
        if self.collides_with_paddle(ball_pos, self.paddle1) or self.collides_with_paddle(ball_pos, self.paddle2):
            self.ball_dx *= -1
        if ball_pos[0] <= 0:
            self.score2 += 1
            self.update_score()
            self.reset_ball()
        elif ball_pos[2] >= WIDTH:
            self.score1 += 1
            self.update_score()
            self.reset_ball()

    def collides_with_paddle(self, ball_pos, paddle):
        paddle_pos = self.canvas.coords(paddle)
        if ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]:
            if ball_pos[3] >= paddle_pos[1] and ball_pos[1] <= paddle_pos[3]:
                return True
        return False

    def on_key_press(self, event):
        key = event.keysym
        if key == "w":
            self.move_paddle(self.paddle1, -PADDLE_SPEED)
        elif key == "s":
            self.move_paddle(self.paddle1, PADDLE_SPEED)
        elif key == "Up":
            self.move_paddle(self.paddle2, -PADDLE_SPEED)
        elif key == "Down":
            self.move_paddle(self.paddle2, PADDLE_SPEED)

    def on_key_release(self, event):
        key = event.keysym
        if key == "w" or key == "s":
            self.move_paddle(self.paddle1, 0)
        elif key == "Up" or key == "Down":
            self.move_paddle(self.paddle2, 0)

    def update(self):
        self.move_ball()
        self.update_timer()
        self.root.after(10, self.update)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS)
        self.ball_dx *= random.choice([1, -1])
        self.ball_dy *= random.choice([1, -1])

    def update_score(self):
        score_text = f"{self.score1} : {self.score2}"
        self.canvas.itemconfigure(self.score_label, text=score_text)

    def update_timer(self):
        minutes = self.timer // 60
        seconds = self.timer % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        self.canvas.itemconfigure(self.timer_label, text=timer_text)
        if self.timer > 0:
            self.timer -= 1
        else:
            self.end_game()

    def ai_move(self):
        ball_pos = self.canvas.coords(self.ball)
        paddle2_pos = self.canvas.coords(self.paddle2)
        if ball_pos[1] < paddle2_pos[1] + PADDLE_HEIGHT//2:
            self.move_paddle(self.paddle2, -PADDLE_SPEED)
            self.ai_move_up = True
            self.ai_move_down = False
        elif ball_pos[3] > paddle2_pos[3] - PADDLE_HEIGHT//2:
            self.move_paddle(self.paddle2, PADDLE_SPEED)
            self.ai_move_up = False
            self.ai_move_down = True
        else:
            self.move_paddle(self.paddle2, 0)
            self.ai_move_up = False
            self.ai_move_down = False
        self.root.after(10, self.ai_move)

    def end_game(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH//2, HEIGHT//2, text="Game Over!", fill="white", font=("Arial", 30)
        )

    def return_home(self):
        self.canvas.delete("all")
        self.home_button.pack_forget()
        self.root.title("Hand Gesture Glove")
        self.root.after(10, self.update_home)

    def update_home(self):
        self.root.title("Hand Gesture Glove")
        self.home_button.pack()
        self.root.after(100, self.update_home)


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

        self.gesture_button = tk.Button(self.app_buttons_frame, text="Hand Gesture Recognition", command=self.show_gesture_app, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.gesture_button.pack(side=tk.LEFT, padx=10)

        self.app2_button = tk.Button(self.app_buttons_frame, text="Application 2", command=self.open_app2, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
        self.app2_button.pack(side=tk.LEFT, padx=10)

        self.app3_button = tk.Button(self.app_buttons_frame, text="Application 3", command=self.open_app3, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
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
        self.active_app = "Application 2"
        self.update_title("Application 2")
        # Add code to open Application 2

    def open_app3(self):
        self.reset_status()
        self.active_app = "Application 3"
        self.update_title("Application 3")
        # Add code to open Application 3

        ############################################
        # self.reset_status()
        # self.active_app = "Application 3"
        # self.update_title("Application 3")
        ping_pong_game = PingPongGame()
        # ping_pong_game.run()
        ping_pong_game.update()  # Add this line to start the game update loop
        self.root.mainloop() 

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
        self.update_title("Hand Gesture Glove")

    def reset_status(self):
        self.status_label.config(text="Status: Not Receiving Data", fg="white", bg="#232323")
        self.info_label.config(text="Hand Gesture Glove!", fg="white")

    def update_title(self, app_name):
        self.root.title(f"Hand Gesture Glove - {app_name}")

    def receive_data(self):
        while self.is_receiving:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                # Process received data
                # Add code to process the received data for gesture recognition
            except socket.error as e:
                print("Error: ", e)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GestureRecognitionApp()
    app.run()
