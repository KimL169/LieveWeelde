import pygame, sys, csv
from math import e, pi, cos, sin, sqrt, fabs
import math
from random import randint
from pygame.locals import *
import datetime, time

#lijst met alle rectangles, voor collide check
houselist = []    

# lijst met alle afstanden tot andere huizen
afstanden = []

# lijst met vrijstand voor elk huis
vrijstand = []

# variable voor de hoogste waarde tot nu toe.
highest_value = 0

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
        self.rect_extra = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = BLUE
        self.kleur_vrijstand = YELLOW
        self.waarde = 610000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (RED))
        screen.blit(label, (self.x_vr, self.y_vr))

    def name(self, name):
        self.name = name
        

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
        self.rect_extra = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = RED
        self.kleur_vrijstand = YELLOW
        self.waarde = 399000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (BLUE))
        screen.blit(label, (self.x_vr, self.y_vr))

    def name(self, name):
        self.name = name


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
        self.rect_extra = pygame.Rect(self.x_vr, self.y_vr, self.w_vr, self.h_vr)
        self.kleur = GREEN
        self.kleur_vrijstand = YELLOW
        self.waarde = 285000
        self.vrijstand = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, (self.rect_extra))
        pygame.draw.rect(screen, self.kleur_vrijstand, (self.rect_vr))
        pygame.draw.rect(screen, self.kleur, (self.rect))
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(house.name, 1, (RED))
        screen.blit(label, (self.x_vr, self.y_vr))


    def name(self, name):
        self.name = name


def verdeelVrijstand(vrijstand):
    m = Maison()
    e = Eengezins()
    b = Bungalow()
    Mvrijstand = 0
    Bvrijstand = 0
    Evrijstand = 0
    total = 0

    while True:

        if total == vrijstand:
            print "\nMaison: %d\n Bungalow: %d\n Eengezins:%d\n" % (Mvrijstand, Bvrijstand, Evrijstand)
            return

        MvrijstandNew = (Mvrijstand + 1)
        Mold = float(m.waarde + (((Mvrijstand)- (m.verplichte_vrijstand/4)) * (m.waarde * 0.06)))
        Mnew = float(m.waarde + (((MvrijstandNew/4) - (m.verplichte_vrijstand/4)) * (m.waarde * 0.06)))
        Mextra = Mnew - Mold

        BvrijstandNew = (Bvrijstand + 1)
        Bold = float(b.waarde + (((Bvrijstand/4) - (b.verplichte_vrijstand/4)) * (b.waarde * 0.04)))
        Bnew = float(b.waarde + (((BvrijstandNew/4) - (b.verplichte_vrijstand/4)) * (b.waarde * 0.04)))
        Bextra = Bnew - Bold

        EvrijstandNew = (Evrijstand + 1)
        Eold = float(e.waarde + (((Evrijstand/4) - (e.verplichte_vrijstand/4)) * (e.waarde * 0.03)))
        Enew = float(e.waarde + (((EvrijstandNew/4) - (e.verplichte_vrijstand/4)) * (e.waarde * 0.03)))
        Eextra = Enew - Eold

        if Mextra >= Bextra and Mextra >= Eextra:
            Mvrijstand += 1
        elif Bextra >= Mextra and Bextra >= Eextra:
            Bvrijstand += 1
        elif Eextra >= Mextra and Eextra >= Bextra: 
            Evrijstand += 1

        total = Mvrijstand + Bvrijstand + Evrijstand

verdeelVrijstand(10000)