import pygame, sys, csv, random, re, cStringIO, codecs
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

bewegingstriesMax = 15000

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

#geef hier in hoeveel vrijstand mee geven
extraMaison = 50
extraBungalow = 40
extraEengezins = 30


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
        self.rect_extra = pygame.Rect(self.x_vr-(extraMaison/2), self.y_vr-(extraMaison/2), self.w_vr+extraMaison, self.h_vr+extraMaison)
        self.kleur = BLUE
        self.kleur_vrijstand = YELLOW
        self.waarde = 610000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (WHITE))
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
        self.rect_extra = pygame.Rect(self.x_vr-(extraBungalow/2), self.y_vr-(extraBungalow/2), self.w_vr+(extraBungalow), self.h_vr+(extraBungalow))
        self.kleur = RED
        self.kleur_vrijstand = YELLOW
        self.waarde = 399000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (WHITE))
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
        self.rect_extra = pygame.Rect(self.x_vr-(extraEengezins/2), self.y_vr-(extraEengezins/2), self.w_vr+(extraEengezins), self.h_vr+(extraEengezins))
        self.kleur = GREEN
        self.kleur_vrijstand = YELLOW
        self.waarde = 285000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        self.label = myfont.render(house.name, 1, (WHITE))
        screen.blit(self.label, (self.x, self.y))


    def name(self, name):
        self.name = name

    def price(self):
        price = float(self.waarde + ((self.vrijstand - (self.verplichte_vrijstand/4)) * (self.waarde * 0.03)))
        return price


# Collision Detect functies
#------------------------------------------------------------------
def screenCapture():
    
    imagename = "Hillclimber_%sh_w%d_r%d.jpg" %(total_Houses, Total_Value, ronde)
    pygame.image.save(screen, imagename)

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
    if (x >= huis.rect_extra.left) and (x <= huis.rect_extra.right) and (y >= huis.rect_extra.top) and (y <= huis.rect_extra.bottom):
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

        #muur rechts
        afstand = ((WIDTH - a.rect.right) /4)
        afstanden.append(afstand)
        #muur links
        afstand = (a.rect.left /4)
        afstanden.append(afstand)
        #muur boven
        afstand = ((HEIGHT - a.rect.top) /4)
        afstanden.append(afstand)
        #muur onder
        afstand = (a.rect.bottom /4)
        afstanden.append(afstand)

        for b in houselist:
            if b != a:
               position = positionHelper(a, b, afstanden)
        a.vrijstand = min(afstanden)


