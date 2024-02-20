import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Typing Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables

max_meteors = 5


# Falling speed of the meteors
falling_speed = 0.1

# Delay between meteor generation (in milliseconds)
meteor_generation_delay = 1500

# Timer for meteor generation delay
meteor_generation_timer = pygame.time.get_ticks()

# Game states
MAIN_MENU = "main_menu"
GAME_PLAY = "game_play"
GAME_OVER = "game_over"
PAUSE = "pause"  # New state for pause

# Initial game state
current_state = MAIN_MENU

# Function to generate a random word
def generate_word():
    word_list = ["meteor", "space", "ship", "python", "coding", "challenge", "pygame", "keyboard"]
    return random.choice(word_list)

# Function to reset game variables
def reset_game():
    global player_word, player_score, player_health, meteors,max_meteors
    player_word = ""
    player_score = 0
    player_health = 10
    meteors = []
    max_meteors = 4
  # Add this line to declare the 'paused' variable
paused = False
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if current_state == MAIN_MENU:
                if event.key == pygame.K_RETURN:
                    current_state = GAME_PLAY
                    reset_game()
            elif current_state == GAME_PLAY:
                if event.key == pygame.K_ESCAPE:
                    current_state = PAUSE
                elif event.key == pygame.K_SPACE and not paused:
                    for meteor in meteors:
                        if player_word == meteor['word']:
                            player_score += 1
                            meteors.remove(meteor)
                            player_word = ""
                            break
                elif event.key == pygame.K_BACKSPACE and not paused:
                    player_word = player_word[:-1]
                elif not paused:
                    player_word += event.unicode
            elif current_state == PAUSE:
                if event.key == pygame.K_RETURN:
                    current_state = MAIN_MENU
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    screen.fill(black)  # Black background

    if current_state == MAIN_MENU:
        # Display main menu text
        menu_text = font.render("Press Enter to Start", True, white)  # White text for main menu
        screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 - menu_text.get_height() // 2))
        pygame.quit()
        sys.exit()
    elif current_state == GAME_PLAY:
        # Game play logic
        if not paused:
            # Generate meteors with delay
            current_time = pygame.time.get_ticks()
            if len(meteors) < max_meteors and current_time - meteor_generation_timer > meteor_generation_delay:
                meteor_word = generate_word()
                meteor = {
                    'word': meteor_word,
                    'x': random.randint(0, width - 50),
                    'y': 0
                }
                meteors.append(meteor)
                meteor_generation_timer = current_time  # Reset the timer

            # Update meteors
            for meteor in meteors:
                meteor['y'] += falling_speed
                meteor_text = font.render(meteor['word'], True, white)  # White text for meteors
                screen.blit(meteor_text, (meteor['x'], meteor['y']))

                if meteor['y'] > height:
                    player_health -= 1
                    meteors.remove(meteor)

            # Display player's word
            player_word_text = font.render(player_word, True, white)  # White text for player's word
            screen.blit(player_word_text, (width // 2 - player_word_text.get_width() // 2, height - 50))

            # Display score
            score_text = font.render("Score: {}".format(player_score), True, white)  # White text for score
            screen.blit(score_text, (10, 10))

            # Display health
            health_text = font.render("Health: {}".format(player_health), True, white)  # White text for health
            screen.blit(health_text, (width - 150, 10))

            # Check for game over condition
            if player_health <= 0:
                current_state = GAME_OVER
    
    elif current_state == PAUSE:
        # Display pause screen
        pause_text = font.render("Game Paused", True, white)  # White text for pause screen
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

        # Display options
        option_text = font.render("Press Enter to go to Main Menu or Esc to Exit", True, white)
        screen.blit(option_text, (width // 2 - option_text.get_width() // 2, height // 2 + 50))
        

    pygame.display.flip()
    pygame.time.delay(10)  # Small delay to avoid high CPU usage
