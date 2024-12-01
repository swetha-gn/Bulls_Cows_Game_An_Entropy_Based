import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import math
import itertools

# This class represents a Bulls and Cows game application using the Tkinter library for the GUI.
class BullsCowsGame:
    
    # The constructor initializes the main window and sets up the initial UI components.
    def __init__(self):
        # Create the main window for the application.
        self.root = tk.Tk()
        
        # Set the title of the window to "Bulls and Cows Game".
        self.root.title("Bulls and Cows Game")
        
        # Define the size of the window as 800x900 pixels.
        self.root.geometry("800x900")
        
        # Set the background color of the window to a light grey color.
        self.root.configure(bg='#f0f0f0')
        
        # Call a method to create mode selection UI elements.
        self._create_mode_selection()

    # This method creates and displays UI components for selecting game modes.
    def _create_mode_selection(self):
        # Create a label widget with the text "Bulls and Cows", styled with a specific font and background color.
        title_label = tk.Label(
            self.root,
            text="Bulls and Cows",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0'
        )
        
        # Pack (add) the label to the window with padding on the y-axis.
        title_label.pack(pady=20)

        # Create a frame widget to hold mode selection buttons, with a specified background color.
        mode_frame = tk.Frame(self.root, bg='#f0f0f0')
        
        # Pack (add) the frame to expand within its parent container.
        mode_frame.pack(expand=True)

        # Create a button for starting a game where the computer guesses the player's number.
        player_button = tk.Button(
            mode_frame,
            text="Computer Guesses Your Number",
            command=self._start_computer_guessing_mode,  # Set command to trigger when button is pressed.
            font=('Arial', 12),
            bg='#4CAF50',  # Button background color (green).
            fg='white',    # Button text color.
            width=25,
            height=2
        )
        
        # Pack (add) the button with padding on the y-axis.
        player_button.pack(pady=10)

        # Create another button for starting a game where the player guesses the computer's number.
        computer_button = tk.Button(
            mode_frame,
            text="You Guess Computer's Number",
            command=self._start_player_guessing_mode,  # Set command to trigger when button is pressed.
            font=('Arial', 12),
            bg='#2196F3',  # Button background color (blue).
            fg='white',    # Button text color.
            width=25,
            height=2
        )
        
        # Pack (add) this button with padding on the y-axis.
        computer_button.pack(pady=10)

    # This method clears all widgets from the main window, preparing it for new content.
    def _clear_window(self):
        # Iterate over all child widgets of the root window and destroy them.
        for widget in self.root.winfo_children():
            widget.destroy()

    # This method starts a game mode where the computer guesses the player's number.
    def _start_computer_guessing_mode(self):
        self._clear_window()  # Clear existing widgets from the window.
        
        # Initialize and display the ComputerGuessingMode interface (assumed to be defined elsewhere).
        ComputerGuessingMode(self.root)

    # This method starts a game mode where the player guesses the computer's number.
    def _start_player_guessing_mode(self):
        self._clear_window()  # Clear existing widgets from the window.

        # Initialize and display the PlayerGuessingMode interface (assumed to be defined elsewhere).
        PlayerGuessingMode(self.root)

    # This method runs the main event loop of Tkinter, keeping the application responsive.
    def run(self):
        self.root.mainloop()

