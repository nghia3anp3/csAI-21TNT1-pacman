from Variables import *

luffy_left = pygame.image.load("images/luffy_left.png")
luffy_right = pygame.image.load("images/luffy_right.png")
luffy_left = pygame.transform.scale(luffy_left, (CELL_SIZE, CELL_SIZE))
luffy_right = pygame.transform.scale(luffy_right, (CELL_SIZE, CELL_SIZE))

class Pacman:
    def __init__(self, pos_x, pos_y, agent=0) -> None:
        self.x = pos_x
        self.y = pos_y
        self.agent = agent

    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def copy(self):
        new_pacman = Pacman(self.x, self.y, self.agent)
        return new_pacman