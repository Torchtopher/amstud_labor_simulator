# making a game that simulates what the life of a laborer would be in the 1800s
# clone of cookie clicker essentially but difficult

import pygame
import random
import time
import math
import os
import sys
import textwrap
pygame.init()

DIALOGUE = ["Hello there I am Orestes. You are a factory worker in the 1800s. Your goal is to survive. If you are lucky you might have a chance to live a miserable life. More than likley you wil die.              Click anywhere to continue."]
DIALOGUE.append("To play, simply click the loom, after you click enough times you will get your weekly wage. However be warned, you need to pay for food and housing, as well as other random costs that come up. If you don't have enough money to pay for these things you will die. Click anywhere to continue.")
DIALOGUE.append("You can track your progress in the top right corner. When you character has pushed the rock to the top of the hill, you will have won the game. Click anywhere to continue.")
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
LIGHT_RED = (255, 128, 128)

# make a window
WIDTH = 1920
HEIGHT = 1080

# display the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laborer's Life")

#  main loop
running = True

# load background image
background = pygame.image.load("factory.jpeg")
# resize background image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# load character image
character = pygame.image.load("orestes_face.jpg")
# resize character image to be 50% bigger
character = pygame.transform.scale(character, (int(character.get_width()*1.5), int(character.get_height()*1.5)))

# load speech bubble image
speech_bubble = pygame.image.load("speechbubble.png")
# fill inside of speech bubble with white
#speech_bubble.fill(WHITE)
# scale down by 50%
speech_bubble = pygame.transform.scale(speech_bubble, (int(speech_bubble.get_width()*0.5), int(speech_bubble.get_height()*0.5)))
print(speech_bubble.get_width(), speech_bubble.get_height())
print("------------------")

# make a simple rectangle that can be clicked on to get money
class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

# rectangle for money
money_rect = Rectangle(100, 100, 100, 100, WHITE)
money = 0

user_has_into = False
draw_text = True 

def talk(text):
    # make character talk
    # make speech bubble above character's head
    # make text appear in speech bubble
    # also wrap text so it fits in the speech bubble
    STARTING_X = 325
    STARTING_Y = HEIGHT-character.get_height()-speech_bubble.get_height()+450
    FONT_SIZE = 30
    FONT = pygame.font.SysFont("Arial", FONT_SIZE)
    # wrap text
    text = textwrap.wrap(text, width=30)
    # draw text
    for line in text:
        screen.blit(FONT.render(line, True, BLACK), (STARTING_X, STARTING_Y))
        STARTING_Y += 30


current_text = ""
while running:
    pos = pygame.mouse.get_pos()



    # draw background
    screen.blit(background, (0, 0))

    # blit character to the bottom left
    screen.blit(character, (0, HEIGHT-character.get_height()))
    # draw speech bubble above charact5r's head
    if draw_text:
        screen.blit(speech_bubble, (200, HEIGHT-character.get_height()-speech_bubble.get_height()+350))
        talk(current_text  )
    money_rect.draw()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if user_has_into:
                # click off of dialogue
                draw_text = False
            if not user_has_into:
                current_text = DIALOGUE.pop(0)
                if len(DIALOGUE) == 0:
                    user_has_into = True

            # check if money_rect was clicked
            if money_rect.click(pos):
                print(f"clicked {money} ")
                # add money
                money += 1
                draw_text = not draw_text
    # flip the display
    pygame.display.flip()