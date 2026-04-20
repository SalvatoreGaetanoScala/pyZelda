import pygame
import random
import math
from settings import *
from .environment import Water, Obstacle, Tree

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 69, 0)) # Arancione fuoco
        try:
            img = pygame.image.load(FIREBALL_IMG_PATH).convert_alpha()
            self.image = pygame.transform.scale(img, (20, 20))
        except: pass
        
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-5, -5)
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0: dist = 1
        
        dir_x = (dx / dist)
        dir_y = (dy / dist)
        self.velocity = pygame.math.Vector2(dir_x, dir_y) * FIREBALL_SPEED

    def update(self, obstacles):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y
        self.hitbox.center = self.rect.center
        
        if not (0 <= self.rect.x <= WINDOW_WIDTH and 0 <= self.rect.y <= WINDOW_HEIGHT):
            self.kill()
        
        hits = pygame.sprite.spritecollide(self, obstacles, False)
        for hit in hits:
            if isinstance(hit, Water): continue
            if isinstance(hit, (Obstacle, Tree)):
                self.kill()
                return

class Zola(pygame.sprite.Sprite):
    _zola_img = None
    def __init__(self, water_tiles, player):
        super().__init__()
        self.water_tiles = water_tiles
        self.player = player
        if Zola._zola_img is None:
            try:
                img = pygame.image.load(ZOLA_IMG_PATH).convert_alpha()
                Zola._zola_img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.fill((0, 100, 100))
                Zola._zola_img = s
        self.original_image = Zola._zola_img
        self.transparent = pygame.Surface((1,1), pygame.SRCALPHA)
        self.image = self.transparent
        self.rect = self.image.get_rect(topleft=(-1000, -1000)) 
        self.hitbox = self.rect
        
        # --- CORREZIONE: DEFINITO MAX_HP ---
        self.max_hp = 6
        self.hp = 6
        
        self.state = "HIDDEN"
        self.timer = 60 + random.randint(0, 30) 
        self.shoot_flag = False

    def update(self, obstacles):
        self.timer -= 1
        if self.state == "HIDDEN":
            self.rect.topleft = (-1000, -1000) 
            if self.timer <= 0:
                self.state = "EMERGING"
                if self.water_tiles:
                    new_pos = random.choice(self.water_tiles)
                    # Imposta l'immagine visibile
                    self.image = self.original_image
                    # --- CORREZIONE CRUCIALE ---
                    # Aggiorniamo il rect per prendere le dimensioni della nuova immagine (64x64)
                    # Altrimenti rimane 1x1 (dall'immagine trasparente) e la barra vita viene minuscola.
                    self.rect = self.image.get_rect(topleft=new_pos)
                    self.hitbox = self.rect.inflate(-10, -10)
                    self.timer = 120 
        elif self.state == "EMERGING":
            if self.timer <= 0: self.state = "SHOOTING"
        elif self.state == "SHOOTING":
            self.shoot_flag = True 
            self.state = "SUBMERGING"
            self.timer = 30 
        elif self.state == "SUBMERGING":
            if self.timer <= 0:
                self.state = "HIDDEN"
                self.image = self.transparent
                # Reset del rect a dimensioni nulle/fuori schermo per sicurezza
                self.rect = self.image.get_rect(topleft=(-1000, -1000))
                self.timer = 60 + random.randint(0, 20)

    def check_shoot(self):
        if self.shoot_flag:
            self.shoot_flag = False
            return True
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, R, (4, 4, 40, 40))
        pygame.draw.rect(self.image, K, (4, 4, 40, 40), 4)
        pygame.draw.rect(self.image, K, (12, 16, 8, 8))
        pygame.draw.rect(self.image, K, (28, 16, 8, 8))
        pygame.draw.rect(self.image, K, (20, 32, 8, 8))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), 0)
        self.move_timer = 0
        
        self.max_hp = 2
        self.hp = self.max_hp

    def update(self, obstacles):
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.move_timer = random.randint(30, 90)
            choice = random.choice(['move', 'move', 'stop'])
            if choice == 'move':
                dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                dx, dy = random.choice(dirs)
                self.direction = pygame.math.Vector2(dx, dy)
            else:
                self.direction = pygame.math.Vector2(0, 0)
        
        old_pos = self.rect.topleft
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        if pygame.sprite.spritecollideany(self, obstacles):
            self.rect.topleft = old_pos
            self.direction *= -1 
            
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ROOM_WIDTH: self.rect.right = ROOM_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > ROOM_HEIGHT: self.rect.bottom = ROOM_HEIGHT