import pygame

class Cop(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/cars/cop/front.png")
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = 16+self.pos[0]*32, 16+self.pos[1]*32
        self.properties = {"gas":100, "energy":100, "passengers":1}
        self.path = None
        self.moving = False
        self.target = None
    def pathfind(self, position, roads, mapsize):
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
            if stop:
                while str(i) in visited and visited[str(i)] != None:
                    if i != None:
                        retrace.append(i)
                    i = visited[str(i)]
                retrace.reverse()
                self.path = retrace
                self.moving = True
                self.target = (16+self.path[0][0]*32, 16+self.path[0][1]*32)
    def update(self, window):
        window.blit(self.image, self.rect.topleft)
        if self.moving:
            if not self.rect.center == self.target:
                if self.rect.centerx < self.target[0]:
                    self.rect.centerx+=8
                elif self.rect.centerx > self.target[0]:
                    self.rect.centerx-=8
                if self.rect.centery < self.target[1]:
                    self.rect.centery+=8
                elif self.rect.centery > self.target[1]:
                    self.rect.centery-=8
            elif self.rect.center == self.target:
                self.pos = self.path[0]
                self.path = self.path[1:len(self.path)]
                if len(self.path) > 0:
                    self.target = (16+self.path[0][0]*32, 16+self.path[0][1]*32)
                    if self.rect.centerx < self.target[0]:
                        self.rect.centerx+=8
                    elif self.rect.centerx > self.target[0]:
                        self.rect.centerx-=8
                    if self.rect.centery < self.target[1]:
                        self.rect.centery+=8
                    elif self.rect.centery > self.target[1]:
                        self.rect.centery-=8
                else:
                    self.moving = False
                    self.target = None
