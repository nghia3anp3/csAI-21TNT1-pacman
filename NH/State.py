import Pacman
import Ghost
import Astar
import Luffy
import Food
import Mouse
from Variables import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
luffy = Luffy.luffy_right
mouse = Mouse.mouse_left
meat = Food.meat
endings = Luffy.endings

class State():

    def __init__(self, pacman, list_ghost, list_food, wall, map, score =0)->None:
        self.pacman = pacman
        self.list_ghost = list_ghost
        self.score = score
        self.list_food = list_food
        self.wall = wall
        self.map = map

    def repain(self):
        map = self.map
        mouse_list = [x.get_pos() for x in self.list_ghost]
        food = [x for x in self.list_food]
        pac_pos = self.pacman.get_pos()
        screen.blit(luffy, (get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[0] * CELL_SIZE))
        for x, y in food:
            if (x,y) not in mouse_list:
                screen.blit(meat, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
        for x, y in mouse_list:
            screen.blit(mouse, (get_map_pos_y(map,CELL_SIZE)+y * CELL_SIZE,get_map_pos_x(map,CELL_SIZE)+ x * CELL_SIZE))
        pygame.display.update()
        
    def copy(self):
            # Tạo bản sao của đối tượng State
        new_pacman = self.pacman  # Tạo bản sao của Pacman (tùy theo cách bạn đã triển khai lớp Pacman)
        new_list_ghost = [ghost.copy() for ghost in self.list_ghost]  # Tạo bản sao của danh sách Ghost
        new_list_food = self.list_food.copy()  # Tạo bản sao của danh sách đồ ăn
        new_wall = self.wall.copy()  # Tạo bản sao của danh sách tường
        new_score = self.score  # Sao chép điểm số
        new_map = self.map
        # Tạo một đối tượng State mới với các bản sao đã tạo
        new_state = State(new_pacman, new_list_ghost, new_list_food, new_wall, new_map, new_score)
        return new_state
    
    def get_astar(self, index):
        pac_pos = self.pacman.get_pos()
        ghost_pos = self.list_ghost[index].get_pos()
        if (Astar.lv4_astar(self.map,pac_pos,ghost_pos)==None):
            return 0
        return len(Astar.astar(self.map,pac_pos,ghost_pos))
    def update(self, new_value, index):
        if index == 0:
            new_food = self.list_food
            if new_value.get_pos() in self.list_food:
                new_food.remove(new_value.get_pos())
                self.score += 20
            else:
                self.score -=1
            self.pacman = new_value
            self.list_food = new_food
        else:
            self.list_ghost[index-1] = new_value

    def is_win(self):
        if not self.list_food:
            return True
        # self.score = 999
        return False
    
    def is_lose(self):
        pacman_pos = self.pacman.get_pos()
        for ghost in self.list_ghost:
            ghost_pos = ghost.get_pos()
            if pacman_pos == ghost_pos:
                # self.score = -99
                return True
        return False
    
    def update_score(self, score):
        self.score += score

    def get_score(self):
        return self.score
    
    def manhattanDistance(self, xy1, xy2):
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    
    def get_min_distance_to_ghost(self):
        min_distance = 999

        for index in range(len(self.list_ghost)):
            distance = self.get_astar(index)
            if distance < min_distance:
                min_distance = distance

        return min_distance
    
    def get_min_distance_to_food(self):
        min_distance = float('inf')
        pac_pos = self.pacman.get_pos()
        for index in range(len(self.list_food)):
            if (Astar.astar(self.map,pac_pos, self.list_food[index])==None):
                distance = 0
            else:
                distance = len(Astar.astar(self.map,pac_pos, self.list_food[index]))
            if distance < min_distance:
                    min_distance = distance

        return min_distance
    

    def eval_state(self, agentIndex):
        pacman_pos = self.pacman.get_pos()
        min_distance = 999
        for food_pos in self.list_food:
            distance = self.manhattanDistance(pacman_pos, food_pos)
            if distance < min_distance:
                min_distance = distance
        min_ghost_distance = self.get_min_distance_to_ghost()
        
        # if agentIndex == 0:
        #     if (self.is_win()):
        #         return 999
        #     elif (self.is_lose()):
        #         return -999
        #     elif min_ghost_distance<=2:
        #         return -999   
        #     else:
        #         return self.score

        # else:
        if (self.is_win()):
            return 99999
        elif (self.is_lose()):
            return -99999
        elif min_ghost_distance<=2:
            return -900 
        #     else:
        #         return min_ghost_distance
        # if min_ghost_distance<=3:
        #         return -999 + min_ghost_distance
        return self.score + 2*min_ghost_distance - min_distance
    def getNumAgents(self):
        return len(self.list_ghost)+1
    
    def getAgents(self):
        ret = []
        ret.append(self.pacman)
        for x in self.list_ghost:
            ret.append(x)
        return ret