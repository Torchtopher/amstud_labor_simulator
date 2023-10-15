# making a game that simulates what the life of a laborer would be in the 1800s
# clone of cookie clicker essentially but difficult

import pygame
import random
import time
import math
import os
import sys
import textwrap
import random
pygame.init()

REASONS_FOR_DEATH = ["Prolonged exposure to toxic chemicals in the air.", "Fatal accident with machinery.", "Dehydration from exhuastion"]

REASONS_FOR_INJURY = ["Broken arm from machinery.", "Burns from hot metal.", "Cuts from sharp metal.", "Inhaling toxic chemicals."]

DIALOGUE = ["Hello there I am Orestes. You are a factory worker in the 1800s. Your goal is to survive. If you are lucky you might have a chance to live a miserable life. More than likley you wil die.              Click anywhere to continue."]
DIALOGUE.append("To play, simply click the loom, after you click enough times you will get your weekly wage. If you don't have enough money to pay for living things you will die. Click anywhere to continue.")
DIALOGUE.append("Now you may notice that clicking a black box is not very fun. You are correct. Do you work or you will die. Click anywhere to continue.")
DIALOGUE.append("You can track your progress in the top right corner. When you are able to buy your own house, you will have won the game. Click anywhere to continue.")
DIALOGUE.append("The house you are trying to buy costs $900. Good luck. Click anywhere to continue.")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
LIGHT_RED = (255, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0) 

# make a window
WIDTH = 1920
HEIGHT = 1080

# display the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("images/Laborer's Life")

#  main loop
running = True

# load background image
background = pygame.image.load("images/factory.jpeg")
# resize background image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# load character image
character = pygame.image.load("images/orestes_face.jpg")
# resize character image to be 50% bigger
character = pygame.transform.scale(character, (int(character.get_width()*1.5), int(character.get_height()*1.5)))

# load speech bubble image
speech_bubble = pygame.image.load("images/speechbubble.png")

# scale down by 50%
speech_bubble = pygame.transform.scale(speech_bubble, (int(speech_bubble.get_width()*0.5), int(speech_bubble.get_height()*0.5)))

sound_effects = []
# load sound effects
for file in os.listdir("images"):
    if file.endswith(".wav"):
        sound_effects.append(pygame.mixer.Sound(os.path.join("images", file)))

# play all for intro
for sound in sound_effects:
    sound.play()


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
money_rect = Rectangle(100, 300, 200, 200, BLACK)
# move rectangle to right side of screen
money_rect.rect.x = WIDTH-money_rect.rect.width-100
clicks_since_last_pay = 0
needed_clicks = random.randint(10, 20) 
total_clicks = 0 
money = 0
user_has_into = False
draw_text = True 
current_text = ""
progress = 0
progress_MAXWIDTH = 500
injury_state = [False, 0]

def _talk(text):
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


def say_message(text):
    global draw_text
    global current_text
    draw_text = True
    current_text = text
    
def advance_intro():
    global current_text
    global user_has_into
    if draw_text:
        screen.blit(speech_bubble, (200, HEIGHT-character.get_height()-speech_bubble.get_height()+350))
        _talk(current_text)
    current_text = DIALOGUE.pop(0)
    if len(DIALOGUE) == 0:
        user_has_into = True

def injury_screen(msg):
    global money
    FONT = pygame.font.SysFont("Arial", 70)
    say_message("You have been injured: " + msg + " You will be unable to work for a while and have lost money.")
    if random.randint(1, 2) == 1:
        money /= 2
    else:
        money -= 10
    pygame.display.flip()
    pygame.display.update()
    # stop all sound effects
    for sound in sound_effects:
        sound.stop()
    injury_state[0] = True   

