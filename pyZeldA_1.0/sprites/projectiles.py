import pygame
import math
from settings import *
# MODIFICA: Import per gestire l'attraversamento dell'acqua
from .environment import Water

class PlayerFireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=None, target_pos=None):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(RED)
        try:
            img = pygame.image.load(FIRE_MAGIC_IMG_PATH).convert_alpha()
            self.image = pygame.transform.scale(img, (24, 24))
        except:
            pass

        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-10, -10)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_FIREBALL_SPEED
        self.lifetime = 120 

        self.velocity = pygame.math.Vector2(0, 0)
        
        if target_pos:
            dest = pygame.math.Vector2(target_pos)
            start = pygame.math.Vector2(x, y)
            vec = dest - start
            if vec.length() > 0:
                self.velocity = vec.normalize() * self.speed
                angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
                self.image = pygame.transform.rotate(self.image, angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                
        elif direction:
            if direction == 'UP': self.velocity.y = -self.speed
            elif direction == 'DOWN': self.velocity.y = self.speed
            elif direction == 'LEFT': self.velocity.x = -self.speed
            elif direction == 'RIGHT': self.velocity.x = self.speed

    def update(self, obstacles_group=None):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            return

        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.hitbox.center = self.rect.center
        
        # MODIFICA: Collisione che ignora l'acqua (Water)
        if obstacles_group:
            hits = pygame.sprite.spritecollide(self, obstacles_group, False)
            for hit in hits:
                # Se colpiamo acqua, ignoriamola (non distruggere la fireball)
                if isinstance(hit, Water):
                    continue
                # Se è un altro ostacolo (Muro, Albero), distruggi fireball
                self.kill()
                return