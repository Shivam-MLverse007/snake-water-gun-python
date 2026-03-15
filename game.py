import random
import tkinter as tk
from tkinter import messagebox
import os

# ---------- SETTINGS ----------
LEADERBOARD_FILE = "leaderboard.txt"
ROUND_TIME = 10

# ---------- GLOBALS ----------
score_user = 0
score_computer = 0
time_left = ROUND_TIME
timer_running = False
player_name = ""

choices = {"Snake": 1, "Water": -1, "Gun": 0}
names = {1: "Snake", -1: "Water", 0: "Gun"}

# ---------- FUNCTIONS ----------
def save_score():
    if player_name == "":
        return
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(f"{player_name} - You:{score_user} Computer:{score_computer}\n")

def show_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        messagebox.showinfo("Leaderboard", "No scores yet!")
        return

    with open(LEADERBOARD_FILE, "r") as f:
        data = f.read()

    messagebox.showinfo("Leaderboard", data)

def start_timer():
    global time_left, timer_running
    time_left = ROUND_TIME
    timer_running = True
    update_timer()

def update_timer():
    global time_left, timer_running
    if timer_running:
        timer_label.config(text=f"Time left: {time_left}s")
        if time_left > 0:
            time_left -= 1
            root.after(1000, update_timer)
        else:
            timer_running = False
            messagebox.showinfo("Time Up", "Round missed!")
            start_timer()

def play(user_choice):
    global score_user, score_computer, timer_running

    if not timer_running:
        return

    timer_running = False

    computer = random.choice([-1, 0, 1])
    user = choices[user_choice]

    result = f"You: {user_choice}\nComputer: {names[computer]}\n"

    if computer == user:
        result += "Draw!"
    elif (computer == -1 and user == 1) or \
         (computer == 1 and user == 0) or \
         (computer == 0 and user == -1):
        result += "You Win!"
        score_user += 1
    else:
        result += "You Lose!"
        score_computer += 1

    score_label.config(
        text=f"Score -> You: {score_user} | Computer: {score_computer}"
    )

    messagebox.showinfo("Result", result)
    start_timer()

def reset_game():
    global score_user, score_computer
    score_user = 0
    score_computer = 0
    score_label.config("Score -> You: 0 | Computer: 0")

def set_player():
    global player_name
    player_name = name_entry.get()
    if player_name:
        messagebox.showinfo("Welcome", f"Welcome {player_name}!")
        start_timer()

def exit_game():
    save_score()
    root.destroy()

# ---------- WINDOW ----------
root = tk.Tk()
root.title("Snake Water Gun - Pro Edition")
root.geometry("450x480")
root.config(bg="#202020")

title = tk.Label(
    root,
    text="Snake Water Gun Game",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#202020"
)
title.pack(pady=10)

# Player name
tk.Label(root, text="Enter Name:", bg="#202020", fg="white").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Button(root, text="Start Game", command=set_player).pack(pady=5)

score_label = tk.Label(
    root,
    text="Score -> You: 0 | Computer: 0",
    font=("Arial", 12),
    fg="white",
    bg="#202020"
)
score_label.pack(pady=5)

timer_label = tk.Label(
    root,
    text="Time left: 10s",
    font=("Arial", 12),
    fg="yellow",
    bg="#202020"
)
timer_label.pack(pady=5)

btn_style = {
    "width": 15,
    "height": 2,
    "font": ("Arial", 11, "bold"),
    "bg": "#4CAF50",
    "fg": "white"
}

tk.Button(root, text="Snake",
          command=lambda: play("Snake"), **btn_style).pack(pady=5)

tk.Button(root, text="Water",
          command=lambda: play("Water"), **btn_style).pack(pady=5)

tk.Button(root, text="Gun",
          command=lambda: play("Gun"), **btn_style).pack(pady=5)

tk.Button(root, text="Leaderboard",
          command=show_leaderboard).pack(pady=5)

tk.Button(root, text="Exit Game",
          bg="red", fg="white",
          command=exit_game).pack(pady=10)

root.mainloop()
