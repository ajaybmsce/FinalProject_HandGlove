import tkinter as tk
import random

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
        key = event.char
        if key == "w":
            self.move_paddle(self.paddle1, -PADDLE_SPEED)
        elif key == "s":
            self.move_paddle(self.paddle1, PADDLE_SPEED)
        elif key == "Up":
            self.move_paddle(self.paddle2, -PADDLE_SPEED)
        elif key == "Down":
            self.move_paddle(self.paddle2, PADDLE_SPEED)

    def on_key_release(self, event):
        key = event.char
        if key == "w" or key == "s":
            self.move_paddle(self.paddle1, 0)
        elif key == "Up" or key == "Down":
            self.move_paddle(self.paddle2, 0)

    def update(self):
        self.move_ball()
        self.root.after(10, self.update)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS)
        self.ball_dx *= random.choice([1, -1])
        self.ball_dy *= random.choice([1, -1])

    def update_score(self):
        score_text = f"{self.score1} : {self.score2}"
        self.canvas.itemconfigure(self.score_label, text=score_text)

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

    def run(self):
        self.update()
        self.root.mainloop()

if __name__ == "__main__":
    game = PingPongGame()
    game.run()
