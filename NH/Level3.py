from Variables import *
from Astar import *
import copy
import random
import time
import sys
import Map
import Luffy
import Mouse
import Astar
import Food
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PacMan")
font = pygame.font.Font(None, 20)
score = 0
game_bg = pygame.transform.scale(pygame.image.load("images/game_bg.png"),(WIDTH,HEIGHT))


def Euclid_distance(A,B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def MonsterNode(current_pos, orginal_pos):
    return [current_pos,orginal_pos]

def get_neighbors(maze, position):
    neighbors = []
    for dx, dy in [(1, 0), (-1,0), (0, 1), (0, -1)]:
        x, y = position[0] + dx, position[1] + dy
        if (0 <= x < len(maze) and 0 <= y < len(maze[0])and (maze[x][y] in [0,2])):
            neighbors.append((x, y))
    return neighbors

def get_monster_neighbors(maze, position):
    neighbors = []
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        x, y = position[0] + dx, position[1] + dy
        if (0 <= x < len(maze) and 0 <= y < len(maze[0])and maze[x][y]!=1):
            neighbors.append((x, y))
    return neighbors
# Tất cả các monster di chuyển ngẫu nhiên.
def MonsterMove(maze,monsters_node,foods, monsters_path):
    maze1 = copy.deepcopy(maze)
    monsters_subpath = []
    for i, monster_node in enumerate(monsters_node):
        if monster_node[0] == monster_node[1]: # đi qua các vị trí xung quanh nó
            able_move = get_monster_neighbors(maze,monster_node[0])
            if len(able_move)==2:
                if able_move[0] not in foods:
                    weights = [0.7,0.3]
                    monster_node[0] = random.choices(able_move,weights)[0]
                elif able_move[1] not in foods:
                    weights = [0.3,0.7]
                    monster_node[0] = random.choices(able_move,weights)[0]
                else:
                    monster_node[0] = random.choice(able_move)
            elif len(able_move)==3:
                if able_move[0] not in foods:
                    weights = [0.8,0.1,0.1]
                    monster_node[1] = random.choices(able_move,weights)[0]
                elif able_move[1] not in foods:
                    weights = [0.1,0.8,0.1]
                    monster_node[0] = random.choices(able_move,weights)[0]
                else:
                    monster_node[0] = random.choice(able_move)
            else:
                monster_node[0] = random.choice(able_move)
            monster_node[0] = random.choice(able_move)
            maze1[monster_node[1][0]][monster_node[1][1]] = 0
            maze1[monster_node[0][0]][monster_node[0][1]] = 3
        else: # Về lại vị trí cũ
            if monster_node[0] in foods:
                maze1[monster_node[0][0]][monster_node[0][1]] = 2
            else:
                maze1[monster_node[0][0]][monster_node[0][1]] = 0
            monster_node[0] = monster_node[1]
            maze1[monster_node[0][0]][monster_node[0][1]] = 3
        monsters_subpath.append(monster_node[0])
    monsters_path.append(monsters_subpath)
    return maze1, monsters_node, monsters_path


# Tầm nhìn của pac man
def get_pacman_visible(maze, pacman_pos):
    list_d = []
    visible = []
    for x in range(-3,4):
        for y in range(-3,4):
            if abs(x) + abs(y) <= 3 and (x != 0 or y != 0):
                list_d.append((x,y))
    for dx, dy in list_d:
        new_x = pacman_pos[0] + dx
        new_y = pacman_pos[1] + dy
        if 0<= new_y<len(maze[0]) and 0<=new_x<len(maze):
            visible.append((new_x,new_y))
    return visible

# Ăn thức ăn
def eatFood(maze,pacman_pos,foods):
    maze1 = copy.deepcopy(maze)
    foods1 = copy.deepcopy(foods)
    x = pacman_pos[0]
    y = pacman_pos[1]
    maze1[x][y] = 0
    foods1.remove(pacman_pos)
    return maze1, foods1

def get_region_neighbor(maze, pacman_pos,neighbor):
    list_d = []
    list_pos = []
    delta_x, delta_y = neighbor[0] - pacman_pos[0], neighbor[1] - pacman_pos[1]
    if delta_x != 0:
        for dx in range(2):
            for dy in range(-2,3):
                if abs(dx) + abs(dy) <= 2:
                    list_d.append((delta_x*dx,dy))
        list_d.append((delta_x*2,0))
    else:
        for dy in range(2):
            for dx in range(-2,3):
                if abs(dx) + abs(dy) <= 2:
                    list_d.append((dx,delta_y*dy))
        list_d.append((0,delta_y*2))
    for dx, dy in list_d:
        new_x = pacman_pos[0] + dx
        new_y = pacman_pos[1] + dy
        if 0<= new_y<len(maze[0]) and 0<=new_x<len(maze):
            list_pos.append((new_x,new_y))
    return list_pos


def count_foods_around_neigbor(maze,pacman_pos, neighbor,foods):
    region_neigbor = get_region_neighbor(maze, pacman_pos,neighbor)
    count = sum([1 for i in region_neigbor if i in foods])
    return count
def check_safe_move(pos,monsters_node):
    monsters = [i[0] for i in monsters_node]
    for monster in monsters:
        if Euclid_distance(pos,monster)<=1:
            return False
    return True
def heuristic(maze, pacman_pos, dict_score_maze,foods, pacman_path, monsters_node, monsters_path):
    maze1 = copy.deepcopy(maze)
    neighbors = get_neighbors(maze1, pacman_pos)
    dict_score = {}
    for neighbor in neighbors:
        region_neighbor = get_region_neighbor(maze1,pacman_pos,neighbor)
        score = 0
        for i in region_neighbor:
            if maze1[i[0]][i[1]] == 0: # đường đi
                score -= 1
            # elif maze1[i[0]][i[1]] == 1: # wall
            #     distance = Euclid_distance(neighbor,i)
            #     if distance == 1:
            #         score -= 2
            #     else:
            #         score -= 1
            elif maze1[i[0]][i[1]] == 2: # food
                distance = Euclid_distance(neighbor,i)
                if distance == 0:
                    if check_safe_move(i,monsters_node):
                        score += 500
                    elif (count_foods_around_neigbor(maze,pacman_pos,i,foods)>=2
                          and check_safe_move(neighbor,monsters_node) is False):
                        score -= 100
                    else:
                        score += 120
                elif distance == 1:
                    score += 80
                else:
                    score += 40
            elif maze1[i[0]][i[1]] == 3: # monster
                distance = Euclid_distance(neighbor,i)
                if distance == 0:
                    score -= 500
                elif distance == 1:
                    score -= 150
                else:
                    score -= 60
        dict_score_maze[neighbor] = score
        # if dict_score_maze[neighbor]>0 and neighbor not in foods:
        #     dict_score_maze[neighbor] -= 30
        if neighbor in pacman_path:
            dict_score_maze[neighbor] -= sum([1 for i in pacman_path if i == neighbor])*4
        dict_score[neighbor] = dict_score_maze[neighbor]
    return dict_score, dict_score_maze

def IdentifyStep(maze, pacman_pos, monsters_node, dict_score_maze,foods,pacman_path,monsters_path):
    dict_score, dict_score_maze = heuristic(maze, pacman_pos, dict_score_maze,foods, pacman_path, monsters_node, monsters_path)
    count1 = sum([1 for value in dict_score.values() if value >= 0]) # đếm số lượng neighbor có score lớn hơn 0
    max_value = max(dict_score.values())
    list_keys = [key for key,value in dict_score.items() if value == max_value]
    if count1>0: # có thức ăn trong tầm nhìn
        return random.choice(list_keys)
    else: # không có thức ăn trong tầm nhìn
        # goal = get_foods_no_eaten(maze,pacman_pos,foods,dict_score_maze)
        # if goal is not None:
        #     dict_score_maze[goal] += 100
        #     visible = get_pacman_visible(maze, goal)
        #     for i in visible:
        #         if i not in dict_score_maze:
        #             dict_score[i] = 50
        #         else:
        #             dict_score_maze[i] += 50
        return random.choice(list_keys)
def pre_Level3(maze_in):
    maze_input = copy.deepcopy(maze_in)
    maze = maze_input[0]
    pacman_pos = maze_input[1]
    foods = maze_input[2]
    monsters = maze_input[3]
    monsters_node = [MonsterNode(monster, monster) for monster in monsters]
    pacman_path = [pacman_pos]
    monsters_path = [[i[0] for i in monsters_node]]
    dict_score_maze = {}
    maze1 = copy.deepcopy(maze)
    while(True):
        if not foods:
            break
        # if len(pacman_path)>1000:
        #     break
        dict_score, dict_score_maze = heuristic(maze1, pacman_pos, dict_score_maze,foods, pacman_path, monsters_node,monsters_path)
        pacman_pos = IdentifyStep(maze1,pacman_pos,monsters_node,dict_score_maze,foods, pacman_path,monsters_path)
        maze1, monsters_node, monsters_path = MonsterMove(maze1, monsters_node, foods,monsters_path)
        if pacman_pos in [i[0] for i in monsters_node]:
            return maze1,pacman_path, monsters_path,'dead'
        pacman_path.append(pacman_pos)
        if pacman_pos in foods:
            maze1, foods = eatFood(maze1, pacman_pos,foods)
            if not foods:
                return maze1,pacman_path, monsters_path,'alive'
    return maze1, pacman_path, monsters_path, 'dead'
def Level3(maze_input):
    maze, pacman_path, monsters_path, status = pre_Level3(maze_input)
    foods = maze_input[2]
    print(status)
    luffy = Luffy.luffy_right
    mouse = Mouse.mouse_left
    meat = Food.meat
    running = True
    move_count = 0
    screen.blit(game_bg, (0, 0))
    path_i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(game_bg, (0, 0))
        Map.create_map(maze_input[0], screen, CELL_SIZE)
        for food in foods:
            screen.blit(meat, (get_map_pos_y(maze, CELL_SIZE) + food[1] * CELL_SIZE, get_map_pos_x(maze, CELL_SIZE) + food[0] * CELL_SIZE))
        if pacman_path[path_i] in foods:
            foods.remove(pacman_path[path_i])
        screen.blit(luffy, (get_map_pos_y(maze, CELL_SIZE) + pacman_path[path_i][1] * CELL_SIZE,
                            get_map_pos_x(maze, CELL_SIZE) + pacman_path[path_i][0] * CELL_SIZE))
        for monster_path in monsters_path[path_i]:
            screen.blit(mouse, (get_map_pos_y(maze, CELL_SIZE) + monster_path[1] * CELL_SIZE,
                                get_map_pos_x(maze, CELL_SIZE) + monster_path[0] * CELL_SIZE))
        pygame.display.update()
        time.sleep(0.01)
        path_i += 1
        if (path_i == len(pacman_path)):
            running = False
    pygame.quit()
    sys.exit()