import pygame

pygame.init()

screen = pygame.display.set_mode((1920/2, 1080/2), pygame.RESIZABLE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()
