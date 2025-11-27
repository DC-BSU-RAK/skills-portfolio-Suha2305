import tkinter as tk
from PIL import Image, ImageTk # importing pillow library to handle images
import random # For selecting random jokes from txt file
import pygame # for background music 

# MUSIC SETUP
pygame.mixer.init()  
pygame.mixer.music.load("funnyBackground.mp3")  
pygame.mixer.music.set_volume(0.5)  # setting the volume
pygame.mixer.music.play(-1) # -1 indicates looping forever

# LAUGHING SOUND SETUP
laugh_sound = pygame.mixer.Sound("laughing.mp3")  # can be .wav too
laugh_sound.set_volume(0.7)

# LOAD JOKES FROM TXT FILE
def load_jokes():
    with open("randomJokes.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    jokes = [line.strip() for line in lines if "?" in line] #? IS A LINE SEPERATOR
    return jokes

joke_list = load_jokes() #list of all the jokes
current_joke = "" #joke which is currently displayed


# SWITCH FRAME
def switch_frame(frame):
    frame.tkraise() # bring the selected frame to the front 


# SHOW RANDOM JOKE
def show_random_joke():
    global current_joke
    current_joke = random.choice(joke_list) # generate a random joke  from the file
    setup, punchline = current_joke.split("?") #line break/ splitting jopke from punchline
    joke_setup_label.config(text=setup)
    joke_punchline_label.config(text="") #clear previous puncline when clicking next


# SHOW PUNCHLINE
def show_punchline():
    if current_joke:
        setup, punchline = current_joke.split("?")
        joke_punchline_label.config(text=punchline) # show punchline
        laugh_sound.play(maxtime=2000) # play laughing sound for 2 seconds 


# CREATE IMAGE BUTTON  
def create_img_button(frame, image_path, x=None, y=None,
                      relx=None, rely=None,
                      act=None, width=None, height=None):
    #Creates a button using an image, Falls back to text if image not found
    try:
        img = Image.open(image_path)
        if width and height:
            img = img.resize((width, height)) # to resize image
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(frame, image=photo, bd=0, highlightthickness=0, command=act) # create button with an image
        btn.image = photo
    except:
        btn = tk.Button(frame, text=image_path, command=act) #Falls back to text if image not found

    if relx is not None and rely is not None:
        btn.place(relx=relx, rely=rely, anchor="center")
    else:
        btn.place(x=x, y=y)

    return btn


# SET BACKGROUND IMAGE
# creates a background image and falls back to white if image isnt found
def set_bg(frame, image_path):
    try:
        img = Image.open(image_path).resize((1000, 700)) # resize img to frame size
        photo = ImageTk.PhotoImage(img)
        bg_label = tk.Label(frame, image=photo)
        bg_label.image = photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower() # send background image to the back
    except:
        frame.config(bg="#ffffff") # white fallback


# MAIN WINDOW
root = tk.Tk()
root.title("Alexa Joke Teller")
root.geometry("1000x700") # window size
root.resizable(False, False) # for fixed layout

# FRAMES
frame1 = tk.Frame(root, width=1000, height=700) # starting frame
frame2 = tk.Frame(root, width=1000, height=700) # joke frame
for frame in (frame1, frame2):
    frame.place(x=0, y=0) # places the frames at same position


# FRAME 1
set_bg(frame1, "Start(Alexa).png") # to set the background image

create_img_button(frame1, "LetsBeginBTN(Alexa).png", # start button 
                  relx=0.5, rely=0.80, act=lambda: switch_frame(frame2),
                  width=200, height=60)


create_img_button(frame1, "QuitBTN(Alexa).png", # quit button
                  relx=0.50, rely=0.90, act=root.quit,
                  width=150, height=60)


# FRAME 2
set_bg(frame2, "Frame(Alexa).png")

create_img_button(frame2, "JokeBTN(Alexa).png", #joke button 
                  relx=0.5, rely=0.25, act=show_random_joke,
                  width=250, height=60)


joke_setup_label = tk.Label(frame2, text="", font=("Consolas", 22), # Joke setup label
                            wraplength=850, justify="center")
joke_setup_label.place(relx=0.5, rely=0.42, anchor="center")


joke_punchline_label = tk.Label(frame2, text="", font=("Helvetica", 22, "italic"), # Punchline label
                                fg="blue", wraplength=850, justify="center")
joke_punchline_label.place(relx=0.5, rely=0.6, anchor="center")


create_img_button(frame2, "PunchlineBTN(Alexa).png", # punchline button 
                  relx=0.5, rely=0.75, act=show_punchline,
                  width=200, height=50)


create_img_button(frame2, "GoBackBTN(Alexa).png", # go back button 
                  relx=0.5, rely=0.90, act=lambda: switch_frame(frame1),
                  width=120, height=50)


# START ON FRAME 1
switch_frame(frame1) # to displlay frame 1 AS FIRST SCREEN 
root.mainloop() 
