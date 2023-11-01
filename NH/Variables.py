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
        return [pac_map, pac_pos, food, monster]

map_dict = {'Level1':[read_map('Levels/level1/map1.txt'),read_map('Levels/level1/map2.txt')],
        'Level2':[read_map('Levels/level2/map1.txt'), read_map('Levels/level2/map2.txt')],
        'Level3':[read_map('Levels/level3/map5.txt')],
        'Level4':[]}

change_map_list = [read_map('Levels/level1/map1.txt')[0],read_map('Levels/level1/map2.txt')[0]]
def get_map_pos_y(map,CELL_SIZE):
    return WIDTH // 2 - (CELL_SIZE * len(map[0]) // 2)
def get_map_pos_x(map,CELL_SIZE):
    return HEIGHT // 2 - (CELL_SIZE * len(map) // 2)
