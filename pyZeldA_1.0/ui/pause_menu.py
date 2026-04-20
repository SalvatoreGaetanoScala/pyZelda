import pygame
from settings import *
from .styles import draw_ff1_box
from collections import Counter

class InGameMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        
        # Font
        self.font_size = 36
        self.font = pygame.font.Font(None, self.font_size)
        self.font_small = pygame.font.Font(None, 30)
        self.font_header = pygame.font.Font(None, 50) 
        
        # Stati menu
        self.state = "MAIN" 
        
        # Categorie
        self.categories = ["ARMI", "MAGIE", "OGGETTI"]
        self.selected_cat_idx = 0
        
        # Liste
        self.current_items_raw = []   
        self.current_items_display = [] 
        self.selected_item_idx = 0
        
        # Opzioni
        self.options = []
        self.selected_option_idx = 0
        self.target_item_name = None 

        # Assets
        self.donald_img = None
        self.cursor_img = None
        
        try:
            img = pygame.image.load(DONALD_MENU_IMG_PATH).convert_alpha()
            scale_h = 280 
            scale_w = int(img.get_width() * (scale_h / img.get_height()))
            self.donald_img = pygame.transform.scale(img, (scale_w, scale_h))
        except Exception as e:
            print(f"Menu: Errore img Paperino: {e}")

        try:
            cur = pygame.image.load(MENU_CURSOR_IMG_PATH).convert_alpha()
            self.cursor_img = pygame.transform.scale(cur, (40, 40))
        except Exception as e:
            print(f"Menu: Errore img Cursore: {e}")

    def toggle(self):
        self.active = not self.active
        self.state = "MAIN"
        self.selected_cat_idx = 0
        if self.active:
            self.play_sound("select")
        else:
            self.play_sound("back")

    def play_sound(self, sound_type):
        if sound_type == "cursor" and self.game.cursor_sfx:
            self.game.cursor_sfx.play()
        elif sound_type == "select" and self.game.selection_sfx:
            self.game.selection_sfx.play()
        elif sound_type == "back" and self.game.back_sfx:
            self.game.back_sfx.play()
        elif sound_type == "error" and self.game.error_sfx:
            self.game.error_sfx.play()

    def get_display_list(self, raw_list):
        if not raw_list:
            return ["Vuoto"]
        counts = Counter(raw_list)
        display_list = []
        for name in sorted(counts.keys()):
            count = counts[name]
            if count > 1: display_list.append(f"{name} x{count}")
            else: display_list.append(name)
        return display_list

    def get_real_item_name(self, display_string):
        if display_string == "Vuoto": return None
        return display_string.split(" x")[0]

    def is_equipped(self, category, item_name):
        if not item_name: return False
        player = self.game.player
        if category == "ARMI": return player.equipped['weapon'] == item_name
        elif category == "MAGIE": return item_name in player.equipped['magic']
        elif category == "OGGETTI": return player.equipped['item'] == item_name
        return False

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                if self.state == "OPTIONS":
                    self.state = "LIST"
                    self.play_sound("back")
                elif self.state == "LIST":
                    self.state = "MAIN"
                    self.play_sound("back")
                elif self.state == "MAIN":
                    self.toggle()
                return

            if event.key == pygame.K_UP:
                self.play_sound("cursor")
                if self.state == "MAIN":
                    self.selected_cat_idx = (self.selected_cat_idx - 1) % len(self.categories)
                elif self.state == "LIST":
                    if self.current_items_display:
                        self.selected_item_idx = (self.selected_item_idx - 1) % len(self.current_items_display)
                elif self.state == "OPTIONS":
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
            
            elif event.key == pygame.K_DOWN:
                self.play_sound("cursor")
                if self.state == "MAIN":
                    self.selected_cat_idx = (self.selected_cat_idx + 1) % len(self.categories)
                elif self.state == "LIST":
                    if self.current_items_display:
                        self.selected_item_idx = (self.selected_item_idx + 1) % len(self.current_items_display)
                elif self.state == "OPTIONS":
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                if self.state == "MAIN":
                    cat = self.categories[self.selected_cat_idx]
                    
                    if cat == "ARMI": self.current_items_raw = self.game.player.inventory['weapons']
                    elif cat == "MAGIE": self.current_items_raw = self.game.player.inventory['magic']
                    elif cat == "OGGETTI": self.current_items_raw = self.game.player.inventory['items']
                    
                    self.current_items_display = self.get_display_list(self.current_items_raw)
                    self.state = "LIST"
                    self.selected_item_idx = 0
                    self.play_sound("select")

                elif self.state == "LIST":
                    display_str = self.current_items_display[self.selected_item_idx]
                    if display_str == "Vuoto":
                        self.play_sound("error")
                        return

                    self.target_item_name = self.get_real_item_name(display_str)
                    cat = self.categories[self.selected_cat_idx]
                    
                    self.options = []
                    if cat == "OGGETTI" and self.target_item_name == "POZIONE":
                        self.options.append("USA")
                    
                    if self.is_equipped(cat, self.target_item_name):
                        self.options.append("RIMUOVI")
                    else:
                        self.options.append("EQUIPAGGIA")
                    
                    self.state = "OPTIONS"
                    self.selected_option_idx = 0
                    self.play_sound("select")

                elif self.state == "OPTIONS":
                    action = self.options[self.selected_option_idx]
                    cat = self.categories[self.selected_cat_idx]
                    player = self.game.player
                    
                    if action == "USA":
                        if self.target_item_name == "POZIONE":
                            if player.heal(POTION_HEAL_AMOUNT):
                                player.inventory['items'].remove("POZIONE")
                                self.play_sound("select")
                                self.current_items_raw = player.inventory['items']
                                self.current_items_display = self.get_display_list(self.current_items_raw)
                                
                                if "POZIONE" not in player.inventory['items']:
                                    if player.equipped['item'] == "POZIONE":
                                        player.equipped['item'] = None
                                
                                if not self.current_items_raw:
                                    self.selected_item_idx = 0
                                elif self.selected_item_idx >= len(self.current_items_display):
                                    self.selected_item_idx = len(self.current_items_display) - 1
                                self.state = "LIST" 
                            else:
                                self.game.popup_message = "Gli HP sono già al massimo!"
                                self.game.popup_timer = 120
                                self.play_sound("error")
                                self.toggle()

                    elif action == "EQUIPAGGIA":
                        if cat == "ARMI": player.equipped['weapon'] = self.target_item_name
                        elif cat == "MAGIE":
                            if self.target_item_name not in player.equipped['magic']:
                                player.equipped['magic'].append(self.target_item_name)
                        elif cat == "OGGETTI": player.equipped['item'] = self.target_item_name
                        self.play_sound("select")
                        self.state = "LIST"

                    elif action == "RIMUOVI":
                        if cat == "ARMI":
                            if player.equipped['weapon'] == self.target_item_name: player.equipped['weapon'] = None
                        elif cat == "MAGIE":
                            if self.target_item_name in player.equipped['magic']: player.equipped['magic'].remove(self.target_item_name)
                        elif cat == "OGGETTI":
                            if player.equipped['item'] == self.target_item_name: player.equipped['item'] = None
                        self.play_sound("select")
                        self.state = "LIST"

    def update(self):
        pass

    def draw(self, surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(220)
        surface.blit(overlay, (0, 0))
        
        # --- DEFINIZIONE LAYOUT ---
        top_left_x = 50
        top_left_y = 60
        top_left_w = 300
        top_left_h = 300 

        # Box Info Sotto
        bot_left_x = top_left_x
        bot_left_y = top_left_y + top_left_h + 20 
        bot_left_w = top_left_w
        bot_left_h = WINDOW_HEIGHT - bot_left_y - 60 

        # Box Destro
        right_box_x = top_left_x + top_left_w + 20
        right_box_y = top_left_y
        right_box_w = WINDOW_WIDTH - right_box_x - 50
        right_box_h = WINDOW_HEIGHT - right_box_y - 60

        # --- DISEGNO BOX SINISTRI ---
        draw_ff1_box(surface, pygame.Rect(top_left_x, top_left_y, top_left_w, top_left_h))
        draw_ff1_box(surface, pygame.Rect(bot_left_x, bot_left_y, bot_left_w, bot_left_h))
        
        # --- CONTENUTO: CATEGORIE ---
        start_text_y = top_left_y + 50
        for i, cat in enumerate(self.categories):
            is_active = (i == self.selected_cat_idx)
            col = WHITE if is_active and self.state == "MAIN" else (120, 120, 120)
            if self.state != "MAIN" and is_active: col = YELLOW
            
            txt_surf = self.font.render(cat, True, col)
            pos_y = start_text_y + (i * 60)
            surface.blit(txt_surf, (top_left_x + 50, pos_y))
            
            if self.state == "MAIN" and is_active:
                if self.cursor_img:
                    cy = pos_y + (txt_surf.get_height() // 2) - (self.cursor_img.get_height() // 2)
                    surface.blit(self.cursor_img, (top_left_x + 10, cy))
                else:
                    surface.blit(self.font.render(">", True, WHITE), (top_left_x + 20, pos_y))

        # --- CONTENUTO: INFO ---
        info_start_x = bot_left_x + 30
        info_start_y = bot_left_y + 40
        line_spacing = 50
        info_lines = [
            f"Lire:  {self.game.lire}",
            f"Tempo: {int(self.game.play_time/1000 // 60)}:{int(self.game.play_time/1000 % 60):02d}",
            f"Luogo: {LEVEL_1_NAME}"
        ]
        for i, line in enumerate(info_lines):
            txt = self.font.render(line, True, WHITE) 
            surface.blit(txt, (info_start_x, info_start_y + (i * line_spacing)))

        # --- CONTENUTO: BOX DESTRO ---
        if self.state == "MAIN":
            # --- BOX SUPERIORE ---
            rt_h = 350
            draw_ff1_box(surface, pygame.Rect(right_box_x, right_box_y, right_box_w, rt_h))
            
            content_x = right_box_x + 40
            content_y = right_box_y + 35
            
            if self.donald_img:
                surface.blit(self.donald_img, (content_x, content_y))
                stats_x = content_x + self.donald_img.get_width() + 40
            else:
                stats_x = content_x
            
            stats_y = right_box_y + 20
            p = self.game.player
            
            name_surf = self.font_header.render(PLAYER_NAME, True, WHITE)
            surface.blit(name_surf, (stats_x, stats_y))
            pygame.draw.line(surface, WHITE, (stats_x, stats_y + 40), (stats_x + 300, stats_y + 40), 2)
            
            stats_lines = [
                f"Livello: {p.level}",
                f"HP:      {p.hp} / {p.max_hp}",
                f"MP:      {p.mp} / {p.max_mp}",
            ]
            for k, line in enumerate(stats_lines):
                txt = self.font.render(line, True, (220, 220, 220))
                surface.blit(txt, (stats_x, stats_y + 60 + (k * 50)))

            # --- DISEGNO BARRA ESPERIENZA ---
            # Posizione sotto le statistiche
            xp_bar_y = stats_y + 60 + (len(stats_lines) * 50) + 10
            xp_bar_w = 200
            xp_bar_h = 15
            
            # Sfondo Barra
            pygame.draw.rect(surface, (50, 50, 50), (stats_x, xp_bar_y, xp_bar_w, xp_bar_h))
            pygame.draw.rect(surface, WHITE, (stats_x, xp_bar_y, xp_bar_w, xp_bar_h), 2)
            
            # Riempimento Barra
            if p.xp_needed > 0:
                ratio = p.current_xp / p.xp_needed
                fill_w = int(xp_bar_w * ratio)
                if fill_w > 0:
                    pygame.draw.rect(surface, (0, 200, 255), (stats_x, xp_bar_y, fill_w, xp_bar_h))
            
            # Testo Mancano X XP
            remaining = p.xp_needed - p.current_xp
            xp_text = self.font_small.render(f"Mancano {remaining} XP", True, (180, 180, 255))
            surface.blit(xp_text, (stats_x, xp_bar_y + 20))


            # --- BOX INFERIORE (Vuoto per ora o descrizione) ---
            # Se vuoi lasciare la parte sotto vuota o unita, possiamo fare un unico box grande
            # Ma seguendo il layout 2.jpg che divide le cose:
            rb_y = right_box_y + rt_h + 20
            rb_h = right_box_h - rt_h - 20
            draw_ff1_box(surface, pygame.Rect(right_box_x, rb_y, right_box_w, rb_h))
            
            # Qui potresti mettere descrizione o altro. Per ora vuoto.

        elif self.state in ["LIST", "OPTIONS"]:
            # UNICO BOX GRANDE
            draw_ff1_box(surface, pygame.Rect(right_box_x, right_box_y, right_box_w, right_box_h))
            
            content_x = right_box_x + 40
            content_y = right_box_y + 40
            
            cat_title = self.categories[self.selected_cat_idx]
            title_surf = self.font_header.render(cat_title, True, YELLOW)
            surface.blit(title_surf, (content_x, content_y))
            
            list_start_y = content_y + 70
            for i, item_str in enumerate(self.current_items_display):
                if i > 12: break
                is_sel = (i == self.selected_item_idx)
                col = WHITE if is_sel and self.state == "LIST" else (180, 180, 180)
                if self.state == "OPTIONS" and is_sel: col = YELLOW

                txt_surf = self.font.render(item_str, True, col)
                pos_y = list_start_y + (i * 45)
                surface.blit(txt_surf, (content_x + 40, pos_y))
                
                if self.state == "LIST" and is_sel:
                    if self.cursor_img:
                        cy = pos_y + (txt_surf.get_height()//2) - (self.cursor_img.get_height()//2)
                        surface.blit(self.cursor_img, (content_x, cy))
                    else:
                        surface.blit(self.font.render(">", True, WHITE), (content_x + 10, pos_y))

                real_name = self.get_real_item_name(item_str)
                current_cat = self.categories[self.selected_cat_idx]
                if self.is_equipped(current_cat, real_name):
                    e_surf = self.font_small.render("[E]", True, YELLOW)
                    surface.blit(e_surf, (content_x + 40 + txt_surf.get_width() + 15, pos_y + 5))

        if self.state == "OPTIONS":
            opt_w, opt_h = 250, 80 + (len(self.options)*50)
            opt_x = right_box_x + 100
            opt_y = right_box_y + 150 + (self.selected_item_idx * 45)
            if opt_y + opt_h > right_box_y + right_box_h - 20: opt_y = right_box_y + right_box_h - opt_h - 20
            
            draw_ff1_box(surface, pygame.Rect(opt_x, opt_y, opt_w, opt_h))
            for i, opt in enumerate(self.options):
                col = WHITE if i == self.selected_option_idx else (150, 150, 150)
                txt_surf = self.font.render(opt, True, col)
                tx, ty = opt_x + 60, opt_y + 40 + (i * 50)
                surface.blit(txt_surf, (tx, ty))
                if i == self.selected_option_idx:
                    if self.cursor_img:
                        cy = ty + (txt_surf.get_height()//2) - (self.cursor_img.get_height()//2)
                        surface.blit(self.cursor_img, (tx - 40, cy))
                    else:
                        surface.blit(self.font.render(">", True, WHITE), (tx - 25, ty))