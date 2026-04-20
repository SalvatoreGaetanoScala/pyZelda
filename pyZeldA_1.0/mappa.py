# Questo file assembla la mappa prendendo i pezzi dalla cartella livello1

# Aggiornati gli import per puntare a: mappe -> livello1 -> file
from mappe.livello1.row0 import rc00, rc01
from mappe.livello1.row1 import rc10, rc11
from mappe.livello1.row2 import rc20, rc21
from mappe.livello1.row3 import rc30, rc31

# --- COSTANTI MAPPA ---
# LEGENDA TILE:
# 'H' = pozione
# '.' = Pavimento vuoto
# '#' = Muro / Roccia (Ostacolo)
# 'E' = Nemico generico
# 'Z' = Zola (Nemico acqua)
# 'P' = Player start
# 'S' = Spada
# 'A' = Albero (Ostacolo)
# 'W' = Acqua
# 'B' = Ponte

ROOM_COLS = 20
ROOM_ROWS = 10

# --- ASSEMBLAGGIO WORLD MAP ---
# La struttura è una lista di liste (Matrice)
# [Riga 0], [Riga 1], [Riga 2]

WORLD_MAP = [
    [rc00, rc01, None],  # Riga 0
    [rc10, rc11, None],  # Riga 1
    [rc20, rc21, None],
    [rc30, rc31, None]   # Riga 2
]

# Coordinate iniziali (in quale stanza spawniamo)
START_ROOM_X = 0
START_ROOM_Y = 0