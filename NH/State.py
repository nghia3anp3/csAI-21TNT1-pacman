import Astar
import Luffy
import Food
import Marine
from Variables import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
luffy = Luffy.luffy_right
marine = Marine.marine_left
meat = Food.meat

def getObservation(agents_pos, wall, marine_pos=None):
    legalPath = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 and y != 0) or (abs(x) + abs(y) != 2):
                new_pos = (agents_pos[0] + x, agents_pos[1] + y)
                if (marine_pos != None):
                    if new_pos not in wall and new_pos not in marine_pos:
                        legalPath.append(new_pos)
                else:
                    if new_pos not in wall:
                        legalPath.append(new_pos)
    return legalPath


def getObservation_2(agents_pos, wall, marine_pos=None):
    legalPath = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            new_pos = (agents_pos[0] + x, agents_pos[1] + y)
            if (marine_pos != None):
                if new_pos not in wall and new_pos not in marine_pos:
                    legalPath.append(new_pos)
            else:
                if new_pos not in wall:
                    legalPath.append(new_pos)
    return legalPath


class State():

    def __init__(self, pacman, list_ghost, list_food, wall, map, score=0) -> None:
        self.pacman = pacman
        self.list_ghost = list_ghost
        self.score = score
        self.list_food = list_food
        self.wall = wall
        self.map = map

    def repain(self):
        map = self.map
        marine_list = [x.get_pos() for x in self.list_ghost]
        food = [x for x in self.list_food]
        pac_pos = self.pacman.get_pos()
        screen.blit(luffy, (
        get_map_pos_y(map, CELL_SIZE) + pac_pos[1] * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + pac_pos[0] * CELL_SIZE))

        for x, y in food:
            if (x, y) not in marine_list:
                screen.blit(meat, (
                get_map_pos_y(map, CELL_SIZE) + y * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x * CELL_SIZE))
        for x, y in marine_list:
            screen.blit(marine,
                        (get_map_pos_y(map, CELL_SIZE) + y * CELL_SIZE, get_map_pos_x(map, CELL_SIZE) + x * CELL_SIZE))
        text = get_font(30).render(f"Score: {self.score}", True, BLACK)
        screen.blit(text, (10, 10))
        pygame.display.update()

    def copy(self):
        new_pacman = self.pacman
        new_list_ghost = [ghost.copy() for ghost in self.list_ghost]
        new_list_food = self.list_food.copy()
        new_wall = self.wall.copy()
        new_score = self.score
        new_map = self.map
        new_state = State(new_pacman, new_list_ghost, new_list_food, new_wall, new_map, new_score)
        return new_state

    def get_astar(self, index):
        pac_pos = self.pacman.get_pos()
        ghost_pos = self.list_ghost[index].get_pos()
        if (Astar.lv4_astar(self.map, pac_pos, ghost_pos) == None):
            return 0
        return len(Astar.astar(self.map, pac_pos, ghost_pos))

    def update(self, new_value, index, depth=None):
        if index == 0:
            new_food = self.list_food
            if new_value.get_pos() in self.list_food:
                new_food.remove(new_value.get_pos())
                self.score += 20
                self.score -= 1
            else:
                self.score -= 1
            self.pacman = new_value
            self.list_food = new_food
        else:
            self.list_ghost[index - 1] = new_value

    def is_win(self):
        if not self.list_food:
            return True
        return False

    def is_lose(self):
        pacman_pos = self.pacman.get_pos()
        for ghost in self.list_ghost:
            ghost_pos = ghost.get_pos()
            if pacman_pos == ghost_pos:
                return True
        return False

    def update_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def manhattanDistance(self, xy1, xy2):
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def get_total_distance_to_ghost(self):
        total = 0
        for index in range(len(self.list_ghost)):
            distance = self.get_astar(index)
            total += distance
        return total

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
            if (Astar.astar(self.map, pac_pos, self.list_food[index]) == None):
                distance = 0
            else:
                distance = len(Astar.astar(self.map, pac_pos, self.list_food[index]))
            if distance < min_distance:
                min_distance = distance

        return min_distance

    def eval_state(self, depth=None):
        pacman_pos = self.pacman.get_pos()
        min_distance = 999
        max_distance = -999
        for food_pos in self.list_food:
            distance = self.manhattanDistance(pacman_pos, food_pos)
            if distance < min_distance:
                min_distance = distance
            elif distance > max_distance:
                max_distance = distance

        total_ghost_distance = self.get_total_distance_to_ghost()
        min_ghost_distance = self.get_min_distance_to_ghost()

        if (self.is_win()):
            print("win")
            return 999999999

        elif (self.is_lose()):
            return -999999999

        elif min_ghost_distance <= 3:
            if (depth != None):
                return -99999 + depth + max_distance + self.score
            else:
                return -99999 + self.score
        return self.score + min_ghost_distance - total_ghost_distance - min_distance

    def getNumAgents(self):
        return len(self.list_ghost) + 1

    def getAgents(self):
        ret = []
        ret.append(self.pacman)
        for x in self.list_ghost:
            ret.append(x)
        return ret

    def check_obs(self):
        marine_pos = []
        obs_ghost = []
        for x in self.list_ghost:
            marine_pos.append(x.get_pos())
            for i in getObservation_2(x.get_pos(), self.wall):
                obs_ghost.append(i)
        obs_pac = getObservation_2(self.pacman.get_pos(), self.wall, marine_pos)
        for x in obs_pac:
            if x not in obs_ghost:
                print("khong co")
                return False
        return True
