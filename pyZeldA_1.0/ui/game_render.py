import pygame
from settings import *
from mappa import WORLD_MAP
from .styles import draw_ff1_box

def render_game_ui(surface, assets, score, map_x, map_y, player, max_hp, max_mp):
    font = assets['font']
    pygame.draw.rect(surface, UI_BG_COLOR, (0, 0, WINDOW_WIDTH, UI_HEIGHT))
    
    # HP
    surface.blit(font.render("HP", True, WHITE), (30, 25))
    bar_w = 200
    pygame.draw.rect(surface, BAR_BG_COLOR, (80, 27, bar_w, 18))
    
    if max_hp > 0:
        hp_ratio = player.hp / max_hp
        
        # --- MODIFICA: COLORE ROSSO SOTTO IL 30% ---
        current_hp_color = HP_BAR_COLOR
        # Usa il controllo diretto sul valore HP per sicurezza
        if 0 < player.hp <= (max_hp * 0.3):
            current_hp_color = RED
            
        # Larghezza barra
        fill_w = int(hp_ratio * bar_w)
        if fill_w > 0:
            pygame.draw.rect(surface, current_hp_color, (80, 27, fill_w, 18))
        
    pygame.draw.rect(surface, BAR_BORDER_COLOR, (80, 27, bar_w, 18), 2)
    surface.blit(font.render(f"{player.hp}/{max_hp}", True, WHITE), (290, 25))

    # MP
    surface.blit(font.render("MP", True, WHITE), (30, 55))
    pygame.draw.rect(surface, BAR_BG_COLOR, (80, 57, bar_w, 18))
    if max_mp > 0:
        pygame.draw.rect(surface, MP_BAR_COLOR, (80, 57, int((player.mp/max_mp)*bar_w), 18))
    pygame.draw.rect(surface, BAR_BORDER_COLOR, (80, 57, bar_w, 18), 2)
    surface.blit(font.render(f"{player.mp}/{max_mp}", True, WHITE), (290, 55))

    # Score
    surface.blit(font.render(f"SCORE {score}", True, WHITE), (500, 25))
    
    # Minimappa
    rows = len(WORLD_MAP); cols = len(WORLD_MAP[0]) if rows else 0
    smx = WINDOW_WIDTH - (cols * MINIMAP_ROOM_W) - 20
    smy = 10
    for r in range(rows):
        for c in range(cols):
            if WORLD_MAP[r][c]:
                col = MINIMAP_COLOR_CURRENT if c==map_x and r==map_y else MINIMAP_COLOR_EXISTS
                pygame.draw.rect(surface, col, (smx + c*MINIMAP_ROOM_W, smy + r*MINIMAP_ROOM_H, MINIMAP_ROOM_W-2, MINIMAP_ROOM_H-2))
    surface.blit(font.render(f"X:{map_x} Y:{map_y}", True, WHITE), (smx - 100, 25))

def render_action_menu(surface, assets, buttons, selected_idx, options_list):
    font = assets['font']
    cursor_img = assets.get('cursor_small_img') 
    
    item_h = 35 
    pad = 15
    min_w = 180
    
    max_w = 0
    for opt in options_list:
        w = font.size(str(opt))[0]
        if w > max_w: max_w = w
    
    box_w = max(min_w, max_w + (pad * 4))
    box_h = (len(options_list) * item_h) + (pad * 2)
    
    sx = WINDOW_WIDTH - box_w - 40
    sy = WINDOW_HEIGHT - box_h - 40
    
    draw_ff1_box(surface, pygame.Rect(sx, sy, box_w, box_h))
    
    for i, key in enumerate(options_list):
        lbl = str(key)
        tx = sx + pad + 35
        ty = sy + pad + (i * item_h)
        col = (150, 150, 150) if lbl == "Vuoto" else WHITE
        
        surface.blit(font.render(lbl, True, BLACK), (tx+2, ty+2))
        t_surf = font.render(lbl, True, col)
        surface.blit(t_surf, (tx, ty))
        
        if i == selected_idx:
            if cursor_img:
                cy = ty + (t_surf.get_height()//2) - (cursor_img.get_height()//2)
                surface.blit(cursor_img, (tx - 35, cy))
            else: surface.blit(font.render(">", True, WHITE), (tx - 20, ty))

def render_popup(surface, assets, text):
    font = assets['font']
    t_surf = font.render(text, True, WHITE)
    bw = t_surf.get_width() + 60; bh = t_surf.get_height() + 30
    bx = (WINDOW_WIDTH - bw)//2; by = 120
    draw_ff1_box(surface, pygame.Rect(bx, by, bw, bh))
    surface.blit(t_surf, (bx + 30, by + 15))

def render_dialog_box(surface, assets, text, portrait_img):
    font = assets['font']
    bh = 140
    by = WINDOW_HEIGHT - bh
    pygame.draw.rect(surface, DIALOG_BG_COLOR, (0, by, WINDOW_WIDTH, bh))
    pygame.draw.rect(surface, DIALOG_BORDER_COLOR, (0, by, WINDOW_WIDTH, bh), 4)
    
    tx = 30
    if portrait_img:
        s = bh - 40
        surface.blit(pygame.transform.scale(portrait_img, (s, s)), (20, by + 20))
        tx += s + 20
        
    surface.blit(font.render(text, True, WHITE), (tx, by + (bh//2) - 10))