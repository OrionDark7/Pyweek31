import pygame

pygame.font.init()

font = pygame.font.Font(None, 24)
size = 24
color = [0,0,0]
window = pygame.surface.Surface([800, 600])

def Font(s=24, c=[0,0,0]):
    global font, size, color
    font = pygame.font.Font(None, int(size))
    color = c

def Text(text, pos, centered=False, dorect=False, c=None):
    global font, color, window
    if c == None:
        r = font.render(str(text), 1, color)
    else:
        r = font.render(str(text), 1, list(c))
    if centered or dorect:
        rect = r.get_rect()
    if centered:
        window.blit(r, [pos[0]-(rect.width/2), pos[1]])
    else:
        window.blit(r, pos)
    rv = str(text)
    if dorect:
        rv = rect
    return rv

class Image(pygame.sprite.Sprite): #image class that doubles as a button
    def __init__(self, path, pos, centered=False, dh=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/"+str(path))
        self.rect = self.image.get_rect()
        if centered:
            self.rect.center = list(pos)
        else:
            self.rect.topleft = list(pos)
        self.dh = dh
        if dh:
            self.dhs = pygame.surface.Surface(self.rect.size)
            self.dhs.fill([255, 255, 255])
            self.dhs.set_alpha(50)
    def click(self, mouse):
        rv=False
        if self.rect.collidepoint(mouse):
            rv=True
        return rv
    def update(self, mouse):
        global window
        if self.dh:
            if self.rect.collidepoint(mouse):
                window.blit(self.dhs, self.rect.topleft)
    def draw(self):
        global window
        window.blit(self.image, self.rect.topleft)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, centered, bc=[0,0,0], c=None):
        global font, color
        pygame.sprite.Sprite.__init__(self)
        if c == None:
            self.render = font.render(str(text), 1, list(color))
        else:
            self.render = font.render(str(text), 1, [255, 255, 255])
        self.rect = self.render.get_rect()
        self.image = pygame.surface.Surface([self.rect.width+10, self.rect.height+10]).fill(list(bc))
        self.image.blit(self.render, [5,5])
        self.rect = self.image.get_rect()
        if centered:
            self.rect.center = list(pos)
        else:
            self.rect.topleft = list(pos)
        self.image.set_alpha(200)
    def click(self, mouse):
        rv = False
        if self.rect.collidepoint(mouse):
            rv = True
        return rv
    def update(self, mouse):
        self.image.set_alpha(200)
        if self.rect.collidepoint(mouse):
            self.image.set_alpha(255)
    def draw(self):
        global window
        window.blit(self.image, self.rect.topleft)

def Box(s, p, c=None, centered=False, r=False):
    global window, color
    if c == None:
        surface = pygame.surface.Surface(list(s)).fill(color)
    else:
        surface = pygame.surface.Surface(list(s)).fill(list(c))
    surface.set_alpha(200)
    if centered:
        window.blit(surface, [p[0] - int(s[0]/2), p[1] - int(s[1]/2)])
    else:
        window.blit(surface, p)
    rv = None
    if r:
        rv = surface.get_rect()
    return rv

