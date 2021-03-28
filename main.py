import pygame
from game import ui

pygame.init()
window = pygame.display.set_mode([1280, 960])
pygame.display.set_caption("Pyweek 31")
ui.window = window

settings = {"fullscreen" : False}
screen = "game"
running = True
mouse = [-1, -1]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
    if screen == "game":
        window.fill([255, 255, 255])
    pygame.display.flip()
pygame.quit()