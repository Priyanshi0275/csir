import pygame
import random

pygame.init()

# Screen Setup
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whispering Woods")

# Load & Scale Assets with Error Handling
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, size)
        print(f"Loaded: {path}")
        return img
    except pygame.error:
        print(f"Error loading: {path}")
        return None

background = load_image("upscaled_background.jpg", (WIDTH, HEIGHT))
player = load_image("player-Photoroom.png", (40, 50))
tree_img = load_image("tree_enhanced.png", (50, 70))
bonfire_img = load_image("bonfire_enhanced.png", (50, 50))
bonfire2_img = load_image("bonfire2_enhanced.png", (50, 50))

# Tree Positions - Randomly scattered within screen limits
trees = [(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(15)]

bonfire_x, bonfire_y = 350, 200

# Player Variables
player_x, player_y = 100, 300
player_speed = 5
wood_collected = 0
show_popup = False
near_tree = None
near_bonfire = False
burning = False
burning_start_time = None
game_over = False

# Font
font = pygame.font.Font(None, 24)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if show_popup and near_tree is not None:
                if event.key == pygame.K_c:
                    wood_collected += 1
                    trees.remove(near_tree)  # Remove tree after cutting
                    show_popup = False
                    near_tree = None
                elif event.key == pygame.K_i:
                    show_popup = False
            if near_bonfire and wood_collected >= 5 and event.key == pygame.K_c and not burning:
                wood_collected = 0
                burning = True
                burning_start_time = pygame.time.get_ticks()  # Start timer

    # Get Keys
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    # Player Movement - Restrict player within screen bounds
    if keys[pygame.K_RIGHT] and player_x + player_speed < WIDTH - player.get_width():
        new_x += player_speed
    if keys[pygame.K_LEFT] and player_x - player_speed > 0:
        new_x -= player_speed
    if keys[pygame.K_DOWN] and player_y + player_speed < HEIGHT - player.get_height():
        new_y += player_speed
    if keys[pygame.K_UP] and player_y - player_speed > 0:
        new_y -= player_speed

    # Collision Check with Trees
    near_tree = None
    for tree_x, tree_y in trees:
        if tree_x - 30 < new_x < tree_x + 40 and tree_y - 30 < new_y < tree_y + 40:
            near_tree = (tree_x, tree_y)
            show_popup = True
            break

    if near_tree is None or near_tree not in trees:
        player_x, player_y = new_x, new_y

    # Check if near Bonfire
    near_bonfire = abs(player_x - bonfire_x) < 30 and abs(player_y - bonfire_y) < 30

    # Handle Burning Timer
    if burning and burning_start_time:
        elapsed_time = pygame.time.get_ticks() - burning_start_time
        if elapsed_time > 5000:  # After 5 seconds
            burning = False
            game_over = True
            print("Yay!! Collected Carbon!")

    # Draw Everything
    if background:
        screen.blit(background, (0, 0))
    
    if player:
        screen.blit(player, (player_x, player_y))
    
    if bonfire_img and bonfire2_img:
        screen.blit(bonfire2_img if burning else bonfire_img, (bonfire_x, bonfire_y))
    
    if tree_img:
        for tree_x, tree_y in trees:
            screen.blit(tree_img, (tree_x, tree_y))

    # Popups for Cutting & Burning
    if show_popup and near_tree:
        popup_text = font.render("Press 'C' to Cut or 'I' to Ignore", True, (255, 255, 255))
        screen.blit(popup_text, (near_tree[0] - 50, near_tree[1] - 30))

    if near_bonfire and wood_collected >= 5:
        bonfire_text = font.render("Press 'C' to Burn Wood", True, (255, 255, 255))
        screen.blit(bonfire_text, (bonfire_x - 30, bonfire_y - 30))

    # Display wood collected
    wood_text = font.render(f"Wood Collected: {wood_collected}/5", True, (255, 255, 255))
    screen.blit(wood_text, (10, 10))

    # Game Over message
    if game_over:
        game_over_text = font.render("You Collected Carbon! Game Over.", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.update()
    clock.tick(30)  # Control game speed

pygame.quit()
