import tkinter as tk
from tkinter import messagebox
import random
import time

# ------------------------------
# Word Banks
# ------------------------------
easy_words = [
    "apple",
    "banana",
    "cat",
    "dog",
    "house",
    "green",
    "phone",
    "orange",
    "mouse",
    "robot",
    "water",
    "tree",
    "music",
]
medium_phrases = [
    "good morning",
    "take care",
    "thank you",
    "see you soon",
    "have fun",
    "follow me",
    "try again",
    "nice job",
]
hard_sentences = [
    "I will finish my homework tonight.",
    "Typing practice can improve your accuracy.",
    "This game helps you type faster.",
    "Learning English is fun and useful.",
    "She bought some flowers yesterday.",
]

# ------------------------------
# Main App
# ------------------------------
root = tk.Tk()
root.title("Speed Typing Challenge")
root.geometry("800x600")
root.configure(bg="#233447")

# ------------------------------
# Variables
# ------------------------------
difficulty = tk.StringVar(value="easy")
rounds_total = tk.IntVar(value=5)
current_question = ""
current_round = 0
correct_count = 0
typed_chars = 0
countdown_time = 0
timer_id = None
start_time_game = 0
last_entry_text = ""
completed_difficulties = set()


# ------------------------------
# UI Styles
# ------------------------------
def style_button(btn):
    btn.config(
        width=12,
        height=1,
        font=("Arial", 12),
        bg="white",
        fg="black",
        bd=2,
        relief="ridge",
        activebackground="#ddd",
    )


def style_selected(btn):
    btn.config(bg="#ffdd55")  # yellow highlight


# ------------------------------
# Difficulty Selector
# ------------------------------
def select_difficulty(level):
    difficulty.set(level)
    for b in diff_buttons:
        style_button(b)
    if level == "easy":
        style_selected(btn_easy)
    elif level == "medium":
        style_selected(btn_medium)
    else:
        style_selected(btn_hard)


# ------------------------------
# Frames
# ------------------------------
frame_top = tk.Frame(root, bg="#233447")
frame_top.pack(pady=10)
frame_middle = tk.Frame(root, bg="#233447")
frame_middle.pack(expand=True, fill="both")

# ------------------------------
# Title
# ------------------------------
title = tk.Label(
    frame_top,
    text="Speed Typing Challenge",
    font=("Arial", 26, "bold"),
    fg="white",
    bg="#233447",
)
title.pack()

# ------------------------------
# Rounds
# ------------------------------
frame_round = tk.Frame(frame_top, bg="#233447")
frame_round.pack(pady=5)
tk.Label(
    frame_round, text="Rounds:", fg="white", bg="#233447", font=("Arial", 14)
).pack(side="left", padx=5)
entry_rounds = tk.Entry(
    frame_round,
    textvariable=rounds_total,
    width=5,
    font=("Arial", 14),
    justify="center",
)
entry_rounds.pack(side="left")

# ------------------------------
# Difficulty Buttons
# ------------------------------
frame_diff = tk.Frame(frame_top, bg="#233447")
frame_diff.pack(pady=5)
btn_easy = tk.Button(
    frame_diff, text="Normal", command=lambda: select_difficulty("easy")
)
btn_medium = tk.Button(
    frame_diff, text="Hard", command=lambda: select_difficulty("medium")
)
btn_hard = tk.Button(
    frame_diff, text="Nightmare", command=lambda: select_difficulty("hard")
)
diff_buttons = [btn_easy, btn_medium, btn_hard]
for b in diff_buttons:
    style_button(b)
    b.pack(side="left", padx=5)
style_selected(btn_easy)

# ------------------------------
# Question Display
# ------------------------------
text_question = tk.Text(
    frame_middle,
    height=2,
    width=50,
    font=("Consolas", 32),
    bg="#233447",
    fg="white",
    bd=0,
    highlightthickness=0,
)
text_question.pack(pady=10)
text_question.tag_config("correct", foreground="#00ff00")
text_question.tag_config("wrong", foreground="#ff4444")
text_question.tag_config("normal", foreground="white")
text_question.tag_config("center", justify="center")

# ------------------------------
# Game Over / Round Label
# ------------------------------
label_gameover = tk.Label(
    frame_middle, text="", font=("Arial", 28, "bold"), fg="white", bg="#233447"
)
label_gameover.pack(pady=5)

# ------------------------------
# Timer Label & Progress Bar
# ------------------------------
label_timer = tk.Label(
    frame_middle, text="", font=("Arial", 18), fg="white", bg="#233447"
)
label_timer.pack(pady=5)

progress_timer = tk.Canvas(frame_middle, width=500, height=20, bg="#555")
progress_timer.pack(pady=5)

# ------------------------------
# Entry Typing
# ------------------------------
entry_typing = tk.Entry(
    frame_middle,
    font=("Consolas", 20),
    width=30,
    bg="#333333",
    fg="white",
    insertbackground="white",
    justify="center",
)
entry_typing.pack(pady=5)

# ------------------------------
# Score / WPM Labels
# ------------------------------
label_score = tk.Label(
    frame_middle, text="", font=("Arial", 16), fg="#00ff66", bg="#233447"
)
label_wpm = tk.Label(
    frame_middle, text="", font=("Arial", 16), fg="#00ff66", bg="#233447"
)

