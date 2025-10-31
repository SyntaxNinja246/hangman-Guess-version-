import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import random
import threading
import time


from tkinter import simpledialog
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Hangman Game")
        self.root.resizable(False, False)
        
        
        self.word_list = [
            ("astronaut", "A person trained for space travel"),
            ("blueprint", "Detailed technical drawing or plan"),
            ("carousel", "Rotating amusement park ride"),
            ("dandelion", "Yellow flower that turns into white puffball"),
            ("flamingo", "Pink bird that stands on one leg"),
            ("icecream", "Frozen dessert in cones or cups"),
            ("keyboard", "Used to type on computers"),
            ("lighthouse", "Coastal tower with a guiding light"),
            ("nightmare", "Frightening dream"),
            ("pyramid", "Triangular structure in Egypt"),
            ("Epiphany", "The sudden Realization"),
            ("Maestro", "a distinguished performer of classical music")
            ]

        self.load_images()
        self.setup_ui()
        self.new_game()

    def load_images(self):
        original_bg = Image.open("images/bg_retro.png").convert("RGBA").resize((800,600))
        enhancer = ImageEnhance.Brightness(original_bg)
        dimmed_bg = enhancer.enhance(0.8)  # Reduce brightness by 20%
        self.bg_image = ImageTk.PhotoImage(dimmed_bg)

        self.win_image_raw = Image.open("images/win.png").resize((450, 450))
        self.win_image = ImageTk.PhotoImage(self.win_image_raw)

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack()
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.word_display = self.canvas.create_text(400, 100, text='', font=("Press Start 2P", 24), fill='white')

        self.hint_text = self.canvas.create_text(400, 150, text='', font=("Press Start 2P", 12), fill='white')

        self.letter_buttons = {}
        x_start, y_start = 140, 450
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            x = x_start + (i % 13) * 40
            y = y_start + (i // 13) * 50
            btn = tk.Button(self.root, text=letter, font=("Press Start 2P", 10), bg="#FFCC00", fg="black",
                            command=lambda l=letter: self.check_letter(l))
            btn.place(x=x, y=y, width=35, height=35)
            self.letter_buttons[letter] = btn

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Press Start 2P", 12), bg="black", fg="lime")
        self.score_label.place(x=10, y=10)

        self.reset_button = tk.Button(self.root, text="New Game", font=("Press Start 2P", 10), bg="hot pink", fg="black",
                                      command=self.new_game)
        self.reset_button.place(x=650, y=20)

        self.timer_label = tk.Label(self.root, text="Time: 60", font=("Press Start 2P", 12), bg="black", fg="red")
        self.timer_label.place(x=10, y=50)

    def new_game(self):
        self.word, self.hint = random.choice(self.word_list)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.score = 0
        self.time_left = 60

        self.update_displayed_word()
        self.canvas.itemconfig(self.hint_text, text=f"Hint: {self.hint}")

        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)

        self.score_label.config(text="Score: 0")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.start_timer()
        self.canvas.delete("win_image")
        self.canvas.delete("confetti")

    def update_displayed_word(self):
        display = ' '.join([letter if letter.upper() in self.guessed_letters else '_' for letter in self.word.upper()])
        self.canvas.itemconfig(self.word_display, text=display)

    def check_letter(self, letter):
        self.letter_buttons[letter].config(state=tk.DISABLED)
        if letter.lower() in self.word:
            self.guessed_letters.append(letter)
            self.update_displayed_word()
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            if all(l.upper() in self.guessed_letters for l in self.word):
                self.win_game()
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses == 6:
                self.lose_game()

    def win_game(self):
        self.canvas.create_image(400, 200, image=self.win_image, tags="win_image")
        self.launch_confetti()
        messagebox.showinfo("You Win!", f"You guessed it! The word was '{self.word}'.")
        self.disable_all_buttons()
        self.time_left = 0
        self.save_score("Won")


    def lose_game(self):
        messagebox.showinfo("You Lost", f"The word was '{self.word}'. Try again!")
        self.disable_all_buttons()
        self.time_left = 0
        self.save_score("Lost")


    def disable_all_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state=tk.DISABLED)

    def start_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.root.after(1000, self.start_timer)
        else:
            if all(l.upper() in self.guessed_letters for l in self.word):
                return  # Already won
            self.lose_game()

    def launch_confetti(self):
        colors = ["red", "yellow", "blue", "green", "purple", "orange"]
        for _ in range(100):
            x = random.randint(100, 700)
            y = random.randint(0, 400)
            size = random.randint(5, 10)
            color = random.choice(colors)
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color, tags="confetti")

if __name__ == '__main__':
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
