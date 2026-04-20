import pygame
from settings import *
from .styles import draw_ff1_box
from .note import GAME_NOTES_LIST 

def render_main_menu(surface, assets, buttons, style, selected_idx, options_list):
    """Disegna il menu principale."""
    
    if style == "MODERN":
        surface.blit(assets['menu_bg'], (0, 0))
    else:
        bg_col = assets.get('menu_bg_color', WHITE)
        surface.fill(bg_col)
    
    font = assets['font']
    cursor_img = assets.get('cursor_img')
    
    if style == "CLASSIC":
        all_rects = [buttons[k] for k in options_list if k in buttons]
        box_rect = None
        if all_rects:
            union_rect = all_rects[0].unionall(all_rects)
            box_rect = union_rect.inflate(100, 50)
            draw_ff1_box(surface, box_rect)

        title_img = assets.get('menu_title_img')
        if title_img and box_rect:
            img_rect = title_img.get_rect(midbottom=(WINDOW_WIDTH // 2, box_rect.top - 20))
            surface.blit(title_img, img_rect)
        elif title_img:
            img_rect = title_img.get_rect(center=(WINDOW_WIDTH // 2, 200))
            surface.blit(title_img, img_rect)

    for i, key in enumerate(options_list):
        rect = buttons.get(key)
        if not rect: continue
        
        # Etichette personalizzate
        label_map = {
            "NUOVA_PARTITA": "NUOVA PARTITA",
            "CARICA_PARTITA": "CARICA PARTITA",
            "NOTE": "NOTE",
            "ESCI_MENU": "ESCI"
        }
        label = label_map.get(key, key)
        
        if style == "MODERN" and assets['btn_images'].get(key):
            btn_img = assets['btn_images'][key]
            if i == selected_idx:
                scaled_img = pygame.transform.smoothscale(btn_img, (rect.width + 10, rect.height + 5))
                img_rect = scaled_img.get_rect(center=rect.center)
                surface.blit(scaled_img, img_rect)
            else:
                img_rect = btn_img.get_rect(center=rect.center)
                surface.blit(btn_img, img_rect)
        else:
            txt_shadow = font.render(label, True, BLACK)
            shadow_rect = txt_shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            surface.blit(txt_shadow, shadow_rect)
            
            txt = font.render(label, True, WHITE)
            txt_rect = txt.get_rect(center=rect.center)
            surface.blit(txt, txt_rect)

        if i == selected_idx:
            if cursor_img:
                cy = rect.centery - (cursor_img.get_height() // 2)
                surface.blit(cursor_img, (rect.left - 50, cy))
            else:
                cursor_txt = font.render(">", True, WHITE)
                surface.blit(cursor_txt, (rect.left - 30, rect.centery - 15))

    if style == "CLASSIC":
        hint = font.render("Autore: Scala Salvatore Gaetano", True, BLACK)
        surface.blit(hint, hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))

def render_slot_selection(surface, assets, slots_info, selected_idx, mode):
    """Disegna la schermata di selezione slot (3 box blu)."""
    surface.fill((20, 20, 40)) 
    font = assets['font']
    
    title_text = "SELEZIONA SLOT"
    title = font.render(title_text, True, WHITE)
    surface.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 80)))
    
    # Dimensioni box slot
    slot_w, slot_h = 600, 120
    start_x = (WINDOW_WIDTH - slot_w) // 2
    start_y = 180
    gap = 40
    
    for i, info in enumerate(slots_info):
        rect = pygame.Rect(start_x, start_y + i*(slot_h+gap), slot_w, slot_h)
        
        # Disegno Box Blu
        draw_ff1_box(surface, rect)
        
        # Cursore
        if i == selected_idx:
            cursor_img = assets.get('cursor_img')
            if cursor_img:
                cy = rect.centery - (cursor_img.get_height() // 2)
                surface.blit(cursor_img, (rect.left - 60, cy))
            else:
                arrow = font.render(">", True, WHITE)
                surface.blit(arrow, (rect.left - 40, rect.centery - 15))

        # Testo dentro lo slot
        if info['empty']:
            txt = font.render(f"Nuova Partita", True, (180, 180, 180))
            if mode == "LOAD":
                txt = font.render(f"Slot {i+1} - Vuoto", True, (150, 150, 150))
            surface.blit(txt, txt.get_rect(center=rect.center))
        else:
            name_txt = font.render(f"{info['name']}", True, WHITE)
            lvl_txt = font.render(f"Liv: {info['level']}", True, YELLOW)
            
            min = int(info['play_time'] / 1000 // 60)
            sec = int(info['play_time'] / 1000 % 60)
            time_txt = font.render(f"{min}:{sec:02d}", True, (200, 200, 255))
            
            surface.blit(name_txt, (rect.x + 40, rect.centery - 20))
            surface.blit(lvl_txt, (rect.x + 300, rect.centery - 20))
            surface.blit(time_txt, (rect.x + 450, rect.centery - 20))
    
    # Hint diverso se lo slot non è vuoto
    if not slots_info[selected_idx]['empty']:
        hint_text = "Premi INVIO per selezionare, CANC per eliminare, ESC per tornare"
    else:
        hint_text = "Premi INVIO per selezionare, ESC per tornare indietro"
        
    hint = font.render(hint_text, True, (150, 150, 150))
    surface.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50)))

