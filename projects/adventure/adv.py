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

    q = Queue()
    q.enqueue([player.current_room.id])

    # Until visited has all the nodes in the map on it, keep repeating.
    while len(visited) != len(world.rooms):
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
            player.travel(rand[0])
        # We're at a dead-end. Are there more nodes to explore?
        elif find_if_questions_there(visited):
            directions = find_nearest_unknown(player.current_room, visited)
            directions.pop(0) # [16, 15, 1]
            for i in directions:
                move_one_to_unknown(i)  
        else:
            print(visited)
            return visited

def find_nearest_unknown(starting_node, visited):
    history = set()
    q = Queue()
    q.enqueue([starting_node.id])

    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]

        if v not in history:
            if "?" in visited[v].values():
                return path
            history.add(v)

            for value in visited[v].values():
                newPath = list(path)
                newPath.append(value)
                q.enqueue(newPath)

def find_if_questions_there(visited):
    for i in visited.values():
        for value in i.values():
            if "?" == value:
                return True
    return False

def move_one_to_unknown(i):
    for letter in player.current_room.get_exits(): # west, north, etc
        if player.current_room.get_room_in_direction(letter).id == i:
            # Move player there
            traversal_path.append(letter)
            player.travel(letter)
            return

visited = traverse_everything(player)

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
