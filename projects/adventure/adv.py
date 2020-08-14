from room import Room
from player import Player
from world import World
from util import Stack, Queue
from graph import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#Traverse Maze
def solve():

    g = {}
    d = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }
    def add_vert(current, direction, next_room):
        g[current][direction] = next_room
        g[next_room][d[direction]] = current

    pile = Stack()
    pile.push(player.current_room.id)
    seen = set()

    while pile.size() > 0:
        current = pile.pop()
        if current not in g:
            g[current] = {}
        for exit in player.current_room.get_exits():
            g[current][exit] = "?"
        seen.add(current)

        for exit in player.current_room.get_exits():
            if g[current][exit] == "?":
                #move to next room
                player.travel(exit)
                room = player.current_room.id
                #add room to graph
                if room not in g:
                    g[room] = {}
                #connect two rooms in graph
                add_vert(current, exit, player.current_room.id)
                #add to stack
                if room not in seen:
                    pile.push(room)
                #add direction to my traversal
                traversal_path.append(exit)
    print(g)

        
        


solve()


    # while pile.size() > 0:
    #     current = pile.pop()
    #     seen.add(current)
    #     if isinstance(current, int):
    #         room = current
    #     else:
    #         room = list(current)[-1]
    #     exits = player.current_room.get_exits()
    #     for exit in exits:
    #         if isinstance(current, int):
    #             pile.push(tuple([current] + [exit]))
    #         else:
    #             pile.push(tuple(current.append(exit)))


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
