import pygame

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountain Forge - Iron Discovery")

# Load Images
background = pygame.image.load("mountain_forge.png")
iron_tool = pygame.image.load("iron_weapon.png")
blacksmith = pygame.image.load("blacksmith.png")
player = pygame.image.load("player-Photoroom.png")

# Scale Images
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player = pygame.transform.scale(player, (50, 50))
blacksmith = pygame.transform.scale(blacksmith, (60, 80))
iron_tool = pygame.transform.scale(iron_tool, (40, 40))

# Player Setup
player_x, player_y = 20,10
player_speed = 1

# Tool Collection
tools = [(200, 200), (400, 100), (500, 300), (150, 250), (350, 350)]
collected_tools = 0

game_over = False
font = pygame.font.Font(None, 50)

# Game Loop
running = True
while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed

    # Draw Iron Tools
    for tool in tools[:]:
        screen.blit(iron_tool, tool)
        if pygame.Rect(player_x, player_y, 50, 50).colliderect(pygame.Rect(tool[0], tool[1], 40, 40)):
            tools.remove(tool)
            collected_tools += 1

    # Draw Blacksmith
    screen.blit(blacksmith, (600, 250))
    
    # Check if player delivers tools
    if collected_tools == 5 and pygame.Rect(player_x, player_y, 50, 50).colliderect(pygame.Rect(600, 250, 60, 80)):
        game_over = True
    
    # Draw Player
    screen.blit(player, (player_x, player_y))
    
    # Display End Message
    if game_over:
        text = font.render("IRON HAS BEEN DISCOVERED!", True, (255, 255, 0))
        screen.blit(text, (150, 180))
    
    pygame.display.update()

pygame.quit()
