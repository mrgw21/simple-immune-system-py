import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame

class ImmuneSystemGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Immune Systems Game")

        # Load the background image to get its dimensions
        try:
            self.background_image = tk.PhotoImage(file="assets/images/background.png").subsample(1, 1)  # Use original size
            self.canvas_width = self.background_image.width()
            self.canvas_height = self.background_image.height()
        except tk.TclError:
            print("Error: Background image not found or could not be loaded.")
            self.canvas_width, self.canvas_height = 1200, 800  # Fallback dimensions

        # Set geometry of the window with padding
        self.root.geometry(f"{self.canvas_width + 100}x{self.canvas_height + 200}")

        # Initialize Pygame mixer for sound
        pygame.mixer.init()
        music_file = "assets/sounds/komiku.mp3"
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop music indefinitely
        else:
            print("Music file not found:", music_file)

        # Game state variables
        self.score = 0
        self.time_remaining = 60  # Set game to 1 minute
        self.is_game_running = False
        self.tcell_speed = 10  # Speed of T cell movement

        # Create a frame for the title, score, timer, and play button
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)

        # Title, score, and timer above the canvas
        tk.Label(self.info_frame, text="Simple Immune Systems Game", font=("Arial", 24)).pack(pady=(10, 0))
        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=(5, 0))
        self.timer_label = tk.Label(self.info_frame, text=f"Time: {self.time_remaining}", font=("Arial", 16))
        self.timer_label.pack(pady=(5, 10))

        # Create a play button
        self.play_button = tk.Button(self.info_frame, text="Play", command=self.toggle_game, font=("Arial", 16))
        self.play_button.pack(pady=(10, 10))  # Padding for the button

        # Create a canvas with padding
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(expand=True, padx=25, pady=(0, 25))  # Add padding horizontally and from the bottom

        # Center the background image on the canvas
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.background_image)

        # Load images with error handling
        try:
            self.tcell_image = tk.PhotoImage(file="assets/images/tcell.png").subsample(3, 3)
        except tk.TclError:
            print("Error: T cell image not found or could not be loaded.")

        try:
            self.bacteria_image = tk.PhotoImage(file="assets/images/bacteria.png").subsample(4, 4)
            self.virus_image = tk.PhotoImage(file="assets/images/virus.png").subsample(4, 4)
        except tk.TclError:
            print("Error: Pathogen images not found or could not be loaded.")

        # Player-controlled T cell starting in the center
        self.tcell = self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.tcell_image)

        # Movement bindings
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)

        # Variables to track pathogens and movement
        self.pathogens = []
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def toggle_game(self):
        if not self.is_game_running:
            self.start_game()
        else:
            self.restart_game()

    def start_game(self):
        self.is_game_running = True
        self.score = 0
        self.time_remaining = 60
        self.update_score()
        self.update_timer()
        self.play_button.config(text="Restart")  # Change the button text
        self.run_game_loop()
        self.spawn_pathogens()  # Start spawning pathogens

    def restart_game(self):
        self.is_game_running = False
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.background_image)  # Reset the background
        self.play_button.config(text="Play")  # Change the button back to Play
        self.pathogens.clear()  # Clear pathogens
        self.start_game()  # Restart the game logic

    def spawn_pathogens(self):
        """Spawn pathogens at a slower rate."""
        if not self.is_game_running:
            return

        x = random.randint(100, 900)
        y = random.randint(100, 600)
        image = random.choice([self.bacteria_image, self.virus_image])
        pathogen = self.canvas.create_image(x, y, image=image)
        self.pathogens.append(pathogen)

        # Schedule the next pathogen spawn (every 2000ms for a slower spawn rate)
        self.root.after(2000, self.spawn_pathogens)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Time: {self.time_remaining}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def run_game_loop(self):
        if not self.is_game_running:
            return
        self.check_collisions()
        self.update_movement()  # Call to update movement here
        self.root.after(50, self.run_game_loop)

    def check_collisions(self):
        tcell_coords = self.canvas.coords(self.tcell)
        for pathogen in self.pathogens[:]:
            if self.is_collision(tcell_coords, self.canvas.coords(pathogen)):
                self.pathogens.remove(pathogen)
                self.canvas.delete(pathogen)
                self.score += 10
                self.update_score()

    def is_collision(self, coords1, coords2):
        x1, y1 = coords1
        x2, y2 = coords2
        return abs(x1 - x2) < 30 and abs(y1 - y2) < 30

    def end_game(self):
        self.is_game_running = False
        pygame.mixer.music.stop()  # Stop music when game ends
        messagebox.showinfo("Game Over", f"Time's up! Your score: {self.score}")

    def key_down(self, event):
        if not self.is_game_running:
            return

        if event.keysym == "Up":
            self.moving_up = True
        elif event.keysym == "Down":
            self.moving_down = True
        elif event.keysym == "Left":
            self.moving_left = True
        elif event.keysym == "Right":
            self.moving_right = True

    def key_up(self, event):
        if event.keysym == "Up":
            self.moving_up = False
        elif event.keysym == "Down":
            self.moving_down = False
        elif event.keysym == "Left":
            self.moving_left = False
        elif event.keysym == "Right":
            self.moving_right = False

    def update_movement(self):
        if not self.is_game_running:
            return

        x, y = self.canvas.coords(self.tcell)
        if self.moving_up and y > 30:
            self.canvas.move(self.tcell, 0, -self.tcell_speed)
        if self.moving_down and y < self.canvas_height - 30:  # Adjusted for bottom boundary
            self.canvas.move(self.tcell, 0, self.tcell_speed)
        if self.moving_left and x > 30:
            self.canvas.move(self.tcell, -self.tcell_speed, 0)
        if self.moving_right and x < self.canvas_width - 30:  # Adjusted for right boundary
            self.canvas.move(self.tcell, self.tcell_speed, 0)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ImmuneSystemGame(root)
    root.mainloop()