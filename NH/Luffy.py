from Variables import *

luffy_left = pygame.image.load("images/luffy_left.png")
luffy_right = pygame.image.load("images/luffy_right.png")
luffy_full = pygame.image.load("images/luffy_full.png")
luffy_left = pygame.transform.scale(luffy_left, (CELL_SIZE, CELL_SIZE))
luffy_right = pygame.transform.scale(luffy_right, (CELL_SIZE, CELL_SIZE))
luffy_full = pygame.transform.scale(luffy_full, (CELL_SIZE, CELL_SIZE))
endings = [pygame.image.load("images/endings/1.png"),pygame.image.load("images/endings/2.png"),pygame.image.load("images/endings/3.png"),pygame.image.load("images/endings/4.png"),pygame.image.load("images/endings/5.png"),pygame.image.load("images/endings/6.png"),pygame.image.load("images/endings/7.png"),pygame.image.load("images/endings/8.png"),pygame.image.load("images/endings/9.png"),pygame.image.load("images/endings/10.png"),pygame.image.load("images/endings/11.png"),pygame.image.load("images/endings/12.png"),pygame.image.load("images/endings/13.png"),pygame.image.load("images/endings/14.png"),pygame.image.load("images/endings/15.png"),pygame.image.load("images/endings/16.png"),pygame.image.load("images/endings/17.png"),pygame.image.load("images/endings/18.png"),pygame.image.load("images/endings/19.png"),pygame.image.load("images/endings/20.png")]