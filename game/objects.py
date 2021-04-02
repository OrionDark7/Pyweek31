import pygame, random
from game.map import builds, foods

class Object(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.pos = list(pos)
        self.image = pygame.image.load("./images/tiles/"+self.type+".png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos[0]*64, self.pos[1]*64]
        self.building = False
        self.parking = None
        self.stats = {}
        self.food = False
        if self.type in foods:
            self.food = True
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
    def update(self, action, mouse, pointers=None, clock=0, crimes=None):
        if not crimes == None and self.stats["crime"] == None:
            crimes.remove(self)
        if action == "path":
            if self.building:
                if self.rect.collidepoint(mouse.rect.topleft) and not self.parking == None:
                    print("in")
                    mouse.click = True
                    mouse.rect.topleft = self.parking[0]*64, self.parking[1]*64
            else:
                if self.rect.collidepoint(mouse.rect.topleft):
                    mouse.click = True
        elif action == "crime":
            self.stats["crime"] = "robbery"
            self.stats["cycles"] = random.randint(2,2)
            self.stats["maxcycles"] = self.stats["cycles"]
            self.stats["cooldown"] = random.randint(5000, 15000)
            self.stats["maxcooldown"] = self.stats["cooldown"]
            pointer = Pointer([self.rect.centerx, self.rect.top+24], "", self)
            pointers.add(pointer)
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
                        self.stats["maxcooldown"] = self.stats["cooldown"]
        elif action == "building" and self.building and self.rect.collidepoint(mouse.rect.topleft):
            mouse.building = self
        elif action == "buildingc":
            print(self.rect.collidepoint(mouse.rect.topleft))
            if self.building and self.rect.collidepoint(mouse.rect.topleft):
                mouse.clickedbuilding = self

class Pointer(pygame.sprite.Sprite):
    def __init__(self, pos, type, linked):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/icons/pointer"+str(type)+".png")
        self.oimage = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = list(pos)
        self.orect = self.rect
        self.linked = linked
        self.animationcycle = 0
        self.animation = "grow"
        self.image = pygame.transform.scale(self.oimage, [int(self.orect.width/10), int(self.orect.height/10)])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = self.orect.centerx, self.orect.bottom
        self.bounces = 0
        self.dir = "up"
    def update(self):
        if not self.animation == None:
            if self.animation == "shrink": print("in")
            if self.animation == "bounce":
                if self.dir == "up":
                    self.animationcycle += 1
                else:
                    self.animationcycle -= 1
            else:
                self.animationcycle += 1
        if self.linked.stats["crime"] == None and self.animation == None:
            self.animation = "shrink"
            self.animationcycle = 1
        elif self.linked.stats["cooldown"] == self.linked.stats["maxcooldown"]:
            self.bounces = 0
            self.animation = "bounce"
            self.animationcycle = 0
            self.dir = "up"
        if self.animation == "grow":
            if self.animationcycle < 11:
                self.image = pygame.transform.scale(self.oimage, [int(self.orect.width*(self.animationcycle/10)), int(self.orect.height*(self.animationcycle/10))])
                self.rect = self.image.get_rect()
                self.rect.centerx, self.rect.bottom = self.orect.centerx, self.orect.bottom
            else:
                self.animation = None
                self.animationcycle = 0
        elif self.animation == "shrink":
            if self.animationcycle < 10:
                self.image = pygame.transform.scale(self.oimage, [int(self.orect.width*((10-self.animationcycle)/10)), int(self.orect.height*((10-self.animationcycle)/10))])
                self.rect = self.image.get_rect()
                self.rect.centerx, self.rect.bottom = self.orect.centerx, self.orect.bottom
            else:
                self.kill()
        elif self.animation == "bounce":
            if self.bounces < 3:
                if self.dir == "up" and self.animationcycle >= 10:
                    self.dir = "down"
                    self.rect.centery -= (10-self.animationcycle)/2
                elif self.dir == "down" and self.animationcycle <= 0:
                    self.dir = "up"
                    self.rect.centery += (10-self.animationcycle)/2
                    self.bounces += 1
                if self.dir == "up":
                    self.rect.centery -= (10-self.animationcycle)/2
                elif self.dir == "down":
                    self.rect.centery += (10-self.animationcycle)/2
            else:
                self.bounces = 0
                self.animation = None
                self.animationcycle = 0
                self.dir = "up"
                self.rect.center = self.orect.center