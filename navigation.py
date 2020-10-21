import random
import time
import pickle
import sys
from random import randint

game_state = True


class Object:
    def __init__(self, parent, area, name, portable):
        self.parent = parent
        self.area = area
        self.name = name
        self.portable = portable

class Entity(Object):
    def __init__(self, parent, area, name, portable, health, max_health, inventory):
        super().__init__(parent, area, name, portable)
        self.health = health
        self.max_health = max_health
        self.inventory = inventory


class Player(Entity):
    def __init__(self, parent, area, name, portable, position, health, max_health, inventory, visible_objects,
                 player_map, moved):
        super().__init__(parent, area, name, portable, health, max_health, inventory)
        self.visible_objects = visible_objects
        self.player_map = player_map
        self.moved = moved
        self.position = position

    # movement: increases or decreases player's x or y value depending on the direction.

    def movement_up(self):
        new_y = self.position[1] - 1
        x = self.position[0]
        if areas[self.area].map[new_y][x] == 1 or areas[self.area].map[new_y][x] == 2:
            self.position = [x, new_y]
            self.moved = "up"
            print("You moved", self.moved, ".")
        else:
            print("There is nothing in that direction.")

    def movement_down(self):
        new_y = self.position[1] + 1
        x = self.position[0]
        if areas[self.area].map[new_y][x] == 1 or areas[self.area].map[new_y][x] == 2:
            self.position = [x, new_y]
            self.moved = "down"
            print("You moved", self.moved, ".")
        else:
            print("There is nothing in that direction.")

    def movement_left(self):
        y = self.position[1]
        new_x = self.position[0] - 1
        if areas[self.area].map[y][new_x] == 1 or areas[self.area].map[y][new_x] == 2:
            self.position = [new_x, y]
            self.moved = "left"
            print("You moved", self.moved, ".")
        else:
            print("There is nothing in that direction.")

    def movement_right(self):
        y = self.position[1]
        new_x = self.position[0] + 1
        if areas[self.area].map[y][new_x] == 1 or areas[self.area].map[y][new_x] == 2:
            self.position = [new_x, y]
            self.moved = "right"
            print("You moved", self.moved, ".")
        else:
            print("There is nothing in that direction.")

    def location(self):
        print("##Current##Position##")
        self.player_map = []
        for i in areas[self.area].map:
            self.player_map.append(i.copy())

        self.player_map[self.position[1]][self.position[0]] = 'x'

        unicode_dic = {5: '░', 2: '🬀', 1: '█', 0: '░', 'x': 'x'}

        for a in self.player_map:
            print('[%s]' % ', '.join(map(str, [unicode_dic.get(n, n) for n in a])))

        print("##Current##Position##")
        print(self.position)

    def exit(self):
        if self.area in rooms.keys():

            if tuple(self.position) in rooms[self.area].keys():
                new_room = rooms[self.area][tuple(self.position)].connected_room.copy()
                new_area = rooms[self.area][tuple(self.position)].connected_area

                if rooms[self.area][tuple(self.position)].exit and not rooms[self.area][tuple(self.position)].locked:
                    self.position = []
                    for a in new_room:
                        self.position.append(a)
                    self.area = new_area
                    self.location()
                    for a in self.inventory:
                        objects[a].area = self.area

                elif rooms[self.area][tuple(self.position)].exit and rooms[self.area][tuple(self.position)].locked:
                    print("The exit to", new_room, "in", new_area, "is locked!")

                elif not rooms[self.area][tuple(self.position)].exit:
                    print("There is no exit here.")
            else:
                print("There is no exit here.")

    def look(self):
        if tuple(self.position) in rooms[self.area].keys():
            print("You are", rooms[self.area][tuple(self.position)].description, ".")
            if rooms[self.area][tuple(self.position)].exit:
                exit_area = rooms[self.area][tuple(self.position)].connected_area
                exit_area = areas[exit_area].name
                print("There is an exit to", exit_area, ".")
        else:
            print("You are", areas[self.area].description, ".")


