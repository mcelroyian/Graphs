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
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
count = 0
visited = set()

#Traverse Maze
def solve():
    global count
    global steps

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
    
    def bfs(current):
        # print("searching")
        q = Queue()
        q.enqueue([current])
        seen = set()
        while q.size() > 0:
            if len(visited) == 500:
                return None
            path = q.dequeue()
            room = path[-1]
            path = list(path)
            to_enqueue = []
            for exit in g[room].keys():
                #print(exit, g[room][exit])
                if g[room][exit] == "?":

                    return path
                if g[room][exit] not in seen:
                    new_path = list(path) + [g[room][exit]]
                    to_enqueue.append(new_path)
            if to_enqueue:
                for opt in to_enqueue:
                    q.enqueue(opt)
            seen.add(room)
            visited.add(room)


    def move(direction):
        # print('moving')
        player.travel(direction)
        new_room = player.current_room.id
        if new_room not in g:
            g[new_room] = {}
        for exit in player.current_room.get_exits():
            if exit not in g[new_room]:
                g[new_room][exit] = "?"
        add_vert(current, direction, new_room)
        traversal_path.append(direction)
        #if last room has no "?" mark as visited:
        if "?" not in g[g[new_room][d[direction]]].values():
            visited.add(g[new_room][d[direction]])
        return new_room

    pile = Stack()
    pile.push(player.current_room.id)
    seen = set()


    while pile.size() > 0:
        start = pile.pop()
        if start not in g:
            g[start] = {}
        for exit in player.current_room.get_exits():
            if exit not in g[start]:
                g[start][exit] = "?"
        current = start
        if "n" in g[current] and g[current]['n'] == "?":
            while "n" in g[current] and g[current]['n'] == "?":
                current = move('n')
        backtrack = bfs(current)
        #loop through backtract until current is last value
        if backtrack:
            for i in range(len(backtrack) - 1):
                this_room = backtrack[i]
                for exit in g[this_room]:
                    if g[this_room][exit] == backtrack[i +1]:
                        player.travel(exit)
                        traversal_path.append(exit)
                        current = player.current_room.id
                        break
        if "e" in g[current] and g[current]['e'] == "?":
            while "e" in g[current] and g[current]['e'] == "?":
                current = move('e')
        backtrack = bfs(current)
        #loop through backtract until current is last value
        if backtrack:
            for i in range(len(backtrack) - 1):
                this_room = backtrack[i]
                for exit in g[this_room]:
                    if g[this_room][exit] == backtrack[i +1]:
                        player.travel(exit)
                        traversal_path.append(exit)
                        current = player.current_room.id
                        break

        if "s" in g[current] and g[current]['s'] == "?":
            while "s" in g[current] and g[current]['s'] == "?":
                current = move('s')
        backtrack = bfs(current)
        #loop through backtract until current is last value
        if backtrack:
            for i in range(len(backtrack) - 1):
                this_room = backtrack[i]
                for exit in g[this_room]:
                    if g[this_room][exit] == backtrack[i +1]:
                        player.travel(exit)
                        traversal_path.append(exit)
                        current = player.current_room.id
                        break

        if "w" in g[current] and g[current]['w'] == "?":
            while "w" in g[current] and g[current]['w'] == "?":
                current = move('w')
        backtrack = bfs(current)
        #loop through backtract until current is last value
        if backtrack:
            for i in range(len(backtrack) - 1):
                this_room = backtrack[i]
                for exit in g[this_room]:
                    if g[this_room][exit] == backtrack[i +1]:
                        player.travel(exit)
                        traversal_path.append(exit)
                        current = player.current_room.id
                        break
        if len(visited) != 500:
            pile.push(current)
        steps = len(traversal_path)


    # print(g)
    # print(count)


solve()



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



