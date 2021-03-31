import pygame, math, random
from game import ui, cars, objects, map

pygame.init()
window = pygame.display.set_mode([1280, 960])
pygame.display.set_caption("Good Cop - Bad City")
ui.window = window

settings = {"fullscreen" : False}
screen = "game"
running = True
mouse = [-1, -1]
clock = pygame.time.Clock()
fps = 60
pygame.time.set_timer(pygame.USEREVENT, random.randint(5000, 12500))
showmenu = False

car = cars.Cop([0,7])

tiles = pygame.sprite.Group()
roads = pygame.sprite.Group()
buildings = pygame.sprite.Group()
crimebuildings = pygame.sprite.Group()
tiles, roads, buildings, listmap, mapsize, background = map.load(1)
pointers = pygame.sprite.Group()

class MouseSprite(pygame.sprite.Sprite):
    def __init__(self):
        global mouse
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([1,1])
        self.rect = self.image.get_rect()
        self.rect.topleft = mouse
        self.click = False
        self.building = None
        self.clickedbuilding = None
ms = MouseSprite()

def gamepos(pos):
    return [math.floor(pos[0]/64), math.floor(pos[1]/64)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            ms.rect.topleft = mouse
            roads.update("path", ms)
            buildings.update("path", ms)
            showmenu = False
            if ms.click:
                ms.click = False
                if car.pos == gamepos(ms.rect.topleft):
                    buildings.update("buildingc", ms)
                    showmenu = True
                else:
                    ms.clickedbuilding = None
                    car.pathfind(gamepos(ms.rect.topleft), listmap, mapsize)
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            ms.rect.topleft = mouse
            if pygame.sprite.spritecollide(ms, buildings, False) and not showmenu:
                buildings.update("building", ms)
            else:
                ms.building = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        elif event.type == pygame.USEREVENT:
            if screen == "game" and not len(buildings) == len(crimebuildings):
                building = random.choice(buildings.sprites())
                while crimebuildings.has(building):
                    building = random.choice(buildings.sprites())
                crimebuildings.add(building)
                building.update("crime", ms, pointers, clock.get_time())
                pygame.time.set_timer(pygame.USEREVENT, random.randint(5000, 12500))
            elif screen == "game" and len(buildings) == len(crimebuildings):
                screen = "gameover"
    if screen == "game":
        ui.Font(36, [255, 255, 255])
        window.fill([255, 255, 255])
        window.blit(background, [0,0])
        tiles.draw(window)
        car.update(window)
        pointers.draw(window)
        ui.Box([320, 160], [5, 795], [0, 0, 0])
        if car.properties["gas"] < 26:
            ui.Box([290*(int(car.properties["gas"])/100), 40], [15, 805], [255, 0, 0], t=False)
        elif car.properties["gas"] < 51:
            ui.Box([290*(int(car.properties["gas"])/100), 40], [15, 805], [255, 255, 0], t=False)
        else:
            ui.Box([290*(int(car.properties["gas"])/100), 40], [15, 805], [0, 255, 0], t=False)
        ui.Text("gas: " + str(round(car.properties["gas"])) + "%", [20, 810])
        if ms.building != None and not showmenu:
            ui.Font(42)
            text = ui.font.render(ms.building.type, 1, [255, 255, 255])
            rect = text.get_rect()
            ui.Box([rect.width + 30, 90], [ms.rect.right + 10, ms.rect.bottom + 10], [0, 0, 0])
            window.blit(text, [ms.rect.right + 25, ms.rect.top + 15])
            ui.Font(24)
            if ms.building.stats["crime"] == None:
                ui.Text("no crime!", [ms.rect.right + 10 + (rect.width+30)/2, ms.rect.bottom + 64], centered=True, c=[0,255,0])
            elif ms.building.stats["crime"] != None:
                if (ms.building.stats["cooldown"]/ms.building.stats["maxcooldown"]) < 0.25:
                    BC = [255, 0, 0]
                elif (ms.building.stats["cooldown"]/ms.building.stats["maxcooldown"]) < 0.5:
                    BC = [255, 255, 0]
                else:
                    BC = [0, 255, 0]
                ui.Box([((rect.width+24))*(round((ms.building.stats["cooldown"]/ms.building.stats["maxcooldown"])*100)/100), 25], [ms.rect.right + 10 + (rect.width+30)/2, ms.rect.bottom + 65], centered=True, c=BC, t=False)
                ui.Text(str(ms.building.stats["crime"]), [ms.rect.right + 10 + (rect.width+30)/2, ms.rect.bottom + 55], centered=True, c=[255,255,255])
                ui.Font(18)
                ui.Text("wave "+str(ms.building.stats["maxcycles"]-ms.building.stats["cycles"]+1)+ " out of " + str(ms.building.stats["maxcycles"]), [ms.rect.right + 10 + (rect.width+30)/2, ms.rect.bottom + 83], centered=True, c=[255,255,255])
        if ms.clickedbuilding == None: showmenu = False
        elif showmenu:
            text = ui.font.render(ms.clickedbuilding.type, 1, [255, 255, 255])
            rect = text.get_rect()
            print([ms.clickedbuilding.rect.center, ms.clickedbuilding.rect.top - 130])
            ui.Box([rect.width + 30, 120], [ms.clickedbuilding.rect.centerx, ms.clickedbuilding.rect.top - 65], [0, 0, 0], centered=True)
            window.blit(text, [ms.clickedbuilding.rect.centerx - rect.width/2, ms.clickedbuilding.rect.top - 120])
        buildings.update("update", ms, pointers, clock.get_time(), crimebuildings)
        pointers.update()
    pygame.display.flip()
    clock.tick(60)
    fps = clock.get_fps()
pygame.quit()