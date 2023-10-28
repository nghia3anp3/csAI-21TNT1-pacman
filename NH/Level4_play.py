from Variables import *
import time
import sys
import Map
import Luffy
import Mouse
import Astar
import Food
import State
import Pacman
import Ghost
import random

pygame.init()
pygame.font.init()

global max_depth;
max_depth = 3
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

def getObservation(agents_pos, wall):
    legalPath = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 or y != 0) and abs(x) + abs(y) != 2:
                new_pos = (agents_pos[0] + y, agents_pos[1] + x)
                if new_pos not in wall:
                    legalPath.append(new_pos)
    return legalPath

def alphabeta(agentList, agentIndex, depth, gameState, alpha, beta):
    if gameState.is_win() or gameState.is_lose() or depth==max_depth:
            return gameState.eval_state()
    if agentIndex == 0: #maximize for pacman
        value = -999999
        for action in getObservation(agentList[agentIndex].get_pos(), gameState.wall):
            new_state = gameState.copy()
            value = max(value, alphabeta(agentList, 1, depth, new_state.update(Pacman.Pacman(action[0],action[1]), agentIndex) ,alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        nextAgent = agentIndex + 1
        if gameState.getNumAgents() == nextAgent:
            nextAgent = 0
        if nextAgent == 0:
            depth += 1
        for action in getObservation(agentList[agentIndex].get_pos(), gameState.wall):
            value = 999999
            new_state = gameState.copy()
            value = min(value, alphabeta(agentList, nextAgent, depth, new_state.update(Ghost.Ghost(action[0],action[1]), agentIndex) ,alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def Level4_play(map_input):
    #==========================================INIT MAP=================================================================
    global score
    map = map_input[0]
    pac_pos = map_input[1]
    food = map_input[2]
    monster = map_input[3]
    wall = map_input[4]
    luffy = Luffy.luffy_right
    mouse = Mouse.mouse_left
    meat = Food.meat
    mouse_list = monster
    endings = Luffy.endings
    ending_check = False
    #=========================================INIT STATE===================================================
    list_ghost = []
    for x in monster:
        list_ghost.append(Ghost.Ghost(x[0],x[1]))
    pacman = Pacman.Pacman(pac_pos[0],pac_pos[1])
    init_state = State.State(pacman, list_ghost, food, wall)
    #============================================DRAW MAP=============================================================
    for i in range(len(endings)):
        endings[i] = pygame.transform.scale(endings[i], (WIDTH, HEIGHT))
    running = True
    screen.blit(game_bg, (0, 0))
    Map.create_map(map, screen, CELL_SIZE)
    screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[0] * CELL_SIZE))
    for x, y in mouse_list:
        screen.blit(mouse, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
    for x, y in food:
        screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
    pygame.display.update()
    #===========================================RUN GAME====================================================================
    agentIndex = 0
    numAgents = init_state.getNumAgents()
    wining = False
    luffy_path = []
    mouse_path = [] 
    new_ghost_positions = [] 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not wining:
            agents = init_state.getAgents()
            agent = agents[agentIndex]
            actions = None
            PosibleActions = getObservation(agent.get_pos(), wall)
            # print("Posible action {}:".format(i), PosibleActions)
            alpha = -999999
            beta = 999999  

            screen.blit(game_bg, (0, 0))
            Map.create_map(map, screen, CELL_SIZE)

            state_recusive = init_state.copy()
            if agentIndex==0:
                action_scores = [alphabeta(agents, 0, 0, state_recusive.update(Pacman.Pacman(action[0],action[1]), 0), alpha, beta) for action in PosibleActions]
            else:
                action_scores = [alphabeta(agents, 0, 0, state_recusive.update(Ghost.Ghost(action[0],action[1]), 1), alpha, beta) for action in PosibleActions]
            max_action = max(action_scores)
            max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
            chosenIndex = random.choice(max_indices)
            res = PosibleActions[chosenIndex]
            
            # cap nhat lai map
            if agentIndex == 0:
                # print("Pacman turn: ")
                luffy_path.append(res)
                new_pacman_pos = (res[0], res[1])
                new_pacman = Pacman.Pacman(new_pacman_pos[0], new_pacman_pos[1])
            else:
                # print("Mause turn: ")
                new_ghost_positions.append((res[0], res[1]))
                mouse_path.append(res)

            if agentIndex + 1 == numAgents:
                screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + luffy_path[0][1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + luffy_path[0][0] * CELL_SIZE))
                for x in mouse_path:
                    screen.blit(mouse, (get_map_pos_y(map, CELL_SIZE) + x[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x[0] * CELL_SIZE))
                pygame.display.update()
                luffy_path = []
                mouse_path = []
                new_ghosts = [Ghost.Ghost(new_pos[0], new_pos[1]) for new_pos in new_ghost_positions]

                new_food = init_state.list_food[:]
                if new_pacman_pos in new_food:
                    new_food.remove(new_pacman_pos)
                    print(len(new_food))
                init_state = State.State(new_pacman, new_ghosts, new_food, wall)
                if (init_state.is_win()):
                    wining = True
                new_ghost_positions = []
            agentIndex = (agentIndex + 1) % numAgents
            time.sleep(0.2)
        else:
            print("You win!")
            break
    #==============================================================================================================================
