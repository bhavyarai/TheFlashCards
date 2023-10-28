from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
#---------------------------- READING DATA --------------------------#
try:
    data = pandas.read_csv("data/words_to_lean.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
word_to_learn = data.to_dict(orient="records")
current_card = {}


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="White")
    canvas.itemconfig(card_background, image=back_img)
    canvas.itemconfig(card_word, text=current_card["English"], fill="White")


def show_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = word_to_learn[random.randint(0, len(word_to_learn))]
    to_learn = current_card["French"]
    canvas.itemconfig(card_word, text=to_learn, fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_background, image=front_img)
    flip_timer = window.after(3000, flip_card)


def is_known():
    global current_card
    word_to_learn.remove(current_card)
    data = pandas.DataFrame(word_to_learn)
    data.to_csv("data/words_to_lean.csv", index=False)
    show_card()

#-------------------------------- UI --------------------------------#


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Create card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="Title", font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text="Word", font=('Ariel', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
right_sign = PhotoImage(file="./images/right.png")
right_button = Button(image=right_sign, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_sign = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_sign, highlightthickness=0, command=show_card)
wrong_button.grid(row=1, column=0)

show_card()
window.mainloop()