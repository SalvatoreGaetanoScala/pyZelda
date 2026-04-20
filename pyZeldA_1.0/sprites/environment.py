import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    _wall_image = None 
    def __init__(self, x, y):
        super().__init__()
        if Obstacle._wall_image is None:
            try:
                img = pygame.image.load(WALL_IMG_PATH).convert()
                Obstacle._wall_image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                fallback = pygame.Surface((TILE_SIZE, TILE_SIZE))
                color = M if 'M' in globals() else (255, 0, 255)
                fallback.fill(color)
                Obstacle._wall_image = fallback
        self.image = Obstacle._wall_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(0, -10)

# --- MURO DI LEGNO ---
class HouseWall(pygame.sprite.Sprite):
    _wood_image = None
    def __init__(self, x, y):
        super().__init__()
        if HouseWall._wood_image is None:
            try:
                # Tenta di caricare l'immagine se esiste
                img = pygame.image.load(HOUSE_WALL_IMG_PATH).convert()
                HouseWall._wood_image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except:
                # Altrimenti crea texture procedurale marrone
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.fill(WOOD_WALL_COLOR) # Colore definito in settings
                
                # Disegna assi verticali
                plank_w = TILE_SIZE // 4
                darker_brown = (80, 50, 20)
                lighter_brown = (120, 80, 40)
                
                for i in range(4):
                    pygame.draw.line(s, darker_brown, (i * plank_w, 0), (i * plank_w, TILE_SIZE), 2)
                    if i % 2 == 0:
                        pygame.draw.line(s, lighter_brown, (i*plank_w + 5, 10), (i*plank_w + 5, 30), 1)
                
                pygame.draw.rect(s, darker_brown, (0, 0, TILE_SIZE, TILE_SIZE), 2)
                HouseWall._wood_image = s
        
        self.image = HouseWall._wood_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect

class Tree(pygame.sprite.Sprite):
    _tree_image = None 
    def __init__(self, x, y):
        super().__init__()
        if Tree._tree_image is None:
            try:
                img = pygame.image.load(TREE_IMG_PATH).convert_alpha()
                Tree._tree_image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                fallback = pygame.Surface((TILE_SIZE, TILE_SIZE))
                fallback.fill(GREEN) 
                Tree._tree_image = fallback
        self.image = Tree._tree_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(0, -10)

class Water(pygame.sprite.Sprite):
    _water_image = None
    def __init__(self, x, y):
        super().__init__()
        if Water._water_image is None:
            try:
                img = pygame.image.load(WATER_IMG_PATH).convert()
                Water._water_image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.fill(WATER_COLOR)
                Water._water_image = s
        self.image = Water._water_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect 

class Bridge(pygame.sprite.Sprite):
    _bridge_image = None
    def __init__(self, x, y):
        super().__init__()
        if Bridge._bridge_image is None:
            try:
                img = pygame.image.load(BRIDGE_IMG_PATH).convert()
                Bridge._bridge_image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.fill(BRIDGE_COLOR) 
                plank_height = TILE_SIZE // 4
                for i in range(4):
                    pygame.draw.line(s, (100, 50, 10), (0, i * plank_height), (TILE_SIZE, i * plank_height), 2)
                    pygame.draw.circle(s, (80, 40, 5), (5, i * plank_height + plank_height//2), 2)
                    pygame.draw.circle(s, (80, 40, 5), (TILE_SIZE-5, i * plank_height + plank_height//2), 2)
                Bridge._bridge_image = s
        self.image = Bridge._bridge_image
        self.rect = self.image.get_rect(topleft=(x, y))