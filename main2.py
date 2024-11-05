import pygame
import random

# Initialize Pygame and Pygame mixer for sound
pygame.init()
pygame.mixer.init()

# Constants for initial screen size
INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600

# Set up display for full screen support
screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Immune System Game")

# Load images
background_image = pygame.image.load('assets/images/background.png').convert_alpha()
background_image = pygame.transform.scale(background_image, (INITIAL_SCREEN_WIDTH - 100, INITIAL_SCREEN_HEIGHT - 250))  # Scale background image

tcell_image = pygame.image.load('assets/images/tcell.png').convert_alpha()
tcell_image = pygame.transform.scale(tcell_image, (30, 30))  # Adjusted size for T-cell

bacteria_image = pygame.image.load('assets/images/bacteria.png').convert_alpha()
bacteria_image = pygame.transform.scale(bacteria_image, (20, 20))  # Adjusted size for bacteria

virus_image = pygame.image.load('assets/images/virus.png').convert_alpha()
virus_image = pygame.transform.scale(virus_image, (20, 20))  # Adjusted size for virus

wbcell_image = pygame.image.load('assets/images/wbcell.png').convert_alpha()
wbcell_image = pygame.transform.scale(wbcell_image, (25, 25))  # Adjusted size for white blood cell

# Load and play background music
pygame.mixer.music.load('assets/sounds/komiku.mp3')
pygame.mixer.music.play(-1)  # Loop the music

# Fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 50)

# Game variables
PADDING = 50  # Padding for the game space
HEADER_HEIGHT = 100  # Height for the header area (Div 1)
MARGIN = 30  # Margin between Divs
RESTART_BUTTON_HEIGHT = 60  # Height for the restart button area (Div 3)

