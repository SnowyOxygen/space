import random


class World:
    def __init__(self, name, map):
        self.name = name
        self.map = map


class Area:
    def __init__(self, name, map, max_x, max_y):
        self.name = name
        self.map = map
        self.max_x = max_x
        self.max_y = max_y


class Tile:
    def __init__(self, name, position, connected_tile, connected_area):
        self.name = name
        self.position = position
        self.connected_room = connected_tile
        self.connected_area = connected_area


area_names = ['desert', 'plains', 'grassland', 'rocky', 'mountainous']

world_name = World("world_name",[
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],  # Each 1 is an area
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]
])


worlds = {
    'world_name': world_name
}

areas = {
}

start_tile = Tile('start_room', [1, 2], [], '')

tiles = {
    'start_area': {
        (1, 2): start_tile
    }
}


def area_generator(maps_world):
    y_no = -1
    for y in worlds[maps_world].map:
        y_no += 1
        x_no = -1
        for x in worlds[maps_world].map[y_no]:
            x_no += 1
            if x == 1:
                if worlds[maps_world].name not in areas.keys():
                    areas[worlds[maps_world].name] = {}
                random_x = random.randint(5, 17)
                random_y = random.randint(5, 17)
                area_name = random.choice(area_names) + '_' + str(x_no) + "_" + str(y_no)
                areas[worlds[maps_world].name][(x_no, y_no)] = Area(area_name, [], random_x, random_y)
                tile_generator(areas[worlds[maps_world].name][(x_no, y_no)])


def tile_generator(area_maps):
    for y in range(area_maps.max_y):
        area_maps.map.append([])
        for x in area_maps.map:
            for x_no in range(area_maps.max_x):
                area_maps.map[x].append(0)





area_generator('world_name')

for ab in areas.values():
    print("------")
    for ac in ab.values():
        print(ac.name)

for a in areas['world_name'][(1, 1)].map:
    print(a)
