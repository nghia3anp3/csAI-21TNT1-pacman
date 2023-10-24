import pygame
import math
import sys
import time
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
 
def read_map(filepath):
  with open(filepath, 'r') as file:
            n, m = map(int, file.readline().strip().split(" "))
            pac_map = []
            for _ in range(n):
                row = [int(x) for x in file.readline().strip().split(" ")]
                pac_map.append(row)
            pac_pos = tuple(map(int, file.readline().strip().split(" ")))
            return n, m, pac_map, pac_pos
 
n, m, map, pac_pos = read_map('level1.txt')
 
HEIGHT, WIDTH = 35 * n, 35 * m
CELL_SIZE = 35
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PacMan")
 
pygame.font.init()
font = pygame.font.Font(None, 20)
score = 0
 
def Node(node, parent=None, g=0, h=0):
    return [node, parent, g, h]  # [(tuple chua x,y),parent,g,h]
 
def heuristic(node, goal):
    return abs(node[1] - goal[1]) + abs(node[0] - goal[0])
 
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
                if (neighbor[0] == item[0] for item in open_list):
                    open_list.append(neighbor)
                else:
                    for open_node in open_list:
                        if open_node[0] == neighbor[0] and open_node[2] > neighbor[2]:
                            open_node[2] = neighbor[2]
                            open_node[1] = neighbor[1]
                            open_list.append(neighbor)
                            open_list.remove(open_node)
    return None
food = [(i,j) for i in range(len(map)) for j in range(len(map[0])) if map[i][j] == 2][0]
maze = map
path = astar(maze, pac_pos, food)
def covered_map(map):
    map1 = map
    for i in map1:
        i.insert(0,1)
        i.append(1)
    map1.insert(0,[1]*len(map1[0]))
    map1.append([1]*len(map1[0]))
    return map1
def draw_style(cord):
    max_row = len(map)
    max_col = len(map[0])
    if cord[0] < 0 or cord[0] >= max_row or cord[1] < 0 or cord[1] >= max_col:
        return 'Coordinate out of bounds'
 
    up = map[cord[0] - 1][cord[1]] if cord[0] > 0 else 0
    down = map[cord[0] + 1][cord[1]] if cord[0] < max_row - 1 else 0
    left = map[cord[0]][cord[1] - 1] if cord[1] > 0 else 0
    right = map[cord[0]][cord[1] + 1] if cord[1] < max_col - 1 else 0
 
    if (up == 1 or down == 1) and left != 1 and right != 1:
        return 'vertical line'
    elif (left == 1 or right == 1) and up != 1 and down != 1:
        return 'horizontal line'
    elif right == 1 and down == 1 and up != 1 and left !=1:
        return 'corner1'
    elif left == 1 and down == 1 and up != 1 and right !=1:
        return 'corner2'
    elif right == 1 and up == 1 and down != 1 and left !=1:
        return 'corner3'
    elif left == 1 and up == 1 and down != 1 and right !=1:
        return 'corner4'
    elif left == 1 and right == 1:
        if up == 1 and down == 1:
            return '+'
        elif up == 1:
            return '^'
        elif down == 1:
            return 'v'
    elif up == 1 and down == 1:
        if left== 1:
            return '<'
        elif right ==1:
            return '>'
    return 'Coordinate out of bounds'
 



dora = pygame.image.load("dora.png")
dora_full = pygame.image.load("full.png")
dora = pygame.transform.scale(dora, (CELL_SIZE, CELL_SIZE))
dora_full = pygame.transform.scale(dora_full, (CELL_SIZE, CELL_SIZE*2))



# Main loop
running = True
move_count = 0
screen.fill(BLACK)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)
    # for x in range(0, WIDTH, CELL_SIZE):
    #     for y in range(0, HEIGHT, CELL_SIZE):
    #         rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    #         pygame.draw.rect(screen, WHITE, rect, 1)
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if draw_style((x,y)) == 'vertical line'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
            elif draw_style((x,y)) == 'horizontal line'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE, x * CELL_SIZE  + 0.5 * CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            elif draw_style((x,y)) == 'corner1'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == 'corner2'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == 'corner3'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == 'corner4'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE - 0.5* CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == '+'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE - 0.5* CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == '^'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE - 0.5* CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == 'v'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == '>'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
            elif draw_style((x,y)) == '<'and maze[x][y]==1:
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE], 5)
                pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE+0.5*CELL_SIZE],[y * CELL_SIZE + 0.5*CELL_SIZE, x * CELL_SIZE-0.5*CELL_SIZE], 5)
            #if maze[x][y] == 1:
            #     pygame.draw.rect(screen, BLUE, (y * CELL_SIZE, x * CELL_SIZE, 20, 20))
    # Draw the path
            elif maze[x][y] == 3:
                pygame.draw.rect(screen, RED, (y * CELL_SIZE, x * CELL_SIZE, 10, 10))
    # Draw the path
    # if path:
    #     for x, y in path:
    #         pygame.draw.rect(screen, ORANGE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    #         score -= 1
    #     score += 20
    if move_count < len(path)-1:
        x, y = path[move_count]
        # pygame.draw.rect(screen, ORANGE, (y * CELL_SIZE, x * CELL_SIZE, 35, 10))
        screen.blit(dora, (y * CELL_SIZE, x * CELL_SIZE))
        time.sleep(0.2)
        move_count += 1
        score -= 1
    if move_count < len(path)-1:
        x, y = path[-1]
        pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    elif move_count == len(path)-1:
        score+=20
        x, y = path[move_count]
        screen.blit(dora_full, (y * CELL_SIZE, x * CELL_SIZE))
        move_count += 1
    else:
        screen.blit(dora_full, (food[1] * CELL_SIZE, food[0] * CELL_SIZE))
    text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(text, (10, 10))
 
    # pygame.display.flip()
    pygame.display.update()
 
pygame.quit()
sys.exit()