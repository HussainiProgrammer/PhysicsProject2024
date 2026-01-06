import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
SIDEBAR_WIDTH = 250
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Projectile Motion Simulator")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GROUND_COLOR = (100, 50, 20)

# Font
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 36)

# Input boxes
input_velocity = ""
input_angle = ""
active_velocity = False
active_angle = False

velocity_box = pygame.Rect(20, 100, SIDEBAR_WIDTH - 40, 35)
angle_box = pygame.Rect(20, 180, SIDEBAR_WIDTH - 40, 35)
button_rect = pygame.Rect(20, 260, SIDEBAR_WIDTH - 40, 40)

# Physics constants
g = 9.8  # gravity (m/s^2)
scale = 5  # pixels per meter

# State
launched = False
start_time = 0
velocity = 0
angle = 0

# Ground level
GROUND_Y = HEIGHT - 50

def draw_sidebar():
    # Background
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, SIDEBAR_WIDTH, HEIGHT))

    # Labels
    vel_label = title_font.render("Initial Velocity (m/s):", True, WHITE)
    angle_label = title_font.render("Angle (deg):", True, WHITE)

    screen.blit(vel_label, (20, 70))
    screen.blit(angle_label, (20, 150))

    # Input boxes
    pygame.draw.rect(screen, GREEN if active_velocity else GRAY, velocity_box, 2)
    pygame.draw.rect(screen, GREEN if active_angle else GRAY, angle_box, 2)

    vel_text = font.render(input_velocity, True, WHITE)
    ang_text = font.render(input_angle, True, WHITE)
    screen.blit(vel_text, (velocity_box.x + 5, velocity_box.y + 5))
    screen.blit(ang_text, (angle_box.x + 5, angle_box.y + 5))

    # Start button
    pygame.draw.rect(screen, GREEN, button_rect)
    button_text = font.render("Start", True, BLACK)
    screen.blit(button_text, (button_rect.x + 45, button_rect.y + 8))

def draw_vectors(pos, vx, vy):
    # Draw total velocity
    pygame.draw.line(screen, RED, pos, (pos[0] + vx * 2, pos[1] - vy * 2), 3)

    # x component
    pygame.draw.line(screen, BLUE, pos, (pos[0] + vx * 2, pos[1]), 2)

    # y component
    pygame.draw.line(screen, YELLOW, pos, (pos[0], pos[1] - vy * 2), 2)

    # Gravity vector (constant)
    pygame.draw.line(screen, GREEN, pos, (pos[0], pos[1] + g * 10), 2)

def get_projectile_position(velocity, angle_deg, t):
    angle_rad = math.radians(angle_deg)
    vx = velocity * math.cos(angle_rad)
    vy = velocity * math.sin(angle_rad)

    x = vx * t
    y = vy * t - 0.5 * g * t * t
    return x, y, vx, vy - g * t

def reset():
    global launched, start_time, velocity, angle
    launched = False
    start_time = 0
    velocity = 0
    angle = 0

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill((20, 20, 20))

    draw_sidebar()

    # Ground
    pygame.draw.line(screen, GROUND_COLOR, (SIDEBAR_WIDTH, GROUND_Y), (WIDTH, GROUND_Y), 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if velocity_box.collidepoint(event.pos):
                active_velocity = True
                active_angle = False
            elif angle_box.collidepoint(event.pos):
                active_velocity = False
                active_angle = True
            elif button_rect.collidepoint(event.pos):
                try:
                    velocity = float(input_velocity.strip())
                    angle = float(input_angle.strip())

                    if velocity < 0:
                        print("Velocity must be non-negative.")
                        continue
                    if angle < 0 or angle > 90:
                        print("Angle must be between 0 and 90 degrees.")
                        continue

                    print(f"Starting animation with velocity={velocity}, angle={angle}")
                    launched = True
                    start_time = pygame.time.get_ticks() / 1000
                except ValueError:
                    print("Invalid input: Please enter numeric values for both fields.")
            else:
                active_velocity = False
                active_angle = False

        elif event.type == pygame.KEYDOWN:
            if active_velocity:
                if event.key == pygame.K_BACKSPACE:
                    input_velocity = input_velocity[:-1]
                elif event.key == pygame.K_RETURN:
                    active_velocity = False
                else:
                    input_velocity += event.unicode
            elif active_angle:
                if event.key == pygame.K_BACKSPACE:
                    input_angle = input_angle[:-1]
                elif event.key == pygame.K_RETURN:
                    active_angle = False
                else:
                    input_angle += event.unicode

    if launched:
        current_time = pygame.time.get_ticks() / 1000
        t = current_time - start_time
        x = velocity * math.cos(math.radians(angle)) * t
        y = velocity * math.sin(math.radians(angle)) * t - 0.5 * 9.8 * t**2

        if y < 0:
            y = 0
            launched = False  # Stop animation when it hits the ground

        screen_x = int(1 + x * scale)
        screen_y = int(1 - y * scale)

        # Draw the ball
        pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 10)

        # Velocity components
        vx = velocity * math.cos(math.radians(angle))
        vy = velocity * math.sin(math.radians(angle)) - 9.8 * t

        # Draw vectors
        arrow_scale = 0.5  # To shrink vector arrow lengths
        draw_vectors((screen_x, screen_y), (vx * arrow_scale, -vy * arrow_scale), (255, 255, 0))  # Velocity vector
        draw_vectors((screen_x, screen_y), (vx * arrow_scale, 0), (0, 255, 255))  # Vx
        draw_vectors((screen_x, screen_y), (0, -vy * arrow_scale), (255, 0, 255))  # Vy
        draw_vectors((screen_x, screen_y), (0, 9.8 * arrow_scale), (0, 255, 0))  # Gravity

    pygame.display.flip()

pygame.quit()
sys.exit()
