import pygame, pytmx
from game import objects

builds = []

def load(id):
    global buildings
    data = pytmx.TiledMap("./map/"+str(id)+".tmx")
    tiles = pygame.sprite.Group()
    roads = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    listmap = []
    mapsize = [data.width, data.height]
    for x in range(data.width):
        listmap.append([])
        for y in range(data.height):
            p = data.get_tile_properties(x, y, 0)
            t = objects.Object(p['type'], [x, y])
            tiles.add(t)
            if p['type'].startswith("road"):
                roads.add(t)
                listmap[x].append(1)
            if p['type'] in builds:
                buildings.add(t)
            if not p['type'].startswith("road"):
                listmap[x].append(0)
    return tiles, roads, buildings, listmap, mapsize