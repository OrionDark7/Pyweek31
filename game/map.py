import pygame, pytmx
from game import objects

builds = ["building", "gas station", "coffee stand"]
foods = ["coffee stand"]

def load(id):
    global buildings
    data = pytmx.TiledMap("./map/"+str(id)+".tmx")
    tiles = pygame.sprite.Group()
    roads = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    bkg = pygame.surface.Surface([1280, 960])
    listmap = []
    mapsize = [data.width, data.height]
    for x in range(data.width):
        listmap.append([])
        for y in range(data.height):
            p = data.get_tile_properties(x, y, 0)
            t = objects.Object(p['type'], [x, y])
            if p['type'].startswith("road"):
                roads.add(t)
                listmap[x].append(1)
                tiles.add(t)
            if p['type'] in builds:
                buildings.add(t)
                tiles.add(t)
            if not p['type'].startswith("road"):
                listmap[x].append(0)
                if not p['type'] in builds:
                    bkg.blit(t.image, [x*64, y*64])
    for i in buildings:
        i.findparking(listmap)
    return tiles, roads, buildings, listmap, mapsize, bkg