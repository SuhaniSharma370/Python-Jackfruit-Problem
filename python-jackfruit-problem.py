import tkinter as tk
from tkinter import messagebox
import random
import difflib

class GamesHub:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YOUR GAMES HUB")
        self.root.configure(bg="#020014")
        self.root.resizable(False, False)

        # Make main window fullscreen
        self.root.attributes("-fullscreen", True)

        # Get screen size for positioning
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        canvas = tk.Canvas(self.root, width=screen_w, height=screen_h,
                           bg="#020014", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Gradient-style background using rectangles
        for i in range(0, screen_h, 4):
            color = "#%02x%02x%02x" % (2, int(10 + i / 4), int(31 + i / 5))
            canvas.create_rectangle(0, i, screen_w, i + 4, outline="", fill=color)

        # Neon accent circles
        canvas.create_oval(50, 80, 350, 380, outline="#00ffff", width=4)
        canvas.create_oval(screen_w - 400, screen_h - 400,
                           screen_w - 80, screen_h - 80,
                           outline="#ff00ff", width=4)

        # Beautiful title
        canvas.create_text(screen_w // 2, 160,
                           text="YOUR GAMES",
                           font=("Arial Black", 70, "bold"),
                           fill="#00ffff")
        canvas.create_text(screen_w // 2, 240,
                           text="Choose one to play",
                           font=("Arial", 30),
                           fill="#ff99ff")

        canvas.create_text(screen_w // 2, 300,
                           text="Fun mini-games · Confetti · Neon vibes",
                           font=("Arial", 18, "italic"),
                           fill="#ffffff")

        # Helper to create animated buttons
        def btn(x, y, text, color, cmd):
            rect = canvas.create_round_rectangle if hasattr(canvas, "create_round_rectangle") else canvas.create_rectangle
            # Normal rectangle (rounded not default in tkinter)
            button_rect = canvas.create_rectangle(x - 220, y - 70, x + 220, y + 70,
                                                  fill=color, outline="#ffffff", width=4)
            glow_rect = canvas.create_rectangle(x - 230, y - 80, x + 230, y + 80,
                                                outline=color, width=2)
            txt = canvas.create_text(x, y,
                                     text=text,
                                     font=("Arial Black", 40, "bold"),
                                     fill="white")

            def enter(e):
                canvas.itemconfig(button_rect, fill="#ffffff", outline=color, width=6)
                canvas.itemconfig(txt, fill=color)

            def leave(e):
                canvas.itemconfig(button_rect, fill=color, outline="#ffffff", width=4)
                canvas.itemconfig(txt, fill="white")

            def click(e):
                cmd()

            for item in (button_rect, glow_rect, txt):
                canvas.tag_bind(item, "<Enter>", enter)
                canvas.tag_bind(item, "<Leave>", leave)
                canvas.tag_bind(item, "<Button-1>", click)

        center_x = screen_w // 2
        btn(center_x, 420, "Emoquest", "#ff0066", self.launch_emoquest)
        btn(center_x, 560, "TIC TAC TOE", "#00c777", self.launch_tictactoe)

        # Exit button (bottom-right)
        def exit_app():
            self.root.destroy()

        exit_btn = tk.Button(self.root, text="EXIT", font=("Arial", 14, "bold"),
                             bg="#ff4444", fg="white", command=exit_app)
        exit_btn.place(x=screen_w - 120, y=screen_h - 60, width=90, height=40)

        self.root.mainloop()

    def launch_emoquest(self):
        self.root.withdraw()
        EmoquestGame(self.root)

    def launch_tictactoe(self):
        self.root.withdraw()
        TicTacToeGame(self.root)

# ======================= GAME 1: emoquest =======================
class EmoquestGame:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("🔥 Emoquest – Guess the Emotion! 🔥")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        # Fullscreen for emoquest window
        self.root.attributes("-fullscreen", True)

        # YOUR EXACT ORIGINAL GAME LOGIC (only window/geometry changed)
        PUZZLES = [
            ("😀😃", "happy"),
            ("😢😭", "sad"),
            ("😡🔥", "angry"),
            ("😱👻", "scared"),
            ("🤢😖", "disgusted"),
            ("😴💤", "sleepy"),
            ("🥳🎊", "excited"),
            ("😤💨", "mad")
        ]
        secret_emojis = ""
        secret_answer = ""
        guesses = []
        tries_left = 6
        game_active = False

        def pick_new_puzzle():
            nonlocal secret_emojis, secret_answer
            puzzle = random.choice(PUZZLES)
            secret_emojis = puzzle[0]
            secret_answer = puzzle[1]

        def get_similarity(guess):
            guess_norm = guess.lower().replace(" ", "").replace("-", "")
            secret_norm = secret_answer.lower().replace(" ", "").replace("-", "")
            return difflib.SequenceMatcher(None, guess_norm, secret_norm).ratio()

        def submit_guess():
            nonlocal tries_left, game_active
            guess = guess_entry.get().strip()
            if not guess or not game_active:
                return

            sim = get_similarity(guess)
            guesses.append((guess, sim))

            if sim >= 0.95:
                messagebox.showinfo("🎉 Emoquest WINNER! 🎉", f"You guessed it: '{secret_answer}'!")
                status_label.config(text="🎉 YOU WON! 🎉", fg="lime")
                confetti_explosion()
                game_active = False
                return

            tries_left -= 1
            if tries_left <= 0:
                messagebox.showinfo("💀 GAME OVER 💀", f"The emotion was '{secret_answer}'!")
                status_label.config(text=f"Game Over! Answer: {secret_answer}", fg="red")
                game_active = False
                reveal_answer()
                return

            update_guesses_display()
            guess_entry.delete(0, tk.END)
            status_label.config(text=f"Tries left: {tries_left}", fg="orange")
            guess_entry.focus()

        def update_guesses_display():
            for widget in guesses_frame.winfo_children():
                widget.destroy()

            for guess_text, sim in guesses[-6:]:
                tk.Label(guesses_frame,
                         text=guess_text,
                         font=("Arial", 18, "bold"),
                         bg="#2a2a2a",
                         fg="cyan",
                         relief="ridge",
                         bd=1).pack(fill="x", padx=10, pady=4)

        def reveal_answer():
            answer_label.config(text=f"Answer: {secret_answer}", fg="yellow")

        def new_game():
            nonlocal guesses, tries_left, game_active
            pick_new_puzzle()
            guesses = []
            tries_left = 6
            game_active = True
            emoji_label.config(text=secret_emojis)
            status_label.config(text=f"Tries left: {tries_left} | Guess the emotion!", fg="orange")
            update_guesses_display()
            guess_entry.delete(0, tk.END)
            answer_label.config(text="")
            guess_entry.focus()

        def confetti_explosion():
            colors = ["red", "yellow", "cyan", "lime", "orange", "magenta"]
            pieces = []
            for _ in range(65):
                x = random.randint(0, screen_w)
                y = random.randint(-200, -50)
                length = random.randint(18, 28)
                thick = random.randint(2, 4)
                speed = random.uniform(3, 6)
                tilt = random.choice([-5, -3, -2, 2, 3, 5])
                obj = canvas_confetti.create_polygon(
                    x, y,
                    x + length, y + tilt,
                    x + length - thick, y + thick + tilt,
                    x - thick, y + thick,
                    fill=random.choice(colors), outline=""
                )
                pieces.append([obj, speed])

            def fall():
                active = False
                for item, sp in pieces:
                    canvas_confetti.move(item, 0, sp)
                    coords = canvas_confetti.coords(item)
                    if max(coords[1::2]) > screen_h + 20:
                        canvas_confetti.delete(item)
                        continue
                    active = True
                if active:
                    self.root.after(25, fall)
            fall()

        def on_enter_key(event):
            submit_guess()

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        canvas_confetti = tk.Canvas(self.root,
                                    width=screen_w,
                                    height=screen_h,
                                    bg="#1a1a1a",
                                    highlightthickness=0)
        canvas_confetti.place(x=0, y=0, relwidth=1, relheight=1)

        top_frame = tk.Frame(self.root, bg="#1a1a1a")
        top_frame.place(relx=0.5, rely=0.05, anchor="n")

        tk.Label(top_frame, text="Emoquest",
                 font=("Arial", 48, "bold"),
                 fg="cyan", bg="#1a1a1a").pack()
        tk.Label(top_frame,
                 text="Guess the emotion/phrase from emojis!\n6 tries - type your answer below",
                 font=("Arial", 16),
                 fg="white", bg="#1a1a1a").pack(pady=10)

        emoji_label = tk.Label(self.root, text="",
                               font=("Arial", 120),
                               fg="yellow", bg="#1a1a1a")
        emoji_label.place(relx=0.5, rely=0.25, anchor="n")

        status_label = tk.Label(self.root,
                                text="Click New Game to start!",
                                font=("Arial", 20, "bold"),
                                fg="orange", bg="#1a1a1a")
        status_label.place(relx=0.5, rely=0.45, anchor="n")

        guesses_frame = tk.Frame(self.root, bg="#2a2a2a", relief="sunken", bd=2)
        guesses_frame.place(relx=0.5, rely=0.52, anchor="n",
                            relwidth=0.7, relheight=0.22)

        guess_frame = tk.Frame(self.root, bg="#1a1a1a")
        guess_frame.place(relx=0.5, rely=0.76, anchor="n")
        tk.Label(guess_frame, text="Your Guess:",
                 font=("Arial", 18),
                 fg="white", bg="#1a1a1a").pack(side="left")
        guess_entry = tk.Entry(guess_frame,
                               font=("Arial", 20),
                               width=20,
                               justify="center",
                               bg="#333",
                               fg="white",
                               insertbackground="white")
        guess_entry.pack(side="left", padx=10)
        guess_entry.bind("<Return>", on_enter_key)
        guess_entry.focus()

        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.place(relx=0.5, rely=0.83, anchor="n")
        tk.Button(btn_frame, text="SUBMIT GUESS",
                  font=("Arial", 16, "bold"),
                  width=15, height=2,
                  bg="#4CAF50", fg="white",
                  command=submit_guess).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🔄 NEW GAME",
                  font=("Arial", 16, "bold"),
                  width=15, height=2,
                  bg="cyan", fg="black",
                  command=new_game).pack(side="left", padx=10)

        # Back to hub button (bottom-left)
        bottom_frame = tk.Frame(self.root, bg="#1a1a1a")
        bottom_frame.place(relx=0.01, rely=0.93, anchor="w")
        tk.Button(bottom_frame, text="⬅ BACK TO HUB",
                  font=("Arial", 14, "bold"),
                  width=15, height=1,
                  bg="#666", fg="white",
                  command=self.back).pack()

        answer_label = tk.Label(self.root, text="",
                                font=("Arial", 24, "bold"),
                                fg="gray", bg="#1a1a1a")
        answer_label.place(relx=0.5, rely=0.9, anchor="n")

        new_game()

    def back(self):
        self.root.destroy()
        self.parent.deiconify()

