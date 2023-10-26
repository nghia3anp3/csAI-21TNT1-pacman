from Variables import *
import Button

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

game_paused = False
menu_state = "main"

font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255, 255, 255)


options_img = pygame.image.load("images/Button_options.png").convert_alpha()
quit_img = pygame.image.load("images/Button_quit.png").convert_alpha()
back_img = pygame.image.load('images/Button_back.png').convert_alpha()

play_Button = Button.Button(250, 250, options_img, 1)
options_Button = Button.Button(297, 250, options_img, 1)
quit_Button = Button.Button(336, 375, quit_img, 1)
back_Button = Button.Button(332, 450, back_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

run = True
while run:
  screen.fill((52, 78, 91))
  if game_paused == True:
    if menu_state == "main":
      if options_Button.draw(screen):
        menu_state = "options"
      if quit_Button.draw(screen):
        run = False
    if menu_state == "options":
      if back_Button.draw(screen):
        menu_state = "main"
  else:
    draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()