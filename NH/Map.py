from Variables import *
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
        return n, m, pac_map, pac_pos, food, monster

def draw_style(cord,map):
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
    elif right == 1 and down == 1 and up != 1 and left != 1:
        return 'corner1'
    elif left == 1 and down == 1 and up != 1 and right != 1:
        return 'corner2'
    elif right == 1 and up == 1 and down != 1 and left != 1:
        return 'corner3'
    elif left == 1 and up == 1 and down != 1 and right != 1:
        return 'corner4'
    elif left == 1 and right == 1:
        if up == 1 and down == 1:
            return '+'
        elif up == 1:
            return '^'
        elif down == 1:
            return 'v'
    elif up == 1 and down == 1:
        if left == 1:
            return '<'
        elif right == 1:
            return '>'
    elif up != 1 and down != 1 and left != 1 and right !=1:
        return 'square'
        
def create_map(map,screen,CELL_SIZE):
    for x in range(len(map)):
        for y in range(len(map[0])):
            # if draw_style((x, y),map) == 'vertical line' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'horizontal line' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'corner1' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'corner2' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'corner3' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE - 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'corner4' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE - 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE - 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == '+' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == '^' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE - 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE - 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == 'v' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == '>' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE - 0.5 * CELL_SIZE], 5)
            # elif draw_style((x, y),map) == '<' and map[x][y] == 1:
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE], 5)
            #     pygame.draw.line(screen, BLUE, [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE + 0.5 * CELL_SIZE],
            #                      [y * CELL_SIZE + 0.5 * CELL_SIZE, x * CELL_SIZE - 0.5 * CELL_SIZE], 5)
            #
            if map[x][y] == 1:
                pygame.draw.rect(screen, GRAY, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))