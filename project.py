import pygame, sys
from random import randint
from pygame.locals import *

pygame.init()


#------------------------------------------------------------------
# Variabelen en scherminstellingen
#------------------------------------------------------------------

#kleurtjes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)  # = bungalow
GREEN = (  0, 255,   0) # = maison
BLUE = (  0,   0, 255) # = eensgezins

# De window size (= oppervlakte huizen gedeeld door 5 for now)
# Dan hebben we even een realistische representatie, we moeten de echte afmetingen op een andere manier zien te krijgen, met die pixels werkt zo niet...
WIDTH = 240
HEIGHT = 360
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(WHITE)

# variabelen voor handmatige beweging van de huisjes.
x,y = 0, 0
movex, movey = 0,0


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

			#Om de huisjes ook handmatig te kunnen verplaatsen over het scherm, werkt nog niet, beginnetje
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

		# Loop voor het plaatsen van huizen
		# Komt straks in plaats van de handmatige plaatsing die er nu nog staat. 
		# voor de x en y coordinaten in 'render(x, y)'  moet een functie komen die een random x en y produceert maar zorgt dat ze niet overlappen.
	'''
		#check huizenvariant en render de huizen
 		Hvariant = TwintigH()
		for i in range(1, Hvariant.eengezins):
			name =  "e%d" % (i)
			e = Eengezin()
			e.name(name)
			e.render(x, y)
		for i in range(1, Hvariant.bungalow):
			name = "b%d" % (i)
			b = Bungalow()
			b.name(name)
			b.render(x, y)
		for i in range(1, Hvariant.maison):
			name= "m%d" % (i)
			m = Maison()
			m.name(name)
			m.render(x, y)
	'''

	x+=movex
	y+=movey

	pygame.display.update()

#------------------------------------------------------------------
# Alvast idee voor de classes van de huizen (waarschijnlijk fout, moet nog even in OOP duiken van Python)
#------------------------------------------------------------------
class Huis(object):

	def __int__(self, hoogte, breedte, prijs, vrijstand_vrp, kleur, kleurvrs):
		pygame.draw.rect(screen, BLUE, (10, 20, 100, 50))
		self.hoogte = hoogte
		self.breedte = breedte
		self.prijs = prijs
		self.vrijstand_vrp = vrijstand_vrp
		self.kleur = kleur
		self.kleurvrs = kleurvrs

	def name(self, name):
		self.name = name
	
	def render(self,x,y):
		self.x = x
		self.y = y
		pygame.draw.rect(screen,self.kleur(self.x, self.y, self.breedte, self.hoogte))
		# huis + verplichte vrijstand moeten onderscheidbare oppervlakken zijn.
		# gezien verplichte vrijstand ook 'gedeeld' kan worden.
		return

	def beweeg(self):
		#TODO?
		return

	def flip(self):
		#TODO?
		return


#------------------------------------------------------------------
# Classes van de verschillende Huizenvarianten
#------------------------------------------------------------------

class TwintigH():	

	def __init__(self, eengezins, maisons, bungalows):
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
		




