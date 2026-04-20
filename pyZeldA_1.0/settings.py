import pygame
import os

# --- GESTIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

# --- CONFIGURAZIONI GENERALI ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TILE_SIZE = 64

# --- COLORI ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
O = (255, 165, 0)   
B = (0, 0, 180)     
W_COL = (245, 245, 245) 
M = (255, 0, 255)   

# --- COLORI UI E BARRE ---
BAR_BG_COLOR = (50, 50, 50)       
BAR_BORDER_COLOR = (200, 200, 200) 
HP_BAR_COLOR = (40, 220, 40)      
MP_BAR_COLOR = (40, 100, 255)     

DIALOG_BG_COLOR = (0, 0, 150) 
DIALOG_BORDER_COLOR = (200, 200, 200)
MENU_BG_COLOR = (0, 0, 180)
MENU_BORDER_COLOR = (255, 255, 255)
UI_BG_COLOR = (20, 20, 20)
UI_HEIGHT = 100

# --- COLORI AMBIENTE ---
FLOOR_COLOR = (235, 205, 155) 
WATER_COLOR = (64, 164, 223)
BRIDGE_COLOR = (139, 69, 19)
WOOD_WALL_COLOR = (101, 67, 33)

# Alias per Sprite 8-bit
K = BLACK 
R = RED
W = W_COL
SKIN = (255, 200, 150) 
BROWN = (100, 50, 0)   
S = SKIN
N = BROWN

# --- PARAMETRI GIOCATORE ---
PLAYER_SPEED = 5
PLAYER_MAX_HP = 10
PLAYER_MAX_MP = 6
PLAYER_IFRAMES = 60
PLAYER_FIREBALL_SPEED = 8

# --- PARAMETRI NEMICI ---
FIREBALL_SPEED = 6

# --- MENU DI GIOCO ---
MENU_SLIDE_SPEED = 40
PLAYER_NAME = "Paperino" # Default fallback
LEVEL_1_NAME = "Memelandia"

# --- PARAMETRI TERMINALE ---
TERMINAL_HEIGHT_RATIO = 0.35 
TERMINAL_ANIMATION_SPEED = 15
TERMINAL_FONT_SIZE = 30

# --- PERCORSI ASSETS ---
MENU_IMG_PATH = get_path("assets/sprites/menù/start_menu.png")
MENU_TITLE_IMG_PATH = get_path("assets/sprites/menù/attacco_dei_nani.png")
MENU_TITLE_WIDTH = 550 

BTN_AVVIO_PATH = get_path("assets/sprites/menù/avvio.png")
BTN_NOTE_PATH = get_path("assets/sprites/menù/note.png")
BTN_ESCI_PATH = get_path("assets/sprites/menù/esci.png")
BTN_PAUSE_RIPRENDI_PATH = get_path("assets/sprites/menù/riprendi.png")
BTN_PAUSE_ESCI_PATH = get_path("assets/sprites/menù/esci.png")

MENU_CURSOR_IMG_PATH = get_path("assets/sprites/menù/cursor.png")
DONALD_MENU_IMG_PATH = get_path("assets/sprites/player/menu/donald_menu.png")

# --- OGGETTI ---
POTION_IMG_PATH = get_path("assets/sprites/oggetti/pozione.png")
POTION_HEAL_AMOUNT = 30

# --- MAGICHE ---
MIRROR_MAGIC_IMG_PATH = get_path("assets/sprites/player/magia/specchio.png")
MIRROR_COST = 2
MIRROR_DURATION = 600 # MODIFICATO: 10 Secondi (60fps * 10)

# AMBIENTE
WALL_IMG_PATH = get_path("assets/sprites/level/l1/nature.jpg")
TREE_IMG_PATH = get_path("assets/sprites/level/l1/albero1.png")
BRIDGE_IMG_PATH = get_path("assets/sprites/level/l1/ponte.png")
WATER_IMG_PATH = get_path("assets/sprites/level/l1/water.jpeg") 
HOUSE_WALL_IMG_PATH = get_path("assets/sprites/level/l1/wood_wall.jpg")

# OGGETTI E DROP
SWORD_IMG_PATH = get_path("assets/sprites/player/armi/8bit/sword_8bit.png")
FIRE_MAGIC_IMG_PATH = get_path("assets/sprites/player/magia/fire.png")
COIN_10_IMG_PATH = get_path("assets/sprites/monete/c10.png")
COIN_100_IMG_PATH = get_path("assets/sprites/monete/c100.png")

# NEMICI & NPC
ZOLA_IMG_PATH = get_path("assets/sprites/nemici/zola.png")
FIREBALL_IMG_PATH = get_path("assets/sprites/nemici/fireball.png") 
DIALOG_PORTRAIT_PATH = get_path("assets/sprites/personaggi/bonolis.png")

# AUDIO
MENU_MUSIC_PATH = get_path("assets/audio/musica/ff_11_prelude.mp3")
MUSIC_PATH = get_path("assets/audio/musica/ff4_overworld_8bit.mp3")
MENU_CURSOR_SFX_PATH = get_path("assets/audio/effetti/menu/cursor.mp3")
MENU_SELECTION_SFX_PATH = get_path("assets/audio/effetti/menu/selection.mp3")
PLAYER_HURT_SFX_PATH = get_path("assets/audio/effetti/player/papero_che_si_fa_male.mp3")
SWORD_SFX_PATH = get_path("assets/audio/effetti/player/sword.wav")
PLAYER_LOW_HP_SFX_PATH = get_path("assets/audio/effetti/player/low_hp.mp3")
PLAYER_RECOVERY_SFX_PATH = get_path("assets/audio/effetti/player/recovery.mp3")
ENEMY_DEATH_SFX_PATH = get_path("assets/audio/effetti/nemici/nemico_sconfitto.wav")

PICKUP_COIN_SFX_PATH = get_path("assets/audio/effetti/ambiente/pickupCoin.wav")
FIRE_MAGIC_SFX_PATH = get_path("assets/audio/effetti/magia/fire.wav")
MIRROR_MAGIC_SFX_PATH = get_path("assets/audio/effetti/magia/specchio.wav") 

MENU_BACK_SFX_PATH = get_path("assets/audio/effetti/menu/indietro.mp3")
MENU_ERROR_SFX_PATH = get_path("assets/audio/effetti/menu/error.mp3")

# Parametri UI
PAUSE_BTN_W = 200
PAUSE_BTN_H = 50

# Parametri Minimappa
MINIMAP_ROOM_W = 32
MINIMAP_ROOM_H = 20
MINIMAP_MARGIN_X = 20
MINIMAP_MARGIN_Y = 10 
MINIMAP_COLOR_EXIST = (100, 100, 100)
MINIMAP_COLOR_CURRENT = (0, 255, 0)
MINIMAP_COLOR_EXISTS = (80, 80, 80)

SCROLL_SPEED = 10
ROOM_WIDTH = WINDOW_WIDTH
ROOM_HEIGHT = WINDOW_HEIGHT - UI_HEIGHT