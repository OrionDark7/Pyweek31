import pygame

class Cop(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/cars/cop/front.png")
        self.images = {"front":pygame.image.load("./images/cars/cop/front.png"),
                       "back":pygame.image.load("./images/cars/cop/back.png"),
                       "left":pygame.image.load("./images/cars/cop/left.png"),
                       "right":pygame.image.load("./images/cars/cop/right.png"),}
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = 32+self.pos[0]*64, 32+self.pos[1]*64
        self.properties = {"gas":100, "energy":100, "passengers":1}
        self.path = None
        self.moving = False
        self.target = None
    def pathfind(self, position, roads, mapsize):
        print(position, self.pos)
        if not self.moving:
            queue = []
            visited = {}
            if roads[position[0]][position[1]] == 1:
                queue.append([self.pos, None])
            i = None
            j = None
            k = 0
            stop = False
            while len(queue) > 0 and not stop:
                i = queue[0][0]
                j = queue[0][1]
                queue.pop(0)
                if roads[i[0]][i[1]] == 1 and not str(i) in visited:
                    visited[str(i)] = j
                    if i == position:
                        stop = True
                    else:
                        if i[1]+1 < mapsize[1]:
                            queue.append([[i[0], i[1]+1], i])
                        if i[1]-1 > -1:
                            queue.append([[i[0], i[1]-1], i])
                        if i[0]+1 < mapsize[0]:
                            queue.append([[i[0]+1, i[1]], i])
                        if i[0]-1 > -1:
                            queue.append([[i[0]-1, i[1]], i])
                k += 1
                if k > 10000:
                    break
            retrace = []
            i = position
            if stop and not position == self.pos:
                while str(i) in visited and visited[str(i)] != None:
                    if i != None:
                        retrace.append(i)
                    i = visited[str(i)]
                retrace.reverse()
                self.path = retrace
                self.moving = True
                self.target = (32+self.path[0][0]*64, 32+self.path[0][1]*64)
    def update(self, window):
        window.blit(self.image, self.rect.topleft)
        if self.moving:
            gasfactor = 1
            if self.properties["gas"] < 25:
                gasfactor = 0.5
            if not self.rect.center == self.target:
                if self.rect.centerx < self.target[0]:
                    self.rect.centerx+=4*gasfactor
                    self.properties["gas"] -= 0.0125
                    self.image = self.images["right"]
                elif self.rect.centerx > self.target[0]:
                    self.rect.centerx-=4*gasfactor
                    self.properties["gas"] -= 0.0125
                    self.image = self.images["left"]
                if self.rect.centery < self.target[1]:
                    self.rect.centery+=4*gasfactor
                    self.properties["gas"] -= 0.0125
                    self.image = self.images["front"]
                elif self.rect.centery > self.target[1]:
                    self.rect.centery-=4*gasfactor
                    self.properties["gas"] -= 0.0125
                    self.image = self.images["back"]
            elif self.rect.center == self.target:
                self.pos = self.path[0]
                self.path = self.path[1:len(self.path)]
                if len(self.path) > 0:
                    self.target = (32+self.path[0][0]*64, 32+self.path[0][1]*64)
                    if self.rect.centerx < self.target[0]:
                        self.rect.centerx+=4
                        self.properties["gas"] -= 0.0125
                        self.image = self.images["right"]
                    elif self.rect.centerx > self.target[0]:
                        self.rect.centerx-=4
                        self.properties["gas"] -= 0.0125
                        self.image = self.images["left"]
                    if self.rect.centery < self.target[1]:
                        self.rect.centery+=4
                        self.properties["gas"] -= 0.0125
                        self.image = self.images["front"]
                    elif self.rect.centery > self.target[1]:
                        self.rect.centery-=4
                        self.properties["gas"] -= 0.0125
                        self.image = self.images["back"]
                else:
                    self.moving = False
                    self.target = None
