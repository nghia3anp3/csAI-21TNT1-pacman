from Variables import *

meat = pygame.image.load("images/meat.png")
meat = pygame.transform.scale(meat, (CELL_SIZE*0.7, CELL_SIZE*0.7))
r = meat.get_rect()
# the interesting line
r.center = meat.get_rect().center