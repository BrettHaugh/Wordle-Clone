import tkinter as tk
from tkinter import messagebox
import socket

class WordleClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")

        self.connection_established = False
        self.max_attempts = 6
        self.attempts = 0
        self.tiles = [[self.create_tile(row, col) for col in range(5)] for row in range(6)]
        
        self.guess_var = tk.StringVar()
        guess_entry = tk.Entry(master, textvariable=self.guess_var, font=('Helvetica', 18), width=10)
        guess_entry.bind('<Return>', self.send_guess)
        guess_entry.grid(row=7, column=0, columnspan=5)

        self.connect_to_server()

    def create_tile(self, row, col):
        frame = tk.Frame(self.master, width=60, height=60, highlightbackground='black', highlightthickness=1)
        frame.grid(row=row, column=col, padx=5, pady=5)
        label = tk.Label(frame, text="", bg='lightgray', font=('Helvetica', 18, 'bold'))
        label.pack(expand=True, fill='both')
        return label

    def send_guess(self, event=None):
        if not self.connection_established:
            messagebox.showerror("Error", "Not connected to the server.")
            return
        
        guess = self.guess_var.get().upper()
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showerror("Error", "Invalid guess. Please enter a 5 letter word.")
            return

        self.s.sendall((guess + "\n").encode())
        feedback = self.s.recv(1024).decode().strip()
        self.process_feedback(guess, feedback)
        self.guess_var.set("")

        if feedback == "GGGGG" or self.attempts >= self.max_attempts:
            self.end_game(feedback == "GGGGG")

    def process_feedback(self, guess, feedback):
        colors = {'G': 'green', 'Y': 'yellow', 'X': 'gray'}
        for i, char in enumerate(feedback):
            tile = self.tiles[self.attempts][i]
            tile.config(text=guess[i], bg=colors[char])
        self.attempts += 1

    def connect_to_server(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(('10.23.112.16', 1234))  # Replace with actual server IP and port
            self.connection_established = True
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Could not connect to the server.")

    def end_game(self, won):
        result_message = "Congratulations, you've won!" if won else "Sorry, you've lost."
        messagebox.showinfo("Game Over", result_message)
        self.s.close()
        self.master.quit()

def main():
    root = tk.Tk()
    gui = WordleClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
