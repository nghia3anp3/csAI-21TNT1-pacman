from Variables import *
import time
import sys
import Map
import Doraemon
import Mouse
import Astar
import Food
pygame.init()
pygame.font.init()
n, m, map, pac_pos, food, monster = Map.read_map('Levels/level2.txt')

HEIGHT, WIDTH = 35 * n, 35 * m
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PacMan")
font = pygame.font.Font(None, 20)
score = 0


def display_message(message):
    font = pygame.font.Font(None, 56)  # You can adjust the font size as needed
    text = font.render(message, True, RED)  # Replace BLACK with the color you prefer
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)  # Center the text in the window
    screen.blit(text, text_rect)
def Level12():
    global score
    path = Astar.astar(map, pac_pos, food[0])
    dora = Doraemon.dora_right
    mouse = Mouse.mouse_left
    dorayaki = Food.dorayaki
    mouse_list = monster
    endings = Doraemon.endings
    ending_check = False
    for i in range(len(endings)):
        endings[i] = pygame.transform.scale(endings[i], (HEIGHT, WIDTH))
    running = True
    move_count = 0
    screen.fill(BLACK)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if ending_check == False:
            screen.fill(BLACK)
            Map.create_map(map, screen, CELL_SIZE)
            for x, y in mouse_list:
                screen.blit(mouse, (y * CELL_SIZE, x * CELL_SIZE))
            if path == None:
                screen.blit(dorayaki, (food[0][1] * CELL_SIZE, food[0][0] * CELL_SIZE))
                display_message("No path found!")
                pygame.display.update()
            else:
            # for x in range(0, WIDTH, CELL_SIZE):
            #     for y in range(0, HEIGHT, CELL_SIZE):
            #         rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            #         pygame.draw.rect(screen, WHITE, rect, 1)
                if move_count < len(path) - 1:
                    x, y = path[move_count]
                    if path[move_count][1] < path[move_count + 1][1]:
                        dora = Doraemon.dora_right
                    elif path[move_count][1] > path[move_count + 1][1]:
                        dora = Doraemon.dora_left
                    screen.blit(dora, (y * CELL_SIZE, x * CELL_SIZE))
                    time.sleep(0.2)
                    move_count += 1
                    score -= 1
                if move_count < len(path) - 1:
                    x, y = path[-1]
                    screen.blit(dorayaki, (y * CELL_SIZE, x * CELL_SIZE))
                elif move_count == len(path) - 1:
                    score += 20
                    x, y = path[move_count]
                    screen.blit(Doraemon.dora_full, (y * CELL_SIZE, x * CELL_SIZE))
                    move_count += 1
                else:
                    screen.blit(Doraemon.dora_full, (food[0][1] * CELL_SIZE, food[0][0] * CELL_SIZE))
                    ending_check = True
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