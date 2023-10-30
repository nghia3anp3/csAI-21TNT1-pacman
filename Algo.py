from Variables import *
import math

class Node:
    def __init__(self,x,y, parent, g, h) -> None:
        self.x= x
        self.y = y
        self.parent = parent
        self.g = g
        self.h = h

def key_function(node:Node):
    return node.g + node.h
    
def heuristic(start_pos, end_pos):
    return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])

def reconstruct_path(node:Node):
    path = []
    while node != None:
        path.append((node.x,node.y))
        node = node.parent
    path.reverse()
    return path

def astar(maze, start, goal):
    open_list:list[Node] = []
    closed_list = []
    start_node = Node(start[0], start[1], None, 0, heuristic(start, goal))
    open_list.append(start_node)
    while open_list:
        open_list.sort(key = key_function)
        current_node = open_list[0]
        print((current_node.x,current_node.y))
        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)
        
        open_list.remove(current_node)
        closed_list.append((current_node.x, current_node.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
             new_x = dx + current_node.x
             new_y = dy + current_node.y
             if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1,3):
                 neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, heuristic((new_x,new_y),goal))
                 neigh_pos = (new_x, new_y)
                 if(neigh_pos) in closed_list:
                     continue
                 else:
                    check = False
                    for item in open_list:
                         if(neigh_pos == (item.x,item.y)):
                             check = True
                    if check == False:
                        open_list.append(neighbor_node)
                    else:
                        for open_node in open_list:
                            if open_node.x == neighbor_node.x and open_node.y == neighbor_node.y and open_node.g > neighbor_node.g:
                                open_list.append(neighbor_node)
                                open_list.remove(open_node)
    return None


def BFS(maze, start, goal):
    print("You are using BFS Algorithm")
    open_list:list[Node] = []
    visited = set()
    start_node = Node(start[0],start[1], None, 0,None)
    open_list.append(start_node)
    while open_list :
        current_node:Node = open_list.pop(0)
        visited.add((current_node.x, current_node.y))

        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
             new_x = dx + current_node.x
             new_y = dy + current_node.y
             if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1,3):
                 neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, None)
                 neigh_pos = (new_x, new_y)
                 if neigh_pos not in visited:
                     open_list.append(neighbor_node)
    return None

def DFS(maze, start, goal):
    print("You are using DFS Algorithm")
    open_list:list[Node] = []
    visited = set()
    start_node = Node(start[0],start[1], None, 0,None)
    open_list.append(start_node)
    while open_list :
        current_node:Node = open_list.pop()
        visited.add((current_node.x, current_node.y))

        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
             new_x = dx + current_node.x
             new_y = dy + current_node.y
             if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1,3):
                 neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, None)
                 neigh_pos = (new_x, new_y)
                 if neigh_pos not in visited:
                     open_list.append(neighbor_node)
    return None

def UCS(maze, start, goal):
    open_list:list[Node] = []
    closed_list = []
    start_node = Node(start[0], start[1], None, 0, 0)
    open_list.append(start_node)
    while open_list:
        open_list.sort(key = key_function)
        current_node = open_list[0]
        print((current_node.x,current_node.y))
        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)
        
        open_list.remove(current_node)
        closed_list.append((current_node.x, current_node.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
             new_x = dx + current_node.x
             new_y = dy + current_node.y
             if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1,3):
                 neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, 0)
                 neigh_pos = (new_x, new_y)
                 if(neigh_pos) in closed_list:
                     continue
                 else:
                    check = False
                    for item in open_list:
                         if(neigh_pos == (item.x,item.y)):
                             check = True
                    if check == False:
                        open_list.append(neighbor_node)
                    else:
                        for open_node in open_list:
                            if open_node.x == neighbor_node.x and open_node.y == neighbor_node.y and open_node.g > neighbor_node.g:
                                open_list.append(neighbor_node)
                                open_list.remove(open_node)
    return None