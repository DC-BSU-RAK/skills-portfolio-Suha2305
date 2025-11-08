# main.py
"""
01-MathsQuiz/main.py
Author: Suha Fatima
Acknowledgements:
- Tkinter concepts referenced from class examples.
- Random numbers and GUI logic adapted for quiz functionality.
"""

from tkinter import *
from tkinter import messagebox
import random
     #import pygame  # for music (install via pip)

# Initialize music
     #pygame.mixer.init()
# pygame.mixer.music.load("background.mp3")  # Add your music file here
# pygame.mixer.music.play(-1)  # Loop indefinitely

root = Tk()
root.title("Maths Quiz")
root.geometry("800x600")
root.resizable(False, False)

score = 0
question_num = 0
attempt = 1
difficulty = ""

# ================= Frame Switching ==================
def switch_frame(frame):
    frame.tkraise()

# ================= Display Menu =====================
main_frame = Frame(root, width=800, height=600)
instruction_frame = Frame(root, width=800, height=600)
difficulty_frame = Frame(root, width=800, height=600)
quiz_frame = Frame(root, width=800, height=600)
score_frame = Frame(root, width=800, height=600)

for frame in (main_frame, instruction_frame, difficulty_frame, quiz_frame, score_frame):
    frame.place(x=0, y=0)

# ================= Utility Functions =================
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def decideOperation():
    return random.choice(["+", "-"])

def isCorrect(user_ans, correct_ans):
    return user_ans == correct_ans

# ================== Quiz Logic ======================
questions = []
user_answers = []

def generate_questions():
    global questions, question_num, attempt, user_answers
    questions = []
    user_answers = []
    question_num = 0
    attempt = 1

    min_val, max_val = {
        "Easy": (1,9),
        "Medium": (10,99),
        "Hard": (1000,9999)
    }[difficulty]

    for i in range(10):
        a = randomInt(min_val, max_val)
        b = randomInt(min_val, max_val)
        op = decideOperation()
        questions.append((a, b, op))

def display_question():
    global question_num, attempt
    if question_num >= len(questions):
        displayResults()
        return
    a, b, op = questions[question_num]
    question_label.config(text=f"Question {question_num+1}: {a} {op} {b} =")
    answer_entry.delete(0, END)
    attempt = 1

def next_question():
    global question_num, attempt, score
    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number")
        return

    a, b, op = questions[question_num]
    correct_ans = a + b if op == "+" else a - b

    if isCorrect(user_ans, correct_ans):
        points = 10 if attempt == 1 else 5
        score += points
        question_num += 1
        display_question()
    else:
        if attempt == 1:
            messagebox.showinfo("Try again", "Incorrect! One more chance.")
            attempt = 2
            answer_entry.delete(0, END)
        else:
            messagebox.showinfo("Answer", f"Incorrect! The correct answer was {correct_ans}")
            question_num += 1
            display_question()

# ================= Display Results ==================
def displayResults():
    score_label.config(text=f"Score: {score}/100")
    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B+"
    elif score >= 60:
        rank = "B"
    else:
        rank = "C"
    rank_label.config(text=f"Rank: {rank}")
    switch_frame(score_frame)

# ================= Main Menu =======================
Label(main_frame, text="Maths Quiz", font=("Arial",30)).place(x=300, y=100)
Button(main_frame, text="Start", width=20, command=lambda: switch_frame(difficulty_frame)).place(x=300, y=250)
Button(main_frame, text="Instruction", width=20, command=lambda: switch_frame(instruction_frame)).place(x=300, y=320)
Button(main_frame, text="Exit", width=20, command=root.quit).place(x=300, y=390)

# ================= Instructions =====================
Label(instruction_frame, text="Instructions go here", font=("Arial",20)).place(x=150, y=200)
Button(instruction_frame, text="Go Back", width=20, command=lambda: switch_frame(main_frame)).place(x=300, y=400)

# ================= Difficulty Selection =============
Label(difficulty_frame, text="Select Difficulty", font=("Arial",25)).place(x=250, y=150)
def select_difficulty(level):
    global difficulty, score
    difficulty = level
    score = 0
    generate_questions()
    display_question()
    switch_frame(quiz_frame)

