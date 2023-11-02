from Variables import *

marine_left = pygame.image.load("images/marine_left.png")
marine_right = pygame.image.load("images/marine_right.png")
marine_left = pygame.transform.scale(marine_left, (CELL_SIZE, CELL_SIZE))
marine_right = pygame.transform.scale(marine_right, (CELL_SIZE, CELL_SIZE))


class Ghost:
    def __init__(self, pos_x, pos_y, agent=1) -> None:
        self.x = pos_x
        self.y = pos_y
        self.agent = agent

    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def copy(self):
        # Tạo một bản sao của đối tượng Ghost
        new_ghost = Ghost(self.x, self.y, self.agent)
        return new_ghost