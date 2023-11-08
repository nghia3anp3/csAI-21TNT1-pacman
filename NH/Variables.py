import pygame
import math
from pygame.locals import *
WIDTH = 1280
HEIGHT = 720
CELL_SIZE = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (129, 133, 137)

def read_map(filepath):
    with open(filepath, 'r') as file:
        n, m = map(int, file.readline().strip().split(" "))
        pac_map = []
        for _ in range(n):
            row = [int(x) for x in file.readline().strip().split(" ")]
            pac_map.append(row)
        pac_pos = tuple(map(int, file.readline().strip().split(" ")))
        food = [(i, j) for i in range(len(pac_map)) for j in range(len(pac_map[0])) if pac_map[i][j] == 2]
        monster = [(i, j) for i in range(len(pac_map)) for j in range(len(pac_map[0])) if pac_map[i][j] == 3]
        wall = [(i, j) for i in range(len(pac_map)) for j in range(len(pac_map[0])) if pac_map[i][j] == 1]
        return [pac_map, pac_pos, food, monster, wall]

map_dict = {'Level1':[read_map('Levels/level1/map1.txt'),read_map('Levels/level1/map2.txt'),read_map('Levels/level1/map3.txt'),read_map('Levels/level1/map4.txt'),read_map('Levels/level1/map5.txt')],
        'Level2':[read_map('Levels/level2/map1.txt'), read_map('Levels/level2/map2.txt'),read_map('Levels/level1/map3.txt'),read_map('Levels/level2/map4.txt'),read_map('Levels/level2/map5.txt')],
        'Level3':[read_map('Levels/level3/map1.txt'), read_map('Levels/level3/map2.txt'),read_map('Levels/level3/map3.txt'),read_map('Levels/level3/map4.txt'),read_map('Levels/level3/map5.txt')],
        'Level4':[read_map('Levels/level4/map1.txt'),read_map('Levels/level4/map2.txt'),read_map('Levels/level4/map3.txt'),read_map('Levels/level4/map4.txt'),read_map('Levels/level4/map5.txt')]}

max_depth = 0
change_map_list = [read_map('Levels/level1/map1.txt')[0],read_map('Levels/level1/map2.txt')[0],read_map('Levels/level1/map3.txt')[0],read_map('Levels/level1/map4.txt')[0],read_map('Levels/level1/map5.txt')[0]]
victory_bg = pygame.transform.scale(pygame.image.load("images/victory.png"),(WIDTH,HEIGHT))
lost_bg = pygame.transform.scale(pygame.image.load("images/lost.png"),(WIDTH,HEIGHT))
def get_map_pos_y(map,CELL_SIZE):
    return WIDTH // 2 - (CELL_SIZE * len(map[0]) // 2)
def get_map_pos_x(map,CELL_SIZE):
    return HEIGHT // 2 - (CELL_SIZE * len(map) // 2)

def get_font(size):  # Returns Press-Start-2P in the desired size
  return pygame.font.Font("font/font.ttf", size)

def victory_state(screen):
    screen.blit(victory_bg, (0, 0))

def lost_state(screen):
    screen.blit(lost_bg, (0, 0))