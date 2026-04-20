import pygame
from settings import *
from .utils import create_8bit_sprite

# Layouts esistenti
duck_down_1 = ["....BBBB....", "...BBBBBB...", "...WWWWWW...", "..WKWWWWKW..", "...OOOOOO...", "....OOOO....", "...BBBBBB...", "..BBBRBBB...", "..BBBBBBBB..", "..BBBBBBBB..", "...OO..OO...", "............"]
duck_down_2 = ["....BBBB....", "...BBBBBB...", "...WWWWWW...", "..WKWWWWKW..", "...OOOOOO...", "....OOOO....", "...BBBBBB...", "..BBBRBBB...", "..BBBBBBBB..", "..BBBBBBBB..", "....OOOO....", "...O....O..."]
duck_up_1 = ["....BBBB....", "...BBBBBB...", "...WWWWWW...", "...WWWWWW...", "...WWWWWW...", "...BBBBBB...", "..BBBBBBBB..", "..BBBBBBBB..", "..BBBBBBBB..", "...WWWWWW...", "...OO..OO...", "............"]
duck_up_2 = ["....BBBB....", "...BBBBBB...", "...WWWWWW...", "...WWWWWW...", "...WWWWWW...", "...BBBBBB...", "..BBBBBBBB..", "..BBBBBBBB..", "..BBBBBBBB..", "...WWWWWW...", "....OOOO....", "...O....O..."]
duck_side_1 = ["....BBBB....", "...BBBBBB...", "....WWWWW...", "...WKW..W...", "..OOOOWWW...", "...OOOBBB...", ".....BBBBB..", "....BBBBBB..", "....BBBBBB..", "....BBBBWW..", "....BBBBWW..", ".....OOO...."]
duck_side_2 = ["....BBBB....", "...BBBBBB...", "....WWWWW...", "...WKW..W...", "..OOOOWWW...", "...OOOBBB...", ".....BBBBB..", "....BBBBBB..", "....BBBBBB..", "....BBBBWW..", "....BBBBWW..", "....O...OO.."]

