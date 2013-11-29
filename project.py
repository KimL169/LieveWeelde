import pygame, sys
from math import e, pi, cos, sin, sqrt
from random import randint
from pygame.locals import *
import datetime

pygame.init()

#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

#lijst met alle rectangles, voor collide check
houselist = []    

#define total number of houses
total_Houses = 40

#define total number of each house type
total_Maisons = int(total_Houses * 0.15) 
total_Bungalows = int(total_Houses * 0.25)
total_Eensgezins = int(total_Houses * 0.60)

#display settings
WIDTH = 640
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)


#kleurtjes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)  # = bungalow
GREEN = (  0, 255,   0) # = maison
BLUE = (  0,   0, 255) # = eensgezins
YELLOW = (250, 250, 210)


#--------------------------------
# Classes voor de huisjes
#----------------------------

class Maison():

    def __init__ (self):
        self.vrijstand = 24
        self.w = 44
        self.h = 42
        self.w_vr = 92
        self.h_vr = 90
        self.x = randint(self.vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.vrijstand
        self.y_vr = self.y - self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)  # huis als Rect zodat we de pygame rect library functions kunnen gebruiken
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = BLUE
        self.kleur_vrijstand = YELLOW

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (RED))
        screen.blit(label, (self.x_vr, self.y_vr))

    def name(self, name):
        self.name = name

    # Voor manual movement met muis
    def manual_move(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect_vr.x = pos[0]
        self.rect.y = pos[1]
        self.rect_vr.y = pos[1]  

class Bungalow():

    def __init__ (self):
        self.vrijstand = 12
        self.w = 40
        self.h = 30
        self.w_vr = 64
        self.h_vr = 54
        self.x = randint(self.vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.vrijstand
        self.y_vr = self.y - self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = RED
        self.kleur_vrijstand = YELLOW

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (BLUE))
        screen.blit(label, (self.x_vr, self.y_vr))

    def name(self, name):
        self.name = name

    # Voor manual movement met muis.
    def manual_move(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect_vr.x = pos[0]
        self.rect.y = pos[1]
        self.rect_vr.y = pos[1] 

class Eengezins():

    def __init__ (self):
        self.vrijstand = 8
        self.w = 32
        self.h = 32
        self.w_vr = 48
        self.h_vr = 48
        self.x = randint(self.vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.vrijstand
        self.y_vr = self.y - self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = GREEN
        self.kleur_vrijstand = YELLOW

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (RED))
        screen.blit(label, (self.x_vr, self.y_vr))


    def name(self, name):
        self.name = name

    # Manual movement met muis.
    def manual_move(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect_vr.x = pos[0]
        self.rect.y = pos[1]
        self.rect_vr.y = pos[1]     
        

# Collision Detect functies
#------------------------------------------------------------------

def doHousesOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.rect_vr.left, a.rect_vr.top, b)) or
            (isPointInsideRect(a.rect_vr.left, a.rect_vr.bottom, b)) or
            (isPointInsideRect(a.rect_vr.right, a.rect_vr.top, b)) or
            (isPointInsideRect(a.rect_vr.right, a.rect_vr.bottom, b))):
            return True
    return False

def isPointInsideRect(x, y, huis):
    if (x >= huis.rect_vr.left) and (x <= huis.rect_vr.right) and (y >= huis.rect_vr.top) and (y <= huis.rect_vr.bottom):
        return True
    else:
        return False

def overlapCheck(huisje):

    for house in houselist:

        if doHousesOverlap(huisje, house) == True:
            return True

    return False


# Distance measure function
#-----------------------------------------------------------------

def measureDistance():
    filename = "distances_%dHuizen_%d.txt" % (total_Houses, randint(0,10000000)) #tijdelijk
    f = open(filename, 'w')
    for a in houselist:
        for b in houselist:
            #check so it's not measuring distance to itself.
            if b != a:
                distance = "%s > %s:  x%d, y%d\n" % (a.name, b.name, a.rect.left - b.rect.left, a.rect.top - b.rect.top)
                f.write(distance)

def positionHelper(a, b):
    if b.rect_vr.bottom - a.rect_vr.top > 0:
        # all b.y are above a.y
        if b.rect_vr.left - a.rect_vr.right > 0:
            # house B is top right of house A  (diagonal top right)
            return 'topright'
        elif a.rect_vr.left - b.rect_vr.right > 0:
            # house B is top left of house A (diagonal top left)
            return 'topleft'
        elif b.rect_vr.left - a.rect_vr.right < 0:

            if b.rect_vr.left - a.rect_vr.left > 0:
                # b is above a (vertical Top)
                return 'top'
            elif b.rect_vr.right - a.rect_vr.left > 0:
                # b is above a (vertical Top)
                return 'top'
    if b.rect_vr.bottom - a.rect_vr.top < 0:

        if a.rect_vr.bottom - b.rect_vr.top > 0:
            # all b.y are below a.y
            if b.rect_vr.left - a.rect_vr.right > 0:
                # house B is bottom right of house A  (diagonal bottom right)
                return 'bottomright'
            elif a.rect_vr.left - b.rect_vr.right > 0:
                # house B is bottom left of house A (diagonal bottom left)
                return 'bottomleft'
            elif b.rect_vr.left - a.rect_vr.right < 0:

                if b.rect_vr.left - a.rect_vr.left > 0:
                    # b is above a (vertical bottom)
                    return 'bottom'
                elif b.rect_vr.right - a.rect_vr.left > 0:
                    # b is above a (vertical bottom)  
                    return 'bottom'   

        elif a.rect_vr.bottom - b.rect_vr.top < 0:
            # house b is either to the left or to the right of house a (horizontal)
            if b.rect_vr.left - a.rect_vr.right > 0:
                # house B is to the right of house A  (horizontal right)
                return 'right'
            elif a.rect_vr.left - b.rect_vr.right > 0: 
                # house B is to the left of house a  (horizontal left)
                return 'left'

def houseposition():
    for a in houselist:
        for b in houselist:
            if b != a:
                print "%s > %s:  %s" % (a.name, b.name, positionHelper(a, b))


#------------------------------------------------------------------
# Main program loop                                                                                                   
#------------------------------------------------------------------


while True:

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_q: # return to main
                    screen.fill(BLACK)
                
                counter_m = 0
                counter_b = 0
                counter_e = 0
                if event.key == K_g: # place houses on screen

                    while counter_m < total_Maisons:

                        maison = Maison() 

                        if overlapCheck(maison) == False:
                            counter_m += 1
                            naam = "%dm" % (counter_m)
                            maison.name(naam)
                            houselist.append(maison)

                        
                    while counter_b < total_Bungalows:

                        bungalow = Bungalow() 

                        if overlapCheck(bungalow) == False:
                            counter_b += 1
                            naam = "%db" % (counter_b)
                            bungalow.name(naam)
                            houselist.append(bungalow)

                    while counter_e < total_Eensgezins:

                        eengezins = Eengezins() 

                        if overlapCheck(eengezins) == False:
                            counter_e += 1
                            naam = "%de" % (counter_e)
                            eengezins.name(naam)
                            houselist.append(eengezins)
                    

                    for house in houselist:
                        house.render()

                    pygame.display.update()

                #even tijdelijke test om de huisjes rond te bewegen. 
                if event.key == K_o: #move all houses one place to the left.
                    screen.fill(BLACK)
                    house.rect.x += 10
                    house.rect_vr.x += 10
                    for house in houselist:
                        house.render()
                    pygame.display.update()
                if event.key == K_m:
                    houseposition()