def positionHelper(a, b, afstanden):

    if b.rect.bottom - a.rect.top < 0: #above

        if b.rect.left - a.rect.right > 0:
            afstand = (((b.rect.left - a.rect.right)**2 + (b.rect.bottom - a.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
        elif a.rect.left - b.rect.right > 0:
            afstand = (((a.rect.left - b.rect.right)**2 + (b.rect.bottom - a.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
        else:
            afstand = fabs((a.rect.bottom - b.rect.top)/4)
            afstanden.append(afstand)

    elif a.rect.bottom - b.rect.top < 0: #below

        if b.rect.left - a.rect.right > 0:
            afstand = (((b.rect.left - a.rect.right)**2 + (a.rect.bottom -b.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
        elif a.rect.left - b.rect.right > 0:
            afstand = (((a.rect.left - b.rect.right)**2 + (a.rect.bottom -b.rect.top)**2) **(1.0/2))/4
            afstanden.append(afstand)
        else:
            afstand = fabs((b.rect.bottom - a.rect.top)/4)
            afstanden.append(afstand)

    elif a.rect.left - b.rect.right > 0: #left
        afstand = fabs((a.rect.left - b.rect.right)/4)
        afstanden.append(afstand)

    elif b.rect.left - a.rect.right > 0: #right
        afstand = fabs((b.rect.left - a.rect.right)/4)
        afstanden.append(afstand)

                  
def measureValue(houselist):
    prices = []
    counter = 0
    for house in houselist:
        price = house.price()

        prices.append(price)

    total_value = round(sum(prices),2) 
    return total_value

#------------------------------------------------------------------
# Main program loop                                                                                                   
#------------------------------------------------------------------
def move(house, x, y):
    house.rect.x += x
    house.rect.y += y
    house.rect_vr.x += x
    house.rect_vr.y += y
    house.x += x
    house.y += y
    return house

def moveback(house, x, y):
    house.rect.x -= x
    house.rect.y -= y
    house.rect_vr.x -= x
    house.rect_vr.y -= y
    house.x -= x
    house.y -= y
    return house

def bounce(house):

    if house.rect_vr.x >= WIDTH - house.w_vr or house.rect_vr.x <= house.verplichte_vrijstand:
        return True
    if house.rect_vr.y >= HEIGHT - house.h_vr or house.rect_vr.y <= house.verplichte_vrijstand:
        return True 
    else:
        return False



while True:

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
             
                if event.key == K_g: # place houses on screen
            
                    #Loop om hem te laten herhalen.
                    ronde = 1
                    for ronde in range(100):
                        ronde += 1
                        print (ronde)

                        # Creating the csv output file for writing into as well as defining the writer
                        output = open("Hillclimber_%sh_r%d.csv" %(total_Houses, ronde), "wb")
                        writer = csv.writer(output)

                        # add header row
                        writer.writerow(["time","Total_Value"])

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

                        pygame.display.update()

                        houseposition(houselist)
                        Total_Value = measureValue(houselist)

                        writer.writerow([time.time(), Total_Value])
                        beginWaarde = Total_Value



                        Continue = False
                        bewegingstries = 0
                        firststepscounter = 0        
                        while Continue == False:

                            for house in houselist:

                                trylist = [0,1,2,3]
                                counter = 0
                                while counter != 4:
                                    oldhouse = house
                                    houselist.remove(house)
                                    x = 0
                                    y = 0
                                    #for the first move, try random, then try all others before moving on to the next house.
                                    if counter == 0:
                                        Number = randint(0, 3)
                                        trylist.remove(Number)
                                    elif counter > 0:
                                        Number = trylist.pop()
                                    #probeer eerst iets grotere bewegingen om hem sneller op een hogere waarde te brengen.
                                    #moet met aparte counter, ga daarna over op stappen van 1 en pas wanneer dit niet lukt andere stappen.

                                    if firststepscounter < 200:
                                        firststepscounter += 1
                                        if Number == 0:
                                            x = 3
                                        elif Number == 1:
                                            x = -3
                                        elif Number == 2:
                                            y = 3
                                        elif Number == 3:
                                            y = -3
                                    elif bewegingstries < 1000:
                                        if Number == 0:
                                            x = 1
                                        elif Number == 1:
                                            x = -1
                                        elif Number == 2:
                                            y = 1
                                        elif Number == 3:
                                            y = -1
                                    elif bewegingstries >= 1000:
                                        if Number == 0:
                                            x = 2
                                        elif Number == 1:
                                            x = -2
                                        elif Number == 2:
                                            y = 2
                                        elif Number == 3:
                                            y = -2
                                    elif bewegingstries >= 2000:
                                        if Number == 0:
                                            x = 4
                                        elif Number == 1:
                                            x = -4
                                        elif Number == 2:
                                            y = 4
                                        elif Number == 3:
                                            y = -4
                                    elif bewegingstries >= 3000:
                                        if Number == 0:
                                            x = 2
                                            y = 2
                                        elif Number == 1:
                                            x = -2
                                            y = -2
                                        elif Number == 2:
                                            y = 2
                                            x = -2
                                        elif Number == 3:
                                            y = -2
                                            x = 2
                                    elif bewegingstries >= 4000:
                                        if Number == 0:
                                            x = 2
                                            y = -2
                                        elif Number == 1:
                                            x = -2
                                            y = 2
                                        elif Number == 2:
                                            y = 2
                                            x = 2
                                        elif Number == 3:
                                            y = -2
                                            x = 2
                                    elif bewegingstries >= 5000:
                                        if Number == 0:
                                            x = randint(-3,3)
                                            y = randint(-3,3)
                                        elif Number == 1:
                                            x = randint(-3,3)
                                            y = randint(-3,3)
                                        elif Number == 2:
                                            y = randint(-3,3)
                                            x = randint(-3,3)
                                        elif Number == 3:
                                            y = randint(-3,3)
                                            x = randint(-3,3)
                                    elif bewegingstries >= 6000:
                                        if Number == 0:
                                            x = randint(-5,5)
                                            y = randint(-5,5)
                                        elif Number == 1:
                                            x = randint(-5,5)
                                            y = randint(-5,5)
                                        elif Number == 2:
                                            y = randint(-5,5)
                                            x = randint(-5,5)
                                        elif Number == 3:
                                            y = randint(-5,5)
                                            x = randint(-5,5)


                                    move(house, x, y)
                                    counter += 1

                                    if overlapCheck(house, houselist) == True:
                                        moveback(house, x, y)
                                    elif bounce(house) == True:
                                        moveback(house, x, y)

                                    houselist.append(house)

                                    houseposition(houselist)
                                    NewValue = measureValue(houselist)

                                    if Total_Value <= NewValue:
                                        writer.writerow([time.time(), Total_Value])
                                        screen.fill(BLACK)
                                        for house in houselist:
                                            house.render()
                                            screen.blit(house.label, (house.x, house.y))
                                        pygame.display.update()
                                
                                        counter = 4
                                        if Total_Value == NewValue:
                                            bewegingstries += 1

                                        else:
                                            print "Totale waarde van wijk is: " "%.2f" % + float(Total_Value)
                                            bewegingstries = 0

                                        Total_Value = NewValue
                                    else:
                                        bewegingstries += 1
                                        houselist.remove(house)
                                        houselist.append(oldhouse)
                                        if bewegingstries == bewegingstriesMax:
                                            Continue = True


                    
                        for house in houselist:
                            house.render()
                            screen.blit(house.label, (house.x, house.y))
                            pygame.display.update()
                        screenCapture()

                    output.close()
                    pygame.quit()
                    sys.exit()