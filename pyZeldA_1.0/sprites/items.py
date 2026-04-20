import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(YELLOW) # Fallback
        
        try:
            img = pygame.image.load(image_path).convert_alpha()
            # Ridimensiona alla dimensione appropriata (es. 40x40 per essere visibile)
            self.image = pygame.transform.scale(img, (40, 40)) 
        except Exception as e:
            print(f"Errore caricamento item {item_type}: {e}")
            
        self.rect = self.image.get_rect(center=(x, y))
        self.pickup_delay = 30 

    def update(self):
        if self.pickup_delay > 0:
            self.pickup_delay -= 1

# --- CLASSE REINSERITA: SWORD DROP ---
class SwordDrop(Item):
    def __init__(self, x, y):
        # Assicurati che SWORD_IMG_PATH sia definito in settings.py
        super().__init__(x, y, SWORD_IMG_PATH, 'sword')
        self.type = 'sword'

# --- CLASSE POZIONE ---
class Potion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, POTION_IMG_PATH, 'potion')
        self.type = 'potion'

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        super().__init__()
        self.value = value
        self.type = 'coin'
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        try:
            path = COIN_100_IMG_PATH if value >= 100 else COIN_10_IMG_PATH
            img = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(img, (24, 24))
        except: pass
        self.rect = self.image.get_rect(center=(x, y))
        self.pickup_delay = 30
    
    def update(self):
        if self.pickup_delay > 0: self.pickup_delay -= 1