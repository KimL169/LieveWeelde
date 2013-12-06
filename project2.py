import pygame, sys, csv, random
from math import e, pi, cos, sin, sqrt, fabs
import math
from random import randint
from pygame.locals import *
import datetime, time

pygame.init()

#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

#lijst met alle rectangles, voor collide check
houselist = []    

# lijst met alle afstanden tot andere huizen
afstanden = []

# lijst met vrijstand voor elk huis
vrijstand = []

# variable voor de hoogste waarde tot nu toe.
Total_Value = 0

#define total number of houses
total_Houses = 20

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
RED = (255,   0,   0)  
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255) 
YELLOW = (250, 250, 170)


#--------------------------------
# Classes voor de huisjes
#----------------------------

class Maison():

    def __init__ (self):
        self.verplichte_vrijstand = 24
        self.w = 44
        self.h = 42
        self.w_vr = 92
        self.h_vr = 90
        self.x = randint(self.verplichte_vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.verplichte_vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.verplichte_vrijstand
        self.y_vr = self.y - self.verplichte_vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)  # huis als Rect zodat we de pygame rect library functions kunnen gebruiken
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.rect_extra = pygame.Rect(self.x_vr-10, self.y_vr-10, self.w_vr+20, self.h_vr+20)
        self.kleur = BLUE
        self.kleur_vrijstand = YELLOW
        self.waarde = 610000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (RED))
        screen.blit(self.label, (self.x, self.y))

    def name(self, name):
        self.name = name
        
    def price(self):
        price = float(self.waarde + ((self.vrijstand - (self.verplichte_vrijstand/4)) * (self.waarde * 0.06)))
        return price

class Bungalow():

    def __init__ (self):
        self.verplichte_vrijstand = 12
        self.w = 40
        self.h = 30
        self.w_vr = 64
        self.h_vr = 54
        self.x = randint(self.verplichte_vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.verplichte_vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.verplichte_vrijstand
        self.y_vr = self.y - self.verplichte_vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.rect_extra = pygame.Rect(self.x_vr-10, self.y_vr-10, self.w_vr+20, self.h_vr+20)
        self.kleur = RED
        self.kleur_vrijstand = YELLOW
        self.waarde = 399000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (BLUE))
        screen.blit(self.label, (self.x, self.y))

    def name(self, name):
        self.name = name

    def price(self):
        price = float(self.waarde + ((self.vrijstand - (self.verplichte_vrijstand/4)) * (self.waarde * 0.04)))
        return price

class Eengezins():

    def __init__ (self):
        self.verplichte_vrijstand = 8
        self.w = 32
        self.h = 32
        self.w_vr = 48
        self.h_vr = 48
        self.x = randint(self.verplichte_vrijstand, WIDTH-self.w_vr)
        self.y = randint(self.verplichte_vrijstand, HEIGHT-self.h_vr)
        self.x_vr = self.x - self.verplichte_vrijstand
        self.y_vr = self.y - self.verplichte_vrijstand
        self.rect =  pygame.Rect(self.x, self.y, self.w, self.h)
        self.rect_vr = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.rect_extra = pygame.Rect(self.x_vr-10, self.y_vr-10, self.w_vr+20, self.h_vr+20)
        self.kleur = GREEN
        self.kleur_vrijstand = YELLOW
        self.waarde = 285000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (RED))
        screen.blit(self.label, (self.x, self.y))


    def name(self, name):
        self.name = name

    def price(self):
        price = float(self.waarde + ((self.vrijstand - (self.verplichte_vrijstand/4)) * (self.waarde * 0.03)))
        return price

# Collision Detect functies
#------------------------------------------------------------------
def screenCapture(highest_value, total_value):

    if (highest_value == 0) or (total_value > highest_value):
        highest_value = total_value
        imagename = "1_%sh_w%d.jpg" %(total_Houses, total_value)
        pygame.image.save(screen, imagename)
        return highest_value

def doHousesOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.rect.left, a.rect.top, b)) or
            (isPointInsideRect(a.rect.left, a.rect.bottom, b)) or
            (isPointInsideRect(a.rect.right, a.rect.top, b)) or
            (isPointInsideRect(a.rect.right, a.rect.bottom, b))):
            return True
    return False

def isPointInsideRect(x, y, huis):
    if (x >= huis.rect_extra.left) and (x <= huis.rect_extra.right) and (y >= huis.rect_extra.top) and (y <= huis.rect_vr.bottom):
        return True
    else:
        return False

def overlapCheck(huisje, houselist):

    for house in houselist:

        if doHousesOverlap(huisje, house) == True:
            return True

    return False

def houseposition(houselist):
    for a in houselist:
        afstanden = []
        for b in houselist:
            if b != a:
               position = positionHelper(a, b, afstanden)
        a.vrijstand = min(afstanden)

