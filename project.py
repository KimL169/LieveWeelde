import pygame, sys
from random import randint
from pygame.locals import *

pygame.init()

#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

#lijst met alle rectangles, voor collide check
rects = []    

#define total number of houses
total_Houses = 20

#define total number of each house type
total_Maisons = int(total_Houses * 0.15) 
total_Bungalows = int(total_Houses * 0.25)
total_Eensgezins = int(total_Houses * 0.60)

#display settings
WIDTH = 600
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)


#kleurtjes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)  # = bungalow
GREEN = (  0, 255,   0) # = maison
BLUE = (  0,   0, 255) # = eensgezins

# De window size (= oppervlakte huizen gedeeld door 5 for now)
# Dan hebben we even een realistische representatie, we moeten de echte afmetingen op een andere manier zien te krijgen, met die pixels werkt zo niet...
# variabelen voor handmatige beweging van de huisjes.
x,y = 0, 0
movex, movey = 0,0

#--------------------------------
# Classes voor de huisjes
#----------------------------

class Maison():

    def __init__ (self, hoogte, breedte, kleur, vrijstand):
        self.hoogte = hoogte #nu nog met vrijstand included 
        self.breedte = breedte
        self.kleur = kleur
        self.vrijstand = vrijstand
        self.breedte_totaal = self.breedte + (self.vrijstand * 2)
        self.hoogte_totaal = self.hoogte + (self.vrijstand * 2)

    def render(self):
        #plaats huisje_zonder_vrijstand op dezelfde positie als met_vrijstand.
        # breedte_totaal en hoogte_totaal omdat ook de verplichte vrijstand niet buiten het scherm mag vallen.
        self.x = randint(self.breedte_totaal, WIDTH-self.breedte_totaal)
        self.y = randint(self.hoogte_totaal, WIDTH-self.hoogte_totaal) 
        # een verandering van huis.x en huisje.y zal nu allebei de rechthoeken evenredig bewegen.
        self.totaal = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte_totaal, self.hoogte_totaal))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte, self.hoogte))

class Bungalow():

    def __init__ (self, hoogte, breedte, kleur, vrijstand):
        self.hoogte = hoogte #nu nog met vrijstand included 
        self.breedte = breedte
        self.kleur = kleur
        self.vrijstand = vrijstand
        self.breedte_totaal = self.breedte + (self.vrijstand * 2)
        self.hoogte_totaal = self.hoogte + (self.vrijstand * 2)

    def render(self):
        #plaats huisje_zonder_vrijstand op dezelfde positie als met_vrijstand.
        # breedte_totaal en hoogte_totaal omdat ook de verplichte vrijstand niet buiten het scherm mag vallen.
        self.x = randint(self.breedte_totaal, WIDTH-self.breedte_totaal)
        self.y = randint(self.hoogte_totaal, WIDTH-self.hoogte_totaal) 
        # een verandering van huis.x en huisje.y zal nu allebei de rechthoeken evenredig bewegen.
        self.totaal = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte_totaal, self.hoogte_totaal))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte, self.hoogte))

class Eengezins():

    def __init__ (self, hoogte, breedte, kleur, vrijstand):
        self.hoogte = hoogte #nu nog met vrijstand included 
        self.breedte = breedte
        self.kleur = kleur
        self.vrijstand = vrijstand
        self.breedte_totaal = self.breedte + (self.vrijstand * 2)
        self.hoogte_totaal = self.hoogte + (self.vrijstand * 2)

    def render(self):
        #plaats huisje_zonder_vrijstand op dezelfde positie als met_vrijstand.
        # breedte_totaal en hoogte_totaal omdat ook de verplichte vrijstand niet buiten het scherm mag vallen.
        self.x = randint(self.breedte_totaal, WIDTH-self.breedte_totaal)
        self.y = randint(self.hoogte_totaal, WIDTH-self.hoogte_totaal) 
        # een verandering van huis.x en huisje.y zal nu allebei de rechthoeken evenredig bewegen.
        self.totaal = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte_totaal, self.hoogte_totaal))
        self.zonder_vrijstand = pygame.draw.rect(screen, self.kleur, (self.x, self.y, self.breedte, self.hoogte))


#------------------------------------------------------------------
# Functies. Deze zijn nog niet geschreven, maar heb ze opgedoken en dacht dat ze erg van pas zouden komen.
# Online is genoeg te vinden over coordinatie van objecten ten opzichte van elkaar en handling van overlap in pygame.
#------------------------------------------------------------------

# kijkt of een huis overlapped met een ander huis, dit is een beginnetje.
def do_houses_overlap():
        for house in houses:
                #.... 
            for a, b in [(rect1, rect2), (rect2, rect1)]:
                # Check if a's corners are inside b
                if ((is_point_inside_house(a.left, a.top, b)) or
                    (is_point_inside_house(a.left, a.bottom, b)) or
                    (is_point_inside_house(a.right, a.top, b)) or
                    (is_point_inside_house(a.right, a.bottom, b))):
                    return True

# helper voor de overlap functie, moet ook nog worden gemaakt.
def is_point_inside_house(x, y, House):
    if (x > House.left) and (x < House.right) and (y > House.top) and (y < House.bottom):
        return True
    else:
        return False

def collision_detect():   
    plaatsing = False
    while plaatsing == False:

        newhouse = pygame.draw.rect(screen, BLUE, (randint(24,WIDTH-24),randint(24,HEIGHT-24), 24, 24))
        
        if newhouse.collidelist(rects) == -1:
            #add newhouse to [rects]
            rects.append(newhouse)
            plaatsing = True
            pygame.display.update(rects)
    



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
                #randint zet ze random op het scherm - de breedte en hoogte van het huis+verplichtvrst zodat het allemaal op de map valt. 
            if event.type == KEYDOWN:
                if event.key == K_q: # return to main
                    screen.fill(BLACK)
                
               
                if event.key == K_g: #go 

                    #Plaatsing Maisons
                    for y in range (total_Maisons):

                        maison = Maison(33, 45, RED, 6) #moet nog even veranderd worden naar juiste waarden
                        maison.render()

                        #add newhouse to [rects]
                        rects.append(maison)
                
                    for y in range (total_Bungalows):

                        bungalow = Bungalow(30, 22, BLUE, 3) #moet nog even veranderd worden naar juiste waarden
                        bungalow.render()

                        #add newhouse to [rects]
                        rects.append(bungalow)

                    for y in range (total_Eensgezins):

                        eengezins = Eengezins(24, 24, GREEN, 2) #moet nog even veranderd worden naar juiste waarden
                        eengezins.render()

                        #add newhouse to [rects]
                        rects.append(eengezins)
            
                        pygame.display.update()




#------------------------------------------------------------------
# Alvast idee voor de classes van de huizen (waarschijnlijk fout, moet nog even in OOP duiken van Python)
#------------------------------------------------------------------


#------------------------------------------------------------------
# Classes van de verschillende Huizenvarianten
#------------------------------------------------------------------

class TwintigH():        

        def __init__(self , eengezins, maisons, bungalows):
                self.eengezins = 12
                self.bungalow = 5
                self.maison = 3
                
class VeertigH():

        def __init__(self, eengezins, maisons, bungalows):
                self.eengezins = 24
                self.bungalow = 10
                self.maison = 6
        

class ZestigH():

        def __init__(self, eengezins, maisons, bungalows):
                self.eengezins = 36
                self.bungalow = 15
                self.maison = 9
                