Button(difficulty_frame, text="Easy", width=20, command=lambda: select_difficulty("Easy")).place(x=300, y=250)
Button(difficulty_frame, text="Medium", width=20, command=lambda: select_difficulty("Medium")).place(x=300, y=320)
Button(difficulty_frame, text="Hard", width=20, command=lambda: select_difficulty("Hard")).place(x=300, y=390)

# ================= Quiz Frame =======================
question_label = Label(quiz_frame, text="", font=("Arial",20))
question_label.place(x=150, y=200)
answer_entry = Entry(quiz_frame, font=("Arial",16))
answer_entry.place(x=350, y=260)
Button(quiz_frame, text="Next", width=15, command=next_question).place(x=300, y=320)
Button(quiz_frame, text="Exit", width=15, command=lambda: switch_frame(main_frame)).place(x=450, y=320)

# ================= Score Frame ======================
score_label = Label(score_frame, text="", font=("Arial",25))
score_label.place(x=300, y=200)
rank_label = Label(score_frame, text="", font=("Arial",20))
rank_label.place(x=340, y=260)
Button(score_frame, text="Play Again", width=20, command=lambda: switch_frame(difficulty_frame)).place(x=250, y=350)
Button(score_frame, text="Exit", width=20, command=lambda: switch_frame(main_frame)).place(x=450, y=350)

# Start the game
switch_frame(main_frame)
root.mainloop()















# main.py
"""
01-MathsQuiz/main.py
Author: Suha Fatima
Acknowledgements:
- Tkinter concepts referenced from class examples.
- Random numbers and GUI logic adapted for quiz functionality.
"""

from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
     #import pygame  # for music

# =================== Music Setup ====================
     #pygame.mixer.init()
# pygame.mixer.music.load("background.mp3")  # add your music file
# pygame.mixer.music.play(-1)  # loop indefinitely

root = Tk()
root.title("Maths Quiz")
root.geometry("800x600")
root.resizable(False, False)

score = 0
question_num = 0
attempt = 1
difficulty = ""

# ================= Frame Switching ==================
def switch_frame(frame):
    frame.tkraise()

# ================= Utility Functions =================
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def decideOperation():
    return random.choice(["+", "-"])

def isCorrect(user_ans, correct_ans):
    return user_ans == correct_ans

# ================== Quiz Logic ======================
questions = []

def generate_questions():
    global questions, question_num, attempt
    questions = []
    question_num = 0
    attempt = 1

    min_val, max_val = {
        "Easy": (1,9),
        "Medium": (10,99),
        "Hard": (1000,9999)
    }[difficulty]

    for i in range(10):
        a = randomInt(min_val, max_val)
        b = randomInt(min_val, max_val)
        op = decideOperation()
        questions.append((a, b, op))

def display_question():
    global question_num, attempt
    if question_num >= len(questions):
        displayResults()
        return
    a, b, op = questions[question_num]
    question_label.config(text=f"Question {question_num+1}: {a} {op} {b} =")
    answer_entry.delete(0, END)
    attempt = 1

def next_question():
    global question_num, attempt, score
    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number")
        return

    a, b, op = questions[question_num]
    correct_ans = a + b if op == "+" else a - b

    if isCorrect(user_ans, correct_ans):
        points = 10 if attempt == 1 else 5
        score += points
        question_num += 1
        display_question()
    else:
        if attempt == 1:
            messagebox.showinfo("Try again", "Incorrect! One more chance.")
            attempt = 2
            answer_entry.delete(0, END)
        else:
            messagebox.showinfo("Answer", f"Incorrect! The correct answer was {correct_ans}")
            question_num += 1
            display_question()

# ================= Display Results ==================
def displayResults():
    score_label.config(text=f"Score: {score}/100")
    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B+"
    elif score >= 60:
        rank = "B"
    else:
        rank = "C"
    rank_label.config(text=f"Rank: {rank}")
    switch_frame(score_frame)

# ================= Frames ===========================
main_frame = Frame(root, width=800, height=600)
instruction_frame = Frame(root, width=800, height=600)
difficulty_frame = Frame(root, width=800, height=600)
quiz_frame = Frame(root, width=800, height=600)
score_frame = Frame(root, width=800, height=600)

for frame in (main_frame, instruction_frame, difficulty_frame, quiz_frame, score_frame):
    frame.place(x=0, y=0)

# ================= Background Placeholders ==========
# fallback: solid color if image missing
def set_bg(frame, image_path=None):
    if image_path:
        try:
            img = Image.open(image_path).resize((800,600))
            photo = ImageTk.PhotoImage(img)
            label = Label(frame, image=photo)
            label.image = photo
            label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            frame.config(bg="#ffffff")
    else:
        frame.config(bg="#ffffff")

