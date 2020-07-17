from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# player.travel("n")
# print("HEY! ", player.current_room.get_exits()) ## Gives ['n', 's']
# print("HEY! ", player.current_room.id) ## Gives 0

def traverse_everything(player):
    visited = dict()

    # Until visited has all the nodes in the map on it, keep repeating.
    while len(visited) != len(world.rooms):
        # print("CURRENT ROOM: ", player.current_room.id)
        if player.current_room.id not in visited:
            visited[player.current_room.id] = dict()

            for room in player.current_room.get_exits():
                visited[player.current_room.id][room] = "?" 

        # Prioritize going to unknown values
        if "?" in list(visited[player.current_room.id].values()):
            rand = [None, None]
            while rand[1] != "?":
                rand = list(random.choices(list(visited[player.current_room.id].items()))[0]) # ['n', '?']
            traversal_path.append(rand[0])
            visited[player.current_room.id][rand[0]] = player.current_room.get_room_in_direction(rand[0]).id  
            old = player.current_room.id
            player.travel(rand[0])
        else:
            rand = list(random.choices(list(visited[player.current_room.id].items()))[0]) # ['n', '?']
            traversal_path.append(rand[0])
            player.travel(rand[0])

        # Add node we just travelled to
        if player.current_room.id not in visited:
            visited[player.current_room.id] = dict()
            for room in player.current_room.get_exits():
                visited[player.current_room.id][room] = "?" 

        # Edge-cases so we don't go back again while prioriting ?'s
        if rand[0] == "n":
            visited[player.current_room.id]["s"] = old
        elif rand[0] == "s":
            visited[player.current_room.id]["n"] = old
        elif rand[0] == "w":
            visited[player.current_room.id]["e"] = old
        elif rand[0] == "e":
            visited[player.current_room.id]["w"] = old

    return visited


visited = traverse_everything(player)

# print("HIS IS VISITED ", visited)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