# This class represents the game mode where the computer guesses the player's number
class ComputerGuessingMode:
    def __init__(self, master):
        self.master = master  # Store the parent window
        
        # Generate all possible 4-digit combinations with unique digits
        self.possible_combinations = [
            ''.join(combo) for combo in itertools.permutations('0123456789', 4)
            if len(set(combo)) == 4
        ]
        
        # Initialize the count of current possibilities
        self.current_possibilities = len(self.possible_combinations)
        
        self.guesses = []  # List to store previous guesses
        self._create_widgets()  # Create and set up UI components
        self._display_initial_stats()  # Display initial game statistics
        self._make_guess()  # Make the first guess

    # Method to create and set up all UI widgets
    def _create_widgets(self):
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self.master)
        notebook.pack(expand=True, fill=tk.BOTH)

        # Create and set up the Game tab
        game_frame = ttk.Frame(notebook)
        notebook.add(game_frame, text="Game")

        # Add instructions label
        tk.Label(
            game_frame,
            text="Think of a 4-digit number with unique digits",
            font=('Arial', 12)
        ).pack(pady=10)

        # Label to display computer's guess
        self.guess_label = tk.Label(
            game_frame,
            text="",
            font=('Arial', 16, 'bold')
        )
        self.guess_label.pack(pady=10)

        # Frame for input fields and submit button
        input_frame = tk.Frame(game_frame)
        input_frame.pack(pady=10)

        # Bulls input
        tk.Label(input_frame, text="Bulls:").pack(side=tk.LEFT)
        self.bulls_entry = tk.Entry(input_frame, width=5)
        self.bulls_entry.pack(side=tk.LEFT, padx=5)

        # Cows input
        tk.Label(input_frame, text="Cows:").pack(side=tk.LEFT)
        self.cows_entry = tk.Entry(input_frame, width=5)
        self.cows_entry.pack(side=tk.LEFT, padx=5)

        # Submit button
        tk.Button(
            input_frame,
            text="Submit",
            command=self._process_feedback,
            bg='#4CAF50',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)

        # Text area to display game progress
        self.game_text = scrolledtext.ScrolledText(
            game_frame,
            height=15,
            width=60,
            font=('Courier', 10)
        )
        self.game_text.pack(pady=10)

        # Frame for displaying statistics
        stats_frame = tk.Frame(game_frame)
        stats_frame.pack(pady=10)

        # Label to show number of possibilities
        self.possibilities_label = tk.Label(
            stats_frame,
            text=f"Possibilities: {self.current_possibilities}"
        )
        self.possibilities_label.pack(side=tk.LEFT, padx=10)

        # Label to show entropy
        self.entropy_label = tk.Label(
            stats_frame,
            text=f"Entropy: {self.calculate_entropy():.4f}"
        )
        self.entropy_label.pack(side=tk.LEFT, padx=10)

        # Create and set up the Possibilities tab
        possibilities_frame = ttk.Frame(notebook)
        notebook.add(possibilities_frame, text="Possibilities")

        # Text area to display all possible combinations
        self.possibilities_text = scrolledtext.ScrolledText(
            possibilities_frame,
            height=40,
            width=70,
            font=('Courier', 10)
        )
        self.possibilities_text.pack(expand=True, fill=tk.BOTH)

        self._update_possibilities_display()  # Update the possibilities display

    # Method to display initial game statistics
    def _display_initial_stats(self):
        initial_possibilities = len(self.possible_combinations)
        initial_entropy = self.calculate_entropy()
        self.game_text.insert(tk.END, f"Initial Possibilities: {initial_possibilities}\n")
        self.game_text.insert(tk.END, f"Initial Entropy: {initial_entropy:.4f}\n\n")
        self.game_text.see(tk.END)
        self.possibilities_label.config(text=f"Possibilities: {initial_possibilities}")
        self.entropy_label.config(text=f"Entropy: {initial_entropy:.4f}")

    # Method to update the display of possible combinations
    def _update_possibilities_display(self):
        self.possibilities_text.delete('1.0', tk.END)
        for i, combo in enumerate(self.possible_combinations, 1):
            self.possibilities_text.insert(tk.END, f"{combo} ")
            if i % 10 == 0:
                self.possibilities_text.insert(tk.END, "\n")

    # Method to calculate the entropy of the current game state
    def calculate_entropy(self):
        if self.current_possibilities == 0:
            return 0.001
        p = 1 / self.current_possibilities
        return max(0.001, -self.current_possibilities * (p * math.log2(p)))

    # Method to make a guess
    def _make_guess(self):
        if not self.possible_combinations:
            messagebox.showerror("Error", "No valid possibilities remain!")
            return
        self.current_guess = self.possible_combinations[0]
        self.guess_label.config(text=f"Computer's guess: {self.current_guess}")

    # Method to process player's feedback on the guess
    def _process_feedback(self):
        try:
            bulls = int(self.bulls_entry.get())
            cows = int(self.cows_entry.get())

            # Validate input
            if not (0 <= bulls <= 4 and 0 <= cows <= 4 and bulls + cows <= 4):
                messagebox.showerror("Error", "Invalid bulls/cows values!")
                return

            # Check if the guess is correct
            if bulls == 4:
                messagebox.showinfo("Success", "Computer found your number!")
                self.master.quit()
                return

            # Update possible combinations based on feedback
            self.possible_combinations = [
                combo for combo in self.possible_combinations
                if self._compare_numbers(self.current_guess, combo) == (bulls, cows)
            ]
            self.current_possibilities = len(self.possible_combinations)
            entropy = self.calculate_entropy()

            # Display result of the guess
            result_line = (
                f"Guess: {self.current_guess} | "
                f"Bulls: {bulls} | Cows: {cows} | "
                f"Possibilities: {self.current_possibilities} | "
                f"Entropy: {entropy:.4f}\n"
            )
            self.game_text.insert(tk.END, result_line)
            self.game_text.see(tk.END)

            # Update statistics display
            self.possibilities_label.config(text=f"Possibilities: {self.current_possibilities}")
            self.entropy_label.config(text=f"Entropy: {entropy:.4f}")

            # Clear input fields
            self.bulls_entry.delete(0, tk.END)
            self.cows_entry.delete(0, tk.END)

            # Update possibilities display and make next guess
            self._update_possibilities_display()
            self._make_guess()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    # Method to update possible combinations based on a guess and feedback
    def update_possibilities(self, guess, bulls, cows):
        new_possibilities = []
        for combo in self.possible_combinations:
            bulls_count, cows_count = self._compare_numbers(guess, combo)
            if bulls_count == bulls and cows_count == cows:
                new_possibilities.append(combo)
        
        self.possible_combinations = new_possibilities
        self.current_possibilities = len(self.possible_combinations)

    # Method to compare two numbers and return bulls and cows
    def _compare_numbers(self, guess, secret):
        bulls = sum(g == s for g, s in zip(guess, secret))
        cows = sum(min(guess.count(d), secret.count(d)) for d in set(guess)) - bulls
        return bulls, cows

