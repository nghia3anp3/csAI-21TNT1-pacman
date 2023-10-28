import Pacman
import Ghost

class State():

    def __init__(self, pacman, list_ghost, list_food, wall, score = 0)->None:
        self.pacman = pacman
        self.list_ghost = list_ghost
        self.score = score
        self.list_food = list_food
        self.wall = wall
    def copy(self):
            # Tạo bản sao của đối tượng State
        new_pacman = self.pacman  # Tạo bản sao của Pacman (tùy theo cách bạn đã triển khai lớp Pacman)
        new_list_ghost = [ghost.copy() for ghost in self.list_ghost]  # Tạo bản sao của danh sách Ghost
        new_list_food = self.list_food.copy()  # Tạo bản sao của danh sách đồ ăn
        new_wall = self.wall.copy()  # Tạo bản sao của danh sách tường
        new_score = self.score  # Sao chép điểm số

        # Tạo một đối tượng State mới với các bản sao đã tạo
        new_state = State(new_pacman, new_list_ghost, new_list_food, new_wall, new_score)
        return new_state
    def update(self, new_value, index):
        if index == 0:
            new_state = State(new_value, self.list_ghost, self.list_food, self.wall, self.score)
        else:
            self.list_ghost[index-1] = new_value
            new_state = State(self.pacman, self.list_ghost, self.list_food, self.wall, self.score)
        return new_state

    def is_win(self):
        if not self.list_food:
            return True
        return False
    
    def is_lose(self):
        pacman_pos = self.pacman.get_pos()
        for ghost in self.list_ghost:
            ghost_pos = ghost.get_pos()
            if pacman_pos == ghost_pos:
                self.score = 0
                return True
        return False
    
    def update_score(self, score):
        self.score += score

    def get_score(self):
        return self.score
    
    def manhattanDistance(self, xy1, xy2):
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    
    def get_min_distance_to_ghost(self):
        pacman_pos = self.pacman.get_pos()
        min_distance = float('inf')

        for ghost in self.list_ghost:
            ghost_pos = ghost.get_pos()
            distance = self.manhattanDistance(pacman_pos, ghost_pos)
            if distance < min_distance:
                min_distance = distance

        return min_distance
    
    def eval_state(self):
        pacman_pos = self.pacman.get_pos()
        min_distance = float('inf')

        for food_pos in self.list_food:
            distance = self.manhattanDistance(pacman_pos, food_pos)
            if distance < min_distance:
                min_distance = distance
        
        min_ghost_distance = self.get_min_distance_to_ghost()
        if min_ghost_distance <= 1:
            return -999999
        return self.score - min_distance
    
    def getNumAgents(self):
        return len(self.list_ghost)+1
    
    def getAgents(self):
        ret = []
        ret.append(self.pacman)
        for x in self.list_ghost:
            ret.append(x)
            test = x.get_pos()
        return ret