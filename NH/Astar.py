from Variables import *
def Node(node, parent=None, g=0, h=0):
    return [node, parent, g, h]  # [(tuple chua x,y),parent,g,h]
def heuristic(A,B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
def Euclid_distance(A,B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
def astar(maze, start, goal):
    open_list = [Node(start)]
    closed_list = set()
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
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = cord[0] + dx, cord[1] + dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] not in (1, 3):
                neighbor = Node((new_x, new_y), current_node, g + 1, heuristic((new_x, new_y), goal))
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
    return None

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