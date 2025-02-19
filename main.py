import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whispering Woods")

# Load & Scale Background
background = pygame.image.load("background.png")
bg_width, bg_height = background.get_width() // 2, background.get_height() // 2
background = pygame.transform.scale(background, (bg_width, bg_height))

# Load & Scale Player
player = pygame.image.load("player-Photoroom.png")
player = pygame.transform.scale(player, (40, 50))

# Player & Game Variables
player_x, player_y = 100, 300
player_speed = 5
scroll_x = 0
wood_pieces = 0  # Tracks collected wood
carbon_collected = False  # Tracks if carbon has been obtained

# Tree and Bonfire Positions
trees = [(300, 250), (450, 220), (600, 270)]  # Adjust positions as needed
bonfire = (100, 320)  # Position of bonfire

# Questions for the quiz
quiz_questions = [
    ("What is the main component of wood?", "carbon"),
    ("What gas do trees absorb from the air?", "carbon dioxide"),
    ("Which element is known as the building block of life?", "carbon"),
    ("What do trees release during photosynthesis?", "oxygen")
]

# Function to Display Quiz
def ask_quiz():
    question, answer = random.choice(quiz_questions)
    font = pygame.font.Font(None, 24)
    input_text = ""
    asking = True

    while asking:
        screen.fill((0, 0, 0))
        screen.blit(background, (scroll_x, 0))

        # Render Question
        question_surface = font.render(question, True, (255, 255, 255))
        screen.blit(question_surface, (100, 100))

        # Render User Input
        input_surface = font.render(input_text, True, (255, 255, 0))
        screen.blit(input_surface, (100, 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Submit answer
                    if input_text.lower() == answer.lower():
                        return True
                    return False
                elif event.key == pygame.K_BACKSPACE:  # Remove last character
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Add character

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Keys
    keys = pygame.key.get_pressed()

    # Move Player & Scroll Background
    if keys[pygame.K_RIGHT]:
        if player_x < WIDTH // 2:
            player_x += player_speed
        elif scroll_x > WIDTH - bg_width:
            scroll_x -= player_speed

    if keys[pygame.K_LEFT]:
        if player_x > WIDTH // 4:
            player_x -= player_speed
        elif scroll_x < 0:
            scroll_x += player_speed

    if keys[pygame.K_DOWN] and player_y + player_speed < HEIGHT - player.get_height():
        player_y += player_speed
    if keys[pygame.K_UP] and player_y - player_speed > 0:
        player_y -= player_speed

    # Check if player reaches a tree
    for tree_x, tree_y in trees:
        if abs(player_x - tree_x) < 30 and abs(player_y - tree_y) < 30:  # Collision check
            if wood_pieces < 5:  # Only ask if they need wood
                correct = ask_quiz()
                if correct:
                    wood_pieces += 1
                break  # Prevent multiple quizzes at once

    # Check if player reaches bonfire
    if abs(player_x - bonfire[0]) < 30 and abs(player_y - bonfire[1]) < 30:
        if wood_pieces >= 5 and not carbon_collected:
            print("You burned the wood and collected Carbon!")
            carbon_collected = True  # Player now has carbon
            wood_pieces = 0  # Reset wood count

    # Draw Background & Player
    screen.blit(background, (scroll_x, 0))
    screen.blit(player, (player_x, player_y))

    # Display Wood Count
    font = pygame.font.Font(None, 24)
    wood_text = font.render(f"Wood: {wood_pieces}/5", True, (255, 255, 255))
    screen.blit(wood_text, (10, 10))

    pygame.display.update()

pygame.quit()
