import pygame

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whispering Woods")

# Load & Scale Background
background = pygame.image.load("background.png")
bg_width, bg_height = background.get_width() // 2, background.get_height() // 2  # Scale Down
background = pygame.transform.scale(background, (bg_width, bg_height))

# Load & Scale Player
player = pygame.image.load("player-Photoroom.png")  # Replace with your sprite
player = pygame.transform.scale(player, (70, 50))  # Adjust size if needed

# Player & Camera Variables
player_x, player_y = 100, 300  # Player's Position
player_speed = 5
scroll_x = 0  # Background scroll position

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Keys
    keys = pygame.key.get_pressed()

    # Move Player & Scroll Background
    if keys[pygame.K_RIGHT]:
        if player_x < WIDTH // 2:  # Move player until center
            player_x += player_speed
        elif scroll_x > WIDTH - bg_width:  # Scroll background
            scroll_x -= player_speed

    if keys[pygame.K_LEFT]:
        if player_x > WIDTH // 4:  # Move player until left side
            player_x -= player_speed
        elif scroll_x < 0:  # Scroll background left
            scroll_x += player_speed

    if keys[pygame.K_DOWN] and player_y + player_speed < HEIGHT - player.get_height():
        player_y += player_speed
    if keys[pygame.K_UP] and player_y - player_speed > 0:
        player_y -= player_speed

    # Draw Background & Player
    screen.blit(background, (scroll_x, 0))
    screen.blit(player, (player_x, player_y))

    pygame.display.update()

pygame.quit()



