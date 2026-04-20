import pygame
import platform
import os
import subprocess
from settings import *

class Terminal:
    def __init__(self):
        self.active = False          
        self.target_y = WINDOW_HEIGHT 
        self.current_y = WINDOW_HEIGHT 
        
        # Terminale alto al 70%
        self.height = int(WINDOW_HEIGHT * 0.70)
        self.width = WINDOW_WIDTH
        
        self.input_text = ""
        
        # Font monospazio
        try:
            self.font = pygame.font.SysFont("consolas", 22)
        except:
            self.font = pygame.font.SysFont("courier", 22)
            
        self.cursor_visible = True
        self.cursor_timer = 0
        self.blink_interval = 30 
        
        # Log messaggi
        self.history = [] 
        
    def toggle(self):
        """Apre o chiude il terminale"""
        self.active = not self.active
        if self.active:
            self.target_y = WINDOW_HEIGHT - self.height
            self.input_text = ""
        else:
            self.target_y = WINDOW_HEIGHT

    def handle_event(self, event, game_instance):
        if not self.active: return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSLASH:
                return True
            elif event.key == pygame.K_RETURN:
                self.execute_command(game_instance)
                self.input_text = "" 
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 50: 
                    self.input_text += event.unicode
            return True
        return False

    def execute_command(self, game):
        """Gestisce l'input utente, supportando comandi multipli con ';'"""
        raw_input = self.input_text.strip()
        
        # Se l'input è vuoto non fare nulla
        if not raw_input:
            return

        # 1. Dividi i comandi usando il punto e virgola
        commands = raw_input.split(';')
        
        # 2. Esegui ogni comando in sequenza
        for cmd_str in commands:
            clean_cmd = cmd_str.strip().lower()
            if clean_cmd: # Evita comandi vuoti (es: "cmd1;;cmd2")
                self._run_single_command(clean_cmd, game)

        # Gestione buffer storico
        if len(self.history) > 100: self.history = self.history[-100:]

    def _run_single_command(self, cmd, game):
        """Logica di esecuzione per un singolo comando"""
        
        if cmd == "invincibile":
            game.god_mode = not game.god_mode
            status = "ATTIVO" if game.god_mode else "DISATTIVATO"
            self.history.append(f"[SYS] GOD MODE: {status}")
            
        elif cmd == "ghost":
            game.ghost_mode = not game.ghost_mode
            status = "ATTIVO" if game.ghost_mode else "DISATTIVATO"
            self.history.append(f"[SYS] GHOST MODE: {status}")
            
        elif cmd == "gandalf":
            game.infinite_mp = not game.infinite_mp
            status = "ATTIVO" if game.infinite_mp else "DISATTIVATO"
            self.history.append(f"[SYS] MP INFINITI: {status}")
            
        elif cmd == "screenfetch":
            self.run_screenfetch()
            
        elif cmd == "clear":
            self.history = []
            
        elif cmd == "exit":
            self.toggle()
            
        elif cmd == "help":
            self.history.append("--- LISTA COMANDI ---")
            self.history.append("invincibile : Toggle Immortalita'")
            self.history.append("ghost       : Attraversa muri")
            self.history.append("gandalf     : MP Infiniti")
            self.history.append("screenfetch : Info Sistema")
            self.history.append("clear       : Pulisci schermo")
            self.history.append("exit        : Chiudi terminale")
            # Nota sui comandi multipli
            self.history.append("Usa ';' per comandi multipli") 
            
        else:
            self.history.append(f"[ERR] Comando '{cmd}' ignoto.")

    def run_screenfetch(self):
        # 1. Info Hardware
        try: user = os.getlogin()
        except: user = "Paperino"

        try:
            cpu = platform.processor()
            if not cpu: cpu = platform.machine()
        except: cpu = "Unknown CPU"

        try:
            cmd = "wmic computersystem get totalphysicalmemory"
            ram_output = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
            ram_gb = round(int(ram_output) / (1024**3), 2)
            ram_str = f"{ram_gb} GB"
        except: ram_str = "Unknown RAM"

        try:
            cmd = "wmic path win32_videocontroller get caption"
            gpu_output = subprocess.check_output(cmd, shell=True).decode().split('\n')
            gpu_str = next((line.strip() for line in gpu_output if line.strip() and "Caption" not in line), "Generic GPU")
        except: gpu_str = "Integrated GPU"

        # 2. ASCII ART (Giallo)
        logo = [
            "  .------._",
            "  /        \\.-.",
            "  \\_-_:===='; _.)",
            "   .'/''..''\\', \\\\",
            "  | '   ||   '.|",
            "  | |   ||   | |",
            "  | | 0 || 0 | |",
            " .'_ __.--.__ _'.",
            "(__. _.----._ .__)",
            "   `--======--'      dlK"
        ]

        # 3. Dati Info
        gpu_short = (gpu_str[:25] + '..') if len(gpu_str) > 25 else gpu_str
        cpu_short = (cpu[:25] + '..') if len(cpu) > 25 else cpu

        # Lista di tuple (Label, Valore)
        info_data = [
            ("User:", user),
            ("OS:", "PaperinOS"),
            ("Kernel:", "x86_64 Topix 4.6"),
            ("Shell:", "Ascell"),
            ("CPU:", cpu_short),
            ("RAM:", ram_str),
            ("GPU:", gpu_short)
        ]

        self.history.append("") 
        
        offset_info = (len(logo) - len(info_data)) // 2
        
        for i in range(len(logo)):
            line_segments = []
            
            # Parte Sinistra (Logo) -> Giallo
            logo_part = logo[i]
            logo_padded = f"{logo_part:<30}" # Padding fisso
            line_segments.append((logo_padded, YELLOW))
            
            # Parte Destra (Info) -> Label Rosso, Valore Verde
            info_idx = i - offset_info
            if 0 <= info_idx < len(info_data):
                label, value = info_data[info_idx]
                label_padded = f"{label:<10}" 
                line_segments.append((label_padded, RED))
                line_segments.append((value, GREEN))
            
            self.history.append(line_segments)
            
        self.history.append("") 

    def update(self):
        if self.current_y < self.target_y:
            self.current_y += TERMINAL_ANIMATION_SPEED
            if self.current_y > self.target_y: self.current_y = self.target_y
        elif self.current_y > self.target_y:
            self.current_y -= TERMINAL_ANIMATION_SPEED
            if self.current_y < self.target_y: self.current_y = self.target_y

        self.cursor_timer += 1
        if self.cursor_timer >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        if self.current_y >= WINDOW_HEIGHT:
            return

        rect = pygame.Rect(0, self.current_y, self.width, self.height)
        pygame.draw.rect(surface, B, rect) 
        pygame.draw.rect(surface, W, rect, 4) 
        
        margin_x = 30
        margin_y = 30
        line_height = 24 
        
        available_height = self.height - (margin_y * 2) - line_height
        max_lines = max(0, available_height // line_height)
        
        visible_history = self.history[-max_lines:]
        
        for i, line in enumerate(visible_history):
            y_pos = self.current_y + margin_y + (i * line_height)
            
            # Se la riga è una lista, significa che è multicolore (screenfetch)
            if isinstance(line, list):
                current_x = margin_x
                for text, color in line:
                    txt_surf = self.font.render(text, True, color)
                    surface.blit(txt_surf, (current_x, y_pos))
                    current_x += txt_surf.get_width()
            
            # Altrimenti è una stringa semplice (comandi normali)
            else:
                color = (220, 220, 220)
                if "[SYS]" in line: color = GREEN
                elif "[ERR]" in line: color = RED
                
                txt_surf = self.font.render(line, True, color) 
                surface.blit(txt_surf, (margin_x, y_pos))

        # Input
        prompt = "> " + self.input_text
        if self.cursor_visible and self.active: prompt += "_"
        
        input_y = self.current_y + self.height - margin_y - line_height
        txt_input = self.font.render(prompt, True, WHITE)
        surface.blit(txt_input, (margin_x, input_y))