# NUOVO Layout per Paperino morto (sdraiato a terra)
duck_dead = [
    "................",
    ".....WWWWWW.....", # Corpo bianco
    "...WWWWWWWWWW...",
    "..OOOWWWWWWOOO..", # Becco e piedi arancioni sparsi
    ".....WWWWWW.....",
    "................"
]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = {
            'down': [create_8bit_sprite(duck_down_1), create_8bit_sprite(duck_down_2)],
            'up':   [create_8bit_sprite(duck_up_1), create_8bit_sprite(duck_up_2)],
            'side': [create_8bit_sprite(duck_side_1), create_8bit_sprite(duck_side_2)]
        }
        # Generazione sprite morto procedurale
        self.dead_image = create_8bit_sprite(duck_dead)
        
        self.direction_str = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.sprites['down'][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-10, -5) 
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2(0, 0)
        self.last_direction = pygame.math.Vector2(0, 1)
        
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.max_mp = PLAYER_MAX_MP
        self.mp = self.max_mp
        self.invincible_timer = 0
        self.is_dead = False 
        
        self.level = 1
        self.current_xp = 0
        self.xp_needed = 10 

        self.inventory = {
            'weapons': [],      
            'magic': ['FIRE', 'SPECCHIO'],
            'items': [] 
        }
        self.equipped = {
            'weapon': None,
            'magic': [],
            'item': None 
        }
        
        self.attacking = False
        self.attack_cooldown = 0
        self.sword_rect = None
        self.sword_images = {}
        self.current_sword_image = None
        
        self.mirror_active = False
        self.mirror_timer = 0
        self.mirror_img = None
        try:
            m_img = pygame.image.load(MIRROR_MAGIC_IMG_PATH).convert_alpha()
            self.mirror_img = pygame.transform.scale(m_img, (75, 75))
        except Exception as e: pass

        try:
            original = pygame.image.load(SWORD_IMG_PATH).convert_alpha()
            scale = 0.4 
            w = int(original.get_width() * scale)
            h = int(original.get_height() * scale)
            scaled = pygame.transform.scale(original, (w, h))
            self.sword_images['UP'] = scaled
            self.sword_images['DOWN'] = pygame.transform.rotate(scaled, 180)
            self.sword_images['LEFT'] = pygame.transform.rotate(scaled, 90)
            self.sword_images['RIGHT'] = pygame.transform.rotate(scaled, -90)
        except: self.sword_images = None

        self.hurt_sfx = None
        try:
            self.hurt_sfx = pygame.mixer.Sound(PLAYER_HURT_SFX_PATH)
            self.hurt_sfx.set_volume(0.4) 
        except Exception as e: pass

        self.sword_sfx = None
        try:
            self.sword_sfx = pygame.mixer.Sound(SWORD_SFX_PATH)
            self.sword_sfx.set_volume(0.3) 
        except Exception as e: pass

        self.low_hp_sfx = None
        self.low_hp_playing = False
        try:
            self.low_hp_sfx = pygame.mixer.Sound(PLAYER_LOW_HP_SFX_PATH)
            self.low_hp_sfx.set_volume(1.0) 
        except Exception as e: pass

        self.recovery_sfx = None
        try:
            self.recovery_sfx = pygame.mixer.Sound(PLAYER_RECOVERY_SFX_PATH)
            self.recovery_sfx.set_volume(0.5)
        except Exception as e: pass

    def trigger_death(self):
        """Imposta lo stato di morte e cambia sprite."""
        self.is_dead = True
        self.stop_sounds()
        self.image = self.dead_image
        # Centra lo sprite della morte rispetto alla posizione precedente
        new_rect = self.image.get_rect(center=self.rect.center)
        self.rect = new_rect

    def activate_mirror(self):
        if self.is_dead: return
        self.mirror_active = True
        self.mirror_timer = MIRROR_DURATION
        self.mp -= MIRROR_COST
        if self.mp < 0: self.mp = 0

    def gain_xp(self, amount):
        if self.is_dead: return False
        self.current_xp += amount
        leveled_up = False
        if self.current_xp >= self.xp_needed:
            self.current_xp -= self.xp_needed
            self.level += 1
            self.xp_needed = 10 + (self.level - 1) * 2
            self.max_hp += 1
            self.max_mp += 1
            self.hp += 1
            self.mp += 1
            if self.hp > self.max_hp: self.hp = self.max_hp
            if self.mp > self.max_mp: self.mp = self.max_mp
            leveled_up = True
        return leveled_up

    def stop_sounds(self):
        if self.low_hp_sfx:
            self.low_hp_sfx.stop()
        self.low_hp_playing = False

    def heal(self, amount):
        if self.is_dead: return False
        if self.hp >= self.max_hp:
            return False 
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.recovery_sfx:
            self.recovery_sfx.play()
        return True

    def get_input(self):
        if self.is_dead: return 
        
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a]: 
            self.direction.x = -1
            self.direction_str = 'left'
            self.last_direction = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_d]: 
            self.direction.x = 1
            self.direction_str = 'right'
            self.last_direction = pygame.math.Vector2(1, 0)
        elif keys[pygame.K_w]: 
            self.direction.y = -1
            self.direction_str = 'up'
            self.last_direction = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_s]: 
            self.direction.y = 1
            self.direction_str = 'down'
            self.last_direction = pygame.math.Vector2(0, 1)

        if keys[pygame.K_SPACE] and not self.attacking and self.equipped['weapon'] == 'SPADA':
            self.attacking = True
            self.attack_cooldown = 15
            if self.sword_sfx:
                self.sword_sfx.play()

    def move(self, obstacles):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal', obstacles)
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical', obstacles)
        self.rect.center = self.hitbox.center

    def collision(self, direction, obstacles):
        for sprite in obstacles:
            if self.hitbox.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

    def take_damage(self):
        if self.is_dead: return
        if self.invincible_timer == 0:
            self.hp -= 1
            self.invincible_timer = PLAYER_IFRAMES
            if self.hurt_sfx:
                self.hurt_sfx.play()

    def animate(self):
        if self.is_dead: return 

        anim_type = self.direction_str
        flip_x = False
        if self.direction_str == 'right': anim_type = 'side'; flip_x = True 
        elif self.direction_str == 'left': anim_type = 'side'; flip_x = False
        if self.direction.magnitude() != 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.sprites[anim_type]): self.frame_index = 0
        else: self.frame_index = 0
        image = self.sprites[anim_type][int(self.frame_index)]
        if flip_x: image = pygame.transform.flip(image, True, False)
        
        if self.invincible_timer > 0:
            alpha = 255 if (self.invincible_timer // 5) % 2 == 0 else 50
            image.set_alpha(alpha)
        else:
            image.set_alpha(255)
        self.image = image

    def update(self, obstacles):
        if self.is_dead:
            return

        self.get_input()
        if self.invincible_timer > 0: self.invincible_timer -= 1
        
        if self.mirror_active:
            self.mirror_timer -= 1
            if self.mirror_timer <= 0:
                self.mirror_active = False
        
        if self.max_hp > 0:
            threshold = self.max_hp * 0.3
            if 0 < self.hp <= threshold:
                if not self.low_hp_playing and self.low_hp_sfx:
                    self.low_hp_sfx.play(-1)
                    self.low_hp_playing = True
            else:
                if self.low_hp_playing and self.low_hp_sfx:
                    self.low_hp_sfx.stop()
                    self.low_hp_playing = False
        
        if not self.attacking:
            self.move(obstacles)
            self.animate()
        if self.attacking:
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.attacking = False
                self.sword_rect = None
                self.current_sword_image = None
            else:
                if self.sword_images:
                    dir_key = 'DOWN'
                    if self.last_direction.y < 0: dir_key = 'UP'
                    elif self.last_direction.y > 0: dir_key = 'DOWN'
                    elif self.last_direction.x < 0: dir_key = 'LEFT'
                    elif self.last_direction.x > 0: dir_key = 'RIGHT'
                    self.current_sword_image = self.sword_images[dir_key]
                    self.sword_rect = self.current_sword_image.get_rect()
                    if dir_key == 'UP':
                        self.sword_rect.bottomleft = self.rect.center; self.sword_rect.x += 8; self.sword_rect.y -= 8
                    elif dir_key == 'DOWN':
                        self.sword_rect.topright = self.rect.center; self.sword_rect.x -= 8; self.sword_rect.y += 8
                    elif dir_key == 'RIGHT':
                        self.sword_rect.midleft = self.rect.midright; self.sword_rect.x -= 6; self.sword_rect.y += 2
                    elif dir_key == 'LEFT':
                        self.sword_rect.midright = self.rect.midleft; self.sword_rect.x += 6; self.sword_rect.y += 2

    def draw(self, surface, ui_height):
        if self.is_dead:
            surface.blit(self.image, (self.rect.x, self.rect.y + ui_height))
            return

        sword_pos = (0,0)
        draw_sword = (self.attacking and self.current_sword_image and self.sword_rect)
        if draw_sword: sword_pos = (self.sword_rect.x, self.sword_rect.y + ui_height)
        sword_on_top = True
        if self.last_direction.x < 0 or self.last_direction.y < 0: sword_on_top = False 
        
        if draw_sword and not sword_on_top: surface.blit(self.current_sword_image, sword_pos)
        
        surface.blit(self.image, (self.rect.x, self.rect.y + ui_height))
        
        if draw_sword and sword_on_top: surface.blit(self.current_sword_image, sword_pos)

        if self.mirror_active and self.mirror_img:
            m_rect = self.mirror_img.get_rect(center=self.rect.center)
            
            offset_dist = 40 
            offset_x = 0
            offset_y = 0
            
            if self.last_direction.y > 0: 
                offset_y = offset_dist
            elif self.last_direction.y < 0:
                offset_y = -offset_dist
            elif self.last_direction.x > 0:
                offset_x = offset_dist
            elif self.last_direction.x < 0:
                offset_x = -offset_dist
                
            draw_pos = (m_rect.x + offset_x, m_rect.y + offset_y + ui_height)
            surface.blit(self.mirror_img, draw_pos)