# from Variables import *
# import Level12
# import pygame
# import time
# import sys
#
#
# # Main loop
# if __name__ == "__main__":
#     Level12.Level12()
import State
import Level12
import Level4_play
from Variables import *
import pygame, sys
from Button import Button
import Map
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Piece Pacman")

BG = pygame.transform.scale(pygame.image.load("images/Background.png"),(WIDTH,HEIGHT))
LOGO = pygame.transform.scale(pygame.image.load("images/logo.png"),(500,300))
map_pos = 0
def get_font(size):  # Returns Press-Start-2P in the desired size
  return pygame.font.Font("font/font.ttf", size)


def play():
  while True:
    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    screen.fill("black")

    PLAY_TEXT = get_font(45).render("Choose level:", True, "White")
    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 50))
    screen.blit(PLAY_TEXT, PLAY_RECT)

    PLAY_LEVEL1 = Button(image=None, pos=(640, 150),
                       text_input="LEVEL 1", font=get_font(40), base_color="White", hovering_color="Green")
    PLAY_LEVEL2 = Button(image=None, pos=(640, 250),
                       text_input="LEVEL 2", font=get_font(40), base_color="White", hovering_color="Green")
    PLAY_LEVEL3 = Button(image=None, pos=(640, 350),
                       text_input="LEVEL 3", font=get_font(40), base_color="White", hovering_color="Green")
    PLAY_LEVEL4 = Button(image=None, pos=(640, 450),
                       text_input="LEVEL 4", font=get_font(40), base_color="White", hovering_color="Green")
    PLAY_BACK = Button(image=None, pos=(640, 600),
                       text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

    for button in [PLAY_LEVEL1, PLAY_LEVEL2, PLAY_LEVEL3, PLAY_LEVEL4, PLAY_BACK]:
      button.changeColor(PLAY_MOUSE_POS)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_LEVEL1.checkForInput(PLAY_MOUSE_POS):
          Level1()
        if PLAY_LEVEL2.checkForInput(PLAY_MOUSE_POS):
          Level2()
        if PLAY_LEVEL3.checkForInput(PLAY_MOUSE_POS):
          Level3()
        if PLAY_LEVEL4.checkForInput(PLAY_MOUSE_POS):
          Level4()
        if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
          main_menu()

    pygame.display.update()

def Level1():
  global map_pos
  Level12.Level12(map_dict['Level1'][map_pos])
def Level2():
  return
def Level3():
  return
def Level4():
  global map_pos
  Level4_play.Level4_play(map_dict['Level4'][0])
def options():
  global map_pos
  while True:
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    screen.fill("BLACK")
    Map.create_map(change_map_list[map_pos], screen, 15)
    OPTIONS_PREVIOUS = Button(image=None, pos=(300, 360),
                         text_input="<", font=get_font(40), base_color="White", hovering_color="Green")
    OPTIONS_NEXT = Button(image=None, pos=(980, 360),
                         text_input=">", font=get_font(40), base_color="White", hovering_color="Green")
    OPTIONS_BACK = Button(image=None, pos=(640, 600),
                       text_input="CONFIRM", font=get_font(20), base_color="White", hovering_color="Green")
    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(screen)

    for button in [OPTIONS_PREVIOUS, OPTIONS_NEXT, OPTIONS_BACK]:
      button.changeColor(OPTIONS_MOUSE_POS)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
          main_menu()
        if OPTIONS_PREVIOUS.checkForInput(OPTIONS_MOUSE_POS):
          if map_pos == 0:
            map_pos = len(change_map_list)-1
          else:
            map_pos -=1
        if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
          if map_pos == len(change_map_list) - 1:
            map_pos = 0
          else:
            map_pos += 1

    pygame.display.update()


def main_menu():
  while True:
    screen.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(30).render("Pac Man but in......", True, BLACK)
    MENU_RECT = MENU_TEXT.get_rect(center=(400, 50))

    PLAY_BUTTON = Button(image=None, pos=(640, 250),
                         text_input="PLAY", font=get_font(50), base_color=BLACK, hovering_color="White")
    OPTIONS_BUTTON = Button(image=None, pos=(640, 400),
                            text_input="OPTIONS", font=get_font(50), base_color=BLACK, hovering_color="White")
    QUIT_BUTTON = Button(image=None, pos=(640, 550),
                         text_input="QUIT", font=get_font(50), base_color=BLACK, hovering_color="White")

    screen.blit(MENU_TEXT, MENU_RECT)

    LOGO_RECT = LOGO.get_rect(center=(400,150))
    screen.blit(LOGO, LOGO_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()  
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
          play()
        if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
          options()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
          pygame.quit()
          sys.exit()

    pygame.display.update()


main_menu()