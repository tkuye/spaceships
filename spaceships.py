import os 
import sys 
import pygame 
import pygame_menu
from pygame.locals import *
import math
import random
import time

# Maybe add highscore and sound objects 
# maybe add a better play again page and make more seamless? 
# maybe add lives so you can get hit more than once
#possibly add levels with different numbers of meteors? 

# Initialize pygame and create the window used in the classes
# Initialize menu
pygame.init()
window = pygame.display.set_mode((1200, 1200))
menu = pygame_menu.Menu(600, 600, "Spaceships", theme=pygame_menu.themes.THEME_DARK) 
scores = []

# Class for the falling of the meteors within the game
class Meteor(pygame.sprite.Sprite):
    def __init__(self):

        screen = pygame.display.get_surface()
        meteors = os.path.join("data", "meteor.png")
        pygame.sprite.Sprite.__init__(self)
        # load and scale the image
        self.image = pygame.image.load(meteors)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
        self.rect = self.image.get_rect()
        # get the width and height of the display
        self.width = screen.get_width()
        self.height = screen.get_height()
        # create a move variable with speed between 5-7 to start with 
        self.move = random.randint(5, 7)
        # Starting point of the meteors, anywhere on the screen and anywhere between 0 or above display
        self.rect.topleft = random.randint(0, self.width-self.rect.width), random.randint(-self.height, 0)
        
        self.start = time.time()
        self.increment = 10
        self.counter = 1.1
        self.window = window

        # function runs within while loop, calls these functions
    def update(self):
        self._fly()
        self._speedup()
       
        # function puts meteors on the screen
    def blit(self):
        self.window.blit(self.image, self.rect.topleft)
        
        # function moves meteors back to top of screen
    def _initmet(self):
        self.rect.left = random.randrange(0, self.width-self.rect.width)
        
    
        # function that causes the meteors to move
    def _fly(self):
        position = self.rect.move(0, self.move)
        if self.rect.top > self.height:
            self.rect.top = -self.rect.height
            return self._initmet()
        self.rect = position

        # function speeds up the meteors after certain amount of time
    def _speedup(self):
        end = time.time()
        diff = end - self.start
        if diff > self.increment:
            self.counter = self.counter**1.08
            self.move += self.counter
            self.increment += 10

        # boolean function that returns true or false if meteor collides with ship
    def hit(self, target):
        return self.rect.colliderect(target)

    # Outer function that creates instances of the meteor class, args is number of meteors
def createMeteors(number=1):
    meteorlist = []
    for i in range(number):
        i = Meteor()
        meteorlist.append(i)
    return meteorlist

    # class used for fonts and updates the score for the ship
class Ship:
    def __init__(self):
        # font instance
        self.font = pygame.font.SysFont("ubuntu", 60)
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.window = window
        
        # runs in while loop to call functions
    def update(self):
        self._scorecount()
        self._renderFont()
        
        # shows font on screen with score
    def _renderFont(self):
        text = self.font.render(  str(self.score), 1, (255,255, 255))
        textpos = text.get_rect()
        textpos.centerx = 600
        textpos.top = 20
        self.window.blit(text, textpos)

        # score increment
    def _scorecount(self):
        self.score += 1

        # background class
class Background:
    """ Background class uses two images of the background,
        one that appears in the window and one is directly below,
        background moves upwards and once one of them has left the window,
        the rect location is moved back to the start"""

    def __init__(self):
        self.window = window
        background = os.path.join("data", "night.png")
        self.w,self.x,self.y,self.z = window.get_rect()
        self.bgimage = pygame.image.load(background)
        # initializes all starting points for the background
        self.bgy1 = 0 
        self.bgx1 = 0
        self.bgimage = pygame.transform.scale(self.bgimage, (self.y, self.z))
        self.bg_rect = self.bgimage.get_rect()
        self.bgx2 = 0 
        self.bgy2 = self.bg_rect.height
        self.bg_speed = 5
        self.start = time.time()
        self.increment = 10
        
        # function increments the speed every 10 second and additionally moves the rect downwards
        # if background is above the window, it's moved back to below
    def update(self):
        diff = time.time() - self.start
        if diff > self.increment:
            self.bg_speed += 1
            self.increment += 10
        self.bgy1 -= self.bg_speed
        self.bgy2 -= self.bg_speed
       
        if self.bgy1 <= -self.bg_rect.height:
            self.bgy1 = self.bg_rect.height
        if self.bgy2 <= -self.bg_rect.height:
            self.bgy2 = self.bg_rect.height
    # renders background on the screen
    def render(self):
        self.window.blit(self.bgimage, (self.bgx1, self.bgy1))
        self.window.blit(self.bgimage, (self.bgx2, self.bgy2))


# function for replacing score with the latest score so only one appears in the menu
def widget_remove(menus, scorelist):
    if len(scorelist) < 2:
        return
    else:
        menus.remove_widget(scorelist[-2])
        scorelist.pop(-2)


def main():
    # initializes everything
    explosion = os.path.join("data", "explosion.png")
    explosionimg = pygame.image.load(explosion)
    spaceship = os.path.join("data", "space.png")
    
    spaceshipimg = pygame.image.load(spaceship)
    spaceshipimg = pygame.transform.rotozoom(spaceshipimg, 0, 0.2)
    explosionimg = pygame.transform.rotozoom(explosionimg, 0, 0.5)
    space_rect = spaceshipimg.get_rect()
    # calls instances of background, ship and createsmeteors
    ship = Ship()
    meteors = createMeteors(8)
    background = Background()
    
    # creates clock instance
    clock = pygame.time.Clock()   


    
    pygame.display.set_caption("Spaceships")
    screen = pygame.display.get_surface()
    # updates screen with new instances
    pygame.display.flip()

    # spaceship starting point 
    space_rect.centerx = 600
    space_rect.centery = 600
    

    while True:

        clock.tick(60)
        # quit event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            else:
                pass
            
        # moves the keys with left and right arrows
        # additionally creates loop if ship object leaves the screen
        keys = pygame.key.get_pressed()
        if space_rect.left > screen.get_width():
            space_rect.left = -space_rect.width
        if space_rect.left < -space_rect.width:
            space_rect.left = 1200
        if keys[pygame.K_LEFT]:
            space_rect.centerx -= 7
        if keys[pygame.K_RIGHT]:
            space_rect.centerx += 7 

        
        background.update()
        background.render()
        # puts spaceship image on the screen after background 
        window.blit(spaceshipimg,space_rect)

        ship.update()
        for meteor in meteors:
            # update meteor position and moves it onto screen 
            meteor.blit()
            meteor.update()

            # check if meteor is hit 
            if meteor.hit(space_rect):
                # put new score on the menu
                scorenum = ship.score
                score = menu.add_label("Your Score: " + str(scorenum), font_size=30, key=1)
                scores.append(score)
                # calls widget remove function to remove previous score from menu
                widget_remove(menu, scores)
                # creates explosion on the screen
                meteor.window.blit(explosionimg, (space_rect.left - space_rect.width+30, space_rect.top - space_rect.height))
                # updates display one last time with explosion image
                pygame.display.flip()
                # returns function back to menu on delay 
                time.sleep(0.1)
                return
            # updates display
        pygame.display.flip()

# add the menu buttons to play and title 
menu.add_label("CLICK TO PLAY", font_size=50)
# clicking calls main function and initializes everything

menu.add_button('Play', main)
# also add quit function
menu.add_button("Quit", pygame_menu.events.EXIT)

# needed to keep menu open
menu.mainloop(window)

