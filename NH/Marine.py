from Variables import *

marine_left = pygame.image.load("images/marine_left.png")
marine_right = pygame.image.load("images/marine_right.png")
marine_left = pygame.transform.scale(marine_left, (CELL_SIZE, CELL_SIZE))
marine_right = pygame.transform.scale(marine_right, (CELL_SIZE, CELL_SIZE))