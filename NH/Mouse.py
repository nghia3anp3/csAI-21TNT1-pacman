from Variables import *

mouse_left = pygame.image.load("images/mouse_left.png")
mouse_right = pygame.image.load("images/mouse_right.png")
mouse_left = pygame.transform.scale(mouse_left, (CELL_SIZE, CELL_SIZE))
mouse_right = pygame.transform.scale(mouse_right, (CELL_SIZE, CELL_SIZE))