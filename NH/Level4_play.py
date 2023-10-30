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

global max_depth
max_depth = 7

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

def getObservation(agents_pos, wall, mouse_pos=None):
    legalPath = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 or y != 0) and abs(x) + abs(y) != 2:
                new_pos = (agents_pos[0] + x, agents_pos[1] + y)
                if (mouse_pos!=None):
                    if new_pos not in wall and new_pos not in mouse_pos:
                        legalPath.append(new_pos)
                else:
                    if new_pos not in wall:
                        legalPath.append(new_pos)
    return legalPath

def alphabeta(agentList, agentIndex, depth, gameState, alpha, beta):
    new_state = gameState.copy()
    agents = new_state.getAgents()
    if new_state.is_win() or new_state.is_lose() or depth==max_depth:
        return new_state.eval_state(agentIndex)
        
    if agentIndex == 0: #maximize for pacman
        depth += 1
        global value
        value = -999999
        ghost_pos = []
        for x in agents[1:]:
            ghost_pos.append(x.get_pos())
        for action in getObservation(agents[agentIndex].get_pos(), new_state.wall, ghost_pos):
            # print("index 0 action alphabeta: ", action)
            pacman = Pacman.Pacman(action[0],action[1])
            backup_state = new_state.copy()
            new_state.update(pacman, agentIndex)
            value = max(value, alphabeta(agents, 1, depth, new_state ,alpha, beta))
            alpha = max(alpha, value)
            
            if beta <= alpha:
                del backup_state
                break
            else:
                del new_state
                new_state = backup_state.copy()
                del backup_state
        return value
    else:
        nextAgent = agentIndex + 1
        depth += 1
        if new_state.getNumAgents() == nextAgent:
            nextAgent = 0
        for action in getObservation(agents[agentIndex].get_pos(), new_state.wall):
            # print("index 1 action alphabeta: ", action)
            value = 999999
            ghost = Ghost.Ghost(action[0],action[1])
            backup_state = new_state.copy()
            new_state.update(ghost, agentIndex)
            value = min(value, alphabeta(agents, nextAgent, depth, new_state ,alpha, beta))
            beta = min(beta, value)
            if beta >= alpha:
                del backup_state
                break
            else:
                del new_state
                new_state = backup_state.copy()
                del backup_state

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
    init_state = State.State(pacman, list_ghost, food, wall, map)
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
        print("Diem: ",init_state.get_score())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not wining:
            state_recusive = init_state.copy()
            backup_state = init_state.copy()
            agents = init_state.getAgents()
            agent = agents[agentIndex]
            
            mouse_pos = []
            # print("Posible action {}:".format(i), PosibleActions)
            alpha = -999999
            beta = 999999  

            screen.blit(game_bg, (0, 0))
            Map.create_map(map, screen, CELL_SIZE)
            action_scores = []
            if agentIndex==0:
                for x in agents[1:]:
                    pos = x.get_pos()
                    mouse_pos.append(pos)
                PosibleActions = getObservation(agent.get_pos(), wall, mouse_pos)
                for action in PosibleActions:
                    state_recusive.update(Pacman.Pacman(action[0],action[1]), 0)
                    action_scores.append(alphabeta(agents, 1, 0, state_recusive, alpha, beta))
                    state_recusive = backup_state.copy()
                if len(action_scores)==0:
                    for ending in endings:
                        screen.blit(ending, (0, 0))
                        time.sleep(0.05)
                        pygame.display.update()
                max_action = max(action_scores)
                max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
                chosenIndex = random.choice(max_indices)
                # chosenIndex = max_indices[0]
                # position = [PosibleActions[index] for index in range(len(action_scores))]
                # print("Cac huong di: ", position)
                # print("Diem chon: ", max_action)
                res = PosibleActions[chosenIndex]
            else:
                # PosibleActions = getObservation(agent.get_pos(), wall)
                # for action in PosibleActions:
                #     state_recusive.update(Ghost.Ghost(action[0],action[1]), agentIndex)
                #     action_scores.append(alphabeta(agents, 0, 0, state_recusive, alpha, beta))
                #     state_recusive = backup_state.copy()
                # max_action = min(action_scores)
                path = Astar.lv4_astar(state_recusive.map, state_recusive.pacman.get_pos(), state_recusive.list_ghost[agentIndex-1].get_pos())
                res = path[-2]

            # max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
            # chosenIndex = random.choice(max_indices)
            # # chosenIndex = max_indices[0]
            # position = [PosibleActions[index] for index in range(len(action_scores))]
            # print("Cac huong di: ", position)
            # print("Diem chon: ", max_action)
            # res = PosibleActions[chosenIndex]

            print("Score la {}, res la {}, cua index {} || ".format(action_scores, res, agentIndex))
            # cap nhat lai map
            if agentIndex == 0:
                # print("Pacman turn: ")
                luffy_path.append(res)
                new_pacman_pos = (res[0], res[1])
                new_pacman = Pacman.Pacman(new_pacman_pos[0], new_pacman_pos[1])
                init_state.update(new_pacman,0)
            else:
                mouse_path.append((res[0], res[1]))
                for x in mouse_path:
                    init_state.update(Ghost.Ghost(x[0],x[1]), agentIndex)

            if agentIndex + 1 == numAgents:
                init_state.repain()
                mouse_path = []
                luffy_path=[]

                # =======================================================
                mouse_pos = [x.get_pos() for x in init_state.list_ghost]
                # if (init_state.pacman.get_pos() in mouse_pos):
                #     wining = True
                #     print("You lose!")
                #     break
                # =======================================================
                print(len(init_state.list_food))

                if (len(init_state.list_food)==0):
                    wining=True
                    for ending in endings:
                        screen.blit(ending, (0, 0))
                        time.sleep(0.05)
                        pygame.display.update()

            agentIndex = (agentIndex + 1) % numAgents
            time.sleep(0.1)
        else:
            print("You win!")
            break
    #==============================================================================================================================