def render_name_input(surface, assets, current_text):
    """Disegna la schermata di inserimento nome."""
    surface.fill((20, 20, 40))
    font = assets['font']
    
    msg = font.render("Inserisci il nome del tuo eroe:", True, WHITE)
    surface.blit(msg, msg.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80)))
    
    input_w, input_h = 400, 60
    input_rect = pygame.Rect((WINDOW_WIDTH - input_w)//2, (WINDOW_HEIGHT - input_h)//2, input_w, input_h)
    draw_ff1_box(surface, input_rect)
    
    txt = font.render(current_text + "_", True, YELLOW)
    surface.blit(txt, txt.get_rect(center=input_rect.center))
    
    hint = font.render("Invio per confermare, ESC per annullare", True, (150, 150, 150))
    surface.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)))

def render_confirmation(surface, assets, selected_idx):
    """Disegna il popup 'Vuoi sovrascrivere?' sopra il menu pausa."""
    # Overlay scuro
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    # Box centrale
    box_w, box_h = 400, 250
    box_rect = pygame.Rect((WINDOW_WIDTH - box_w)//2, (WINDOW_HEIGHT - box_h)//2, box_w, box_h)
    draw_ff1_box(surface, box_rect)
    
    font = assets['font']
    cursor_img = assets.get('cursor_img')
    
    # Testo Domanda
    q_line1 = font.render("Vuoi sovrascrivere", True, WHITE)
    q_line2 = font.render("i dati esistenti?", True, WHITE)
    surface.blit(q_line1, q_line1.get_rect(center=(box_rect.centerx, box_rect.top + 50)))
    surface.blit(q_line2, q_line2.get_rect(center=(box_rect.centerx, box_rect.top + 80)))
    
    # Opzioni SI / NO
    opts = ["Sì", "No"]
    start_y = box_rect.top + 150
    gap = 50
    
    for i, opt in enumerate(opts):
        col = YELLOW if i == selected_idx else (180, 180, 180)
        txt = font.render(opt, True, col)
        txt_rect = txt.get_rect(center=(box_rect.centerx, start_y + i*gap))
        surface.blit(txt, txt_rect)
        
        if i == selected_idx:
             if cursor_img:
                 cy = txt_rect.centery - (cursor_img.get_height() // 2)
                 surface.blit(cursor_img, (txt_rect.left - 50, cy))
             else:
                 cursor = font.render(">", True, WHITE)
                 surface.blit(cursor, (txt_rect.left - 25, txt_rect.centery - 15))

def render_delete_confirmation(surface, assets, selected_idx):
    """Disegna il popup di conferma eliminazione."""
    # Overlay scuro
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    # Box centrale
    box_w, box_h = 500, 250
    box_rect = pygame.Rect((WINDOW_WIDTH - box_w)//2, (WINDOW_HEIGHT - box_h)//2, box_w, box_h)
    draw_ff1_box(surface, box_rect)
    
    font = assets['font']
    cursor_img = assets.get('cursor_img')
    
    # Testo Domanda
    q_line1 = font.render("Sei sicuro di voler", True, WHITE)
    q_line2 = font.render("eliminare il salvataggio?", True, WHITE)
    surface.blit(q_line1, q_line1.get_rect(center=(box_rect.centerx, box_rect.top + 50)))
    surface.blit(q_line2, q_line2.get_rect(center=(box_rect.centerx, box_rect.top + 80)))
    
    # Opzioni SI / NO
    opts = ["Sì", "No"]
    start_y = box_rect.top + 150
    gap = 50
    
    for i, opt in enumerate(opts):
        col = YELLOW if i == selected_idx else (180, 180, 180)
        txt = font.render(opt, True, col)
        txt_rect = txt.get_rect(center=(box_rect.centerx, start_y + i*gap))
        surface.blit(txt, txt_rect)
        
        if i == selected_idx:
             if cursor_img:
                 cy = txt_rect.centery - (cursor_img.get_height() // 2)
                 surface.blit(cursor_img, (txt_rect.left - 50, cy))
             else:
                 cursor = font.render(">", True, WHITE)
                 surface.blit(cursor, (txt_rect.left - 25, txt_rect.centery - 15))

def render_notes(surface, assets, style):
    if style == "MODERN":
        surface.blit(assets['menu_bg'], (0, 0))
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) 
        surface.blit(overlay, (0, 0))
    else:
        surface.fill(BLACK)
        
    font = assets['font']
    lines = GAME_NOTES_LIST
    
    if style == "CLASSIC":
        margin = 100
        box_rect = pygame.Rect(margin, margin, WINDOW_WIDTH - 2*margin, WINDOW_HEIGHT - 2*margin)
        draw_ff1_box(surface, box_rect)

    y = 120 if style == "MODERN" else 150
    for line in lines:
        col = O if "Premi ESC" in line else WHITE
        txt = font.render(line, True, col)
        x = (WINDOW_WIDTH - txt.get_width()) // 2
        surface.blit(txt, (x, y))
        y += 50

def render_pause(surface, assets, buttons, style, selected_idx, options_list):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)
    surface.blit(overlay, (0, 0))
    
    font = assets['font_large']
    font_btn = assets['font']
    cursor_img = assets.get('cursor_img')
    
    title_text = "PAUSA"
    if style == "CLASSIC": title_text = "- PAUSA -"
    
    title = font.render(title_text, True, WHITE)
    surface.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    
    if style == "CLASSIC":
        all_rects = [buttons[k] for k in options_list if k in buttons]
        if all_rects:
            union_rect = all_rects[0].unionall(all_rects)
            box_rect = union_rect.inflate(100, 50)
            draw_ff1_box(surface, box_rect)

    for i, key in enumerate(options_list):
        rect = buttons.get(key)
        if not rect: continue
        
        label = key
        
        if style == "MODERN" and assets['btn_images'].get(key):
             btn_img = assets['btn_images'][key]
             if i == selected_idx:
                 scaled_img = pygame.transform.smoothscale(btn_img, (rect.width+10, rect.height+5))
                 img_rect = scaled_img.get_rect(center=rect.center)
                 surface.blit(scaled_img, img_rect)
             else:
                 img_rect = btn_img.get_rect(center=rect.center)
                 surface.blit(btn_img, img_rect)
        else:
            txt_shadow = font_btn.render(label, True, BLACK)
            surface.blit(txt_shadow, (rect.centerx - txt_shadow.get_width()//2 + 2, rect.centery - txt_shadow.get_height()//2 + 2))
            
            txt = font_btn.render(label, True, WHITE)
            txt_rect = txt.get_rect(center=rect.center)
            surface.blit(txt, txt_rect)
            
        if i == selected_idx:
            if cursor_img:
                cy = rect.centery - (cursor_img.get_height() // 2)
                surface.blit(cursor_img, (rect.left - 50, cy))
            else:
                cursor = font_btn.render(">", True, WHITE)
                surface.blit(cursor, (rect.left - 30, rect.centery - 15))