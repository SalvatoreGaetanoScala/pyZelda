import pygame
from settings import *
from .utils import create_8bit_sprite

# Layout
npc_francesco_layout = [
    "....NNNN....",
    "...NSNNSN...",
    "...SSSSSS...",
    "...SKSKSK...",
    "....SSSS....",
    "...NNNNNN...",
    "..NNNNNNNN..",
    "..NNNNNNNN..",
    "..NNNNNNNN..",
    "...BBBBBB...",
    "...BB..BB...",
    "...BB..BB..."
]

class NPC_Francesco(pygame.sprite.Sprite):
    _npc_image = None
    def __init__(self, x, y):
        super().__init__()
        if NPC_Francesco._npc_image is None:
            NPC_Francesco._npc_image = create_8bit_sprite(npc_francesco_layout)
        
        self.image = NPC_Francesco._npc_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(20, 20)
        self.dialog_text = "Vah Paperino, cento di questi giorni!"