class Area:
    def __init__(self, map, name, description):
        self.map = map
        self.name = name
        self.description = description


class Room:
    def __init__(self, coordinates, name, description, exit, area, connected_room, connected_area, locked):
        self.coordinates = coordinates
        self.name = name
        self.description = description
        self.exit = exit
        self.area = area
        self.connected_room = connected_room
        self.connected_area = connected_area
        self.locked = locked


# coordinates start at 0
# 0 = nothing, 1 = room, 2 = exit, 5 = map border
# Area(map, name, description)

crashed_ship = Area([
    [5, 5, 5, 5, 5],  # [5, 5, 5, 5, 5]
    [5, 0, 1, 1, 5],  # [5, 0, 1, 1, 5]
    [5, 1, 2, 0, 5],  # [5, 1, 2, 0, 5] Exit to desert_map1 at (x = 2, y = 2)
    [5, 0, 1, 1, 5],  # [5, 0, 1, 1, 5]
    [5, 5, 5, 5, 5],  # [5, 5, 5, 5, 5]
], "crashed ship", "in the vessel you crash-landed into the planet")
desert_map1 = Area([
    [5, 5, 5, 5, 5, 5, 5],  # [5, 5, 5, 5, 5, 5, 5]
    [5, 1, 1, 1, 0, 2, 5],  # [5, 1, 1, 1, 0, 2, 5] Exit to crashed_ship at (x = 5, y = 1)
    [5, 1, 0, 1, 1, 1, 5],  # [5, 1, 0, 1, 1, 1, 5]
    [5, 1, 0, 1, 0, 0, 5],  # [5, 1, 0, 1, 0, 0, 5]
    [5, 1, 0, 1, 1, 1, 5],  # [5, 1, 0, 1, 1, 1, 5]
    [5, 1, 1, 1, 0, 1, 5],  # [5, 1, 1, 1, 0, 1, 5]
    [5, 5, 5, 5, 5, 5, 5]   # [5, 5, 5, 5, 5, 5, 5]
], "stony desert", "in a stony desert")


# Room(coordinates, name, description, exit, area, connected_room, connected_area, locked)

crashed_ship_cockpit = Room([1, 2], "crashed ship cockpit",
                            "in the cockpit of your crashed ship", False, "crashed_ship", "", "", False)
crashed_ship_hangar = Room([2, 2], "crashed ship hangar",
                           "the hangar of your crashed ship", True, "crashed_ship", [5, 1], "desert_map1", False)

crashed_ship_outside = Room([5, 1], "crashed ship outside",
                            "outside your crashed ship", True, "desert_map1", [2, 2], "crashed_ship", False)

# Container(parent, area, name, portable, inventory, closed, locked)

# parent, name, portable, position, health, max_health, inventory, area, visible_objects,
#                  player_map, moved
you = Player("", "", False, [1, 2], 25, 50, [], 'crashed_ship', [], [], "")

objects = {

}

rooms = {
    'crashed_ship': {
        (2, 2): crashed_ship_hangar,
        (1, 2): crashed_ship_cockpit
    },
    'desert_map1': {
        (5, 1): crashed_ship_outside
    }
}

areas = {
    'desert_map1': desert_map1,
    'crashed_ship': crashed_ship
}

verbs = {
    'north': you.movement_up,
    'up': you.movement_up,

    'south': you.movement_down,
    'down': you.movement_down,

    'west': you.movement_left,
    'left': you.movement_left,

    'east': you.movement_right,
    'right': you.movement_right,

    'location': you.location,
    'exit': you.exit,
}


you.name = input("> ")

you.location()

while game_state:
    command = input("> ").split()
    verb = command[0]

    if len(command) == 1:
        if verb in verbs.keys():
            verbs[verb]()
        else:
            print("Command not understood.")
            print("Type \"Help\" to return a list of commands.")

    if len(command) > 1 or len(command) == 0:
        print("Command not understood.")
        print("Tip: try commands with two words.")

'''
On startup, type your name.
Then type either a direction (up, down, left, right) or "location"
'''