def positionHelper(a, b, afstanden):

    if b.rect.bottom - a.rect.top < 0: #above

        if b.rect.left - a.rect.right > 0:
            afstand = (((b.rect.left - a.rect.right)**2 + (b.rect.bottom - a.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
            return 'topright'
        elif a.rect.left - b.rect.right > 0:
            afstand = (((a.rect.left - b.rect.right)**2 + (b.rect.bottom - a.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
            return 'topleft'
        else:
            afstand = fabs((a.rect.bottom - b.rect.top)/4)
            afstanden.append(afstand)
            return 'top'

    elif a.rect.bottom - b.rect.top < 0: #below

        if b.rect.left - a.rect.right > 0:
            afstand = (((b.rect.left - a.rect.right)**2 + (a.rect.bottom -b.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
            return 'bottomright'
        elif a.rect.left - b.rect.right > 0:
            afstand = (((a.rect.left - b.rect.right)**2 + (a.rect.bottom -b.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
            return 'bottomleft'
        else:
            afstand = fabs((b.rect.bottom - a.rect.top)/4)
            afstanden.append(afstand)
            return 'bottom'

    elif a.rect.left - b.rect.right > 0: #left
        afstand = fabs((a.rect.left - b.rect.right)/4)
        afstanden.append(afstand)
        return 'left'

    elif b.rect.left - a.rect.right > 0: #right
        afstand = fabs((b.rect.left - a.rect.right)/4)
        afstanden.append(afstand)
        return 'right'

    #om handmatig zo efficient mogelijk de vrijstand te verdelen.

                  

def measureValue(houselist):
    prices = []
    counter = 0
    for house in houselist:
        price = house.price()

        prices.append(price)

    total_value = sum(prices) 
    return total_value

#------------------------------------------------------------------
# Main program loop                                                                                                   
#------------------------------------------------------------------
def move(house, random_x, random_y):
    house.rect.x += random_x
    house.rect.y += random_y
    house.rect_vr.x += random_x
    house.rect_vr.y += random_y
    house.rect_extra.x += random_x
    house.rect_extra.y += random_y
    house.x += random_x
    house.y += random_y
    return house

def getRandInt():
    return random.randint(-1,1)

def moveback(house, random_x, random_y):
    house.rect.x -= random_x
    house.rect.y -= random_y
    house.rect_vr.x -= random_x
    house.rect_vr.y -= random_y
    house.rect_extra.x -= random_x
    house.rect_extra.y -= random_y
    house.x -= random_x
    house.y -= random_y
    return house

def bounce(house):

    if house.rect_vr.x >= WIDTH - house.w_vr or house.rect_vr.x <= house.verplichte_vrijstand:
        return True
    if house.rect_vr.y >= HEIGHT - house.h_vr or house.rect_vr.y <= house.verplichte_vrijstand:
        return True 
    else:
        return False


def moveHouses(oldHouselist):

    newHouselist = []
    for house in oldHouselist:
        random_x = getRandInt()
        random_y = getRandInt()
        move(house, random_x, random_y)

        if overlapCheck(house, oldHouselist) == True:
            moveback(house, random_x, random_y)
        if bounce(house) == True:
            moveback(house, random_x, random_y)

        newHouselist.append(house)
        oldHouselist.remove(house)

    return newHouselist

while True:

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
             
                if event.key == K_g: # place houses on screen
            
                    #Loop om hem te laten herhalen.
                    for a in range(1):
                        counter_m = 0
                        counter_b = 0
                        counter_e = 0
                        houselist = []
                        afstanden = []
                        vrijstand = []

                        screen.fill(BLACK)
                    
                        while counter_m < total_Maisons:

                            maison = Maison() 

                            if overlapCheck(maison, houselist) == False:
                                counter_m += 1
                                naam = "%dm" % (counter_m)
                                maison.name(naam)
                                houselist.append(maison)

                            
                        while counter_b < total_Bungalows:

                            bungalow = Bungalow() 

                            if overlapCheck(bungalow, houselist) == False:
                                counter_b += 1
                                naam = "%db" % (counter_b)
                                bungalow.name(naam)
                                houselist.append(bungalow)

                        while counter_e < total_Eensgezins:

                            eengezins = Eengezins() 

                            if overlapCheck(eengezins, houselist) == False:
                                counter_e += 1
                                naam = "%de" % (counter_e)
                                eengezins.name(naam)
                                houselist.append(eengezins)
                        

                        for house in houselist:
                            house.render()

                        houseposition(houselist)
                        Total_Value = measureValue(houselist)
                    
                        '''
                        #maak screencapture als total_value de hoogste waarde tot nu toe is.
                        highest_value = screenCapture(highest_value, total_value)
                        '''
                        pygame.display.update()

                if event.key == K_o: #move all houses random 0.25, 0.5, 0.75 or 1 meter (to the left, right, top or bottom)

                    while True:

                        #we gebruiken alleen deze list, eerst removen we het huisje uit de list en daarna appenden we hem weer.
                        # anders werkt de overlap check namelijk niet. We kunnen niet twee aparte lists gebruiken.
                        oldHouselist = []
                        for house in houselist:
                            oldHouselist.append(house)

                        for house in houselist:
                            houselist.remove(house)
                            random_x = getRandInt()
                            random_y = getRandInt()
                            move(house, random_x, random_y)

                            if overlapCheck(house, houselist) == True:
                                moveback(house, random_x, random_y)
                            elif bounce(house) == True:
                                moveback(house, random_x, random_y)

                            houselist.append(house)

                        

                        houseposition(houselist)
                        NewValue = measureValue(houselist)

                        if Total_Value < NewValue:
                            Total_Value = NewValue
                            screen.fill(BLACK)
                            for house in houselist:
                                house.render()
                                screen.blit(house.label, (house.x, house.y))
                            print "Totale waarde van wijk is: " "%.2f" % + float(Total_Value)


                        else:
                            houselist = []
                            for house in oldHouselist:
                                houselist.append(house)

                        

                        pygame.display.update()



 