import random
import time
import pickle
import sys
from random import randint

# Testing for containers and items in containers.

game_state = True


class Object:
    def __init__(self, parent, name, portable):
        self.parent = parent
        self.name = name
        self.portable = portable

    def take(self):
        if self.name in you.visible_objects:
            if not self.portable:
                print("Object can not be taken.")
            else:
                self.obtain()
        else:
            print(self.name.title(), "not found.")

    def obtain(self):
        you.inventory.append(self.name)
        self.parent = you.name
        print("You take the", self.name, ".")


class Container(Object):
    def __init__(self, parent, name, portable, closed, inventory):
        super().__init__(parent, name, portable)
        self.closed = closed
        self.inventory = inventory

    def open(self):
        if not self.closed:
            print(self.name.title(), "is already open!")
        else:
            print("You open", self.name, ".")
            self.closed = False

    def close(self):
        if self.closed:
            print(self.name.title(), "is already closed!")
        else:
            print("You close", self.name, ".")
            self.closed = False

    def access(self):
        if self.parent == you.parent:
            if self.closed:
                print(self.name.title(), "is closed!")
            else:
                print(self.name.title(), "contains:")
                print(self.inventory)
                print("Options: Take \"x\", Store \"x\", Help, Quit.")
                access_command = input("> ")
                if access_command.lower() == "help":
                    print("Take: Type \"take\" followed by the object you wish to take.")
                    print("Store: Type \"store\" followed by the object you wish to store.")
                    print("Quit: Exit the container.")
                    self.access()
                elif access_command.lower() == "quit":
                    print("You finish accessing", self.name, ".")
                elif len(access_command.split()) == 2:
                    access_command = access_command.split()
                    verb = str(access_command[0])
                    object = str(access_command[1])
                    if verb == "take":
                        if object in self.inventory:
                            objects[object].parent = you.name
                            self.inventory.remove(objects[object].name)
                            you.inventory.append(objects[object].name)
                            self.access()
                        else:
                            print("Can not find,", object, "in container", self.name, ".")
                            self.access()
                    elif verb == "store":
                        if object in you.inventory:
                            objects[object].parent = self.name
                            you.inventory.remove(objects[object].name)
                            self.inventory.append(objects[object].name)
                            self.access()
                        else:
                            print("Can not find", object, "in your inventory.")
                            self.access()
                    else:
                        print("Command not understood.")
                        self.access()
        else:
            print("The container \"", self.name, "\"can be found.")


class Entity(Object):
    def __init__(self, parent, name, portable, health, max_health, inventory):
        super().__init__(parent, name, portable)
        self.health = health
        self.max_health = max_health
        self.inventory = inventory


class Player(Entity):
    def __init__(self, parent, name, portable, health, max_health, inventory, visible_objects):
        super().__init__(parent, name, portable, health, max_health, inventory)
        self.visible_objects = visible_objects

    def status(self):
        print("Your name is", self.name, "; Health:", self.health, "/", self.max_health)

    def contain(self):
        print("You are carrying:")
        print(self.inventory)


class Room:
    def __init__(self, name, is_parent):
        self.name = name
        self.is_parent = is_parent


room = Room("room", True)
room2 = Room("room2", True)

you = Player("room", "", False, 25, 50, [], ['apple', 'locker'])

locker = Container("room", "locker", False, True, ['banana'])
locker2 = Container("room2", "locker2", False, True, ['apricot'] )

apple = Object("room", "apple", True)
banana = Object("locker", "banana", True)
apricot = Object("locker2", "apricot", True)
orange = Object("room2", "orange", True)

verbs = {
    'take': Object.take,
    'access': Container.access,
    'open': Container.open,
    'inventory': you.contain,
}

objects = {
    'apple': apple,
    'banana': banana,
    'apricot': apricot,
    'orange': orange,
    'locker': locker,
    'locker2': locker2
}

containers = {
    'locker': locker,
    'locker2': locker2
}

you.name = input("> ")

while game_state:
    command = input("> ").split()
    verb = command[0]

    if len(command) == 2:
        object = command[1]
        if verb in verbs.keys():
            if object in objects.keys():
                verbs[verb](objects[object])
            else:
                print(object.title(), "can not be found.")
        else:
            print("Command not understood.")

    if len(command) == 1:
        if verb in verbs.keys():
            verbs[verb]()
        else:
            print("Command not understood.")
            print("Type \"Help\" to return a list of commands.")

    if len(command) > 2 or len(command) == 0:
        print("Command not understood.")
        print("Tip: try commands with two words.")
