import pygame, random
from game.map import builds

class Object(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.pos = list(pos)
        self.image = pygame.image.load("./images/tiles/"+self.type+".png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos[0]*32, self.pos[1]*32]
        self.building = False
        self.parking = None
        self.stats = {}
        if self.type in builds:
            self.building = True
            self.stats = {"crime" : None, "stock" : 100, "open" : True, "cooldown" : random.randint(5000, 15000), "cycles":0}
    def findparking(self, listmap):
        if listmap[self.pos[0]][self.pos[1]+1] > 0:
            self.parking = [self.pos[0], self.pos[1]+1]
        elif listmap[self.pos[0]+1][self.pos[1]] > 0:
            self.parking = [self.pos[0]+1, self.pos[1]]
        elif listmap[self.pos[0]-1][self.pos[1]] > 0:
            self.parking = [self.pos[0]-1, self.pos[1]]
        elif listmap[self.pos[0]][self.pos[1]-1] > 0:
            self.parking = [self.pos[0], self.pos[1]-1]
    def update(self, action, mouse, clock=0, crimes=None):
        if self.building:
            print(self.stats)
        if action == "path":
            if self.building:
                if self.rect.collidepoint(mouse.topleft) and not self.parking == None:
                    mouse.click = True
                    mouse.topleft = self.parking[0]*32, self.parking[1]*32
            else:
                if self.rect.collidepoint(mouse.topleft):
                    mouse.click = True
        elif action == "crime":
            self.stats["crime"] = "robbery"
            self.stats["cycles"] = random.randint(4,6)
            self.stats["cooldown"] = random.randint(5000, 15000)
        elif action == "update":
            if self.stats["crime"] != None:
                self.stats["cooldown"] -= clock
                if self.stats["cooldown"] <= 0:
                    self.stats["cycles"] -= 1
                    if self.stats["cycles"] <= 0:
                        self.stats["crime"] = None
                        if not crimes == None:
                            crimes.remove(self)
                    else:
                        self.stats["cooldown"] = random.randint(5000, 15000)