def die_screen(msg=None):
    # make screen go black
    screen.fill(BLACK)
    # display text in red and different font
    FONT = pygame.font.SysFont("Arial", 100)
    tiny_font = pygame.font.SysFont("Arial", 60)

    screen.blit(FONT.render("You died:", True, RED), (WIDTH/2-100, HEIGHT/2-100))
    if msg:
        screen.blit(tiny_font.render(msg, True, RED), (WIDTH/2-900, HEIGHT/2))
    pygame.display.flip()
    time.sleep(3)
    # launch game again and kill this one
    os.execl(sys.executable, sys.executable, *sys.argv)

def win_screen():
    # make screen go black
    screen.fill(BLACK)
    # display text in red and different font
    FONT = pygame.font.SysFont("Arial", 70)

    screen.blit(FONT.render("You won? At what cost though...", True, GREEN), (WIDTH/2-700, HEIGHT/2-100))
    for sound in sound_effects:
        sound.stop()
    pygame.display.flip()
    time.sleep(6)
    # launch game again and kill this one
    os.execl(sys.executable, sys.executable, *sys.argv)

def safe_div(a, b):
    if b == 0:
        return 0
    else:
        return a/b

last_update = time.time()

was_in_debt = False 

while running:
    if money >= 900: 
        win_screen()
    # every 7 seconds, subtract weekly expenses from money
    if user_has_into and time.time() - last_update >= 7:
        money -= 3
        if money < 0:
            if was_in_debt:
                die_screen(msg="You were unable to pay for living expenses")
            was_in_debt = True
   
        last_update = time.time()

    pos = pygame.mouse.get_pos()

    # draw background
    screen.blit(background, (0, 0))
    # progress bar for money out of 900
    progress = min(safe_div(money, 900), 1)*progress_MAXWIDTH


    screen.blit(pygame.font.SysFont("Arial", 60).render("Progress:", True, BLUE), (100, 50))
    # blit rectangle for progress bar
    pygame.draw.rect(screen, BLUE, (100, 125, progress, 50))
    pygame.draw.rect(screen, BLACK, (100, 125, progress_MAXWIDTH, 50), 5)

    # blit character to the bottom left
    screen.blit(character, (0, HEIGHT-character.get_height()))
    # draw speech bubble above charact5r's head
    if draw_text:
        screen.blit(speech_bubble, (200, HEIGHT-character.get_height()-speech_bubble.get_height()+350))
        _talk(current_text)
    else:
        # display money in top right corner
        FONT = pygame.font.SysFont("Arial", 60)
        screen.blit(FONT.render(f"Money: ${money}", True, BLACK), (WIDTH-400, 100))

    money_rect.draw()
    # start intro dialogue
    if current_text == "" and not user_has_into:
        advance_intro()
    
    if random.randint(1, 4000) == 1 and not injury_state[0]:
        injury_screen(msg=random.choice(REASONS_FOR_INJURY))
    
    if injury_state[0]:
        injury_state[1] += 1
        if injury_state[1] >= 700:
            injury_state[0] = False
            injury_state[1] = 0
            draw_text = False
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if total_clicks % 100 == 0 and total_clicks != 0:
                injury_screen(msg=random.choice(REASONS_FOR_INJURY))
            if not user_has_into:
                advance_intro()
                if user_has_into:
                    # click off of dialogue
                    draw_text = False
            # check if money_rect was clicked
            if money_rect.click(pos):
                # play sound effect randomly 
                if random.randint(1, 3) == 1:
                    sound_effects[random.randint(0, len(sound_effects)-1)].play()
                
                if random.randint(1, 1000) == 1:
                    die_screen(msg=random.choice(REASONS_FOR_DEATH))
                
                clicks_since_last_pay += 1
                total_clicks += 1
                print(f"clicked {total_clicks} times ")

            if clicks_since_last_pay >= needed_clicks:
                money += round(random.random()*2, 2)
                money = round(money, 2)
                clicks_since_last_pay = 0
                needed_clicks = random.randint(5, 10)

            
    # flip the display
    pygame.display.flip()