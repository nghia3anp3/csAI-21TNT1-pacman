from Variables import *

dora_left = pygame.image.load("images/dora_left.png")
dora_right = pygame.image.load("images/dora_right.png")
dora_full = pygame.image.load("images/full.png")
dora_left = pygame.transform.scale(dora_left, (CELL_SIZE, CELL_SIZE))
dora_right = pygame.transform.scale(dora_right, (CELL_SIZE, CELL_SIZE))
dora_full = pygame.transform.scale(dora_full, (CELL_SIZE, CELL_SIZE))