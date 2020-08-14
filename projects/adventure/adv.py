from room import Room
from player import Player
from world import World
from util import Stack, Queue
from graph import Graph
import pygame

import random
from ast import literal_eval

#Setup Pygame
win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Lambda Maze")

room_size = 10
grid = 30
width = room_size 
height = room_size


run = True

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
d = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}

g = {}

#Traverse Maze
def solve():
    global count
    global steps
    global d
    global g
    

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
# print(player.current_room.description)
# print("holla")
# print(traversal_path)
fast = 16
medium = 32
slow = 60

i = 0
prev_room_id = 0
hallway = 0
player.current_room = world.starting_room
while run:
    pygame.time.delay(fast)
    if i != 0:
        prev_dir = traversal_path[i-1]
        backwards = d[prev_dir]
        prev_room_id = g[player.current_room.id][backwards]
        x = room_graph[prev_room_id][0][0]
        y = room_graph[prev_room_id][0][1]
        prev_location = {"x":x,
        "y":y}
    else:
        prev_location = {"x":room_graph[player.current_room.id][0][0], "y":room_graph[player.current_room.id][0][1]}


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        if i < 499:
            #draw prev location
            if prev_room_id in visited:
                color = (248,248,255)
            else:
                color = (220,220,220)
            pygame.draw.rect(win, color, ((prev_location['x'] * grid), (prev_location['y'] * grid), width, height))
            #draw current location of player
            if 'e' in g[player.current_room.id]:
                hallway = ((player.current_room.x * grid) + width, (player.current_room.y * grid) + height // 4, grid - width, height // 2)
                pygame.draw.rect(win,color, tuple(hallway))
            if 's' in g[player.current_room.id]:
                hallway = ((player.current_room.x * grid + width // 4), (player.current_room.y * grid) + height, width // 2, height * 2)
                pygame.draw.rect(win,color, tuple(hallway))
            if 'w' in g[player.current_room.id]:
                hallway = ((player.current_room.x * grid) - (grid - width), (player.current_room.y * grid) + height // 4, grid - width, height // 2)
                pygame.draw.rect(win,color, tuple(hallway))
            if 'n' in g[player.current_room.id]:
                hallway = ((player.current_room.x * grid) + width // 4, (player.current_room.y * grid) - (grid - height), width // 2, grid - height)
                pygame.draw.rect(win,color, tuple(hallway))
            pygame.draw.rect(win, (255, 0, 0), ((player.current_room.x * grid), (player.current_room.y * grid), room_size, room_size))
            exits = player.current_room.get_exits()
            pygame.display.update()
            player.travel(traversal_path[i])
            print("i", i, " ", "path: ", traversal_path[i])

            i +=1



# # TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



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



