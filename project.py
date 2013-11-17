import pygame, sys
from random import randint
from pygame.locals import *

pygame.init()


#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

# De window size (= oppervlakte huizen gedeeld door 5 for now)
# Dan hebben we even een realistische representatie, we moeten de echte afmetingen op een andere manier zien te krijgen.
WIDTH = 240
HEIGHT = 360
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(WHITE)

#kleurtjes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)  # = bungalow
GREEN = (  0, 255,   0) # = maison
BLUE = (  0,   0, 255) # = eensgezins

# variabelen voor handmatige beweging van de huisjes.
x,y = 0, 0
movex, movey = 0,0


#------------------------------------------------------------------
# Functies. Deze zijn nog niet geschreven, maar heb ze opgedoken en dacht dat ze erg van pas zouden komen.
#------------------------------------------------------------------

# kijkt of een huis overlapped met een ander huis, dit is een beginnetje.
def do_houses_overlap():
	for each house in houses:

	    for a, b in [(rect1, rect2), (rect2, rect1)]:
	        # Check if a's corners are inside b
	        if ((is_point_inside_house(a.left, a.top, b)) or
	            (is_point_inside_house(a.left, a.bottom, b)) or
	            (is_point_inside_house(a.right, a.top, b)) or
	            (is_point_inside_house(a.right, a.bottom, b))):
	            return True

# helper voor de overlap functie, moet ook nog worden gemaakt.
def is_point_inside_house(x, y, House a):
    if (x > a.left) and (x < a.right) and (y > a.top) and (y < a.bottom):
        return True
    else:
        return False

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
			# toetsen: E = eengezinsswoning, M = Maison, B = Bungalow
			if event.key == K_e: #eensgezins
				pygame.draw.rect(screen, BLUE, (randint(24,WIDTH-24),randint(24,HEIGHT-24), 24, 24))
			elif event.key == K_b: #bungalow
				pygame.draw.rect(screen, RED, (randint(32,WIDTH-32),randint(27,HEIGHT-27), 32, 27))
			elif event.key == K_m: #maison
				pygame.draw.rect(screen, GREEN, (randint(46,WIDTH-46),randint(45,HEIGHT-45), 46, 45))

			#Om de huisjes te kunnen verplaatsen over het scherm, werkt nog niet, beginnetje
			if event.key == K_LEFT:
				movex = -1
			elif event.key == K_RIGHT:
				movex = +1
			elif event.key == K_UP:
				movey = -1
			elif event.key == K_DOWN:
				movey= +1
		if event.type == KEYUP:
			if event.key == K_LEFT:
				movex = 0
			elif event.key == K_RIGHT:
				movex = 0
			elif event.key == K_UP:
				movey = 0
			elif event.key == K_DOWN:
				movey= 0

		x+=movex
		y+=movey
	
		pygame.display.update()

#------------------------------------------------------------------
# Alvast idee voor de classes van de huizen (waarschijnlijk al fout, moet nog even in OOP duiken van Python)
#------------------------------------------------------------------
class Huis(object):

	def __int__(self, hoogte, breedte, prijs, vrijstand_vrp):
		pygame.draw.rect(screen, BLUE, (10, 20, 100, 50))
		self.hoogte = hoogte
		self.breedte = breedte
		self.prijs = prijs
		self.vrijstand_vrp = vrijstand_vrp
	
	def teken_huis(self):
		#TODO
		# huis + verplichte vrijstand moeten onderscheidbare oppervlakken zijn.
		# gezien verplichte vrijstand ook 'gedeeld' kan worden.
		return

	def beweeg(self):
		#TODO?
		return

	def flip(self):
		#TODO?
		return

class Maison(Huis):
	# TODO
	return
class Eenpersoons(Huis):
 	# TODO
 	return
class Bungalow(Huis):
	# TODO
	return

#------------------------------------------------------------------
# Classes van de verschillende oppervlak-typen.
#------------------------------------------------------------------
class Oppervlakte (object)

	def __init__(self):
		return

class TwintigHuizen(Oppervlakte):	

	def __init__(self):
		return

class VeertigHuizen(Oppervlakte):

	def __init__(self):
		return

class ZestigHuizen(Oppervlakte):

	def __init__(self):
		return




