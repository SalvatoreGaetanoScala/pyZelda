import pygame
from settings import *
from .menu_render import render_main_menu, render_notes, render_pause
from .game_render import render_game_ui, render_action_menu, render_popup, render_dialog_box

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 60)
        self.font_title = pygame.font.Font(None, 80)
        
        self.menu_bg = None
        self.btn_images = {}
        try:
            img = pygame.image.load(MENU_IMG_PATH).convert()
            self.menu_bg = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            self.menu_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.menu_bg.fill(BLACK)
            
        paths = {
            "AVVIO": BTN_AVVIO_PATH, "NOTE": BTN_NOTE_PATH, "ESCI_MENU": BTN_ESCI_PATH, 
            "RIPRENDI": BTN_PAUSE_RIPRENDI_PATH, "ESCI_PAUSE": BTN_PAUSE_ESCI_PATH    
        }
        for key, path in paths.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                self.btn_images[key] = img
            except: self.btn_images[key] = None 

        self.dialog_portrait = None
        try:
            img = pygame.image.load(DIALOG_PORTRAIT_PATH).convert_alpha()
            self.dialog_portrait = img
        except Exception as e:
            self.dialog_portrait = None

        # --- MODIFICA: GESTIONE TRIPLO CURSORE ---
        self.cursor_img = None        # Standard (Menu Principale/Pausa) - INGRANDITO
        self.cursor_small_img = None  # Piccolo (Menu Azione '+') - INALTERATO
        self.cursor_target_img = None # Targeting (Magia) - GRANDE
        
        try:
            img = pygame.image.load(MENU_CURSOR_IMG_PATH).convert_alpha()
            
            # 1. Cursore Standard (Menu Principale, Pausa): Ingrandito a 36x36
            self.cursor_img = pygame.transform.scale(img, (36, 36))
            
            # 2. Cursore Piccolo (Menu Azione '+'): Resta 24x24 per non coprire scritte
            self.cursor_small_img = pygame.transform.scale(img, (24, 24))
            
            # 3. Cursore Targeting (Magia): 40x40
            self.cursor_target_img = pygame.transform.scale(img, (40, 40))
            
        except Exception as e:
            print(f"Errore caricamento cursore: {e}")
            self.cursor_img = None
            self.cursor_small_img = None
            self.cursor_target_img = None

        self.donald_menu_img = None
        try:
            img = pygame.image.load(DONALD_MENU_IMG_PATH).convert_alpha()
            self.donald_menu_img = img
        except Exception as e:
            print(f"Errore caricamento donald menu: {e}")
            self.donald_menu_img = None

        # --- GESTIONE TITOLO E COLORE SFONDO ---
        self.menu_title_img = None
        self.menu_bg_color = WHITE 

        try:
            img = pygame.image.load(MENU_TITLE_IMG_PATH).convert_alpha()
            
            try:
                captured_col = img.get_at((0, 0))
                if captured_col.a > 0:
                    self.menu_bg_color = captured_col
            except:
                pass 

            target_w = MENU_TITLE_WIDTH
            original_w = img.get_width()
            original_h = img.get_height()
            
            ratio = target_w / original_w
            new_h = int(original_h * ratio)
            
            self.menu_title_img = pygame.transform.smoothscale(img, (target_w, new_h))
            
        except Exception as e:
            print(f"Errore caricamento titolo menu: {e}")
            self.menu_title_img = None

        self.assets = {
            'font': self.font, 
            'font_large': self.font_large, 
            'font_title': self.font_title,
            'menu_bg': self.menu_bg, 
            'btn_images': self.btn_images,
            'dialog_portrait': self.dialog_portrait,
            'cursor_img': self.cursor_img,              # STANDARD (Grande per menu principali)
            'cursor_small_img': self.cursor_small_img,  # PICCOLO (Per Action Menu)
            'cursor_target_img': self.cursor_target_img, # TARGETING (Magia)
            'donald_menu_img': self.donald_menu_img,
            'menu_title_img': self.menu_title_img,
            'menu_bg_color': self.menu_bg_color 
        }

    def draw_menu(self, surface, buttons, style, selected_idx, options_list):
        render_main_menu(surface, self.assets, buttons, style, selected_idx, options_list)
    def draw_notes(self, surface, style):
        render_notes(surface, self.assets, style)
    def draw_pause(self, surface, buttons, style, selected_idx, options_list):
        render_pause(surface, self.assets, buttons, style, selected_idx, options_list)
    
    def draw_game_ui(self, surface, score, map_x, map_y, player, max_hp, max_mp):
        render_game_ui(surface, self.assets, score, map_x, map_y, player, max_hp, max_mp)
        
    def draw_action_menu(self, surface, buttons, selected_idx, options_list):
        render_action_menu(surface, self.assets, buttons, selected_idx, options_list)
    def draw_popup(self, surface, text):
        render_popup(surface, self.assets, text)
    def draw_dialog(self, surface, text):
        render_dialog_box(surface, self.assets, text, self.assets['dialog_portrait'])