set_bg(main_frame, "main.png")
set_bg(instruction_frame, "instructions.png")
set_bg(difficulty_frame, "Difficulty.png")
set_bg(quiz_frame, "question.png")
set_bg(score_frame, "question.png")

# ================= Helper for centered image buttons ========
def create_img_button(frame, image_path, y, cmd, width=200, height=60):
    x_center = (800 - width)//2
    try:
        img = Image.open(image_path).resize((width,height))
        photo = ImageTk.PhotoImage(img)
        btn = Button(frame, image=photo, bd=0, highlightthickness=0, command=cmd)
        btn.image = photo
    except:
        btn = Button(frame, text=image_path, width=20, height=2, command=cmd)
    btn.place(x=x_center, y=y)
    return btn

# ================= Main Menu Buttons =================
create_img_button(main_frame, "startBUT.png", 250, lambda: switch_frame(difficulty_frame))
create_img_button(main_frame, "instructionsBUT.png", 320, lambda: switch_frame(instruction_frame))
create_img_button(main_frame, "exitBUT.png", 390, root.quit)

# ================= Instructions Frame Button ========
create_img_button(instruction_frame, "gobackBUT.png", 500, lambda: switch_frame(main_frame))

# ================= Difficulty Buttons =================
def select_difficulty(level):
    global difficulty, score
    difficulty = level
    score = 0
    generate_questions()
    display_question()
    switch_frame(quiz_frame)

create_img_button(difficulty_frame, "easyBUT.png", 250, lambda: select_difficulty("Easy"))
create_img_button(difficulty_frame, "mediumBUT.png", 320, lambda: select_difficulty("Medium"))
create_img_button(difficulty_frame, "hardBUT.png", 390, lambda: select_difficulty("Hard"))

# ================= Quiz Frame =======================
# List of 10 question backgrounds
question_bg_images = [
    "question.png", "instructions.png", "q3.png", "q4.png", "q5.png",
    "q6.png", "q7.png", "q8.png", "q9.png", "q10.png"
]

quiz_frame_bg_label = None

# Question label
question_label = Label(quiz_frame, text="", font=("Arial", 20, ), bg="#3d5d3e", fg="white")
question_label.place(x=360, y=240)

# Create answer entry and buttons ONCE
answer_entry = Entry(quiz_frame, font=("Arial", 16), bg="#3d5d3e", fg="white")
answer_entry.place(x=277, y=280)

next_button = create_img_button(quiz_frame, "nextBUT.png", 320, next_question)
exit_button = create_img_button(quiz_frame, "exitBUT.png", 390, lambda: switch_frame(main_frame))

def display_question():
    global question_num, attempt, quiz_frame_bg_label
    if question_num >= len(questions):
        displayResults()
        return

    # Load the background for current question
    try:
        img = Image.open(question_bg_images[question_num]).resize((800,600))
        photo = ImageTk.PhotoImage(img)
        if quiz_frame_bg_label:
            quiz_frame_bg_label.config(image=photo)
            quiz_frame_bg_label.image = photo
        else:
            quiz_frame_bg_label = Label(quiz_frame, image=photo)
            quiz_frame_bg_label.image = photo
            quiz_frame_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        quiz_frame.config(bg="#ffffff")

    # Display ONLY the question (no numbering)
    a, b, op = questions[question_num]
    question_label.config(text=f"{a} {op} {b} =")

    # Clear entry and reset attempt
    answer_entry.delete(0, END)
    attempt = 1

    # Lift widgets above the background
    quiz_frame_bg_label.lift()
    question_label.lift()
    answer_entry.lift()
    next_button.lift()
    exit_button.lift()

# ================= Score Frame ======================
score_label = Label(score_frame, text="", font=("Arial",25), bg="#ffffff")
score_label.place(x=300, y=200)
rank_label = Label(score_frame, text="", font=("Arial",20), bg="#ffffff")
rank_label.place(x=340, y=260)
create_img_button(score_frame, "playagainBUT.png", 350, lambda: switch_frame(difficulty_frame))
create_img_button(score_frame, "exitBUT.png", 420, lambda: switch_frame(main_frame))

# Start the game
switch_frame(main_frame)
root.mainloop()
