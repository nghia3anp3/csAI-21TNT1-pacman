from Variables import *

dora_left = pygame.image.load("images/dora_left.png")
dora_right = pygame.image.load("images/dora_right.png")
dora_full = pygame.image.load("images/full.png")
dora_left = pygame.transform.scale(dora_left, (CELL_SIZE, CELL_SIZE))
dora_right = pygame.transform.scale(dora_right, (CELL_SIZE, CELL_SIZE))
dora_full = pygame.transform.scale(dora_full, (CELL_SIZE, CELL_SIZE))
endings = [pygame.image.load("images/endings/1.png"),pygame.image.load("images/endings/2.png"),pygame.image.load("images/endings/3.png"),pygame.image.load("images/endings/4.png"),pygame.image.load("images/endings/5.png"),pygame.image.load("images/endings/6.png"),pygame.image.load("images/endings/7.png"),pygame.image.load("images/endings/8.png"),pygame.image.load("images/endings/9.png"),pygame.image.load("images/endings/10.png"),pygame.image.load("images/endings/11.png"),pygame.image.load("images/endings/12.png"),pygame.image.load("images/endings/13.png"),pygame.image.load("images/endings/14.png"),pygame.image.load("images/endings/15.png"),pygame.image.load("images/endings/16.png"),pygame.image.load("images/endings/17.png"),pygame.image.load("images/endings/18.png"),pygame.image.load("images/endings/19.png"),pygame.image.load("images/endings/20.png")]