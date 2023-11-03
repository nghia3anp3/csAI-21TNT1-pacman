from Variables import *
import time
import sys
import Map
import Luffy
import Marine
import Astar
import Food
import State
import random

pygame.init()
pygame.font.init()

global max_depth
max_depth = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One piece Pac Man")
font = get_font(20)
score = 0
game_bg = pygame.transform.scale(pygame.image.load("images/game_bg.png"), (WIDTH, HEIGHT))


def display_message(message):
    font = pygame.font.Font(None, 56)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)


def getObservation(agents_pos, wall, marine_pos=None):
    legalPath = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 or y != 0) and abs(x) + abs(y) != 2:
                new_pos = (agents_pos[0] + x, agents_pos[1] + y)
                if (marine_pos != None):
                    if new_pos not in wall and new_pos not in marine_pos:
                        legalPath.append(new_pos)
                else:
                    if new_pos not in wall:
                        legalPath.append(new_pos)
    return legalPath


def alphabeta(agentList, agentIndex, depth, gameState, alpha, beta):
    new_state = gameState.copy()
    agents = new_state.getAgents()
    if new_state.is_win() or new_state.is_lose() or depth == max_depth:
        return new_state.eval_state(depth)

    if agentIndex == 0:
        depth += 1
        global value
        value = -999999
        ghost_pos = []
        for x in agents[1:]:
            ghost_pos.append(x.get_pos())
        for action in getObservation(agents[agentIndex].get_pos(), new_state.wall, ghost_pos):
            pacman = Luffy.Pacman(action[0], action[1])
            backup_state = new_state.copy()
            new_state.update(pacman, agentIndex, depth)
            value = max(value, alphabeta(agents, 1, depth, new_state, alpha, beta))
            alpha = max(alpha, value)

            del new_state
            new_state = backup_state.copy()
            del backup_state

        return value
    else:
        nextAgent = agentIndex + 1
        depth += 1
        if new_state.getNumAgents() == nextAgent:
            nextAgent = 0
        value = 999999

        path = Astar.lv4_astar(new_state.map, new_state.pacman.get_pos(),
                               new_state.list_ghost[agentIndex - 1].get_pos())
        res = path[-2]
        ghost = Marine.Ghost(res[0], res[1])
        new_state.update(ghost, agentIndex)
        value = min(value, alphabeta(agents, nextAgent, depth, new_state, alpha, beta))
        beta = min(beta, value)
        return value


def Level4(map_input):
    global score
    map = map_input[0]
    pac_pos = map_input[1]
    food = map_input[2]
    monster = map_input[3]
    wall = map_input[4]
    luffy = Luffy.luffy_right
    marine = Marine.marine_left
    meat = Food.meat
    marine_list = monster
    victory_check = False
    lost_check = False
    list_ghost = []
    for x in monster:
        list_ghost.append(Marine.Ghost(x[0], x[1]))
    pacman = Luffy.Pacman(pac_pos[0], pac_pos[1])
    init_state = State.State(pacman, list_ghost, food, wall, map)
    # ============================================DRAW MAP=============================================================
    running = True
    screen.blit(game_bg, (0, 0))
    Map.create_map(map, screen, CELL_SIZE)
    screen.blit(luffy, (
    get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[0] * CELL_SIZE))
    for x, y in marine_list:
        screen.blit(marine,
                    (get_map_pos_y(map, CELL_SIZE) + y * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x * CELL_SIZE))
    for x, y in food:
        screen.blit(meat,
                    (get_map_pos_y(map, CELL_SIZE) + y * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x * CELL_SIZE))
    pygame.display.update()
    # ===========================================RUN GAME====================================================================
    agentIndex = 0
    numAgents = init_state.getNumAgents()
    luffy_path = []
    marine_path = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if init_state.is_lose():
            print("lost")
            lost_check = True
            continue
        if not victory_check and not lost_check:
            state_recusive = init_state.copy()
            backup_state = init_state.copy()
            agents = init_state.getAgents()
            agent = agents[agentIndex]

            marine_pos = []
            alpha = -999999
            beta = 999999

            screen.blit(game_bg, (0, 0))
            Map.create_map(map, screen, CELL_SIZE)
            action_scores = []
            if agentIndex == 0:
                for x in agents[1:]:
                    pos = x.get_pos()
                    marine_pos.append(pos)
                PosibleActions = getObservation(agent.get_pos(), wall, marine_pos)
                for action in PosibleActions:
                    state_recusive.update(Luffy.Pacman(action[0], action[1]), 0)
                    action_scores.append(alphabeta(agents, 1, 0, state_recusive, alpha, beta))
                    state_recusive = backup_state.copy()
                
                if len(action_scores)==0:
                    lost_check =True
                    continue
                max_action = max(action_scores)
                max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
                chosenIndex = random.choice(max_indices)
                res = PosibleActions[chosenIndex]
            else:
                path = Astar.lv4_astar(state_recusive.map, state_recusive.pacman.get_pos(),
                                       state_recusive.list_ghost[agentIndex - 1].get_pos())
                res = path[-2]

            if agentIndex == 0:
                luffy_path.append(res)
                new_pacman_pos = (res[0], res[1])
                new_pacman = Luffy.Pacman(new_pacman_pos[0], new_pacman_pos[1])
                init_state.update(new_pacman, 0)
            else:
                marine_path.append((res[0], res[1]))
                for x in marine_path:
                    init_state.update(Marine.Ghost(x[0], x[1]), agentIndex)

            if agentIndex + 1 == numAgents:
                init_state.repain()
                marine_path = []
                luffy_path = []

                marine_pos = [x.get_pos() for x in init_state.list_ghost]

                if (len(init_state.list_food) == 0):
                    victory_check = True
                    text = get_font(50).render(f"Score: {score}", True, BLACK)
                    screen.blit(text, (60, 500))
                    victory_state(screen)
                    pygame.display.update()
            agentIndex = (agentIndex + 1) % numAgents
            time.sleep(0.001)
        elif victory_check:
            text = get_font(50).render(f"Score: {score}", True, BLACK)
            screen.blit(text, (60, 500))
            victory_state(screen)
            pygame.display.update()
        elif lost_check:
            lost_state(screen)
            pygame.display.update()