# ======================= GAME 2: TIC TAC TOE =======================
class TicTacToeGame:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("Tic Tac Toe 🎊")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        # Fullscreen for Tic Tac Toe
        self.root.attributes("-fullscreen", True)

        player = "X"
        board = [" "] * 9
        score_x = 0
        score_o = 0
        confetti_items = []

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        def update_score():
            score_label.config(text=f"Score X: {score_x}   O: {score_o}")

        def reset_board():
            nonlocal board, player, confetti_items
            board = [" "] * 9
            player = "X"
            result_label.config(text="Match in Progress...", fg="black")
            confetti_canvas.delete("all")
            confetti_items.clear()
            for btn in buttons:
                btn.config(text=" ", state="normal", bg="#f0f0f0")

        def check_win(player):
            win_pos = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]
            ]
            return any(board[a] == board[b] == board[c] == player for a, b, c in win_pos)

        def create_falling_confetti():
            for _ in range(60):
                x = random.randint(0, screen_w)
                length = random.randint(12, 25)
                thickness = random.randint(2, 4)
                angle = random.choice([-6, -4, -2, 2, 4, 6])
                color = random.choice(["red", "blue", "yellow", "green", "purple", "orange", "pink"])
                item = confetti_canvas.create_polygon(
                    x, -10,
                    x + length, -10 + angle,
                    x + length - thickness, -10 + thickness + angle,
                    x - thickness, -10 + thickness,
                    fill=color, outline=color
                )
                confetti_items.append((item, random.uniform(3, 6)))

        def animate_confetti():
            for item, speed in confetti_items:
                confetti_canvas.move(item, 0, speed)
                coords = confetti_canvas.coords(item)
                if max(coords[1::2]) > screen_h + 20:
                    new_x = random.randint(0, screen_w)
                    confetti_canvas.move(item, -(coords[0] - new_x), -screen_h - 50)
            confetti_canvas.after(20, animate_confetti)

        def celebrate():
            create_falling_confetti()
            animate_confetti()

        def button_click(i):
            nonlocal player, score_x, score_o
            if board[i] == " ":
                board[i] = player
                buttons[i].config(text=player,
                                  bg="lightgreen" if player == "X" else "lightblue")
                if check_win(player):
                    result_label.config(text=f"🏆 Player {player} WINS! 🏆",
                                        fg="green" if player == "X" else "blue")
                    celebrate()
                    if player == "X":
                        score_x += 1
                    else:
                        score_o += 1
                    update_score()
                    for btn in buttons:
                        btn.config(state="disabled")
                    return
                if " " not in board:
                    result_label.config(text="😐 It's a DRAW!", fg="red")
                    return
                player = "O" if player == "X" else "X"
                result_label.config(text=f"Turn: {player}", fg="black")

        confetti_canvas = tk.Canvas(self.root,
                                    width=screen_w,
                                    height=screen_h,
                                    highlightthickness=0,
                                    bg="white")
        confetti_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        title_label = tk.Label(self.root, text="Tic Tac Toe",
                               font=("Helvetica", 40, "bold"),
                               bg="white")
        title_label.place(relx=0.5, rely=0.05, anchor="n")

        score_label = tk.Label(self.root,
                               text="Score X: 0   O: 0",
                               font=("Arial", 18, "bold"),
                               bg="white")
        score_label.place(relx=0.5, rely=0.14, anchor="n")

        result_label = tk.Label(self.root,
                                text="Match in Progress...",
                                font=("Arial", 22, "bold"),
                                bg="white")
        result_label.place(relx=0.5, rely=0.2, anchor="n")

        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.38, anchor="n")

        buttons = []
        for i in range(9):
            btn = tk.Button(frame, text=" ",
                            font=("Helvetica", 32, "bold"),
                            width=4, height=1,
                            bg="#f0f0f0",
                            command=lambda i=i: button_click(i))
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            buttons.append(btn)

        reset_button = tk.Button(self.root,
                                 text="Reset Game",
                                 font=("Arial", 18, "bold"),
                                 command=reset_board,
                                 bg="#ff9999")
        reset_button.place(relx=0.5, rely=0.78, anchor="n", width=200, height=50)


        # Back to hub button at bottom-left
        back_button = tk.Button(self.root,
                                text="⬅ BACK TO HUB",
                                font=("Arial", 16, "bold"),
                                bg="#666", fg="white",
                                command=self.back)
        back_button.place(relx=0.02, rely=0.93, anchor="w", width=200, height=45)

    def back(self):
        self.root.destroy()
        self.parent.deiconify()

# ======================= LAUNCH =======================
if __name__ == "__main__":
    GamesHub()

