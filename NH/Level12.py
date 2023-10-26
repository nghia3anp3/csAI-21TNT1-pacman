from Variables import *
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
def display_message(message):
    font = pygame.font.Font(None, 56)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)
def Level12(map_input):
    global score
    map = map_input[0]
    pac_pos = map_input[1]
    food = map_input[2]
    monster = map_input[3]
    path = Astar.astar(map, pac_pos, food[0])
    luffy = Luffy.luffy_right
    mouse = Mouse.mouse_left
    meat = Food.meat
    mouse_list = monster
    endings = Luffy.endings
    ending_check = False
    for i in range(len(endings)):
        endings[i] = pygame.transform.scale(endings[i], (WIDTH, HEIGHT))
    running = True
    move_count = 0
    screen.blit(game_bg, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not ending_check:
            screen.blit(game_bg, (0, 0))
            Map.create_map(map, screen, CELL_SIZE)
            for x, y in mouse_list:
                screen.blit(mouse, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
            if path == None:
                screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE))
                screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+food[0][1] * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ food[0][0] * CELL_SIZE))
                display_message("No path found!")
                pygame.display.update()
            else:
                if move_count < len(path) - 1:
                    x, y = path[-1]
                    screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+ y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE) + x * CELL_SIZE))
                    x, y = path[move_count]
                    if path[move_count][1] < path[move_count + 1][1]:
                        luffy = Luffy.luffy_right
                    elif path[move_count][1] > path[move_count + 1][1]:
                        luffy = Luffy.luffy_left
                    screen.blit(luffy, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
                    time.sleep(0.2)
                    move_count += 1
                    score -= 1
                elif move_count == len(path) - 1:
                    score += 20
                    x, y = path[move_count]
                    screen.blit(Luffy.luffy_full, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
                    time.sleep(0.2)
                    move_count += 1
                else:
                    screen.blit(Luffy.luffy_full, (get_map_pos_y(map,CELL_SIZE)+food[0][1] * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ food[0][0] * CELL_SIZE))
                    ending_check = True
                    time.sleep(0.4)
                text = font.render(f"Score: {score}", True, GREEN)
                screen.blit(text, (10, 10))

                # pygame.display.flip()
                pygame.display.update()
        else:
            for ending in endings:
                screen.blit(ending, (0, 0))
                time.sleep(0.05)
                pygame.display.update()
    pygame.quit()
    sys.exit()