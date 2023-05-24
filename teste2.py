import pygame
from pygame.locals import *

def start_game():
    player_x = 400
    player_y = 300
    player_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player_x -= player_speed
        if keys[K_RIGHT]:
            player_x += player_speed
        if keys[K_UP]:
            player_y -= player_speed
        if keys[K_DOWN]:
            player_y += player_speed

        screen.fill((0, 0, 0))  # Clear the screen
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(player_x, player_y, 50, 50))  # Draw the player rectangle

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()

def draw_menu():
    screen.fill((0, 0, 0))  # Clear the screen
    font = pygame.font.Font(None, 36)  # Create a font object
    for i, option in enumerate(menu_options):
        text = font.render(option, True, (255, 255, 255))  # Render the option text
        text_rect = text.get_rect(center=(400, 300 + i * 50))  # Position the text
        screen.blit(text, text_rect)  # Draw the text
        if i == selected_option:
            pygame.draw.circle(screen, (255, 255, 255), (380, 300 + i * 50), 8)  # Draw a circle indicator

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menu Example")
clock = pygame.time.Clock()

menu_options = ["Play", "Exit"]
selected_option = 0  # Index of the currently selected option

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_UP:
                selected_option = (selected_option - 1) % len(menu_options)  # Move up through the options
            elif event.key == K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)  # Move down through the options
            elif event.key == K_RETURN:
                if selected_option == 0:  # Play option selected
                    print("Starting the game...")
                    start_game()
                    # Add your game code here
                elif selected_option == 1:  # Exit option selected
                    print("Exiting the game...")
                    running = False

    draw_menu()
    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()

