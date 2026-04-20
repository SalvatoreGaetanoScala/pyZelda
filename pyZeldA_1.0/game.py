import pygame
import sys
from settings import *
from sprites import Player, PlayerFireball, Zola
from sprites.items import Potion, Coin, SwordDrop 
from mappa import WORLD_MAP, START_ROOM_X, START_ROOM_Y
from world import World
from ui import UI
from terminale import Terminal
from ui.pause_menu import InGameMenu
from ui.styles import draw_ff1_box
from ui.menu_render import render_slot_selection, render_name_input, render_confirmation, render_delete_confirmation
from save_manager import SaveManager

class Game:
    def __init__(self):
        try: pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
        except: pass
        pygame.init()
        if not pygame.mixer.get_init():
            try: pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            except: pass
            
        flags = pygame.SCALED | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags, vsync=1)
        pygame.display.set_caption("Paperino: Attacco dei Nani")
        self.clock = pygame.time.Clock()

        self.ui = UI()
        self.world = World()
        self.terminal = Terminal()
        self.save_manager = SaveManager()
        
        self.god_mode = False 
        self.ghost_mode = False 
        self.infinite_mp = False
        
        self.lire = 0
        self.play_time = 0
        self.player_name = PLAYER_NAME
        self.current_slot_id = 0 
        
        self.ingame_menu = InGameMenu(self)

        self.cursor_sfx = None
        self.selection_sfx = None
        self.coin_sfx = None
        self.magic_sfx = None
        self.mirror_sfx = None 
        self.back_sfx = None
        self.error_sfx = None
        self.enemy_death_sfx = None
        
        try: self.cursor_sfx = pygame.mixer.Sound(MENU_CURSOR_SFX_PATH); self.cursor_sfx.set_volume(0.2) 
        except: pass
        try: self.selection_sfx = pygame.mixer.Sound(MENU_SELECTION_SFX_PATH); self.selection_sfx.set_volume(0.3)
        except: pass
        try: self.coin_sfx = pygame.mixer.Sound(PICKUP_COIN_SFX_PATH); self.coin_sfx.set_volume(0.3)
        except: pass
        try: self.magic_sfx = pygame.mixer.Sound(FIRE_MAGIC_SFX_PATH); self.magic_sfx.set_volume(0.4)
        except: pass
        
        try: 
            self.mirror_sfx = pygame.mixer.Sound(MIRROR_MAGIC_SFX_PATH)
            self.mirror_sfx.set_volume(0.4)
        except: pass

        try: self.back_sfx = pygame.mixer.Sound(MENU_BACK_SFX_PATH); self.back_sfx.set_volume(0.3)
        except: pass
        try: self.error_sfx = pygame.mixer.Sound(MENU_ERROR_SFX_PATH); self.error_sfx.set_volume(0.3)
        except: pass
        try: self.enemy_death_sfx = pygame.mixer.Sound(ENEMY_DEATH_SFX_PATH); self.enemy_death_sfx.set_volume(0.5)
        except: pass

        self.play_menu_music()

        self.state = "MENU" 
        self.menu_style = "CLASSIC" 
        self.game_over_timer = 0 

        self.menu_options_list = ["NUOVA_PARTITA", "CARICA_PARTITA", "NOTE", "ESCI_MENU"]
        self.pause_options_list = ["RIPRENDI", "SALVA", "ESCI"]
        self.action_options_list = ["ATTACCO", "MAGIA", "OGGETTI"]
        
        self.action_submenu = None
        self.current_action_list = self.action_options_list
        
        self.selected_index = 0
        self.menu_buttons = {}
        self.pause_buttons = {}
        self.action_menu_buttons = {}
        self.show_action_menu = False
        
        self.popup_message = ""
        self.popup_timer = 0
        self.show_dialog = False
        self.current_dialog_text = ""

        self.targeting_enemies = []
        self.target_index = 0
        
        self.slots_info = []
        self.input_text = ""
        self.slot_mode = "NEW" 
        self.show_confirm_overwrite = False
        self.confirm_index = 0 

        self.create_menu_buttons()
        self.create_pause_buttons()
        self.create_action_menu_buttons()

    def create_menu_buttons(self):
        if self.menu_style == "MODERN":
            btn_w, btn_h = 300, 80 
            gap = 90
            start_x = WINDOW_WIDTH - btn_w - 50
            total_h = (btn_h * 4) + (gap * 3)
            start_y = WINDOW_HEIGHT - total_h - 20
            self.menu_buttons = {
                "NUOVA_PARTITA": pygame.Rect(start_x, start_y, btn_w, btn_h),
                "CARICA_PARTITA": pygame.Rect(start_x, start_y + gap, btn_w, btn_h),
                "NOTE": pygame.Rect(start_x, start_y + gap * 2, btn_w, btn_h),
                "ESCI_MENU": pygame.Rect(start_x, start_y + gap * 3, btn_w, btn_h)
            }
        else:
            btn_w, btn_h = 280, 50
            gap = 60
            start_x = (WINDOW_WIDTH // 2) - (btn_w // 2)
            start_y = (WINDOW_HEIGHT // 2) - 20 
            self.menu_buttons = {
                "NUOVA_PARTITA": pygame.Rect(start_x, start_y, btn_w, btn_h),
                "CARICA_PARTITA": pygame.Rect(start_x, start_y + gap, btn_w, btn_h),
                "NOTE": pygame.Rect(start_x, start_y + gap * 2, btn_w, btn_h),
                "ESCI_MENU": pygame.Rect(start_x, start_y + gap * 3, btn_w, btn_h)
            }

    def create_pause_buttons(self):
        p_center_x = WINDOW_WIDTH // 2
        p_center_y = WINDOW_HEIGHT // 2
        if self.menu_style == "MODERN":
            p_btn_w, p_btn_h = PAUSE_BTN_W, PAUSE_BTN_H
            p_gap = 80
        else:
            p_btn_w, p_btn_h = 240, 50
            p_gap = 60
        start_x = p_center_x - (p_btn_w // 2)
        total_h = (p_btn_h * 3) + (p_gap * 2)
        start_y = p_center_y - (total_h // 2) + 50
        
        self.pause_buttons = {
            "RIPRENDI": pygame.Rect(start_x, start_y, p_btn_w, p_btn_h),
            "SALVA": pygame.Rect(start_x, start_y + p_gap, p_btn_w, p_btn_h),
            "ESCI": pygame.Rect(start_x, start_y + p_gap * 2, p_btn_w, p_btn_h)
        }

    def create_action_menu_buttons(self):
        btn_w, btn_h = 180, 40
        gap = 10
        margin_right = 50
        margin_bottom = 50
        total_height = (btn_h * 3) + (gap * 2)
        start_x = WINDOW_WIDTH - btn_w - margin_right
        start_y = WINDOW_HEIGHT - total_height - margin_bottom
        self.action_menu_buttons = {
            "ATTACCO": pygame.Rect(start_x, start_y, btn_w, btn_h),
            "MAGIA":   pygame.Rect(start_x, start_y + btn_h + gap, btn_w, btn_h),
            "OGGETTI": pygame.Rect(start_x, start_y + (btn_h + gap) * 2, btn_w, btn_h)
        }

    def play_menu_music(self):
        try:
            if not pygame.mixer.get_init(): pygame.mixer.init()
            pygame.mixer.music.load(MENU_MUSIC_PATH)
            pygame.mixer.music.set_volume(0.3) 
            pygame.mixer.music.play(-1)
        except Exception as e: print(f"Errore musica menu: {e}")

    def init_game_session(self, load_data=None):
        if hasattr(self, 'player'):
            self.player.stop_sounds()
            
        self.world.reset()
        
        self.score = 0
        self.lire = 0
        self.play_time = 0
        self.map_x = START_ROOM_X
        self.map_y = START_ROOM_Y
        self.player_name = PLAYER_NAME
        
        start_pos = (ROOM_WIDTH // 2, ROOM_HEIGHT // 2)
        if WORLD_MAP[self.map_y][self.map_x]:
            for r, row in enumerate(WORLD_MAP[self.map_y][self.map_x]):
                for c, char in enumerate(row):
                    if char == 'P': start_pos = (c * TILE_SIZE, r * TILE_SIZE)
        
        self.player = Player(*start_pos)
        
        if load_data:
            self.player.level = load_data.get('level', 1)
            self.player.current_xp = load_data.get('current_xp', 0)
            self.player.xp_needed = load_data.get('xp_needed', 10)
            self.player.max_hp = load_data.get('max_hp', 10)
            self.player.hp = load_data.get('hp', 10)
            self.player.max_mp = load_data.get('max_mp', 6)
            self.player.mp = load_data.get('mp', 6)
            self.player.inventory = load_data.get('inventory', {'weapons':[], 'magic':['FIRE', 'SPECCHIO'], 'items':[]})
            self.player.equipped = load_data.get('equipped', {'weapon':None, 'magic':[], 'item':None})
            self.lire = load_data.get('lire', 0)
            self.play_time = load_data.get('play_time', 0)
            self.player_name = load_data.get('player_name', "Eroe")
            
            if 'SPADA' in self.player.inventory['weapons']:
                self.world.sword_collected = True

        self.world.load_room(self.map_x, self.map_y, self.player)
        
        self.transition_offset = pygame.math.Vector2(0, 0)
        self.next_map_coords = (0, 0)
        self.scroll_dir = pygame.math.Vector2(0, 0)
        self.last_player_dir = (0, 0)
        
        self.show_action_menu = False
        self.action_submenu = None
        self.current_action_list = self.action_options_list
        self.god_mode = False 
        self.ghost_mode = False 
        self.infinite_mp = False 
        
        self.popup_timer = 0 
        self.show_dialog = False 
        
        test_potion = Potion(self.player.rect.x + 100, self.player.rect.y)
        self.world.items.add(test_potion)
        
        if self.ingame_menu.active: self.ingame_menu.toggle()

    def gather_save_data(self):
        return {
            "player_name": self.player_name,
            "level": self.player.level,
            "current_xp": self.player.current_xp,
            "xp_needed": self.player.xp_needed,
            "hp": self.player.hp,
            "max_hp": self.player.max_hp,
            "mp": self.player.mp,
            "max_mp": self.player.max_mp,
            "inventory": self.player.inventory,
            "equipped": self.player.equipped,
            "lire": self.lire,
            "play_time": self.play_time
        }
    
    def trigger_game_over(self):
        """Attiva la sequenza di morte."""
        self.state = "GAME_OVER"
        pygame.mixer.music.stop()
        self.player.trigger_death()
        self.game_over_timer = 240 

    def spawn_coin_drop(self, enemy):
        from sprites import Zola
        from sprites.items import Coin
        drop_value = 0
        drop_x, drop_y = enemy.rect.centerx, enemy.rect.centery
        if isinstance(enemy, Zola):
            drop_value = 100
            drop_x, drop_y = self.world.find_safe_drop_pos(drop_x, drop_y)
        else:
            drop_value = 10
        self.world.items.add(Coin(drop_x, drop_y, drop_value))

    def check_collisions(self):
        current_enemies = self.world.get_current_enemies()
        def hitbox_collide(sprite_a, sprite_b):
            rect_a = getattr(sprite_a, 'hitbox', sprite_a.rect)
            rect_b = getattr(sprite_b, 'hitbox', sprite_b.rect)
            return rect_a.colliderect(rect_b)

        if self.player.attacking and self.player.sword_rect:
            for enemy in list(current_enemies):
                if self.player.sword_rect.colliderect(enemy.rect):
                    if hasattr(enemy, 'hp'):
                        enemy.hp -= 1
                        if enemy.hp <= 0:
                            if self.enemy_death_sfx: self.enemy_death_sfx.play()
                            xp_gain = 3 if isinstance(enemy, Zola) else 1
                            if self.player.gain_xp(xp_gain):
                                self.popup_message = "Aumento di livello!"
                                self.popup_timer = 120
                            self.spawn_coin_drop(enemy) 
                            enemy.kill()
                            self.score += 200
                    else:
                        if self.enemy_death_sfx: self.enemy_death_sfx.play()
                        xp_gain = 3 if isinstance(enemy, Zola) else 1
                        if self.player.gain_xp(xp_gain):
                            self.popup_message = "Aumento di livello!"
                            self.popup_timer = 120
                        self.spawn_coin_drop(enemy) 
                        enemy.kill()
                        self.score += 100 
        
        hits = pygame.sprite.groupcollide(self.world.player_projectiles, current_enemies, True, False, collided=hitbox_collide)
        for proj, enemies_hit in hits.items():
            for enemy in enemies_hit:
                if hasattr(enemy, 'hp'):
                    damage = 3 if isinstance(enemy, Zola) else 1
                    enemy.hp -= damage
                    if enemy.hp <= 0:
                        if self.enemy_death_sfx: self.enemy_death_sfx.play()
                        xp_gain = 3 if isinstance(enemy, Zola) else 1
                        if self.player.gain_xp(xp_gain):
                            self.popup_message = "Aumento di livello!"
                            self.popup_timer = 120
                        self.spawn_coin_drop(enemy) 
                        enemy.kill()
                        self.score += 200
                else:
                    if self.enemy_death_sfx: self.enemy_death_sfx.play()
                    xp_gain = 3 if isinstance(enemy, Zola) else 1
                    if self.player.gain_xp(xp_gain):
                        self.popup_message = "Aumento di livello!"
                        self.popup_timer = 120
                    self.spawn_coin_drop(enemy) 
                    enemy.kill()
                    self.score += 100

        hits = pygame.sprite.spritecollide(self.player, current_enemies, False, collided=hitbox_collide)
        if hits:
            if not self.god_mode:
                self.player.take_damage()
                if self.player.hp <= 0:
                    self.trigger_game_over()
        
        proj_hits = pygame.sprite.spritecollide(self.player, self.world.projectiles, False, collided=hitbox_collide)
        for proj in proj_hits:
            if self.player.mirror_active:
                if hasattr(proj, 'velocity'):
                    proj.velocity *= -1
                elif hasattr(proj, 'direction'):
                    proj.direction *= -1
                self.world.projectiles.remove(proj)
                self.world.player_projectiles.add(proj)
            else:
                proj.kill()
                if not self.god_mode:
                    self.player.take_damage()
                    if self.player.hp <= 0:
                        self.trigger_game_over()

        item_hits = pygame.sprite.spritecollide(self.player, self.world.items, False)
        for item in item_hits:
            if hasattr(item, 'type'):
                if item.type == 'sword':
                    item.kill()
                    if 'SPADA' not in self.player.inventory['weapons']:
                        self.player.inventory['weapons'].append('SPADA')
                        if self.player.equipped['weapon'] is None:
                            self.player.equipped['weapon'] = 'SPADA'
                    self.world.sword_collected = True
                    self.popup_message = "Hai ottenuto: Spada"
                    self.popup_timer = 180 
                elif item.type == 'coin':
                    if hasattr(item, 'pickup_delay') and item.pickup_delay <= 0:
                        item.kill()
                        self.lire += item.value
                        if self.coin_sfx: self.coin_sfx.play()
                elif item.type == 'potion':
                    item.kill()
                    self.player.inventory['items'].append("POZIONE")
                    self.popup_message = "Hai trovato: Pozione"
                    self.popup_timer = 180
                    if self.coin_sfx: self.coin_sfx.play()

    def check_room_transition(self):
        p = self.player.rect
        dx, dy = 0, 0
        change = False
        if p.left < 0: dx, dy = -1, 0; change = True
        elif p.right > ROOM_WIDTH: dx, dy = 1, 0; change = True
        elif p.top < 0: dx, dy = 0, -1; change = True
        elif p.bottom > ROOM_HEIGHT: dx, dy = 0, 1; change = True

        if change:
            new_mx, new_my = self.map_x + dx, self.map_y + dy
            if 0 <= new_my < len(WORLD_MAP) and 0 <= new_mx < len(WORLD_MAP[0]):
                if WORLD_MAP[new_my][new_mx] is not None:
                    self.start_transition(dx, dy, new_mx, new_my)
                    return
            if dx == -1: self.player.rect.left = 0
            if dx == 1: self.player.rect.right = ROOM_WIDTH
            if dy == -1: self.player.rect.top = 0
            if dy == 1: self.player.rect.bottom = ROOM_HEIGHT

    def start_transition(self, dx, dy, nmx, nmy):
        self.state = "TRANSITION"
        self.scroll_dir = pygame.math.Vector2(-dx, -dy)
        self.last_player_dir = (dx, dy)
        self.transition_offset = pygame.math.Vector2(0, 0)
        self.next_map_coords = (nmx, nmy)
        self.world.ensure_enemies_loaded(nmx, nmy)
        self.show_action_menu = False
        self.action_submenu = None
        self.show_dialog = False 

    def update_transition(self):
        move_vec = self.scroll_dir * SCROLL_SPEED
        self.transition_offset += move_vec
        
        if abs(self.transition_offset.x) >= ROOM_WIDTH or abs(self.transition_offset.y) >= ROOM_HEIGHT:
            self.state = "PLAYING"
            self.map_x, self.map_y = self.next_map_coords
            self.world.load_room(self.map_x, self.map_y, self.player)
            
            if self.map_x == 1 and self.map_y == 0: pygame.mixer.music.fadeout(500)
            else:
                if not pygame.mixer.music.get_busy():
                    try: 
                        pygame.mixer.music.load(MUSIC_PATH)
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                    except: pass
            
            p_dx, p_dy = self.last_player_dir
            safe_margin = 10 
            if p_dx == 1: self.player.rect.left = safe_margin
            elif p_dx == -1: self.player.rect.right = ROOM_WIDTH - safe_margin
            elif p_dy == 1: self.player.rect.top = safe_margin
            elif p_dy == -1: self.player.rect.bottom = ROOM_HEIGHT - safe_margin
            self.player.hitbox.center = self.player.rect.center

    def handle_navigation(self, direction, list_length):
        if list_length == 0: return
        old_index = self.selected_index
        if direction == "UP": self.selected_index = (self.selected_index - 1) % list_length
        elif direction == "DOWN": self.selected_index = (self.selected_index + 1) % list_length
        if old_index != self.selected_index and self.cursor_sfx: self.cursor_sfx.play()

    def execute_menu_action(self, option_key):
        if self.selection_sfx: self.selection_sfx.play()

        if self.state == "PLAYING" and self.show_action_menu:
            if option_key == "Vuoto":
                if self.error_sfx: self.error_sfx.play()
                return
            
            if self.action_submenu == 'WEAPON':
                if option_key == "SPADA":
                    self.player.attacking = True
                    self.player.attack_cooldown = 15
                    self.show_action_menu = False
                    self.action_submenu = None
                return

            if self.action_submenu == 'MAGIC':
                spell_name = option_key
                if spell_name == "SPECCHIO":
                    if self.player.mp >= MIRROR_COST or self.infinite_mp:
                        self.player.activate_mirror()
                        if self.mirror_sfx: self.mirror_sfx.play()
                        self.show_action_menu = False
                        self.action_submenu = None
                    else:
                        if self.error_sfx: self.error_sfx.play()
                        self.popup_message = "MP Insufficienti!"
                        self.popup_timer = 60
                    return

                if spell_name == "FIRE":
                    if self.player.mp >= 1 or self.infinite_mp:
                        visible_enemies = list(self.world.get_current_enemies())
                        if visible_enemies:
                            self.state = "TARGETING"
                            self.targeting_enemies = visible_enemies
                            self.target_index = 0
                            self.show_action_menu = False
                            self.action_submenu = None
                        else:
                            if self.error_sfx: self.error_sfx.play()
                            self.popup_message = "Nessun bersaglio!"
                            self.popup_timer = 60
                    else:
                        self.popup_message = "MP Insufficienti!"
                        self.popup_timer = 60
                return

            if self.action_submenu == 'ITEMS':
                item_name = option_key.split(" x")[0]
                if item_name == "POZIONE":
                    if "POZIONE" in self.player.inventory['items']:
                        if self.player.heal(POTION_HEAL_AMOUNT):
                            self.player.inventory['items'].remove("POZIONE")
                            if "POZIONE" not in self.player.inventory['items']:
                                if self.player.equipped['item'] == "POZIONE":
                                    self.player.equipped['item'] = None
                            
                            self.show_action_menu = False
                            self.action_submenu = None
                        else:
                            self.popup_message = "Gli HP sono già al massimo!"
                            self.popup_timer = 120
                            if self.error_sfx: self.error_sfx.play()
                            self.show_action_menu = False
                            self.action_submenu = None
                    else:
                        if self.error_sfx: self.error_sfx.play()
                return

            if option_key == "ATTACCO":
                equipped_weapon = self.player.equipped['weapon']
                self.action_submenu = 'WEAPON'
                self.current_action_list = [equipped_weapon] if equipped_weapon else ["Vuoto"]
                self.selected_index = 0
            
            elif option_key == "MAGIA":
                equipped_magic = self.player.equipped['magic']
                self.action_submenu = 'MAGIC'
                self.current_action_list = equipped_magic if equipped_magic else ["Vuoto"]
                self.selected_index = 0
            
            elif option_key == "OGGETTI":
                self.action_submenu = 'ITEMS'
                equipped = self.player.equipped['item']
                if equipped:
                    count = self.player.inventory['items'].count(equipped)
                    display_text = f"{equipped} x{count}" if count > 1 else equipped
                    self.current_action_list = [display_text]
                else:
                    self.current_action_list = ["Vuoto"]
                self.selected_index = 0
            return

        if self.state == "MENU":
            if option_key == "NUOVA_PARTITA":
                self.state = "SLOT_SELECTION"
                self.slot_mode = "NEW"
                self.slots_info = self.save_manager.get_slots_info()
                self.selected_index = 0
            elif option_key == "CARICA_PARTITA":
                self.state = "SLOT_SELECTION"
                self.slot_mode = "LOAD"
                self.slots_info = self.save_manager.get_slots_info()
                self.selected_index = 0
            elif option_key == "NOTE": self.state = "NOTES"
            elif option_key == "ESCI_MENU": pygame.quit(); sys.exit()
        
        elif self.state == "PAUSED":
            if option_key == "RIPRENDI": 
                self.state = "PLAYING"; pygame.mixer.music.unpause()
            elif option_key == "ESCI": 
                self.state = "MENU"; self.play_menu_music(); self.selected_index = 0 
            elif option_key == "SALVA":
                self.show_confirm_overwrite = True
                self.state = "CONFIRM_SAVE"
                self.confirm_index = 0

    def run(self):
        while True:
            dt = self.clock.tick(FPS) 
            if self.state in ["PLAYING", "PAUSED", "TRANSITION", "TARGETING"]:
                self.play_time += dt

            current_options = []
            current_buttons_dict = {} 
            
            if self.state == "MENU": 
                current_options = self.menu_options_list
                current_buttons_dict = self.menu_buttons
            elif self.state == "PAUSED": 
                current_options = self.pause_options_list
                current_buttons_dict = self.pause_buttons
            elif self.state == "PLAYING" and self.show_action_menu and not self.terminal.active:
                current_options = self.current_action_list
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                if self.state == "NAME_INPUT":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(self.input_text) > 0:
                                self.player_name = self.input_text
                                if self.selection_sfx: self.selection_sfx.play()
                                try: pygame.mixer.music.load(MUSIC_PATH); pygame.mixer.music.play(-1)
                                except: pass
                                self.init_game_session() 
                                self.player_name = self.input_text 
                                self.state = "PLAYING"
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "SLOT_SELECTION"
                        else:
                            if len(self.input_text) < 12 and event.unicode.isprintable():
                                self.input_text += event.unicode
                    continue

                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if self.state == "PLAYING" and not self.terminal.active and not self.show_dialog and not self.show_action_menu:
                        self.ingame_menu.toggle()
                        if self.ingame_menu.active and self.selection_sfx:
                            self.selection_sfx.play()
                        continue 
                
                if self.ingame_menu.active:
                    self.ingame_menu.handle_input(event)
                    continue

                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH:
                    if self.state == "PLAYING": self.terminal.toggle()
                if self.terminal.active: self.terminal.handle_event(event, self); continue 

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11: pygame.display.toggle_fullscreen()
                    
                    if self.state == "SLOT_SELECTION":
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                            self.state = "MENU"
                            self.selected_index = 0
                            if self.back_sfx: self.back_sfx.play()
                        elif event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % 3
                            if self.cursor_sfx: self.cursor_sfx.play()
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % 3
                            if self.cursor_sfx: self.cursor_sfx.play()
                        
                        elif event.key == pygame.K_DELETE:
                            if not self.slots_info[self.selected_index]['empty']:
                                self.state = "DELETE_CONFIRM"
                                self.confirm_index = 1 
                                if self.selection_sfx: self.selection_sfx.play()

                        elif event.key == pygame.K_RETURN:
                            self.current_slot_id = self.selected_index
                            if self.slot_mode == "NEW":
                                self.state = "NAME_INPUT"
                                self.input_text = ""
                                if self.selection_sfx: self.selection_sfx.play()
                            elif self.slot_mode == "LOAD":
                                data = self.save_manager.load_game(self.current_slot_id)
                                if data:
                                    if self.selection_sfx: self.selection_sfx.play()
                                    try: pygame.mixer.music.load(MUSIC_PATH); pygame.mixer.music.play(-1)
                                    except: pass
                                    self.init_game_session(load_data=data)
                                    self.state = "PLAYING"
                                else:
                                    if self.error_sfx: self.error_sfx.play()
                        continue

                    if self.state == "CONFIRM_SAVE":
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            self.confirm_index = (self.confirm_index + 1) % 2
                            if self.cursor_sfx: self.cursor_sfx.play()
                        elif event.key == pygame.K_RETURN:
                            if self.confirm_index == 0: 
                                data = self.gather_save_data()
                                self.save_manager.save_game(self.current_slot_id, data)
                                self.popup_message = "Partita Salvata!"
                                self.popup_timer = 120
                                self.state = "PAUSED" 
                            else: 
                                self.state = "PAUSED"
                            if self.selection_sfx: self.selection_sfx.play()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "PAUSED"
                        continue

                    if self.state == "DELETE_CONFIRM":
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            self.confirm_index = (self.confirm_index + 1) % 2
                            if self.cursor_sfx: self.cursor_sfx.play()
                        elif event.key == pygame.K_RETURN:
                            if self.confirm_index == 0: 
                                self.save_manager.delete_save(self.selected_index)
                                self.slots_info = self.save_manager.get_slots_info()
                                self.state = "SLOT_SELECTION"
                            else: 
                                self.state = "SLOT_SELECTION"
                            if self.selection_sfx: self.selection_sfx.play()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "SLOT_SELECTION"
                        continue

                    if self.state == "TARGETING":
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                            self.state = "PLAYING"
                            if self.back_sfx: self.back_sfx.play()
                        
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                            self.target_index = (self.target_index - 1) % len(self.targeting_enemies)
                            if self.cursor_sfx: self.cursor_sfx.play()
                        
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                            self.target_index = (self.target_index + 1) % len(self.targeting_enemies)
                            if self.cursor_sfx: self.cursor_sfx.play()
                            
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            if self.targeting_enemies:
                                target = self.targeting_enemies[self.target_index]
                                if target.alive():
                                    if not self.infinite_mp:
                                        self.player.mp -= 1
                                    
                                    fb = PlayerFireball(self.player.rect.centerx, self.player.rect.centery, 
                                                      target_pos=target.rect.center)
                                    self.world.player_projectiles.add(fb)
                                    if self.magic_sfx: self.magic_sfx.play()
                                    self.state = "PLAYING"
                                else:
                                    self.state = "PLAYING"
                            else:
                                self.state = "PLAYING"
                        continue 
                    
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.state == "PLAYING":
                            if self.show_dialog:
                                self.show_dialog = False
                                if self.selection_sfx: self.selection_sfx.play()
                            elif not self.show_action_menu and not self.ingame_menu.active:
                                npc_hit = pygame.sprite.spritecollideany(self.player, self.world.npcs, collided=pygame.sprite.collide_rect_ratio(1.2)) 
                                if npc_hit:
                                    self.show_dialog = True
                                    self.current_dialog_text = npc_hit.dialog_text
                                    if self.selection_sfx: self.selection_sfx.play()

                        if current_options and (self.state != "PLAYING" or self.show_action_menu):
                            self.execute_menu_action(current_options[self.selected_index])

                    if current_options:
                        if event.key == pygame.K_UP: self.handle_navigation("UP", len(current_options))
                        elif event.key == pygame.K_DOWN: self.handle_navigation("DOWN", len(current_options))
                        
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        if self.state == "PLAYING" and not self.show_dialog and not self.ingame_menu.active: 
                            if self.show_action_menu:
                                self.show_action_menu = False
                                self.action_submenu = None
                                self.current_action_list = self.action_options_list
                            else:
                                self.show_action_menu = True
                                self.action_submenu = None
                                self.current_action_list = self.action_options_list
                                self.selected_index = 0
                            
                    if event.key == pygame.K_BACKSPACE:
                        if self.state == "PLAYING" and self.show_action_menu:
                            if self.back_sfx: self.back_sfx.play()
                            if self.action_submenu: 
                                self.action_submenu = None
                                self.current_action_list = self.action_options_list
                                self.selected_index = 0
                            else:
                                self.show_action_menu = False

                    if event.key == pygame.K_g:
                        if self.state in ["MENU", "PAUSED", "NOTES"]:
                            self.menu_style = "CLASSIC" if self.menu_style == "MODERN" else "MODERN"
                            self.create_menu_buttons(); self.create_pause_buttons()
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "NOTES": self.state = "MENU"; self.selected_index = 0
                        elif self.state == "PLAYING":
                            if self.show_dialog: self.show_dialog = False 
                            elif self.show_action_menu: 
                                if self.action_submenu:
                                    self.action_submenu = None
                                    self.current_action_list = self.action_options_list
                                    self.selected_index = 0
                                else:
                                    self.show_action_menu = False
                            else: self.state = "PAUSED"; self.selected_index = 0; pygame.mixer.music.pause()
                        elif self.state == "PAUSED": self.state = "PLAYING"; pygame.mixer.music.unpause()
                
                elif event.type == pygame.MOUSEMOTION:
                    if not self.show_action_menu and self.state in ["MENU", "PAUSED"]:
                        mouse_pos = event.pos
                        if current_options and current_buttons_dict:
                            new_index = self.selected_index; found = False
                            for i, key in enumerate(current_options):
                                if current_buttons_dict.get(key) and current_buttons_dict[key].collidepoint(mouse_pos):
                                    new_index = i; found = True; break
                            if found and new_index != self.selected_index: self.selected_index = new_index; self.cursor_sfx.play() if self.cursor_sfx else None
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.show_action_menu and self.state in ["MENU", "PAUSED"]:
                        mouse_pos = event.pos
                        if current_options and current_buttons_dict:
                            for key in current_options:
                                if current_buttons_dict.get(key) and current_buttons_dict[key].collidepoint(mouse_pos):
                                    self.execute_menu_action(key); break

            self.terminal.update()
            self.ingame_menu.update()

            self.screen.fill(BLACK)
            
            if self.state == "MENU":
                self.ui.draw_menu(self.screen, self.menu_buttons, self.menu_style, self.selected_index, self.menu_options_list)
            elif self.state == "SLOT_SELECTION":
                render_slot_selection(self.screen, self.ui.assets, self.slots_info, self.selected_index, self.slot_mode)
            
            elif self.state == "DELETE_CONFIRM":
                render_slot_selection(self.screen, self.ui.assets, self.slots_info, self.selected_index, self.slot_mode)
                render_delete_confirmation(self.screen, self.ui.assets, self.confirm_index)

            elif self.state == "NAME_INPUT":
                render_name_input(self.screen, self.ui.assets, self.input_text)
            elif self.state == "NOTES":
                self.ui.draw_notes(self.screen, self.menu_style)
            
            elif self.state == "GAME_OVER":
                self.game_over_timer -= 1
                if self.game_over_timer <= 0:
                    self.state = "SLOT_SELECTION"
                    self.slot_mode = "LOAD"
                    self.slots_info = self.save_manager.get_slots_info()
                    self.selected_index = 0
                
                self.world.draw(self.screen, self.map_x, self.map_y, 0, 0)
                self.player.draw(self.screen, UI_HEIGHT)
                
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0,0))
                
                box_w, box_h = 600, 120
                box_rect = pygame.Rect((WINDOW_WIDTH - box_w)//2, (WINDOW_HEIGHT - box_h)//2, box_w, box_h)
                draw_ff1_box(self.screen, box_rect)
                
                font_big = self.ui.assets['font_large']
                text = font_big.render("Il party è stato sconfitto", True, WHITE)
                text_rect = text.get_rect(center=box_rect.center)
                self.screen.blit(text, text_rect)

            elif self.state == "PLAYING" or self.state == "CONFIRM_SAVE":
                if not self.terminal.active and not self.ingame_menu.active and not self.show_action_menu and self.state == "PLAYING":
                    player_obstacles = [] if self.ghost_mode else self.world.obstacles
                    self.player.update(player_obstacles)
                    
                    self.world.get_current_enemies().update(self.world.obstacles)
                    self.world.update_projectiles(self.player)
                    self.check_collisions()
                    self.check_room_transition()
                    if self.popup_timer > 0: self.popup_timer -= 1
                    self.world.items.update()
                
                self.world.draw(self.screen, self.map_x, self.map_y, 0, 0)
                self.player.draw(self.screen, UI_HEIGHT)
                
                self.ui.draw_game_ui(self.screen, self.score, self.map_x, self.map_y, 
                                     self.player, self.player.max_hp, self.player.max_mp)
                
                # --- AGGIUNTO DISEGNO TIMER SPECCHIO ---
                if self.player.mirror_active:
                    box_w, box_h = 220, 60
                    box_x = (WINDOW_WIDTH - box_w) // 2
                    box_y = 120 
                    
                    rect = pygame.Rect(box_x, box_y, box_w, box_h)
                    draw_ff1_box(self.screen, rect)
                    
                    time_left = (self.player.mirror_timer // 60) + 1
                    txt = self.ui.assets['font'].render(f"Specchio: {time_left}s", True, WHITE)
                    txt_rect = txt.get_rect(center=rect.center)
                    self.screen.blit(txt, txt_rect)
                
                if self.show_action_menu:
                    self.ui.draw_action_menu(self.screen, {}, self.selected_index, self.current_action_list)
                
                if self.popup_timer > 0:
                    self.ui.draw_popup(self.screen, self.popup_message)
                if self.show_dialog:
                    self.ui.draw_dialog(self.screen, self.current_dialog_text)
                if self.ingame_menu.active:
                    self.ingame_menu.draw(self.screen)

            elif self.state == "PAUSED":
                self.world.draw(self.screen, self.map_x, self.map_y, 0, 0)
                self.player.draw(self.screen, UI_HEIGHT)
                self.ui.draw_game_ui(self.screen, self.score, self.map_x, self.map_y, self.player, self.player.max_hp, self.player.max_mp)
                self.ui.draw_pause(self.screen, self.pause_buttons, self.menu_style, self.selected_index, self.pause_options_list)
            
            if self.state == "CONFIRM_SAVE":
                self.ui.draw_pause(self.screen, self.pause_buttons, self.menu_style, self.selected_index, self.pause_options_list)
                render_confirmation(self.screen, self.ui.assets, self.confirm_index)

            elif self.state == "TARGETING":
                self.world.draw(self.screen, self.map_x, self.map_y, 0, 0)
                self.player.draw(self.screen, UI_HEIGHT)
                self.ui.draw_game_ui(self.screen, self.score, self.map_x, self.map_y, self.player, self.player.max_hp, self.player.max_mp)
                
                info_text_str = "Selezionare il bersaglio"
                info_surf = self.ui.assets['font'].render(info_text_str, True, WHITE)
                info_rect = info_surf.get_rect(center=(WINDOW_WIDTH//2, 100))
                box_rect = info_rect.inflate(40, 20)
                draw_ff1_box(self.screen, box_rect)
                self.screen.blit(info_surf, info_rect)
                
                if self.targeting_enemies:
                    target = self.targeting_enemies[self.target_index]
                    cursor_img = self.ui.assets['cursor_target_img']
                    if cursor_img:
                        cw = cursor_img.get_width(); ch = cursor_img.get_height(); padding = -15 
                        if target.rect.left > (cw + 10): 
                            draw_x = target.rect.left - cw - padding
                            draw_y = target.rect.centery - (ch // 2)
                            self.screen.blit(cursor_img, (draw_x, draw_y))
                        else:
                            flipped_cursor = pygame.transform.flip(cursor_img, True, False)
                            draw_x = target.rect.right + padding
                            draw_y = target.rect.centery - (ch // 2)
                            self.screen.blit(flipped_cursor, (draw_x, draw_y))
                    else:
                        pygame.draw.rect(self.screen, RED, target.rect, 3)

            elif self.state == "TRANSITION":
                self.update_transition()
                self.world.draw(self.screen, self.map_x, self.map_y, self.transition_offset.x, self.transition_offset.y)
                next_off_x = self.transition_offset.x - (ROOM_WIDTH * self.scroll_dir.x)
                next_off_y = self.transition_offset.y - (ROOM_HEIGHT * self.scroll_dir.y)
                self.world.draw(self.screen, self.next_map_coords[0], self.next_map_coords[1], next_off_x, next_off_y)
                self.ui.draw_game_ui(self.screen, self.score, self.map_x, self.map_y, self.player, self.player.max_hp, self.player.max_mp)

            self.terminal.draw(self.screen)
            pygame.display.flip()