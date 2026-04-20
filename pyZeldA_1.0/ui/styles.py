import pygame
from settings import *

# Colori specifici stile Final Fantasy
FF_BLUE = (0, 0, 170)
FF_BORDER = (245, 245, 245)

def draw_ff1_box(surface, rect):
    """Disegna un singolo box stile FF1 (Blu con bordo bianco)"""
    pygame.draw.rect(surface, FF_BLUE, rect) 
    pygame.draw.rect(surface, FF_BORDER, rect, 4) # Bordo spessore 4