# This class represents the game mode where the player guesses the computer's number
class PlayerGuessingMode:
    def __init__(self, master):
        self.master = master  # Store the parent window
        self.secret_number = self._generate_secret_number()  # Generate a secret number
        self.guesses = []  # List to store player's guesses
        
        # Generate all possible 4-digit combinations with unique digits
        self.possible_combinations = [
            ''.join(combo) for combo in itertools.permutations('0123456789', 4)
            if len(set(combo)) == 4
        ]
        
        # Initialize the count of current possibilities
        self.current_possibilities = len(self.possible_combinations)
        
        self._create_widgets()  # Create and set up UI components
        self._display_initial_stats()  # Display initial game statistics

    # Method to generate a random 4-digit secret number with unique digits
    def _generate_secret_number(self):
        digits = list('0123456789')
        random.shuffle(digits)
        return ''.join(digits[:4])

    # Method to create and set up all UI widgets
    def _create_widgets(self):
        # Add title label
        tk.Label(
            self.master,
            text="Guess the 4-digit number",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        ).pack(pady=10)

        # Create frame for input and submit button
        input_frame = tk.Frame(self.master, bg='#f0f0f0')
        input_frame.pack(pady=10)

        # Entry field for player's guess
        self.guess_entry = tk.Entry(
            input_frame,
            font=('Arial', 14),
            width=10
        )
        self.guess_entry.pack(side=tk.LEFT, padx=5)

        # Submit button
        tk.Button(
            input_frame,
            text="Submit Guess",
            command=self._process_guess,
            bg='#4CAF50',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)

        # Text area to display game results
        self.results_text = scrolledtext.ScrolledText(
            self.master,
            height=15,
            width=60,
            font=('Courier', 10)
        )
        self.results_text.pack(pady=10)

        # Frame for displaying statistics
        stats_frame = tk.Frame(self.master)
        stats_frame.pack(pady=10)

        # Label to show number of possibilities
        self.possibilities_label = tk.Label(
            stats_frame,
            text=f"Possibilities: {self.current_possibilities}"
        )
        self.possibilities_label.pack(side=tk.LEFT, padx=10)

        # Label to show entropy
        self.entropy_label = tk.Label(
            stats_frame,
            text=f"Entropy: {self.calculate_entropy():.4f}"
        )
        self.entropy_label.pack(side=tk.LEFT, padx=10)

        # Text area to display all possible combinations
        self.possibilities_text = scrolledtext.ScrolledText(
            self.master,
            height=10,
            width=60,
            font=('Courier', 10)
        )
        self.possibilities_text.pack(pady=10)

        # Button to reveal the answer
        tk.Button(
            self.master,
            text="Get Answer",
            command=self._show_answer,
            bg='#FF5722',
            fg='white'
        ).pack(pady=10)

        self._update_possibilities_display()  # Update the possibilities display

    # Method to display initial game statistics
    def _display_initial_stats(self):
        initial_possibilities = len(self.possible_combinations)
        initial_entropy = self.calculate_entropy()
        self.results_text.insert(tk.END, f"Initial Possibilities: {initial_possibilities}\n")
        self.results_text.insert(tk.END, f"Initial Entropy: {initial_entropy:.4f}\n\n")
        self.results_text.see(tk.END)
        self.possibilities_label.config(text=f"Possibilities: {initial_possibilities}")
        self.entropy_label.config(text=f"Entropy: {initial_entropy:.4f}")

    # Method to update the display of possible combinations
    def _update_possibilities_display(self):
        self.possibilities_text.delete('1.0', tk.END)
        for i, combo in enumerate(self.possible_combinations, 1):
            self.possibilities_text.insert(tk.END, f"{combo} ")
            if i % 10 == 0:
                self.possibilities_text.insert(tk.END, "\n")

    # Method to calculate the entropy of the current game state
    def calculate_entropy(self):
        if self.current_possibilities == 0:
            return 0.001
        p = 1 / self.current_possibilities
        return max(0.001, -self.current_possibilities * (p * math.log2(p)))

    # Method to process player's guess
    def _process_guess(self):
        guess = self.guess_entry.get().strip()
        if not (len(guess) == 4 and guess.isdigit() and len(set(guess)) == 4):
            messagebox.showerror("Error", "Enter 4 unique digits!")
            return

        bulls, cows = self._evaluate_guess(guess)
        self.update_possibilities(guess, bulls, cows)
        entropy = self.calculate_entropy()
        
        result = f"Guess: {guess} | Bulls: {bulls} | Cows: {cows} | "
        result += f"Possibilities: {self.current_possibilities} | Entropy: {entropy:.4f}\n"
        self.results_text.insert(tk.END, result)
        self.results_text.see(tk.END)
        self.guess_entry.delete(0, tk.END)

        self.possibilities_label.config(text=f"Possibilities: {self.current_possibilities}")
        self.entropy_label.config(text=f"Entropy: {entropy:.4f}")
        self._update_possibilities_display()

        if bulls == 4:
            messagebox.showinfo("Congratulations!", "You found the number!")
            self.master.quit()

    # Method to evaluate the player's guess
    def _evaluate_guess(self, guess):
        return self._compare_numbers(guess, self.secret_number)

    # Method to update possible combinations based on a guess and feedback
    def update_possibilities(self, guess, bulls, cows):
        new_possibilities = []
        for combo in self.possible_combinations:
            bulls_count, cows_count = self._compare_numbers(guess, combo)
            if bulls_count == bulls and cows_count == cows:
                new_possibilities.append(combo)
        
        self.possible_combinations = new_possibilities
        self.current_possibilities = len(self.possible_combinations)

    # Method to compare two numbers and return bulls and cows
    def _compare_numbers(self, guess, secret):
        bulls = sum(g == s for g, s in zip(guess, secret))
        cows = sum(min(guess.count(d), secret.count(d)) for d in set(guess)) - bulls
        return bulls, cows

    # Method to reveal the secret number
    def _show_answer(self):
        messagebox.showinfo("Answer", f"The secret number is: {self.secret_number}")

# Main function to start the game
def main():
    game = BullsCowsGame()
    game.run()

# Entry point of the program
if __name__ == "__main__":
    main()