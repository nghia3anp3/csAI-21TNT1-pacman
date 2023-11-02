from Variables import *


class Node:
    def __init__(self, x, y, parent, g, h) -> None:
        self.x = x
        self.y = y
        self.parent = parent
        self.g = g
        self.h = h


def key_function(node: Node):
    return node.g + node.h


def heuristic(start_pos, end_pos):
    return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])


# Tra lai path
def reconstruct_path(node: Node):
    path = []
    while node != None:
        path.append((node.x, node.y))
        node = node.parent
    path.reverse()
    return path


def astar(maze, start, goal):
    open_list: list[Node] = []
    closed_list = []
    start_node = Node(start[0], start[1], None, 0, heuristic(start, goal))
    open_list.append(start_node)
    while open_list:
        open_list.sort(key=key_function)
        current_node = open_list[0]
        print((current_node.x, current_node.y))
        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)

        open_list.remove(current_node)
        closed_list.append((current_node.x, current_node.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x = dx + current_node.x
            new_y = dy + current_node.y
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1, 3):
                neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, heuristic((new_x, new_y), goal))
                neigh_pos = (new_x, new_y)
                if (neigh_pos) in closed_list:
                    continue
                else:
                    check = False
                    for item in open_list:
                        if (neigh_pos == (item.x, item.y)):
                            check = True
                    if check == False:
                        open_list.append(neighbor_node)
                    else:
                        for open_node in open_list:
                            if open_node.x == neighbor_node.x and open_node.y == neighbor_node.y and open_node.g > neighbor_node.g:
                                open_list.append(neighbor_node)
                                open_list.remove(open_node)
    return None


def Euclid_distance(A,B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
def get_neighbors(maze, position):
    neighbors = []
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        x, y = position[0] + dx, position[1] + dy
        if (0 <= x < len(maze) and 0 <= y < len(maze[0])and (maze[x][y] in [0,2])):
            neighbors.append((x, y))
    return neighbors

def nearst_astar(maze, start, goal,monsters_node):
    open_list = [Node(start)]
    closed_list = set()
    current_node = open_list[0]
    while open_list:
        current_node = min(open_list, key=lambda x: x[2] + x[3])
        if current_node[0] == goal:
            path = []
            while current_node != None:
                path.append(current_node[0])
                current_node = current_node[1]
            path.reverse()
            return path
        open_list.remove(current_node)
        closed_list.add(current_node[0])
        cord, parent, g, h = current_node
        neighbors = get_neighbors(maze, cord)
        for neighbor in neighbors:
                neighbor = Node(neighbor, current_node, g + 1, Euclid_distance(neighbor, goal))
                if neighbor[0] in closed_list:
                    continue
                check = False
                for item in open_list:
                    if (neighbor[0] == item[0]):
                        check = True
                if check == False:
                    open_list.append(neighbor)
                else:
                    for open_node in open_list:
                        if open_node[0] == neighbor[0] and open_node[2] > neighbor[2]:
                            open_node[2] = neighbor[2]
                            open_node[1] = neighbor[1]
                            open_list.append(neighbor)
                            open_list.remove(open_node)
    path = []
    while current_node != None:
        path.append(current_node[0])
        current_node = current_node[1]
    path.reverse()
    return path



def lv4_astar(maze, start, goal):
    maze[goal[0]][goal[1]] = 0
    open_list: list[Node] = []
    closed_list = []
    start_node = Node(start[0], start[1], None, 0, heuristic(start, goal))
    open_list.append(start_node)
    while open_list:
        open_list.sort(key=key_function)
        current_node = open_list[0]
        print((current_node.x, current_node.y))
        if current_node.x == goal[0] and current_node.y == goal[1]:
            return reconstruct_path(current_node)

        open_list.remove(current_node)
        closed_list.append((current_node.x, current_node.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x = dx + current_node.x
            new_y = dy + current_node.y
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1, 3):
                neighbor_node = Node(new_x, new_y, current_node, current_node.g + 1, heuristic((new_x, new_y), goal))
                neigh_pos = (new_x, new_y)
                if (neigh_pos) in closed_list:
                    continue
                else:
                    check = False
                    for item in open_list:
                        if (neigh_pos == (item.x, item.y)):
                            check = True
                    if check == False:
                        open_list.append(neighbor_node)
                    else:
                        for open_node in open_list:
                            if open_node.x == neighbor_node.x and open_node.y == neighbor_node.y and open_node.g > neighbor_node.g:
                                open_list.append(neighbor_node)
                                open_list.remove(open_node)
    return None