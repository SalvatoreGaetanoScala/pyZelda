import pygame
from settings import *

def create_8bit_sprite(layout):
    pixel_size = TILE_SIZE // 12 
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Mappa colori completa
    color_map = {'K': K, 'W': W, 'B': B, 'O': O, 'R': R, 'S': S, 'N': N, '.': None}
    
    for r, row in enumerate(layout):
        for c, char in enumerate(row):
            color = color_map.get(char)
            if color:
                pygame.draw.rect(surface, color, (c * pixel_size, r * pixel_size, pixel_size, pixel_size))
    return surface