from Variables import *
def create_map(map,screen,CELL_SIZE):
    wall = pygame.image.load("images/gold_wall.png")
    wall = pygame.transform.scale(wall, (CELL_SIZE, CELL_SIZE))
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == 1:
                screen.blit(wall, (get_map_pos_y(map, CELL_SIZE) + y * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x * CELL_SIZE))