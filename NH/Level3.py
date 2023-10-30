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



def MonsterNode(current_pos, orginal_pos):
    return [current_pos,orginal_pos]


def check_move(pacman_pos, monsters_node):
    for monster_node in monsters_node:
        if heuristic(pacman_pos, monster_node[0]) <= 1:
            return False
    return True

# Tất cả các monster di chuyển ngẫu nhiên.

def MonsterMove(maze,monsters_node,foods):
    maze1 = copy.deepcopy(maze)
    monsters_path = []
    for monster_node in monsters_node:
        if monster_node[0] == monster_node[1]: # đi qua các vị trí xung quanh nó
            able_move = []
            for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
                new_x = monster_node[0][0] + dx
                new_y = monster_node[0][1] + dy
                if 0<= new_y<len(maze1[0]) and 0<=new_x<len(maze1) and maze1[new_x][new_y] != 1:
                    able_move.append((new_x,new_y))
            monster_node[0] = random.choice(able_move)
            maze1[monster_node[1][0]][monster_node[1][1]] = 0
            maze1[monster_node[0][0]][monster_node[0][1]] = 3
        else: # Về lại vị trí cũ
#             maze1 = copy.deepcopy(original_maze)
            if monster_node[0] in foods:
                maze1[monster_node[0][0]][monster_node[0][1]] = 2
            else:
                maze1[monster_node[0][0]][monster_node[0][1]] = 0
            monster_node[0] = monster_node[1]
            maze1[monster_node[0][0]][monster_node[0][1]] = 3
        monsters_path.append(monster_node[0])
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

def get_invisibility(maze, pacman_pos):
    visible = get_pacman_visible(maze, pacman_pos)
    invisibility = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i,j) not in visible and maze[i][j] in [0,2]:
                invisibility.append((i,j))
    return invisibility


# Thay đổi đường đi
def changePath(maze, pacman_pos, monsters_node):
    able_pos = get_neighbors(maze,pacman_pos)
    for pos in able_pos:
        if check_move(pos, monsters_node) == True:
            pacman_pos = pos
            break
    return pacman_pos

# Ăn thức ăn
def eatFood(maze,pacman_pos,foods):
    maze1 = copy.deepcopy(maze)
    x = pacman_pos[0]
    y = pacman_pos[1]
    if pacman_pos in foods:
        maze1[x][y] = 0
        foods.remove(pacman_pos)
    return maze1, foods

def IdentifyGoal(maze, pacman_pos, foods, monsters_node):
    invisibility = get_invisibility(maze, pacman_pos)
    foods = sorted(foods, key=lambda food: heuristic(pacman_pos, food))
    invisibility = sorted(invisibility, key=lambda inv: heuristic(pacman_pos, inv))
    if foods:
        goal = foods[0]
    elif invisibility:
        goal = invisibility[0]
    else:
        return 0;
    return goal



def pre_Level3(maze_in):
    maze_input = copy.deepcopy(maze_in)
    foods = maze_input[2]
    monsters = maze_input[3]
    maze = maze_input[0]
    pacman_pos = maze_input[1]
    monsters_node = [MonsterNode(monster, monster) for monster in monsters]
    goal = IdentifyGoal(maze, pacman_pos,foods,monsters_node)
    pacman_path = [pacman_pos]
    monsters_path = [[i[0] for i in monsters_node]]
    count_full_foods = len(foods)
    while (True):
        if not foods:
            break
        if pacman_pos == goal:
            maze, foods = eatFood(maze, pacman_pos, foods)
            if not foods:
                break
        goal = IdentifyGoal(maze, pacman_pos, foods, monsters_node)
        pacman_subpath = nearest_astar(maze, pacman_pos, goal)
        if goal == 0 or pacman_subpath is None:
            return maze, pacman_path, monsters_node, monsters_path, 'block'
        if len(pacman_subpath) == 1:
            maze, monsters_node, monsters_subpath = MonsterMove(maze, monsters_node, foods)
            monsters_path.append(monsters_subpath)
            maze, foods = eatFood(maze, pacman_pos, foods)
            pacman_path.append(pacman_subpath[0])
        else:
            pacman_pos = pacman_subpath[0]
            maze, foods = eatFood(maze, pacman_pos, foods)
            new_pos = pacman_subpath[1]
            able_pos = get_neighbors(maze, pacman_pos)
            if new_pos in able_pos and check_move(new_pos, monsters_node):
                maze, monsters_node, monsters_subpath = MonsterMove(maze, monsters_node, foods)
                monsters_path.append(monsters_subpath)
                pacman_pos = new_pos
                pacman_path.append(pacman_pos)
            else:
                maze, monsters_node, monsters_subpath = MonsterMove(maze, monsters_node, foods)
                monsters_path.append(monsters_subpath)
                pacman_pos = changePath(maze, pacman_pos, monsters_node)
                maze, foods = eatFood(maze, pacman_pos, foods)
                pacman_path.append(pacman_pos)
                if (pacman_pos in [i[0] for i in monsters_node]):
                    return maze, pacman_path, monsters_node, monsters_path, 'dead'
    return maze, pacman_path, monsters_node, monsters_path, "alive"

def Level3(maze_input):
    maze, pacman_path, monsters_node, monsters_path, status = pre_Level3(maze_input)
    foods = maze_input[2]
    print(foods)
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
        time.sleep(0.2)
        path_i += 1
        if (path_i == len(pacman_path)):
            running = False
    pygame.quit()
    sys.exit()