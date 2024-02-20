import pygame
import sys
import random
import csv

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Typing")


icon = pygame.image.load("assets/ship.png")  # Replace with the actual path to your icon
pygame.display.set_icon(icon)

# Load assets
background_image = pygame.image.load("assets/bg.png")  # Replace with your actual background image
spaceship_image = pygame.image.load("assets/ship.png")
meteor_image = pygame.image.load("assets/meteor.png")

# Fonts
font = pygame.font.Font(None, 36)

# Load words from CSV
word_database = []

with open("assets/word.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        word_database.extend(row)

# Function to draw text on the screen
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)

def generate_random_word():
    return random.choice(word_database)
# Constants
DEADZONE_LINE = HEIGHT - 20  # Adjust the value as needed
player_health = 5

# Class to represent a falling word
class FallingWord:
    def __init__(self, existing_words):
        self.word = generate_random_word()
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, the position will be adjusted
        self.rect.midtop = (random.randint(50, WIDTH - 50), 0)  # Adjusted the range
    
    
        # Ensure the new word doesn't overlap with existing words
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, WIDTH - 50), 0)  # Update the position

        self.speed = random.uniform(0.5,0.5)
       

    def update(self, player_health):
        self.rect.y += self.speed

        # Check if the falling word has passed the deadzone line
        if self.rect.y > HEIGHT:
            player_health -= 1
            return True  # Signal that the word should be removed

        return False  # Signal that the word should not be removed

    def draw(self, typing_word):
        # Center the text on the meteor image
        text_surface = font.render(self.word, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        #letter_surface = font.render(self.word,True,WHITE)
        #letter_rect = letter_surface.get_rect(center=self.rect.center)
        # Draw meteor image with the correct dimensions
        meteor_rect = meteor_image.get_rect(center=self.rect.midtop)
        screen.blit(meteor_image, meteor_rect.topleft)
        screen.blit(text_surface, text_rect)
        
    def draw(self, player_word):
        # Center the text on the meteor image
        text_surface = font.render(self.word, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw meteor image with the correct dimensions
        meteor_rect = meteor_image.get_rect(center=self.rect.midtop)
        screen.blit(meteor_image, meteor_rect.topleft)

        # Calculate the total width of the characters
        total_width = sum(font.size(char)[0] for char in self.word)

        # Initial x-coordinate for the first character
        x_offset = self.rect.centerx - total_width / 2
        # Move the word up a little bit
        y_offset = self.rect.centery - 5
        
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            char_color = WHITE
            if i < len(player_word) and char == player_word[i]:
                char_color = (0,230,255)  # Change this to the color you want for correct letters
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]

        # Draw text on top of meteor
        #screen.blit(text_surface, text_rect)

class LaserBeam:
    def __init__(self, x, y,target_word):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = -5  # Adjust the speed as needed
        self.target_word = target_word
        self.initial_x = x
    def update(self):
        self.rect.y += self.speed

         # Move the beam towards the x-coordinate of the center of the target word
        target_x = self.target_word.rect.centerx
        if self.rect.x < target_x:
            self.rect.x += 1
        elif self.rect.x > target_x:
            self.rect.x -= 1

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        
# Class to represent the player's spaceship
class Spaceship:
    def __init__(self):
        self.image = spaceship_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.laser_beams = []
    
    def draw(self):
        screen.blit(self.image, self.rect)
    
    
# Main Menu Loop
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))

        draw_text("Space Typing", pygame.font.Font(None,60), WHITE, WIDTH // 2, HEIGHT // 2 - 100, blink=True)

        # Start Button
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
        draw_text("Enter to Start", font, BLACK, WIDTH // 2, HEIGHT // 2 + 25)

        # Exit Button
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50))
        draw_text("Esc to Exit", font, BLACK, WIDTH // 2, HEIGHT // 2 + 125)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "Start"  # Start Button pressed
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Gameplay Loop
def gameplay(player_health):
    player_score = 0
    clock = pygame.time.Clock()
    falling_words = []
    spaceship = Spaceship()
    player_word = ""
    

    running = True

    while running and player_health > 0:
        screen.blit(background_image, (0, 0))

        
        # Display the falling word for the player to type
        if len(falling_words) < 3 and random.randint(0, 100) < 2:
            falling_words.append(FallingWord(falling_words))

        # Display the input word
        draw_text(player_word, font, WHITE, WIDTH // 2, HEIGHT - 100)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player_health = 0  # Set health to 0 to exit the loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player_health = 0  # Set health to 0 to exit the loop
                elif event.key == pygame.K_SPACE:
                    # Check if the typed word matches any falling word
                    correct_word = None
                    for word in falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break

                    if correct_word:
                        word_length = len(correct_word.word)
                        player_score += word_length * 100
                        falling_words.remove(correct_word)
                        player_word = ""  # Clear the input word immediately
                        
                    else:
                        # If the typed word doesn't match any falling word, mark it as incorrect
                        #incorrect_word = player_word
                        player_word = ""  # Clear the input word immediately

                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]  # Remove the last character from the input word
                else:
                    player_word += event.unicode

        # Update and draw falling words
        for word in falling_words:
            if word.update(player_health):  # Pass player_health as an argument
                falling_words.remove(word)
            else:
                word.draw(player_word)

        # Check for collision with the spaceship
        for word in falling_words:
            if word.rect.y >= spaceship.rect.top and word.rect.y <= spaceship.rect.bottom and \
                    word.rect.x >= spaceship.rect.left and word.rect.x <= spaceship.rect.right:
                if player_word == word.word:
                    player_score += 200
                    falling_words.remove(word)
                    player_word = ""
                    spaceship.shoot_laser(word.word) 
                    break
                else:
                    # If the spaceship collides with an incorrect word, handle it accordingly
                    player_health -= 1
                    falling_words.remove(word)
                    player_word = ""  # Clear the input word immediately

        # Check for words that have passed the deadzone line
        for word in falling_words:
            if word.rect.y > DEADZONE_LINE:
                if player_word == word.word:
                    player_score += 200
                else:
                    # If an incorrect word passes the deadzone line, handle it accordingly
                    player_health -= 1
                falling_words.remove(word)
        
        
        # Display player score and health
        draw_text(f"Score : {player_score}", font, WHITE, 80, 20)  # Top left
        draw_text(f"Health : {player_health}", font, WHITE, WIDTH - 80, 20)  # Top right

        # Display the spaceship
        spaceship.draw()
        
        # Remove words that have fallen off the screen
        falling_words = [word for word in falling_words if word.rect.y < HEIGHT]
        pygame.display.flip()
        clock.tick(FPS)
    # Game Over message
    screen.blit(background_image, (0, 0))
    draw_text("Game Over", pygame.font.Font(None,60), WHITE, WIDTH // 2, HEIGHT // 3)
    draw_text(f"Total Score : {player_score}",font,WHITE,WIDTH // 2 , HEIGHT // 2.15)
    draw_text("Enter to Main Menu", font, WHITE, WIDTH // 2, HEIGHT // 1.75)
    
    pygame.display.flip()

    # Wait for the player to press Enter to return to the main menu
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False
        pygame.display.flip()
        clock.tick(FPS)
    
    #pygame.quit()
    #sys.exit()

    # Run the main menu
    return main_menu()

# Run the gameplay loop only if the player selects "Start"
menu_option = main_menu()

while menu_option == "Start":
    menu_option = gameplay(player_health)