# ------------------------------
# Start Button
# ------------------------------
btn_start = tk.Button(
    frame_top,
    text="Start Game",
    font=("Arial", 16),
    width=14,
    command=lambda: start_game(),
)
btn_start.pack(pady=10)


# ------------------------------
# Core Functions
# ------------------------------
def flash_red():
    """Flash the question background red briefly"""
    orig_bg = text_question.cget("bg")

    def flash(times=2):
        if times <= 0:
            text_question.config(bg=orig_bg)
            return
        text_question.config(bg="#ff4444")
        root.after(100, lambda: text_question.config(bg=orig_bg))
        root.after(200, lambda: flash(times - 1))

    flash()


def update_color(event=None):
    global correct_count, typed_chars, current_round, timer_id, last_entry_text
    entry_text = entry_typing.get()
    if entry_text == last_entry_text:
        return
    last_entry_text = entry_text

    text_question.delete("1.0", tk.END)
    wrong_found = False
    for i, ch in enumerate(current_question):
        if i < len(entry_text):
            tag = "correct" if entry_text[i] == ch else "wrong"
            if entry_text[i] != ch:
                wrong_found = True
        else:
            tag = "normal"
        text_question.insert(tk.END, ch, (tag, "center"))

    if wrong_found:
        flash_red()

    if len(entry_text) == len(current_question) and entry_text == current_question:
        correct_count += 1
        typed_chars += len(current_question)
        if timer_id:
            root.after_cancel(timer_id)
        current_round += 1
        next_round()

    update_wpm()


def update_wpm():
    elapsed = time.time() - start_time_game
    wpm = int((typed_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0
    label_wpm.config(text=f"WPM: {wpm}")
    label_wpm.pack()


def update_timer_bar():
    progress_timer.delete("bar")
    limit = get_question()[1]
    bar_length = int((countdown_time / limit) * 500) if limit > 0 else 0
    progress_timer.create_rectangle(0, 0, bar_length, 20, fill="#00ff66", tag="bar")
    root.after(100, update_timer_bar)


def get_question():
    if difficulty.get() == "easy":
        return random.choice(easy_words), 10
    elif difficulty.get() == "medium":
        return random.choice(medium_phrases), 10
    else:
        return random.choice(hard_sentences), 15


def start_game():
    global current_round, correct_count, typed_chars, start_time_game
    completed_difficulties.add(difficulty.get())
    current_round = 0
    correct_count = 0
    typed_chars = 0
    label_gameover.config(text="")
    label_score.config(text="")
    label_wpm.config(text="")
    start_time_game = time.time()
    next_round()
    update_timer_bar()


def next_round():
    global current_question, countdown_time
    if current_round >= rounds_total.get():
        return game_over()
    q, limit = get_question()
    current_question = q
    countdown_time = limit
    current_round_display()
    text_question.delete("1.0", tk.END)
    text_question.insert("1.0", current_question, ("normal", "center"))
    entry_typing.delete(0, tk.END)
    entry_typing.focus()
    update_color()
    update_timer()


def update_timer():
    global timer_id, countdown_time, current_round, typed_chars, correct_count
    # 倒數最後3秒閃動
    if countdown_time <= 3:
        color = "#ff4444" if int(countdown_time * 10) % 2 == 0 else "#233447"
        text_question.config(bg=color)
    else:
        text_question.config(bg="#233447")

    label_timer.config(text=f"Time: {countdown_time:.1f}s")

    if countdown_time <= 0:
        if entry_typing.get().strip() == current_question.strip():
            correct_count += 1
            typed_chars += len(current_question)
        current_round += 1
        return next_round()

    countdown_time -= 0.1
    timer_id = root.after(100, update_timer)


def current_round_display():
    label_gameover.config(
        text=f"Round {current_round + 1}/{rounds_total.get()}", fg="white"
    )


def animate_score(text, label, step_delay=50):
    label.config(text="")

    def step(i=0):
        if i <= len(text):
            label.config(text=text[:i])
            root.after(step_delay, lambda: step(i + 1))

    step()


def animate_wpm(final_wpm):
    wpm_current = 0
    step_val = max(1, final_wpm // 50)

    def step_func():
        nonlocal wpm_current
        if wpm_current >= final_wpm:
            label_wpm.config(text=f"WPM: {final_wpm}")
            return
        wpm_current += step_val
        if wpm_current > final_wpm:
            wpm_current = final_wpm
        label_wpm.config(text=f"WPM: {wpm_current}")
        root.after(30, step_func)

    step_func()


def game_over():
    label_gameover.config(text="Game Over", fg="white")
    if not completed_difficulties:
        messagebox.showwarning("Warning", "請至少完成一種難度！")
    accuracy = int((correct_count / rounds_total.get()) * 100)
    animate_score(
        f"Final Score: {correct_count}/{rounds_total.get()} ({accuracy}%)", label_score
    )
    total_time_sec = time.time() - start_time_game
    wpm = int((typed_chars / 5) / (total_time_sec / 60)) if total_time_sec > 0 else 0
    animate_wpm(wpm)


# ------------------------------
# Bind Typing Event
# ------------------------------
entry_typing.bind("<KeyRelease>", update_color)

root.mainloop()
