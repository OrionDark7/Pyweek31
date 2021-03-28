import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.pos = list(pos)
        self.image = pygame.image.load("./images/tiles/"+self.type+".png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos[0]*32, self.pos[1]*32]
        self.attributes = {}
    def update(self):
        pass