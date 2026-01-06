import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display (initial size)
screen = pygame.display.set_mode((600, 500), pygame.RESIZABLE)
pygame.display.set_caption('Text Input Example')

# Define font and color
font = pygame.font.Font(r"C:\Windows\Fonts\times.ttf", 36)
text_color = (255, 255, 255)  # White
input_box_color = (50, 50, 50)  # Dark grey
active_color = (0, 255, 0)  # Green (for active input)

# Initialize variables
input_text = ""
active = False  # If the text box is active
input_box = pygame.Rect(100, 150, 400, 40)  # Rectangle for the input box

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw the input box
    pygame.draw.rect(screen, active_color if active else input_box_color, input_box, 2)
    
    # Render the current text
    text_surface = font.render(input_text, True, text_color)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update window size dynamically
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle input box active state
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print(f"Entered Text: {input_text}")
                    input_text = ""  # Reset after pressing Enter
                else:
                    input_text += event.unicode  # Add character to text

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
