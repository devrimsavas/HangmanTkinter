import random
import tkinter as tk
from tkinter import ttk, messagebox
from words import words #found in internet dictionary be sure it is in same directory

#let us write game as class this time . 

class Hangman:

    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("1000x800")
        self.root.config(bg="green")

        self.setup_ui()
        self.reset_game()
        self.add_exit_button()

    def setup_ui(self):
        # Styling
        style = ttk.Style()
        style.configure('TLabel', background='lightgray')
        style.configure('TButton', background='lightblue', font=('Arial', 12))
        style.configure('TLabelframe', background='lightgray', font=('Arial', 12))
        style.configure('Selector.TLabelframe', background='green', font=('Arial', 12))

        # Game Frame
        self.game_frame = ttk.LabelFrame(self.root, text="Hangman Game", padding=(10, 5))
        self.game_frame.place(x=100, y=200, width=800, height=500)

        # Load the GIF
        self.hangman_frames = [tk.PhotoImage(file="hangman2.gif", format=f"gif -index {i}") for i in range(10)]
        self.gif_frame = 0
        self.canvas = tk.Canvas(self.game_frame, width=250, height=400)
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        self.canvas_image = self.canvas.create_image(125, 200, image=self.hangman_frames[self.gif_frame])

        # Widgets
        self.label_word = ttk.Label(self.game_frame, font=("Arial", 24))
        self.label_word.grid(row=0, column=1, pady=20)

        self.label_turns = ttk.Label(self.game_frame, font=("Arial", 18))
        self.label_turns.grid(row=1, column=1, pady=20)

        self.entry = ttk.Entry(self.game_frame, font=("Arial", 18))
        self.entry.grid(row=2, column=1, pady=20)

        self.button_guess = ttk.Button(self.game_frame, text="Guess", command=self.make_guess)
        self.button_guess.grid(row=3, column=1, pady=20)

        self.label_used = ttk.Label(self.game_frame, text="", font=("Arial", 18))
        self.label_used.grid(row=4, column=1, pady=20)

        self.word_length_selector()

    def word_length_selector(self):
        self.selector_frame = ttk.LabelFrame(self.root, text="Select Word Length", style='Selector.TLabelframe')
        self.selector_frame.place(x=100, y=50, width=600, height=70)

        self.word_length_var = tk.IntVar(value=5)
        for i in range(3, 16):
            ttk.Radiobutton(self.selector_frame, text=str(i), variable=self.word_length_var, value=i).pack(side=tk.LEFT)

        ttk.Button(self.selector_frame, text="Start Game", command=self.start_game).pack(side=tk.RIGHT)

    def reset_game(self,length=5):
        self.word = self.get_random_word(length)
        self.player_guess = ['_'] * len(self.word)
        self.used_letters = []
        self.turns_left = 10

        # Reset  GIF frame
        self.gif_frame = 0
        self.canvas.itemconfig(self.canvas_image, image=self.hangman_frames[self.gif_frame])

        self.update_ui()

    def start_game(self):
        selected_length = self.word_length_var.get()
        
        self.reset_game(selected_length)
        self.selector_frame.destroy()

    def get_random_word(self, length=5):
        filtered_words = [word for word in words if len(word) == length]
        return random.choice(filtered_words)

    def update_ui(self):
        self.label_word.config(text=' '.join(self.player_guess))
        self.label_turns.config(text=f"You have {self.turns_left} turns left")
        self.label_used.config(text="Used letters: " + ", ".join(self.used_letters))

    def update_gif_frame(self):
        if self.gif_frame < 9:
            self.gif_frame += 1
            self.canvas.itemconfig(self.canvas_image, image=self.hangman_frames[self.gif_frame])

    def make_guess(self):
        guess = self.entry.get().strip().lower()
        if not guess or len(guess) != 1:
            messagebox.showerror("Error", "Enter a single letter")
            return

        if guess in self.used_letters:
            messagebox.showinfo("Info", f"The letter {guess} is already used")
            self.entry.delete(0,tk.END)
            return

        self.used_letters.append(guess)
        
        if guess not in self.word:
            self.turns_left -= 1
            self.update_gif_frame()

        for idx, letter in enumerate(self.word):
            if letter == guess:
                self.player_guess[idx] = guess

        self.update_ui()

        if "_" not in self.player_guess:
            messagebox.showinfo("Congratulations", "You won!")
            self.reset_game()
        elif self.turns_left <= 0:
            messagebox.showerror("Game Over", f"The word was: {self.word}")
            self.reset_game()

        self.entry.delete(0,tk.END)
        
    def add_exit_button(self):
        exit_button = ttk.Button(self.root, text="Exit", command=self.close_app)
        exit_button.place(x=950, y=10, width=40, height=30)
        
    def close_app(self):
        self.root.destroy()

#end class 

root = tk.Tk()
app = Hangman(root)
root.mainloop()
