from tkinter import *
from tkinter import messagebox # for alert box
import random # to generate random numbers
from PIL import Image, ImageTk # importing pillow library to handle images
import pygame  # for background music 

#  MUSIC SETUP 
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")  
pygame.mixer.music.set_volume(0.3) # setting the volume
pygame.mixer.music.play(-1) # -1 indicates looping forever

#  WINDOW SETUP
root = Tk()
root.title("Maths Quiz")
root.geometry("800x600") # window size
root.resizable(False, False) # for fixed layout

#  GLOBAL VARIABLES
score = 0 #current score
question_num = 0 # to track question number
attempt = 1 # no. of attempts
difficulty = ""
questions = []

#  SWITCHING FRAME FUNCTION
def switch_frame(frame):
    frame.tkraise() # to display each frame one by one on demand 

#  UTILITY FUNCTIONS
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val) # to generate random numbers between the given min and max

def decideOperation():
    return random.choice(["+", "-"]) # to randomly generate either "+" or "-"

def isCorrect(user_ans, correct_ans):
    return user_ans == correct_ans # to check answer

#  QUESTION GENERATION
def generate_questions(): # to generate 10 random question based on the difficulty selected
    global questions, question_num, attempt

    questions = []
    question_num = 0 # to start from the first question
    attempt = 1 # to reset attempt for a new quiz

    # min and max value for each difficulty
    min_val, max_val = {
        "Easy": (1, 9),
        "Medium": (10, 99),
        "Hard": (1000, 9999)
    }[difficulty]

    # for loop for generating 10 questions
    for _ in range(10):
        a = randomInt(min_val, max_val) #1st random number
        b = randomInt(min_val, max_val) #2nd random number
        op = decideOperation() 
        questions.append((a, b, op)) # store question tuple instead of list

#  DISPLAY QUESTION
def display_question(): #to show question s on screen and display background
    global question_num, attempt, quiz_frame_bg_label

    if question_num >= len(questions): # to check if quiz is finished
        displayResults() #show result
        return

    # Background
    try:
        img = Image.open(question_bg_images[question_num]).resize((800, 600))
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

    # Display Question
    a, b, op = questions[question_num]
    question_label.config(text=f"{a} {op} {b} =")

    # To Reset entry box 
    answer_entry.delete(0, END)
    attempt = 1

    # Bring elements to the top of the screen so they arent hidden by the background
    question_label.lift()
    answer_entry.lift()
    next_button.lift()
    exit_button.lift()
    score_tracker.lift()  

#  CHECK ANSWER AND MOVE TO NEXT QUESTION
def next_question():
    global question_num, attempt, score

    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number") #message box pops up if answer is wrong
        return

    a, b, op = questions[question_num]
    correct_ans = a + b if op == "+" else a - b

    if isCorrect(user_ans, correct_ans): # to check if answer is correct
        points = 10 if attempt == 1 else 5 # Score will be 10 points on first try and 5 on second
        score += points
        score_tracker.config(text=f"Score: {score}")  # tp update score live 
        question_num += 1
        display_question() # move to next question 
    else:
        if attempt == 1:
            messagebox.showinfo("Try Again", "Incorrect! One more chance.") # to display msg box stating 1 more chance is left
            attempt = 2
            answer_entry.delete(0, END)
        else:
            messagebox.showinfo("Answer", f"Incorrect! Correct answer: {correct_ans}") # to display the correct answer
            question_num += 1
            display_question()

#  DISPLAY FINAL RESULTS
def displayResults():
    score_label.config(text=f"Score: {score}/100") # to display total score]

    if score >= 90: # calculating the rank based on the score 
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
    switch_frame(score_frame) # to show result on screen

#  FRAME CREATION
main_frame = Frame(root, width=800, height=600) # first frame the user sees when running the code
instruction_frame = Frame(root, width=800, height=600) # instrcutions frame, providing the instructios
difficulty_frame = Frame(root, width=800, height=600) # difficulty frame, providing the 3 difficulties
quiz_frame = Frame(root, width=800, height=600) # quiz frame. where the actual questions pop up rotating with different images
score_frame = Frame(root, width=800, height=600) # score frame, to display the end score

