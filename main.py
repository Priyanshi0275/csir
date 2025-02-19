import pygame

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lake Exploration - Collect Elements")

# Load Images
background = pygame.image.load("backgroundl.png")  # Ensure the image is in the same directory
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player = pygame.image.load("player.png")  # Placeholder for player sprite
player = pygame.transform.scale(player, (50, 50))

electrolysis_device = pygame.image.load("electrolysis.png")
electrolysis_device = pygame.transform.scale(electrolysis_device, (80, 80))

# Player Variables
player_x, player_y = 100, 350
player_speed = 1
collecting = False

# Font Setup
font = pygame.font.Font(None, 36)
popup_text = ""
show_popup = False

# Game Loop
running = True
while running:
    screen.blit(background, (0, 0))  # Draw background
    screen.blit(player, (player_x, player_y))  # Draw player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
        player_y += player_speed
    if keys[pygame.K_UP] and player_y > 300:  # Limit movement on grass
        player_y -= player_speed
    
    # Check if Player Reaches the Lake
    if 300 < player_x < 500 and player_y > 320:  # Assuming lake is in this range
        screen.blit(electrolysis_device, (350, 250))
        popup_text = "Press SPACE to Collect H & O"
        show_popup = True
        if keys[pygame.K_SPACE]:
            collecting = True

    # Display Popup
    if show_popup:
        text_surface = font.render(popup_text, True, (255, 255, 255))
        screen.blit(text_surface, (250, 50))
    
    # Show Collection Message
    if collecting:
        pygame.draw.rect(screen, (0, 0, 0), (230, 100, 400, 200))  # Popup box
        collection_text = font.render("Collected Hydrogen & Oxygen!", True, (255, 255, 255))
        screen.blit(collection_text, (250, 150))
        button_text = font.render("Press ENTER to Continue", True, (255, 255, 255))
        screen.blit(button_text, (250, 200))
        if keys[pygame.K_RETURN]:
            collecting = False
            show_popup = False

    pygame.display.update()

pygame.quit()