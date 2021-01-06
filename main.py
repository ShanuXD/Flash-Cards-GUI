from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
learning_words = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    learning_words = original_data.to_dict(orient='records')
else:
    learning_words = data.to_dict(orient='records')


def is_know():
    print(len(learning_words))
    learning_words.remove(current_card)
    data_file = pd.DataFrame(learning_words)
    # So that we don't save the index every time
    data_file.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(learning_words)
    canvas.itemconfig(canvas_title, text="French", fill='black')
    canvas.itemconfig(canvas_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(canvas_title, text="English", fill='white')
    canvas.itemconfig(canvas_word, text=current_card['English'], fill='white')


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

canvas_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
button_green = Button(image=right_image, highlightthickness=0, command=is_know)
button_green.grid(row=1, column=0)

wrong_image = PhotoImage(file="images/wrong.png")
button_red = Button(image=wrong_image, highlightthickness=0, command=next_card)
button_red.grid(row=1, column=1,)

next_card()

window.mainloop()