for frame in (main_frame, instruction_frame, difficulty_frame, quiz_frame, score_frame):
    frame.place(x=0, y=0) # to stack all frames 

#  BACKGROUND SETUP FUNCTION
def set_bg(frame, image_path=None): # to set image for the backgrouund and if an error occurs and image isnt displayed, itll show as a white background
    if image_path:
        try:
            img = Image.open(image_path).resize((800, 600))
            photo = ImageTk.PhotoImage(img)
            label = Label(frame, image=photo)
            label.image = photo
            label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            frame.config(bg="#ffffff")
    else:
        frame.config(bg="#ffffff")

# Apply Backgrounds to frames
set_bg(main_frame, "main.png")
set_bg(instruction_frame, "instructions.png")
set_bg(difficulty_frame, "Difficulty.png")
set_bg(score_frame, "score.png")

#  IMAGE BUTTON CREATOR
def create_img_button(frame, image_path, y, cmd, width=200, height=60): # to set images for buttons, if image fails to show up the button will be shown as a text button
    x_center = (800 - width) // 2
    try:
        img = Image.open(image_path).resize((width, height))
        photo = ImageTk.PhotoImage(img)
        btn = Button(frame, image=photo, bd=0, highlightthickness=0, command=cmd)
        btn.image = photo
    except:
        btn = Button(frame, text=image_path, width=20, height=2, command=cmd)
    btn.place(x=x_center, y=y)
    return btn

#  MAIN MENU
create_img_button(main_frame, "startBUT.png", 250, lambda: switch_frame(difficulty_frame))
create_img_button(main_frame, "instructionsBUT.png", 320, lambda: switch_frame(instruction_frame))
create_img_button(main_frame, "exitBUT.png", 390, root.quit)

#  INSTRUCTIONS FRAME
create_img_button(instruction_frame, "gobackBUT.png", 440, lambda: switch_frame(main_frame))

#  DIFFICULTY FRAME
def select_difficulty(level):
    global difficulty, score
    difficulty = level # set difficulty
    score = 0 # reset score to 0
    score_tracker.config(text="Score: 0")  # score display
    generate_questions() # to generate questions
    display_question() # to display questions 
    switch_frame(quiz_frame) # to switch frame 

create_img_button(difficulty_frame, "easyBUT.png", 250, lambda: select_difficulty("Easy"))
create_img_button(difficulty_frame, "mediumBUT.png", 320, lambda: select_difficulty("Medium"))
create_img_button(difficulty_frame, "hardBUT.png", 390, lambda: select_difficulty("Hard"))

#  QUIZ FRAME 
question_bg_images = [ # images for each of the 10 question
    "question1.png", "question2.png",  "question3.png", "question4.png", "question5.png",
    "question6.png", "question7.png", "question8.png", "question9.png", "question10.png"
]

quiz_frame_bg_label = None

# Question label
question_label = Label(quiz_frame, text="", font=("comic Sans MS", 22, "bold"), bg="#3d5d3e", fg="white")
question_label.place(x=355, y=230)

# Score tracker 
score_tracker = Label(quiz_frame, text="Score: 0", font=("comic Sans MS", 16, "bold"), bg="#9e968c", fg="white")
score_tracker.place(x=10, y=117)

# Answer Entry
answer_entry = Entry(quiz_frame, font=("comic Sans MS", 16), bg="#3d5d3e", fg="white", justify="center")
answer_entry.place(x=277, y=280)

# Buttons
next_button = create_img_button(quiz_frame, "nextBUT.png", 320, next_question)
exit_button = create_img_button(quiz_frame, "exitBUT.png", 390, lambda: switch_frame(main_frame))

#  SCORE FRAME
score_label = Label(score_frame, text="", font=("comic Sans MS", 25), bg="#ffffff")
score_label.place(x=300, y=200)

rank_label = Label(score_frame, text="", font=("comic Sans MS", 20), bg="#ffffff")
rank_label.place(x=340, y=260)

create_img_button(score_frame, "playagainBUT.png", 320, lambda: switch_frame(difficulty_frame))
create_img_button(score_frame, "exitBUT.png", 390, lambda: switch_frame(main_frame))

#  START GAME
switch_frame(main_frame) # to show the main frame first 
root.mainloop()