# Player and game state variables
player_pos = [INITIAL_SCREEN_WIDTH // 2, INITIAL_SCREEN_HEIGHT // 2]
score = 0
timer = 60
game_over = False
play_game = False
pathogens = []
wb_cells = []

# Clock to control frame rate
clock = pygame.time.Clock()

# Functions
def spawn_pathogen():
    x = random.randint(PADDING + 50, INITIAL_SCREEN_WIDTH - PADDING - 20 - 50)
    y = random.randint(HEADER_HEIGHT + PADDING + 50, INITIAL_SCREEN_HEIGHT - RESTART_BUTTON_HEIGHT - PADDING - 200)
    pathogen_type = random.choice(["bacteria", "virus"])
    pathogens.append({"x": x, "y": y, "type": pathogen_type})

def spawn_wbcell():
    x = random.randint(PADDING + 50, INITIAL_SCREEN_WIDTH - PADDING - 25 - 50)
    y = random.randint(HEADER_HEIGHT + PADDING + 50, INITIAL_SCREEN_HEIGHT - RESTART_BUTTON_HEIGHT - PADDING - 200)
    wb_cells.append({"x": x, "y": y})

def move_player(keys):
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    player_pos[0] = max(PADDING + 50, min(player_pos[0], INITIAL_SCREEN_WIDTH - PADDING - 30 - 50))
    player_pos[1] = max(HEADER_HEIGHT + PADDING + 50, min(player_pos[1], INITIAL_SCREEN_HEIGHT - RESTART_BUTTON_HEIGHT - PADDING - MARGIN - 30))

def draw_player():
    screen.blit(tcell_image, (player_pos[0], player_pos[1]))

def draw_pathogens():
    for pathogen in pathogens:
        if pathogen["type"] == "bacteria":
            screen.blit(bacteria_image, (pathogen["x"], pathogen["y"]))
        else:
            screen.blit(virus_image, (pathogen["x"], pathogen["y"]))

def draw_wbcells():
    for wb in wb_cells:
        screen.blit(wbcell_image, (wb["x"], wb["y"]))

def display_score_and_timer():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    timer_text = font.render(f"Time: {timer // 60}:{timer % 60:02}", True, (0, 0, 0))
    screen.blit(score_text, (PADDING + 50, PADDING + 30))
    screen.blit(timer_text, (INITIAL_SCREEN_WIDTH - PADDING - 150, PADDING + 30))

def show_title():
    title_text = title_font.render("Immune System Game", True, (0, 0, 0))
    instructions_text = font.render("Control the T-cell with arrow keys!", True, (0, 0, 0))
    screen.blit(title_text, (INITIAL_SCREEN_WIDTH // 2 - title_text.get_width() // 2, PADDING))
    screen.blit(instructions_text, (INITIAL_SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, PADDING + 40))

def update_timer():
    global timer, game_over
    if not game_over:  # Only update the timer if the game is not over
        timer -= 1
        if timer <= 0:
            game_over = True

def reset_game():
    global player_pos, score, timer, game_over, pathogens, wb_cells, play_game
    player_pos = [INITIAL_SCREEN_WIDTH // 2, INITIAL_SCREEN_HEIGHT // 2]
    score = 0
    timer = 60
    game_over = False
    play_game = True
    pathogens.clear()
    wb_cells.clear()

def check_collisions():
    global score
    for pathogen in pathogens[:]:
        if (player_pos[0] < pathogen["x"] + 20 and
            player_pos[0] + 30 > pathogen["x"] and
            player_pos[1] < pathogen["y"] + 20 and
            player_pos[1] + 30 > pathogen["y"]):
            score += 10
            pathogens.remove(pathogen)

def main():
    global INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, screen, background_image, player_pos, score, timer, game_over, pathogens, wb_cells, play_game

    reset_game()
    timer_event = pygame.USEREVENT + 1
    spawn_event = pygame.USEREVENT + 2

    pygame.time.set_timer(timer_event, 1000)
    pygame.time.set_timer(spawn_event, random.randint(300, 700))

    play_button = pygame.Rect(INITIAL_SCREEN_WIDTH // 2 - 100, INITIAL_SCREEN_HEIGHT // 2 - 50, 200, 50)
    restart_button = pygame.Rect(INITIAL_SCREEN_WIDTH // 2 - 75, INITIAL_SCREEN_HEIGHT - RESTART_BUTTON_HEIGHT - PADDING - MARGIN, 150, 50)

    while True:
        screen.fill((255, 255, 255))

        show_title()
        display_score_and_timer()

        if play_game:
            bg_x = (INITIAL_SCREEN_WIDTH - background_image.get_width()) // 2
            bg_y = HEADER_HEIGHT + PADDING + MARGIN
            screen.blit(background_image, (bg_x, bg_y))

            draw_pathogens()
            draw_wbcells()
            draw_player()
        else:
            # Draw the Play button
            pygame.draw.rect(screen, (0, 0, 0), play_button)
            play_text = font.render("Play", True, (255, 255, 255))
            screen.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) // 2,
                                     play_button.y + (play_button.height - play_text.get_height()) // 2))

        if game_over:
            pygame.draw.rect(screen, (0, 0, 0), restart_button)
            restart_text = font.render("Restart", True, (255, 255, 255))
            screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                                        restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
            game_over_text = font.render("Game Over! Press Restart to play again.", True, (255, 0, 0))
            screen.blit(game_over_text, (INITIAL_SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, INITIAL_SCREEN_HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.VIDEORESIZE:
                INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (INITIAL_SCREEN_WIDTH - 100, INITIAL_SCREEN_HEIGHT - 250))
                play_button.x = INITIAL_SCREEN_WIDTH // 2 - 100
                play_button.y = INITIAL_SCREEN_HEIGHT // 2 - 50
                restart_button.x = INITIAL_SCREEN_WIDTH // 2 - 75
                restart_button.y = INITIAL_SCREEN_HEIGHT - RESTART_BUTTON_HEIGHT - PADDING - MARGIN

            if event.type == timer_event:
                update_timer()
            if event.type == spawn_event and play_game:
                if random.random() < 0.5:
                    spawn_pathogen()
                else:
                    spawn_wbcell()
                pygame.time.set_timer(spawn_event, random.randint(300, 700))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and restart_button.collidepoint(event.pos):
                    reset_game()
                if not play_game and play_button.collidepoint(event.pos):
                    reset_game()  # Reset game to initialize variables
                    play_game = True  # Start the game when the play button is clicked

        if play_game:
            keys = pygame.key.get_pressed()
            move_player(keys)
            check_collisions()

        if game_over:
            play_game = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
