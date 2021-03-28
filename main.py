import pygame, math
from game import ui, cars, objects, map

pygame.init()
window = pygame.display.set_mode([1280, 960])
pygame.display.set_caption("Pyweek 31")
ui.window = window

settings = {"fullscreen" : False}
screen = "game"
running = True
mouse = [-1, -1]

car = cars.Cop([0,2])

tiles = pygame.sprite.Group()
roads = pygame.sprite.Group()
buildings = pygame.sprite.Group()
tiles, roads, buildings, listmap, mapsize = map.load(1)


class MouseSprite(pygame.sprite.Sprite):
    def __init__(self):
        global mouse
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([1,1])
        self.rect = self.image.get_rect()
        self.rect.topleft = mouse
        self.click = False
ms = MouseSprite()

def gamepos(pos):
    return [math.floor(pos[0]/32), math.floor(pos[1]/32)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            ms.topleft = mouse
            roads.update("path", ms)
            if ms.click:
                ms.click = False
                car.pathfind(gamepos(mouse), listmap, mapsize)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
    if screen == "game":
        window.fill([255, 255, 255])
        tiles.draw(window)
        car.update(window)
    pygame.display.flip()
pygame.quit()