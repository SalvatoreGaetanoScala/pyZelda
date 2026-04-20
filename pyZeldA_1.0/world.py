import pygame
from settings import *
from mappa import WORLD_MAP
from sprites import Enemy, Obstacle, SwordDrop, Tree, Water, Bridge, Zola, Fireball, NPC_Francesco, PlayerFireball, HouseWall
from sprites.items import Coin, Potion

class World:
    def __init__(self):
        self.map_x = 0
        self.map_y = 0
        self.obstacles = pygame.sprite.Group()
        self.items = pygame.sprite.Group() 
        self.projectiles = pygame.sprite.Group() 
        self.player_projectiles = pygame.sprite.Group() 
        self.npcs = pygame.sprite.Group() 
        self.enemies_cache = {} 
        self.sword_collected = False 
        
        # Font per debug (HP nemici)
        self.debug_font = pygame.font.Font(None, 24)
        
        # Pre-carica
        _ = Obstacle(0, 0)
        _ = HouseWall(0, 0)
        _ = Tree(0, 0)
        _ = Water(0, 0)
        _ = Bridge(0, 0)
        _ = NPC_Francesco(0, 0)

    def reset(self):
        self.obstacles.empty()
        self.items.empty()
        self.projectiles.empty()
        self.player_projectiles.empty()
        self.npcs.empty()
        self.enemies_cache = {}
        self.sword_collected = False 

    def load_room(self, mx, my, player):
        self.map_x = mx
        self.map_y = my
        self.obstacles.empty()
        self.items.empty() 
        self.projectiles.empty()
        self.player_projectiles.empty()
        self.npcs.empty() 
        
        layout = WORLD_MAP[my][mx]
        if layout is None: return

        water_tiles = []
        zola_count = 0

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                
                if char == '#': self.obstacles.add(Obstacle(x, y))
                elif char == '=': self.obstacles.add(HouseWall(x, y))
                elif char == 'A': self.obstacles.add(Tree(x, y))
                elif char == 'W': 
                    self.obstacles.add(Water(x, y))
                    water_tiles.append((x, y))
                elif char == 'Z':
                    self.obstacles.add(Water(x, y))
                    water_tiles.append((x, y))
                    zola_count += 1
                elif char == 'S':
                    if not self.sword_collected: self.items.add(SwordDrop(x, y))
                elif char == 'F': self.npcs.add(NPC_Francesco(x, y))
                elif char == 'H': self.items.add(Potion(x, y))
        
        # Respawn nemici sempre
        enemy_group = pygame.sprite.Group()
        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                if char == 'E':
                    enemy_group.add(Enemy(c * TILE_SIZE, r * TILE_SIZE))
        
        if zola_count > 0 and water_tiles:
            for _ in range(zola_count):
                enemy_group.add(Zola(water_tiles, player))

        self.enemies_cache[(mx, my)] = enemy_group

    def get_current_enemies(self):
        return self.enemies_cache.get((self.map_x, self.map_y), pygame.sprite.Group())
    
    def ensure_enemies_loaded(self, mx, my):
        pass

    def update_projectiles(self, player):
        for enemy in self.get_current_enemies():
            if isinstance(enemy, Zola):
                if enemy.check_shoot():
                    fb = Fireball(enemy.rect.centerx, enemy.rect.centery, 
                                  player.rect.centerx, player.rect.centery)
                    self.projectiles.add(fb)
        self.projectiles.update(self.obstacles)
        self.player_projectiles.update(self.obstacles)

    def find_safe_drop_pos(self, start_x, start_y):
        grid_x = int(start_x // TILE_SIZE)
        grid_y = int(start_y // TILE_SIZE)
        offsets = [(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1), (2,0), (-2,0), (0,2), (0,-2)]
        
        for dx, dy in offsets:
            check_x = (grid_x + dx) * TILE_SIZE
            check_y = (grid_y + dy) * TILE_SIZE
            check_rect = pygame.Rect(check_x + 20, check_y + 20, 20, 20)
            hits = [s for s in self.obstacles if s.rect.colliderect(check_rect)]
            
            is_safe = True
            for obj in hits:
                if isinstance(obj, (Water, Obstacle, Tree, HouseWall)):
                    is_safe = False
                    break
            
            if is_safe:
                return check_x + TILE_SIZE // 2, check_y + TILE_SIZE // 2
        return start_x, start_y

    def draw(self, surface, mx, my, offset_x, offset_y):
        layout = WORLD_MAP[my][mx]
        if layout is None: return

        room_rect = pygame.Rect(offset_x, offset_y + UI_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT)
        current_floor = BLACK if (mx == 1 and my == 0) else FLOOR_COLOR
        pygame.draw.rect(surface, current_floor, room_rect)
        
        wall_img = Obstacle._wall_image 
        house_wall_img = HouseWall._wood_image
        tree_img = Tree._tree_image
        water_img = Water._water_image
        bridge_img = Bridge._bridge_image

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                draw_x = offset_x + (c * TILE_SIZE)
                draw_y = offset_y + UI_HEIGHT + (r * TILE_SIZE)
                
                if char == '#':
                    if wall_img: surface.blit(wall_img, (draw_x, draw_y))
                    else: pygame.draw.rect(surface, M, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
                elif char == '=':
                    if house_wall_img: surface.blit(house_wall_img, (draw_x, draw_y))
                    else: pygame.draw.rect(surface, WOOD_WALL_COLOR, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
                elif char == 'A':
                    if tree_img: surface.blit(tree_img, (draw_x, draw_y))
                    else: pygame.draw.rect(surface, GREEN, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
                elif char == 'W' or char == 'Z':
                    if water_img: surface.blit(water_img, (draw_x, draw_y))
                    else: pygame.draw.rect(surface, WATER_COLOR, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
                elif char == 'B':
                    if bridge_img: surface.blit(bridge_img, (draw_x, draw_y))
                    else: pygame.draw.rect(surface, BRIDGE_COLOR, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))

        # Item
        for item in self.items:
            pos = (item.rect.x + offset_x, item.rect.y + offset_y + UI_HEIGHT)
            surface.blit(item.image, pos)
            
        for npc in self.npcs:
            pos = (npc.rect.x + offset_x, npc.rect.y + offset_y + UI_HEIGHT)
            surface.blit(npc.image, pos)

        # Nemici + BARRA SALUTE
        if (mx, my) in self.enemies_cache:
            for enemy in self.enemies_cache[(mx, my)]:
                # Solo se il nemico è "visibile" (per Zola che si nasconde)
                # Zola è visibile se rect.x > 0 (o in altro modo), ma disegniamo l'immagine corrente
                pos = (enemy.rect.x + offset_x, enemy.rect.y + offset_y + UI_HEIGHT)
                surface.blit(enemy.image, pos)
                
                # Disegna Barra HP se il nemico è in gioco (ha coordinate valide)
                if enemy.rect.x >= 0 and hasattr(enemy, 'hp') and hasattr(enemy, 'max_hp'):
                    bar_w = enemy.rect.width
                    bar_h = 6
                    bar_x = pos[0]
                    bar_y = pos[1] - 12 # Poco sopra
                    
                    # Sfondo rosso
                    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_w, bar_h))
                    # Vita verde
                    if enemy.max_hp > 0:
                        ratio = max(0, enemy.hp / enemy.max_hp)
                        fill_w = int(bar_w * ratio)
                        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill_w, bar_h))
                    
                    # Numero HP accanto
                    hp_txt = self.debug_font.render(str(enemy.hp), True, WHITE)
                    surface.blit(hp_txt, (bar_x + bar_w + 5, bar_y - 4))

        for proj in self.projectiles:
            pos = (proj.rect.x + offset_x, proj.rect.y + offset_y + UI_HEIGHT)
            surface.blit(proj.image, pos)
            
        for proj in self.player_projectiles:
            pos = (proj.rect.x + offset_x, proj.rect.y + offset_y + UI_HEIGHT)
            surface.blit(proj.image, pos)