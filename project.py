import pygame, sys
from math import e, pi, cos, sin, sqrt
from random import randint
from pygame.locals import *

pygame.init()

#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

#lijst met alle rectangles, voor collide check
houselist = []    

#define total number of houses
total_Houses = 60

#define total number of each house type
total_Maisons = int(total_Houses * 0.15) 
total_Bungalows = int(total_Houses * 0.25)
total_Eensgezins = int(total_Houses * 0.60)

#display settings
WIDTH = 320
HEIGHT = 240
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)


#kleurtjes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)  # = bungalow
GREEN = (  0, 255,   0) # = maison
BLUE = (  0,   0, 255) # = eensgezins
YELLOW = (250, 250, 210)

x,y = 0, 0



#--------------------------------
# Classes voor de huisjes
#----------------------------

class Maison():

    def __init__ (self):
        self.vrijstand = 12
        self.w = 22
        self.h = 21
        self.w_vr = 46
        self.h_vr = 45
        self.x = randint(self.w_vr, WIDTH-self.w_vr)
        self.y = randint(self.h_vr, HEIGHT-self.h_vr)
        self.x_vr = self.x + self.vrijstand
        self.y_vr = self.y + self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)  # huis als Rect zodat we de pygame rect library functions kunnen gebruiken
        self.rect_vrijstand = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = BLUE
        self.kleur_vrijstand = YELLOW

    def render(self):
        self.total = pygame.draw.rect(screen, self.kleur_vrijstand, (self.x, self.y, self.w_vr, self.h_vr))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x_vr, self.y_vr, self.w, self.h))

    def name(self, name):
        self.name = name

class Bungalow():

    def __init__ (self):
        self.vrijstand = 6
        self.w = 20
        self.h = 15
        self.w_vr = 32
        self.h_vr = 27
        self.x = randint(self.w_vr, WIDTH-self.w_vr)
        self.y = randint(self.h_vr, HEIGHT-self.h_vr)
        self.x_vr = self.x + self.vrijstand
        self.y_vr = self.y + self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vrijstand = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = RED
        self.kleur_vrijstand = YELLOW

    def render(self):
        self.total = pygame.draw.rect(screen, self.kleur_vrijstand, (self.x, self.y, self.w_vr, self.h_vr))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x_vr, self.y_vr, self.w, self.h))

    def name(self, name):
        self.name = name

class Eengezins():

    def __init__ (self):
        self.vrijstand = 4
        self.w = 16
        self.h = 16
        self.w_vr = 24
        self.h_vr = 24
        self.x = randint(self.w_vr, WIDTH-self.w_vr)
        self.y = randint(self.h_vr, HEIGHT-self.h_vr)
        self.x_vr = self.x + self.vrijstand
        self.y_vr = self.y + self.vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vrijstand = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = GREEN
        self.kleur_vrijstand = YELLOW

    def render(self):
        self.total = pygame.draw.rect(screen, self.kleur_vrijstand, (self.x, self.y, self.w_vr, self.h_vr))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x_vr, self.y_vr, self.w, self.h))

    def name(self, name):
        self.name = name


# Collision Detect functies
#------------------------------------------------------------------
'''
def overlapDetect(x1, y1, w1, h1, x2, y2, w2, h2):
    
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):

        return true

    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):

        return true

    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):

        return true
        
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):

        return true

    else: 

        return false

def collisionDetect(x, y, w, h, houselist):

    if houselist == 0:
        return False

    for house in houselist:

        if overlapDetect(x, y, w, h, house.x, house.y, house.w, house.h) == True:
            return True

        else:
            return False
'''
'''
def doHousesOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False
def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False
'''
#------------------------------------------------------------------
# Main program loop                                                                                                   
#------------------------------------------------------------------


while True:

    random_pos = (randint(0,WIDTH), randint(0,HEIGHT))
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                #check of een toets is ingedrukt, if so, check welke en plaats het Huisje
                #alle maten van huizen zijn tijdelijk gedeeld door 5 zodat het allemaal mooi op het scherm past.
                #randint zet ze random op het scherm - de w en h van het huis+verplichtvrst zodat het allemaal op de map valt. 
            if event.type == KEYDOWN:
                if event.key == K_q: # return to main
                    screen.fill(BLACK)
                
                counter_m = 0
                counter_b = 0
                counter_e = 0
                if event.key == K_g: #go 

                    while counter_m != total_Maisons:

                        maison = Maison() #moet nog even veranderd worden naar juiste waarden

                        if maison.rect_vrijstand.collidelist(houselist) == -1:
                            counter_m += 1
                            maison.render()
                            naam = "%dm" % (counter_m)
                            maison.name(naam)
                            houselist.append(maison)

                        
                    while counter_b != total_Bungalows:

                        bungalow = Bungalow() #moet nog even veranderd worden naar juiste waarden

                        if bungalow.rect_vrijstand.collidelist(houselist) == -1:
                            counter_b += 1
                            bungalow.render()
                            naam = "%db" % (counter_b)
                            bungalow.name(naam)
                            houselist.append(bungalow)

                    while counter_e != total_Eensgezins:

                        eengezins = Eengezins() #moet nog even veranderd worden naar juiste waarden

                        if eengezins.rect_vrijstand.collidelist(houselist) == -1:
                            counter_e += 1
                            eengezins.render()
                            naam = "%de" % (counter_e)
                            eengezins.name(naam)
                            houselist.append(eengezins)
            
                    pygame.display.update()
