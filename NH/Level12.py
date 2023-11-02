from Variables import *
import time
import sys
import Map
import Luffy
import Marine
import Astar
import Food
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PacMan")
font = get_font(20)
score = 0
game_bg = pygame.transform.scale(pygame.image.load("images/game_bg.png"),(WIDTH,HEIGHT))
def display_message(message):
    font = get_font(50)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)
def Level12(map_input):
    global score
    map = map_input[0]
    pac_pos = map_input[1]
    food = map_input[2][0]
    monster = map_input[3]
    path = Astar.astar(map, pac_pos, food)
    luffy = Luffy.luffy_right
    marine = Marine.marine_left
    meat = Food.meat
    # marine_list = monster
    path_i = 0
    # endings = Luffy.endings
    victory_check = False
    # for i in range(len(endings)):
    #     endings[i] = pygame.transform.scale(endings[i], (WIDTH, HEIGHT))
    running = True
    screen.blit(game_bg, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not victory_check:
            screen.blit(game_bg, (0, 0))
            Map.create_map(map, screen, CELL_SIZE)
            for x, y in monster:
                screen.blit(marine, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
            if path == None:
                screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[0] * CELL_SIZE))
                screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+food[0][1] * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ food[0][0] * CELL_SIZE))
                display_message("No path found!")
                pygame.display.update()
            else:
                screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+ food[1] * CELL_SIZE,get_map_pos_x(map,CELL_SIZE) + food[0] * CELL_SIZE))
                if path_i < len(path)-1:
                    if path[path_i][1] < path[path_i + 1][1]:
                        luffy = Luffy.luffy_right
                    elif path[path_i][1] > path[path_i + 1][1]:
                        luffy = Luffy.luffy_left
                screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + path[path_i][1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + path[path_i][0] * CELL_SIZE))
                if path[path_i] == food:
                    score += 20
                    score -= 1
                    victory_check = True
                else:
                    score -= 1
                for mons in monster:
                    screen.blit(marine, (get_map_pos_y(map, CELL_SIZE) + mons[1] * CELL_SIZE,get_map_pos_x(map, CELL_SIZE) + mons[0] * CELL_SIZE))
                path_i += 1
                text = get_font(30).render(f"Score: {score}", True, BLACK)
                screen.blit(text, (10, 10))
                time.sleep(0.2)
                pygame.display.update()
        else:
            victory_state(screen)
            text = get_font(30).render(f"Score: {score}", True, BLACK)
            screen.blit(text, (80, 500))
            pygame.display.update()
    pygame.quit()
    sys.exit()